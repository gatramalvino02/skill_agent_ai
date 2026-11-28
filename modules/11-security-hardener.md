# Module 11: Security Hardener & Pre-Release Audit

Loaded for `/audit`, auth/payment/permission logic, public APIs, or pre-release hardening.

## 1. High-Signal Security Checklist

1. **Secrets & Credentials**: Verify zero hardcoded API keys, JWT secrets, passwords, private tokens, or committed `.env` files. Ensure secrets load strictly from environment variables.
2. **Input Validation & Injection**: Confirm strict schema validation at every trust boundary. Use parameterized queries/ORM bindings (zero raw SQL string interpolation), avoid unsafe `eval`/`exec`/shell string concatenation, and sanitize rendered HTML to prevent XSS.
3. **Auth & Access Control**: Verify authentication AND object-level authorization (prevent IDOR—confirm the caller actually owns/can access the requested resource). Enforce secure password hashing (`argon2`/`bcrypt`) and `HttpOnly`/`SameSite`/`Secure` cookies where applicable.
4. **Error & Data Exposure**: Never return raw stack traces, internal SQL errors, or sensitive fields (password hashes, tokens) in API responses.
5. **Dependencies & Network**: Avoid unverified packages, enforce explicit HTTP timeouts, restrict overly broad CORS (`*` with credentials), and check file upload size/type validation.

## 2. Output Format for `/audit`

Report findings sorted by severity (`CRITICAL` -> `HIGH` -> `MEDIUM`) with exact `file:line`, exploit impact in <=12 words, and minimal fix. Zero filler if clean.
