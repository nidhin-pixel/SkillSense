# SkillSense — Integration & Security Module

**Smart IGNOU Hackathon 2026 | Hackathon Prototype**

This module provides the security and external-integration boundary for SkillSense. It is intentionally standalone so it can be merged into the team's main FastAPI application with minimal coupling.

## Responsibilities

- Secure authentication with Argon2 password hashing and JWT access tokens
- Role-Based Access Control (RBAC): `official`, `department_admin`, `super_admin`
- Security audit trail for authentication, protected-resource access and integration events
- iGOT Karmayogi integration boundary through a replaceable adapter
- Demo frontend for showing authentication, authorization and audit behaviour

## Architecture

```text
                    +----------------------+
                    |  SkillSense Frontend |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |      FastAPI API      |
                    +----+------+-------+---+
                         |      |       |
                  +------+  +---+---+  +----+-----+
                  | Auth |  |  RBAC |  |   Audit  |
                  +------+  +-------+  +----------+
                         |                 |
                         +--------+--------+
                                  v
                         +----------------+
                         | SQLite / SQL DB|
                         +----------------+
                                  ^
                                  |
                         +----------------+
                         |  iGOT Adapter   |
                         +-------+--------+
                                 |
                    Official API integration point
                    (not enabled in this demo)
```

## Important iGOT boundary

The included iGOT implementation is a **DEMO ADAPTER** with deterministic sample data. It is not a claim of live access to iGOT Karmayogi. In an authorized environment, replace `IGOTAdapter` methods with the official API client, credentials and transport requirements supplied by the platform owner.

## Quick start — Windows

1. Open the project folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create the environment:
   ```powershell
   python -m venv .venv
   ```
4. Activate it:
   ```powershell
   .venv\Scripts\activate
   ```
5. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
6. Copy `.env.example` to `.env` and set `JWT_SECRET`.
7. Start the API:
   ```powershell
   uvicorn app.main:app --reload
   ```
8. Open API documentation: `http://127.0.0.1:8000/docs`
9. In a second terminal, start the demo UI:
   ```powershell
   python -m http.server 5500 --directory frontend
   ```
10. Open `http://127.0.0.1:5500`

## Demo accounts

All demo accounts use the password `Demo@12345`.

| Email | Role | Intended scope |
|---|---|---|
| official@example.com | official | Own profile and learning services |
| department@example.com | department_admin | Department-level management |
| admin@example.com | super_admin | System administration and audit |

## Suggested judging flow

1. Sign in as `official@example.com`.
2. Open **Department Users** and show the expected HTTP 403 response — this demonstrates RBAC enforcement, not just UI hiding.
3. Sign out and sign in as `department@example.com`; open **Department Users** and show access is granted.
4. Sign in as `admin@example.com`; open **Audit Events** and show the recorded login/access events.
5. Open **iGOT Catalogue** to demonstrate the integration boundary.
6. Use `/docs` to show the API surface and protected endpoints.

## Security notes

- Passwords are never stored as plaintext; Argon2 hashing is used through `pwdlib`.
- JWTs carry a user identifier and role and have an expiration time.
- Authorization is enforced server-side through dependency-based RBAC.
- Access-denied events are written to the audit trail.
- CORS is restricted to the local demo UI by default.
- Secrets belong in `.env` and should never be committed.
- This is a hackathon prototype. Production deployment should add managed secrets, HTTPS, a production database, centralized logging, rate limiting, monitoring, key rotation and formal API integration credentials.

## Team integration

The main integration points are intentionally small:

- `app/auth/` — authentication and authorization dependencies
- `app/audit/service.py` — reusable audit recorder
- `app/igot/adapter.py` — external integration boundary
- `app/igot/routes.py` — API-facing iGOT routes
- `app/models.py` — security-related persistence models

The team's primary application can import these components or merge the routers into its existing FastAPI application.
