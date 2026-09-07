class IGOTAdapter:
    """Integration boundary for the iGOT Karmayogi platform.

    This hackathon build uses deterministic demo data. In an authorized deployment,
    these methods are the integration boundary where official iGOT APIs/credentials
    would be wired in without changing the SkillSense business layer.
    """
    def list_courses(self):
        return [
            {"course_id": "IGOT-001", "title": "Digital Governance Essentials", "competency": "Digital Governance", "duration_hours": 4},
            {"course_id": "IGOT-002", "title": "Cyber Security Awareness", "competency": "Cybersecurity Awareness", "duration_hours": 3},
            {"course_id": "IGOT-003", "title": "Data-Driven Decision Making", "competency": "Data Literacy", "duration_hours": 5},
        ]

    def get_competencies(self, user_id: int):
        return {"user_id": user_id, "competencies": [
            {"name": "Digital Governance", "level": "Intermediate"},
            {"name": "Cybersecurity Awareness", "level": "Beginner"},
        ]}

    def accept_learning_progress(self, payload: dict):
        return {"status": "accepted", "course_id": payload.get("course_id"), "progress_percent": payload.get("progress_percent")}
