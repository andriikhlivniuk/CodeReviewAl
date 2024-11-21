import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from services.review_service import generate_code_review
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_repo_contents():
    return {
        "main.py": "def hello():\n    print('Hello, World!')",
        "test.py": "def test_hello():\n    assert True"
    }

@pytest.fixture
def mock_openai_response():
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(
            message=MagicMock(
                content="Found Files: main.py, test.py\nDownsides/Comments: Good code\nRating: 8\nConclusion: Well done"
            )
        )
    ]
    return mock_response

def test_generate_code_review_success(mock_repo_contents, mock_openai_response):
    with patch('services.review_service.client.chat.completions.create', return_value=mock_openai_response):
        result = generate_code_review(
            repo_contents=mock_repo_contents,
            assignment_description="Create a hello world program",
            candidate_level="Junior"
        )
        
        assert isinstance(result, dict)
        assert "review" in result
        assert "Found Files:" in result["review"]
        assert "Rating:" in result["review"]

def test_generate_code_review_api_error(mock_repo_contents):
    with patch('services.review_service.client.chat.completions.create', side_effect=Exception("API Error")):
        with pytest.raises(Exception) as exc_info:
            generate_code_review(
                repo_contents=mock_repo_contents,
                assignment_description="Create a hello world program",
                candidate_level="Junior"
            )
        
        assert "Failed to generate code review" in str(exc_info.value)

def test_generate_code_review_empty_repo():
    with pytest.raises(Exception):
        generate_code_review(
            repo_contents={},
            assignment_description="Create a hello world program",
            candidate_level="Junior"
        )
