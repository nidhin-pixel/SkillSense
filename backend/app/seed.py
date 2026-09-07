"""
Seeds a starter Skill Knowledge Graph and a demo admin + officer account so
the app is usable immediately after `python -m app.seed`.
"""
from app.database import SessionLocal, engine, Base
from app import models
from app.security import hash_password

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        if db.query(models.Skill).first():
            print("Skills already seeded, skipping.")
        else:
            cyber = models.Skill(name="Cybersecurity Awareness", description="Core digital-security hygiene for government officials", is_critical=True)
            db.add(cyber)
            db.flush()

            network = models.Skill(name="Network Security", parent_id=cyber.id, description="Firewalls, IDS/IPS, network attack patterns")
            data_sec = models.Skill(name="Data Privacy", parent_id=cyber.id, description="Encryption, access control, data handling", is_critical=True)
            incident = models.Skill(name="Incident Response", parent_id=cyber.id, description="Detection, analysis, recovery", is_critical=True)
            db.add_all([network, data_sec, incident])

            governance = models.Skill(name="Digital Governance", description="Policy and digital-service delivery")
            ai_lit = models.Skill(name="AI Literacy", description="Practical understanding of AI tools and risks")
            cloud = models.Skill(name="Cloud Computing", description="Cloud infrastructure fundamentals")
            db.add_all([governance, ai_lit, cloud])
            db.commit()
            print("Seeded skill knowledge graph.")

        if not db.query(models.User).filter_by(email="admin@skillsense.gov.in").first():
            admin = models.User(
                full_name="Department Admin",
                email="admin@skillsense.gov.in",
                hashed_password=hash_password("Admin@123"),
                role=models.UserRole.admin,
                department="Ministry of Statistics",
                designation="Training Coordinator",
            )
            db.add(admin)

        if not db.query(models.User).filter_by(email="officer@skillsense.gov.in").first():
            officer = models.User(
                full_name="Aarav Sharma",
                email="officer@skillsense.gov.in",
                hashed_password=hash_password("Officer@123"),
                role=models.UserRole.officer,
                department="Ministry of Statistics",
                designation="Assistant Director",
            )
            db.add(officer)

        db.commit()
        print("Seeded demo accounts: admin@skillsense.gov.in / Admin@123, officer@skillsense.gov.in / Officer@123")
    finally:
        db.close()


if __name__ == "__main__":
    run()
