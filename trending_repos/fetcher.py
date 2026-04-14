"""
fetcher.py
----------
Handles all communication with the GitHub REST API.

KEY CONCEPT: GitHub has no official 'trending' endpoint.
The trick is to use the Search API to find repos CREATED recently,
sorted by star count. That IS trending — new repos with the most stars
= what developers are excited about right now.

API URL we use:
  https://api.github.com/search/repositories
    ?q=created:>2024-12-01
    &sort=stars
    &order=desc
    &per_page=20
"""

import requests
from typing import Optional

# The base URL for GitHub's repository search endpoint
GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

# How long to wait (in seconds) before giving up on a request
REQUEST_TIMEOUT = 10


def fetch_trending_repos(
    start_date: str,
    limit: int = 10,
    language: Optional[str] = None,
) -> list[dict]:
    """
    Fetch trending repositories from the GitHub Search API.

    This function:
    1. Builds the query string (e.g. "created:>2024-12-01 language:python")
    2. Sends a GET request to the GitHub API
    3. Handles all error cases (network errors, rate limits, bad responses)
    4. Returns a clean list of repo dictionaries

    Args:
        start_date:  Date string like '2024-12-01'. Repos created AFTER this
                     date are included.
        limit:       Max number of repos to return (1–100).
        language:    Optional language filter like 'python', 'javascript'.

    Returns:
        A list of dictionaries, each representing one repository.
        Each dict has these keys:
          - name         → 'torvalds/linux'
          - description  → 'Linux kernel source tree'
          - stars        → 180000
          - language     → 'C'
          - url          → 'https://github.com/torvalds/linux'
          - forks        → 52000
          - open_issues  → 300
          - topics       → ['os', 'kernel']

    Raises:
        SystemExit: on any unrecoverable error (rate limit, network failure)
    """

    # --- Step 1: Build the search query ---
    # GitHub search query syntax: field:value
    # 'created:>DATE' = only repos created after DATE
    query_parts = [f"created:>{start_date}"]

    if language:
        # GitHub search supports 'language:python' style filters
        query_parts.append(f"language:{language}")

    query = " ".join(query_parts)

    # --- Step 2: Set up request parameters ---
    params = {
        "q":        query,        # The search query
        "sort":     "stars",      # Sort by number of stars
        "order":    "desc",       # Highest stars first
        "per_page": limit,        # How many results we want
    }

    # --- Step 3: Set up headers ---
    # We tell GitHub what kind of response we want.
    # 'Accept: application/vnd.github.v3+json' is the recommended header.
    headers = {
        "Accept": "application/vnd.github.v3+json",
        # If you add a GitHub token later, add it here:
        # "Authorization": "token YOUR_TOKEN_HERE"
    }

    # --- Step 4: Make the request with error handling ---
    try:
        response = requests.get(
            GITHUB_SEARCH_URL,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

        # --- Step 5: Handle HTTP error status codes ---
        if response.status_code == 403:
            # GitHub rate limits unauthenticated requests to 10/minute
            # for search, 60/hour for general API
            error_msg = response.json().get("message", "")
            if "rate limit" in error_msg.lower():
                print(
                    "\n[ERROR] GitHub API rate limit exceeded.\n"
                    "You've made too many requests. Wait ~1 minute and try again.\n"
                    "Tip: Add a GitHub token (GITHUB_TOKEN env var) for higher limits.\n"
                )
            else:
                print(f"\n[ERROR] Access forbidden: {error_msg}\n")
            raise SystemExit(1)

        elif response.status_code == 422:
            # This happens with malformed queries
            print(
                "\n[ERROR] Invalid search query sent to GitHub API.\n"
                "This is likely a bug — please report it.\n"
            )
            raise SystemExit(1)

        elif response.status_code != 200:
            print(
                f"\n[ERROR] GitHub API returned status {response.status_code}.\n"
                f"Message: {response.json().get('message', 'Unknown error')}\n"
            )
            raise SystemExit(1)

        # --- Step 6: Parse the JSON response ---
        data = response.json()

        # GitHub wraps results in a "items" key
        # 'total_count' tells us how many repos match in total
        raw_repos = data.get("items", [])

        if not raw_repos:
            print(
                f"\n[INFO] No repositories found for the selected time range.\n"
                f"Try a longer duration (e.g. --duration month).\n"
            )
            raise SystemExit(0)

        # --- Step 7: Extract only the fields we care about ---
        return _parse_repos(raw_repos)

    except requests.exceptions.ConnectionError:
        print(
            "\n[ERROR] Could not connect to GitHub API.\n"
            "Check your internet connection and try again.\n"
        )
        raise SystemExit(1)

    except requests.exceptions.Timeout:
        print(
            f"\n[ERROR] Request timed out after {REQUEST_TIMEOUT} seconds.\n"
            "GitHub API might be slow. Try again in a moment.\n"
        )
        raise SystemExit(1)

    except requests.exceptions.RequestException as e:
        print(f"\n[ERROR] Unexpected network error: {e}\n")
        raise SystemExit(1)


def _parse_repos(raw_repos: list[dict]) -> list[dict]:
    """
    Extract only the fields we need from each GitHub API repo object.

    The GitHub API returns ~60 fields per repo. We only need a handful.
    This function cleans up the data into a simple, predictable structure.

    The raw GitHub API item looks like:
    {
      "full_name": "user/repo",
      "description": "...",
      "stargazers_count": 1234,
      "language": "Python",
      "html_url": "https://github.com/...",
      "forks_count": 100,
      "open_issues_count": 20,
      "topics": ["python", "cli"],
      ... (50+ more fields we don't need)
    }
    """
    parsed = []

    for repo in raw_repos:
        parsed.append({
            "name":        repo.get("full_name", "Unknown"),
            "description": repo.get("description") or "No description provided",
            "stars":       repo.get("stargazers_count", 0),
            "language":    repo.get("language") or "Not specified",
            "url":         repo.get("html_url", ""),
            "forks":       repo.get("forks_count", 0),
            "open_issues": repo.get("open_issues_count", 0),
            "topics":      repo.get("topics", []),
        })

    # Sort by stars descending (API usually does this, but we enforce it)
    parsed.sort(key=lambda r: r["stars"], reverse=True)

    return parsed
