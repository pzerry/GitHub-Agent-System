import requests
from langchain_core.tools import tool


@tool
def get_repository_details(owner: str, repo: str) -> dict:
    """Fetch live details of a public GitHub repository.

    Args:
        owner: GitHub username or organization, such as "rongmingsun".
        repo: Repository name, such as "langgraph-dynamic-supervisor".
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"

    try:
        response = requests.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=15,
        )

        response.raise_for_status()
        data = response.json()

        return {
            "name": data["full_name"],
            "description": data["description"],
            "stars": data["stargazers_count"],
            "forks": data["forks_count"],
            "language": data["language"],
            "url": data["html_url"],
        }

    except requests.RequestException as error:
        return {"error": f"GitHub request failed: {error}"}