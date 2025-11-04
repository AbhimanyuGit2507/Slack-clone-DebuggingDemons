# Submission instructions — Slack-clone (Hackathon)

This repository contains a frontend and backend Slack-like clone. It includes Dockerfiles and a docker-compose setup so judges can run the app locally or pull pre-built images.

Contents
- `frontend/` — React (Vite) app and production Dockerfile (served by nginx)
- `backend/` — FastAPI app and production Dockerfile
- `docker-compose.yml` — builds images locally and runs both services (recommended for local judge)
- `docker-compose.images.yml` — uses pre-built images from GitHub Container Registry (GHCR)
- `.github/workflows/publish-images.yml` — CI workflow that builds & pushes images to GHCR on push to `main`

Two ways to run (choose one):

A) Run locally (build from source) — recommended for judges who want to inspect code

Requirements: Docker & Docker Compose

Commands:
```powershell
# from repository root
docker compose build --no-cache
docker compose up -d

# Check logs
docker compose logs -f --tail=200 backend frontend
```

The backend will seed a SQLite DB into `./data/slack_rl.db` on first startup.

B) Pull pre-built images from GHCR and run (fast)

This uses images published by the CI workflow in this repository. Replace the owner if needed.

Commands:
```powershell
# Pull images (replace the owner if your repository uses a different name)
docker pull ghcr.io/abhimanyugit2507/slack-backend:latest
docker pull ghcr.io/abhimanyugit2507/slack-frontend:latest

# Start using the helper compose file
docker compose -f docker-compose.images.yml up -d
```

Notes for judges
- If you use option A, Docker will rebuild images locally and then run them — no network required.
- If you use option B, ensure your machine can access `ghcr.io` and that images exist (they will be published automatically when the repo is pushed to `main`).
- To reset data: stop the containers, remove `./data/slack_rl.db`, then start containers again so the seed runs.

Render deployment
- This repo includes a `Dockerfile` per service. You can instruct Render to deploy directly from this GitHub repository.
- Or use the images in GHCR to create Render services from private images.

If you want, I can also generate a short `render-deploy.md` with exact UI steps and a `render.yaml` to import to Render.