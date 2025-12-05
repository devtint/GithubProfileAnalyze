# GitHub Profile Analyzer 🚀

Analyze GitHub profiles with style! A premium, glassmorphic web application that reveals developer personas, statistics, and "vibe scores" using the GitHub API.

![Demo](https://i.imgur.com/example-placeholder.png)

## ✨ Features

- **💎 Premium Aesthetic**: "Apple Glass" design system with translucent cards and smooth animations.
- **📊 Deep Analysis**:
    - **Vibe Score**: A fun metric based on followers, stars, and activity.
    - **Language Stats**: Visual breakdown of top used languages.
    - **Repo Cards**: beautiful display of top repositories.
    - **Commit Activity**: Heatmap-style commit tracking.
- **⚡ Tech Stack**:
    - **Frontend**: Next.js 14+ (App Router), TypeScript, Tailwind CSS, Framer Motion.
    - **Backend**: FastAPI (Python), httpx.
    - **Security**: Rate limiting safe, Token-based authentication support.

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Clone the Repository
```bash
git clone https://github.com/devtint/GithubProfileAnalyze.git
cd GithubProfileAnalyze
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Important**: Creates a `.env` file in the `backend` folder and add your GitHub Token to avoid rate limits:
```env
GITHUB_TOKEN=your_github_personal_access_token
```

Start the server:
```bash
python -m uvicorn main:app --reload
# Running on http://localhost:8000
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
# Running on http://localhost:3000
```

## 🚀 Deployment (Vercel)

This project is configured for a **Monorepo** deployment on Vercel.

1.  Push this repo to your GitHub.
2.  Import the project into Vercel.
3.  Select **Next.js** as the Framework Preset.
4.  Set the **Root Directory** to `.` (Current Directory).
5.  Add environment variables:
    - `GITHUB_TOKEN`: Your GitHub Personal Access Token.
6.  Deploy! 

The `vercel.json` file automatically routes API requests to the Python backend and page requests to Next.js.

## ⭐ Support

If you like this project, please give it a star!
