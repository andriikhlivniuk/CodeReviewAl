import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from services.github_service import fetch_repo_contents
import responses

@responses.activate
def test_fetch_repo_contents_success():
    # Mock GitHub API response for repository contents
    responses.add(
        responses.GET,
        "https://api.github.com/repos/example/repo/contents",
        json=[
            {"name": "main.py", "type": "file", "download_url": "http://example.com/main.py"},
            {"name": "app.py", "type": "file", "download_url": "http://example.com/app.py"}
        ],
        status=200
    )
    responses.add(
        responses.GET,
        "http://example.com/main.py",
        body="print('Hello, world!')",
        status=200
    )
    responses.add(
        responses.GET,
        "http://example.com/app.py",
        body="from flask import Flask",
        status=200
    )

    # Call the service
    result = fetch_repo_contents("https://github.com/example/repo")

    # Validate the result
    assert result == {
        "main.py": "print('Hello, world!')",
        "app.py": "from flask import Flask"
    }


@responses.activate
def test_fetch_repo_contents_failure():
    # Mock GitHub API failure
    responses.add(
        responses.GET,
        "https://api.github.com/repos/example/repo/contents",
        json={"message": "Not Found"},
        status=404
    )

    # Call the service and assert exception
    with pytest.raises(Exception, match="Failed to fetch GitHub repo contents"):
        fetch_repo_contents("https://github.com/example/fail")

