from .repo_detail_tool import get_repository_details
from .commit_detail_tool import get_recent_commits
from .open_issue_detail_tool import get_open_issues

all_tools = [
    get_repository_details,
    get_recent_commits,
    get_open_issues,
]