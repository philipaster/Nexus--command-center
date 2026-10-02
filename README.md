# ⚡ NEXUS Command Center

A futuristic personal command center built from scratch with **Python, Flask, SQLite, HTML, CSS and JavaScript**.

## Features

- 🧠 Mission/task manager with completion tracking
- 📝 Persistent intelligence/notes log
- 🔐 Cryptographically secure password generator
- 🖥️ Host telemetry (OS, Python, machine and hostname)
- 📊 Live dashboard statistics
- 🗄️ SQLite persistence — no external database required
- 🌐 JSON API endpoints
- 📱 Responsive futuristic interface
- 🚀 Runs locally and is easy to deploy

## Project structure

```text
nexus_command_center/
├── app.py
├── nexus.db              # created automatically
├── requirements.txt
├── README.md
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Run it

### 1. Install Flask

```bash
pip install flask
```

### 2. Start NEXUS

```bash
python app.py
```

### 3. Open

```text
http://127.0.0.1:5000
```

On Android/Pydroid, open the same address in your browser after starting the script.

## API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/system` | Host telemetry |
| GET | `/api/stats` | Dashboard statistics |
| GET | `/api/generate-password?length=20` | Secure password |
| POST | `/api/tasks` | Create task |
| PATCH | `/api/tasks/<id>` | Toggle task |
| DELETE | `/api/tasks/<id>` | Delete task |
| POST | `/api/notes` | Create note |
| DELETE | `/api/notes/<id>` | Delete note |

## GitHub description

> A futuristic Python/Flask command center featuring persistent tasks, intelligence notes, secure password generation, system telemetry and a REST API.

## Ideas for v2

- User authentication
- Real-time WebSocket notifications
- Weather integration
- AI assistant integration
- Charts and analytics
- File explorer
- Dark/light themes
- Docker deployment
