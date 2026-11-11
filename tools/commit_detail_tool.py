import requests
from langchain_core.tools import tool

# Paste the corresponding @tool function here.
@tool
def get_recent_commits(owner: str, repo: str) -> dict:
    """Get the five most recent commits on a public repository's default branch.

    Args:
        owner: GitHub username or organization.
        repo: Repository name.
    """
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/commits",
            headers={"Accept": "application/vnd.github+json"},
            params={"per_page": 5},
            timeout=15,
        )
        response.raise_for_status()

        commits = []
        for item in response.json():
            commits.append({
                "sha": item["sha"][:7],
                "message": item["commit"]["message"],
                "author": item["commit"]["author"]["name"],
                "date": item["commit"]["author"]["date"],
                "url": item["html_url"],
            })

        return {"commits": commits}

    except requests.RequestException as error:
        return {"error": f"GitHub request failed: {error}"}