import requests
import logging

logger = logging.getLogger(__name__)

def fetch_repo_contents(github_repo_url: str) -> dict:
    logger.info(f"Start fetching repo content")
    try:
        # Remove `.git` if it exists in the URL
        if github_repo_url.endswith(".git"):
            github_repo_url = github_repo_url[:-4]

        # Extract owner and repo name from the URL
        parts = github_repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"

        # Fetch repo contents
        response = requests.get(api_url)
        response.raise_for_status()
        repo_files = response.json()

        # Fetch file content for each file
        file_contents = {}
        for file in repo_files:
            if file["type"] == "file":  # Skip directories
                file_response = requests.get(file["download_url"])
                file_response.raise_for_status()
                file_contents[file["name"]] = file_response.text

        return file_contents

    except requests.RequestException as e:
        logger.error(f"Failed to fetch GitHub repo contents: {str(e)}")
        raise Exception(f"Failed to fetch GitHub repo contents: {str(e)}")
