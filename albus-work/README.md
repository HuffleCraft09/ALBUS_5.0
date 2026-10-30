# A.L.B.U.S. 5.0 — Unified Core

A responsive, installable web application for one ALBUS assistant across desktop and mobile. The navigation pages are workspaces; they do not switch assistants or modes.

## Highlights
- Unified conversation with internal research, reasoning, memory, project, file, automation, and device capabilities.
- Puter.js AI integration; sign in through **Settings** to enable AI and cloud storage. No OpenAI/NVIDIA secret is required in this repository.
- Live research desk that sends research requests through ALBUS's web-search workflow. Availability depends on the selected Puter model and account.
- Durable memory and project/task/file metadata, with cloud sync when signed into Puter and local browser fallback.
- Searchable memory and downloadable JSON backup.
- Mobile-responsive interface, camera/file picker, browser voice input/output, PWA manifest, and service-worker app-shell caching.
- Browser reminders and notifications. The page must remain open for timers to execute; static hosting cannot run background jobs.

## Deploy on GitHub Pages
1. Extract the ZIP and upload the **contents of the `albus-work` folder** to the root of a GitHub repository.
2. Push to the `main` branch.
3. Open **Settings → Pages** and choose **GitHub Actions** as the deployment source.
4. The included workflow publishes `web/`.
5. Open the Pages URL, open Settings, and sign in to Puter.
6. On iOS use Safari → Share → Add to Home Screen. On Android use the browser menu → Install app / Add to Home screen.

## Run locally
The site uses relative paths. Serve the `web` directory with any static server (for example `python -m http.server 8000 --directory web`) and open `http://localhost:8000`.

## Important limitations
- AI, cloud KV, and file storage require a signed-in Puter account and the relevant Puter service availability.
- Browser speech recognition varies by browser; device dictation is a fallback.
- Notifications/reminders are best-effort browser features, not server-side scheduled jobs.
- A desktop control node is not included in this release. The web app cannot launch local desktop applications or execute local commands.
- Do not commit API keys, passwords, or private files.

**Release:** 5.0 · Unified Core / Mobile Command Center
