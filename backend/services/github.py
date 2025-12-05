import httpx
import asyncio
import os
from typing import Dict, Any, List

GITHUB_API_URL = "https://api.github.com"

class GitHubService:
    def __init__(self):
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Profile-Analyzer-V1"
        }
        token = os.getenv("GITHUB_TOKEN")
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{GITHUB_API_URL}/users/{username}", headers=self.headers)
            if response.status_code == 404:
                return None
            if response.status_code == 403:
                raise Exception("GitHub API Rate Limit Exceeded. Please try again later or add a GITHUB_TOKEN.")
            response.raise_for_status()
            return response.json()

    async def get_user_repos(self, username: str, limit: int = 100) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{GITHUB_API_URL}/users/{username}/repos?sort=updated&per_page={limit}", 
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def analyze_profile(self, username: str) -> Dict[str, Any]:
        user_data = await self.get_user_profile(username)
        if not user_data:
            return {"error": "User not found"}
        
        repos = await self.get_user_repos(username)
        
        # Basic Stats calculation
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        languages = {}
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
    async def get_recent_commits(self, username: str, repos: List[Dict]) -> List[Dict]:
        """Fetch latest commits across top active repos."""
        commits = []
        # optimization: only check top 5 updated repos to spare API rate limit
        target_repos = sorted(repos, key=lambda r: r['updated_at'], reverse=True)[:5]
        
        async with httpx.AsyncClient() as client:
            for repo in target_repos:
                try:
                    resp = await client.get(
                        f"{GITHUB_API_URL}/repos/{username}/{repo['name']}/commits?per_page=5", 
                        headers=self.headers
                    )
                    if resp.status_code == 200:
                        repo_commits = resp.json()
                        for c in repo_commits:
                            c['repo_name'] = repo['name']
                            commits.append(c)
                except:
                    continue
        
        # Sort all aggregated commits by date
        return sorted(commits, key=lambda c: c['commit']['author']['date'], reverse=True)[:20]

    def scan_for_secrets(self, commits: List[Dict]) -> List[Dict]:
        """Heuristic scan for sensitive data in commit messages and patches."""
        suspicious_keywords = ['password', 'secret', 'key', 'token', 'auth', 'credentials', '.env', 'config']
        findings = []

        for c in commits:
            message = c['commit']['message'].lower()
            # Simple keyword match in message
            if any(k in message for k in suspicious_keywords):
                findings.append({
                    "type": "commit_message_keyword",
                    "keyword": next(k for k in suspicious_keywords if k in message),
                    "commit_url": c['html_url'],
                    "repo": c.get('repo_name', 'unknown'),
                    "message": c['commit']['message']
                })
        
        return findings

    async def analyze_profile(self, username: str) -> Dict[str, Any]:
        user_data = await self.get_user_profile(username)
        if not user_data:
            return {"error": "User not found"}
        
        repos = await self.get_user_repos(username, limit=100)
        recent_commits = await self.get_recent_commits(username, repos)
        security_issues = self.scan_for_secrets(recent_commits)
        
        # Basic Stats calculation
        total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
        languages = {}
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
        
        # Calculate 'Vibe Score' (Arbitrary fun metric)
        follower_ratio = user_data.get("followers", 0) / (user_data.get("following", 1) or 1)
        vibe_score = min(100, int((total_stars * 0.5) + (follower_ratio * 10) + len(repos)))

        return {
            "profile": user_data,
            "stats": {
                "total_stars": total_stars,
                "top_languages": dict(sorted(languages.items(), key=lambda item: item[1], reverse=True)[:5]),
                "repo_count": len(repos),
                "vibe_score": vibe_score
            },
            "repos": sorted(repos, key=lambda r: r['stargazers_count'], reverse=True)[:10], # Top 10 repos
            "recent_commits": recent_commits,
            "security_issues": security_issues
        }
