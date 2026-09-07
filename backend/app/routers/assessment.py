"""
The adaptive assessment engine: start a session -> serve one question at a
time -> adjust difficulty based on the previous answer -> stop after a fixed
number of questions -> score the session -> fold the result into the
officer's Competency Passport.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.deps import get_current_user
from app.ai.question_gen import generate_question
from app.ai import competency_engine as ce

router = APIRouter(prefix="/assessment", tags=["assessment"])

QUESTIONS_PER_SESSION = 5


def _question_to_public(q: models.Question) -> schemas.QuestionPublic:
    return schemas.QuestionPublic(
        id=q.id,
        skill_id=q.skill_id,
        skill_name=q.skill.name,
        prompt=q.prompt,
        option_a=q.option_a,
        option_b=q.option_b,
        option_c=q.option_c,
        option_d=q.option_d,
        difficulty=q.difficulty.value if hasattr(q.difficulty, "value") else q.difficulty,
    )


def _make_and_store_question(db: Session, skill: models.Skill, difficulty: str) -> models.Question:
    generated = generate_question(skill.name, skill.description, difficulty)
    question = models.Question(
        skill_id=skill.id,
        prompt=generated["prompt"],
        option_a=generated["option_a"],
        option_b=generated["option_b"],
        option_c=generated["option_c"],
        option_d=generated["option_d"],
        correct_option=generated["correct_option"],
        difficulty=difficulty,
        explanation=generated.get("explanation", ""),
        is_ai_generated=generated.get("is_ai_generated", False),
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.post("/start", response_model=schemas.SessionQuestionOut)
def start_session(
    payload: schemas.SessionStart,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    skill = db.query(models.Skill).filter(models.Skill.id == payload.skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")

    session = models.AssessmentSession(
        user_id=user.id, skill_id=skill.id, current_difficulty=models.Difficulty.basic
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    question = _make_and_store_question(db, skill, "basic")
    # Tag the active question onto the session via a lightweight response-less link
    db.add(models.AssessmentResponse(
        session_id=session.id, question_id=question.id,
        selected_option="", is_correct=False,
    ))
    db.commit()

    return schemas.SessionQuestionOut(session_id=session.id, question=_question_to_public(question))


@router.post("/{session_id}/answer", response_model=schemas.AnswerResult)
def answer_question(
    session_id: int,
    payload: schemas.AnswerSubmit,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    session = db.query(models.AssessmentSession).filter(
        models.AssessmentSession.id == session_id, models.AssessmentSession.user_id == user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.completed_at is not None:
        raise HTTPException(status_code=400, detail="Session already completed")

    question = db.query(models.Question).filter(models.Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = payload.selected_option.lower() == question.correct_option.lower()

    # Find the placeholder response created at start/next-question time and fill it in.
    pending = (
        db.query(models.AssessmentResponse)
        .filter(
            models.AssessmentResponse.session_id == session.id,
            models.AssessmentResponse.question_id == question.id,
            models.AssessmentResponse.selected_option == "",
        )
        .first()
    )
    if pending:
        pending.selected_option = payload.selected_option
        pending.is_correct = is_correct
    else:
        db.add(models.AssessmentResponse(
            session_id=session.id, question_id=question.id,
            selected_option=payload.selected_option, is_correct=is_correct,
        ))
    db.commit()

    answered_count = db.query(models.AssessmentResponse).filter(
        models.AssessmentResponse.session_id == session.id,
        models.AssessmentResponse.selected_option != "",
    ).count()

    if answered_count >= QUESTIONS_PER_SESSION:
        _complete_session(db, session)
        return schemas.AnswerResult(
            is_correct=is_correct,
            correct_option=question.correct_option,
            explanation=question.explanation,
            next_question=None,
            session_complete=True,
        )

    next_difficulty = ce.next_difficulty(question.difficulty.value, is_correct)
    session.current_difficulty = next_difficulty
    db.commit()

    skill = db.query(models.Skill).filter(models.Skill.id == session.skill_id).first()
    next_q = _make_and_store_question(db, skill, next_difficulty)
    db.add(models.AssessmentResponse(
        session_id=session.id, question_id=next_q.id,
        selected_option="", is_correct=False,
    ))
    db.commit()

    return schemas.AnswerResult(
        is_correct=is_correct,
        correct_option=question.correct_option,
        explanation=question.explanation,
        next_question=_question_to_public(next_q),
        session_complete=False,
    )


def _complete_session(db: Session, session: models.AssessmentSession):
    from datetime import datetime, timezone

    responses = (
        db.query(models.AssessmentResponse)
        .filter(
            models.AssessmentResponse.session_id == session.id,
            models.AssessmentResponse.selected_option != "",
        )
        .all()
    )
    scored = [
        {"difficulty": r.question.difficulty.value, "is_correct": r.is_correct}
        for r in responses
    ]
    result = ce.score_session(scored)
    session.completed_at = datetime.now(timezone.utc)
    session.score_percent = result["score_percent"]
    session.estimated_level = result["estimated_level"]
    db.commit()

    # Fold this session's evidence into the officer's living Competency Passport.
    record = (
        db.query(models.CompetencyRecord)
        .filter(
            models.CompetencyRecord.user_id == session.user_id,
            models.CompetencyRecord.skill_id == session.skill_id,
        )
        .first()
    )
    previous_level = record.level_percent if record else 0.0
    previous_count = record.assessments_count if record else 0
    updated = ce.update_competency_record(previous_level, previous_count, result["score_percent"])

    if record:
        record.previous_level_percent = updated["previous_level_percent"]
        record.level_percent = updated["level_percent"]
        record.assessments_count = updated["assessments_count"]
        record.confidence = updated["confidence"]
        record.last_assessed_at = updated["last_assessed_at"]
    else:
        record = models.CompetencyRecord(
            user_id=session.user_id,
            skill_id=session.skill_id,
            level_percent=updated["level_percent"],
            previous_level_percent=0.0,
            assessments_count=1,
            confidence=updated["confidence"],
            last_assessed_at=updated["last_assessed_at"],
        )
        db.add(record)
    db.commit()


@router.get("/history", response_model=list[schemas.SessionOut])
def session_history(
    db: Session = Depends(get_db), user: models.User = Depends(get_current_user)
):
    sessions = (
        db.query(models.AssessmentSession)
        .filter(models.AssessmentSession.user_id == user.id)
        .order_by(models.AssessmentSession.started_at.desc())
        .all()
    )
    return sessions
