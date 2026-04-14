"""
main.py
-------
Entry point for the trending-repos CLI tool.

This file does exactly two things:
1. Defines and parses command-line arguments using argparse
2. Orchestrates the other modules in the right order

Think of it as the "director" — it doesn't do the heavy lifting itself,
it calls the right specialists at the right time:
  main.py  →  utils.py  →  fetcher.py  →  display.py

USAGE:
  trending-repos
  trending-repos --duration day
  trending-repos --duration month --limit 20
  trending-repos --duration week --limit 5 --language python
"""

import argparse
import sys

from .utils import get_start_date, validate_limit, VALID_DURATIONS
from .fetcher import fetch_trending_repos
from .display import display_repos, display_loading


def build_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser.

    argparse is Python's built-in library for handling CLI arguments.
    It automatically generates --help output and validates input types.

    Returns:
        A configured ArgumentParser ready to parse sys.argv
    """
    parser = argparse.ArgumentParser(
        prog="trending-repos",
        description=(
            "🔥 Discover trending GitHub repositories.\n"
            "Fetches repos sorted by stars for a given time range."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  trending-repos\n"
            "  trending-repos --duration day\n"
            "  trending-repos --duration month --limit 20\n"
            "  trending-repos --duration week --language python\n"
        ),
    )

    # --duration argument
    # choices= restricts input to only these valid values
    # default= sets the fallback if the user doesn't pass this flag
    parser.add_argument(
        "--duration",
        type=str,
        choices=VALID_DURATIONS,
        default="week",
        metavar="DURATION",
        help=(
            f"Time range for trending repos. "
            f"Options: {', '.join(VALID_DURATIONS)}. "
            f"Default: week"
        ),
    )

    # --limit argument
    # type=int means argparse will automatically convert "20" → 20
    # and show a clear error if the user passes "--limit abc"
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        metavar="N",
        help="Number of repositories to display (1–100). Default: 10",
    )

    # --language argument (bonus feature — filter by language)
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        metavar="LANG",
        help="Filter by programming language (e.g. python, javascript, go)",
    )

    return parser


def main():
    """
    Main function — the complete program flow in order:

    1. Parse arguments
    2. Validate inputs
    3. Calculate the start date
    4. Fetch repos from GitHub
    5. Display results
    """

    # --- Step 1: Parse command-line arguments ---
    parser = build_parser()
    args = parser.parse_args()

    # args now has:
    #   args.duration  →  'week' (or whatever the user passed)
    #   args.limit     →  10     (or whatever the user passed)
    #   args.language  →  None   (or 'python' etc.)

    # --- Step 2: Validate inputs ---
    # argparse handles basic type validation.
    # Our custom validate_limit() checks the range (1–100).
    try:
        limit = validate_limit(args.limit)
    except ValueError as e:
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)

    # --- Step 3: Calculate the start date from the duration ---
    # 'week' → '2024-12-20' (7 days ago)
    try:
        start_date = get_start_date(args.duration)
    except ValueError as e:
        print(f"\n[ERROR] {e}\n")
        sys.exit(1)

    # --- Step 4: Show a loading message ---
    display_loading(args.duration)

    # --- Step 5: Fetch repos from GitHub API ---
    repos = fetch_trending_repos(
        start_date=start_date,
        limit=limit,
        language=args.language,
    )

    # --- Step 6: Display the results ---
    display_repos(repos, duration=args.duration, limit=limit)


# This block runs only when you execute main.py directly:
#   python main.py --duration week
# It does NOT run when main.py is imported as a module.
# setup.py's entry_points uses main() directly, bypassing this.
if __name__ == "__main__":
    main()
