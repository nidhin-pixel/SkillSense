# Integration Notes

## What this module owns

This module owns cross-cutting concerns that should remain independent of SkillSense's competency-analysis logic:

1. Identity — who is making the request?
2. Authorization — what is that identity allowed to access?
3. Auditability — what security-relevant event occurred?
4. External learning integration — how does SkillSense communicate with the iGOT boundary?

## Merge strategy

If the main team application already has authentication, avoid maintaining two independent identity systems. Reuse the team's canonical user model and migrate the RBAC/audit concepts into it. The iGOT adapter can remain isolated behind an interface/client layer.

## API groups

- `POST /api/auth/login` — authenticate
- `GET /api/auth/me` — current identity
- `GET /api/official/dashboard` — authenticated official access
- `GET /api/admin/users` — department admin / super admin
- `GET /api/admin/system` — super admin
- `GET /api/audit` — super admin audit access
- `GET /api/igot/courses` — demo iGOT catalogue
- `GET /api/igot/competencies/{user_id}` — role-scoped competency read
- `POST /api/igot/learning-progress` — demo learning-progress push
