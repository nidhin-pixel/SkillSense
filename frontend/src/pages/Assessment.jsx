import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { CheckCircle2, XCircle, ArrowRight } from "lucide-react";
import client from "../api/client";

const TOTAL_QUESTIONS = 5;

export default function Assessment() {
  const [skills, setSkills] = useState([]);
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [question, setQuestion] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [answeredCount, setAnsweredCount] = useState(0);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    client.get("/skills").then((res) => setSkills(res.data.filter((s) => !s.parent_id)));
  }, []);

  const startAssessment = async (skill) => {
    setLoading(true);
    setSelectedSkill(skill);
    setResult(null);
    setAnsweredCount(0);
    try {
      const res = await client.post("/assessment/start", { skill_id: skill.id });
      setSessionId(res.data.session_id);
      setQuestion(res.data.question);
      setSelectedOption(null);
      setFeedback(null);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!selectedOption) return;
    setLoading(true);
    try {
      const res = await client.post(`/assessment/${sessionId}/answer`, {
        question_id: question.id,
        selected_option: selectedOption,
      });
      setFeedback(res.data);
      setAnsweredCount((c) => c + 1);
    } finally {
      setLoading(false);
    }
  };

  const nextQuestion = () => {
    setQuestion(feedback.next_question);
    setSelectedOption(null);
    setFeedback(null);
  };

  const reset = () => {
    setSelectedSkill(null);
    setSessionId(null);
    setQuestion(null);
    setResult(null);
    setFeedback(null);
  };

  const options = question
    ? [
        ["a", question.option_a],
        ["b", question.option_b],
        ["c", question.option_c],
        ["d", question.option_d],
      ]
    : [];

  // ---- Skill picker ----
  if (!selectedSkill) {
    return (
      <div className="max-w-3xl">
        <h1 className="font-serif text-3xl text-ink">Choose a skill to assess</h1>
        <p className="text-sm text-slate-muted mt-2 max-w-lg">
          Each assessment adapts as you answer — {TOTAL_QUESTIONS} questions
          that get harder or easier based on your responses, then feed
          directly into your Competency Passport.
        </p>

        <div className="grid sm:grid-cols-2 gap-4 mt-8">
          {skills.map((skill) => (
            <button
              key={skill.id}
              onClick={() => startAssessment(skill)}
              className="text-left bg-white border border-slate-line hover:border-ink rounded-sm px-5 py-5 transition-colors focus-ring"
            >
              <p className="font-serif text-lg text-ink">{skill.name}</p>
              <p className="text-sm text-slate-muted mt-1 line-clamp-2">{skill.description}</p>
              {skill.is_critical && (
                <span className="inline-block mt-3 text-xs text-brick bg-brick/5 border border-brick/20 rounded px-2 py-0.5">
                  Critical skill
                </span>
              )}
            </button>
          ))}
        </div>
      </div>
    );
  }

  // ---- Session complete ----
  if (result) {
    return (
      <div className="max-w-lg">
        <div className="bg-white border border-slate-line rounded-sm px-8 py-10 text-center">
          <p className="text-sm text-slate-muted">Assessment complete</p>
          <h1 className="font-serif text-3xl text-ink mt-2">{result.skillName}</h1>
          <p className="text-sm text-slate-muted mt-4">
            This session has been added to your Competency Passport.
          </p>
          <div className="flex gap-3 justify-center mt-8">
            <button
              onClick={reset}
              className="text-sm font-medium border border-slate-line px-4 py-2.5 rounded-md hover:border-ink transition-colors"
            >
              Assess another skill
            </button>
            <Link
              to="/passport"
              className="text-sm font-medium bg-ink text-white px-4 py-2.5 rounded-md hover:bg-ink-light transition-colors"
            >
              View passport
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // ---- Question flow ----
  return (
    <div className="max-w-2xl">
      <div className="flex items-center justify-between mb-6">
        <p className="text-sm text-slate-muted">{selectedSkill.name}</p>
        <div className="flex gap-1.5">
          {Array.from({ length: TOTAL_QUESTIONS }).map((_, i) => (
            <span
              key={i}
              className={`h-1.5 w-6 rounded-full ${i < answeredCount ? "bg-ink" : "bg-slate-line"}`}
            />
          ))}
        </div>
      </div>

      {question && (
        <div className="bg-white border border-slate-line rounded-sm px-7 py-7">
          <span className="text-xs uppercase tracking-wide text-gold">{question.difficulty}</span>
          <p className="font-serif text-xl text-ink mt-2 leading-snug">{question.prompt}</p>

          <div className="mt-6 space-y-2.5">
            {options.map(([key, text]) => {
              const isSelected = selectedOption === key;
              const isCorrectAnswer = feedback && key === feedback.correct_option;
              const isWrongSelected = feedback && isSelected && !feedback.is_correct;

              let stateClasses = "border-slate-line hover:border-ink";
              if (feedback) {
                if (isCorrectAnswer) stateClasses = "border-teal bg-teal/5";
                else if (isWrongSelected) stateClasses = "border-brick bg-brick/5";
              } else if (isSelected) {
                stateClasses = "border-ink bg-ink/5";
              }

              return (
                <button
                  key={key}
                  disabled={!!feedback}
                  onClick={() => setSelectedOption(key)}
                  className={`w-full flex items-center justify-between text-left border rounded-md px-4 py-3 text-sm transition-colors focus-ring ${stateClasses}`}
                >
                  <span className="text-slate-text">{text}</span>
                  {feedback && isCorrectAnswer && <CheckCircle2 size={18} className="text-teal shrink-0" />}
                  {feedback && isWrongSelected && <XCircle size={18} className="text-brick shrink-0" />}
                </button>
              );
            })}
          </div>

          {feedback && (
            <p className="mt-5 text-sm text-slate-muted bg-paper border border-slate-line rounded-md px-4 py-3">
              {feedback.explanation}
            </p>
          )}

          <div className="mt-6 flex justify-end">
            {!feedback ? (
              <button
                onClick={submitAnswer}
                disabled={!selectedOption || loading}
                className="inline-flex items-center gap-1.5 text-sm font-medium bg-ink text-white px-5 py-2.5 rounded-md hover:bg-ink-light transition-colors disabled:opacity-50"
              >
                Submit answer
              </button>
            ) : !feedback.session_complete ? (
              <button
                onClick={nextQuestion}
                className="inline-flex items-center gap-1.5 text-sm font-medium bg-ink text-white px-5 py-2.5 rounded-md hover:bg-ink-light transition-colors"
              >
                Next question <ArrowRight size={16} />
              </button>
            ) : (
              <button
                onClick={() => setResult({ skillName: selectedSkill.name })}
                className="inline-flex items-center gap-1.5 text-sm font-medium bg-ink text-white px-5 py-2.5 rounded-md hover:bg-ink-light transition-colors"
              >
                View results <ArrowRight size={16} />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
