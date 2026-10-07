# CyberGuard — Cybersecurity Impact Analyzer

Professional full-stack MWT project using React/Vite, Node.js/Express, MongoDB Atlas, JWT and Google OAuth.

## Folders
Only two application folders are included:
- `frontend`
- `backend`

There is intentionally **no seed folder and no sample decision data**. Users are created through registration/admin user management.

## Backend setup
1. Open `backend`.
2. Copy `.env.example` to `.env`.
3. Put your MongoDB Atlas URI in `MONGODB_URI`.
4. Set a 32+ character `JWT_SECRET`.
5. Set a private `SETUP_ADMIN_KEY` for first-time Admin registration.
6. Optional Google OAuth values can be added.
7. Run `npm install` then `npm run dev`.

Node 20.19+ is required. The backend uses Node's built-in `--watch`; Nodemon is intentionally not included so its old dependency tree cannot be introduced by audit fixes.

## Frontend setup
1. Open `frontend` in another terminal.
2. Copy `.env.example` to `.env`.
3. Run `npm install` then `npm run dev`.
4. Open the Vite URL, normally http://localhost:5173.

## First-time account flow
- Register the first Admin using the `SETUP_ADMIN_KEY`.
- Sign in as Admin.
- Use Admin Console → Create authorized user to create the remaining Analyst/Viewer accounts.
- No seed data is inserted automatically.

## MongoDB collections created by real use
`users`, `decisions`, and `activities`.

Generated API keys can call `GET /api/api-keys/access/decisions` using the `x-api-key` header.

## Google OAuth
Google button is always visible. Actual Google authentication requires a Google OAuth client configured with:
`http://localhost:5000/api/auth/google/callback` as an authorized redirect URI.

## Security
- HttpOnly JWT cookie
- HS256 algorithm restriction
- bcrypt password hashing
- role-based authorization: ADMIN / ANALYST / VIEWER
- Helmet security headers
- CORS allow-list
- rate limiting
- input validation
- no password returned to frontend
- no sample decision records
