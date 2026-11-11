
from langchain.tools import tool
import requests

@tool
def get_open_issues(owner: str, repo: str) -> dict:
    """Get a sample of up to five recently created open issues.

    Scans the first 30 results and excludes pull requests.
    This is not a complete list of all open issues.

    Args:
        owner: GitHub username or organization.
        repo: Repository name.
    """
    try:
        response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers={"Accept": "application/vnd.github+json"},
            params={
                "state": "open",
                "sort": "created",
                "direction": "desc",
                "per_page": 30,
            },
            timeout=15,
        )
        response.raise_for_status()

        issues = []
        for item in response.json():
            if "pull_request" in item:
                continue

            issues.append({
                "number": item["number"],
                "title": item["title"],
                "created_at": item["created_at"],
                "url": item["html_url"],
            })

            if len(issues) == 5:
                break

        return {
            "issues": issues,
            "scope": "Up to five issues from the first 30 API results.",
        }

    except requests.RequestException as error:
        return {"error": f"GitHub request failed: {error}"}