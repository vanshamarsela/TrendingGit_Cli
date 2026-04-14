"""
display.py
----------
All terminal output lives here. Uses the 'rich' library to create
beautiful, colored tables with borders, emojis, and formatting.

WHY RICH?
Plain print() works, but Rich makes output actually readable:
- Color coding by rank (🥇🥈🥉)
- Aligned columns regardless of content length
- Handles long descriptions gracefully (no overflowing)
- Works on Windows, Mac, and Linux terminals
"""

from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding


# Create a single Console instance that we reuse everywhere.
# Console handles all the fancy terminal detection and color support.
console = Console()


def display_repos(repos: list[dict], duration: str, limit: int) -> None:
    """
    Display the fetched repositories in a formatted table.

    This is the main display function. It:
    1. Shows a header panel with context info
    2. Renders a Rich table with one row per repo
    3. Shows a footer with usage tips

    Args:
        repos:    List of repo dicts from fetcher.py
        duration: The duration string used ('day', 'week', etc.)
        limit:    How many repos were requested
    """
    actual_count = len(repos)

    # --- Header Panel ---
    header_text = (
        f"[bold]🔥 GitHub Trending Repositories[/bold]\n"
        f"[dim]Showing top {actual_count} repos from the last [bold]{duration}[/bold][/dim]"
    )
    console.print()
    console.print(Panel(header_text, border_style="bright_blue", padding=(0, 2)))
    console.print()

    # --- Build the Table ---
    table = Table(
        box=box.ROUNDED,            # Nice rounded corners
        show_header=True,
        header_style="bold cyan",
        border_style="bright_black",
        expand=True,                # Use full terminal width
        show_lines=False,           # No lines between rows (cleaner)
    )

    # Define columns with their widths and alignments
    # 'ratio' distributes remaining space proportionally
    table.add_column("#",           style="dim",          width=4,   justify="right")
    table.add_column("Repository",  style="bold white",   ratio=25)
    table.add_column("Description", style="dim white",    ratio=45)
    table.add_column("⭐ Stars",    style="yellow bold",  width=10,  justify="right")
    table.add_column("Language",    style="green",        width=14)
    table.add_column("🍴 Forks",   style="cyan",         width=8,   justify="right")

    # --- Add a row for each repo ---
    for index, repo in enumerate(repos, start=1):
        rank = _get_rank_emoji(index)

        # Truncate long descriptions so the table doesn't break layout
        description = repo["description"]
        if len(description) > 90:
            description = description[:87] + "..."

        # Format star count with commas: 12345 → 12,345
        stars_formatted = f"{repo['stars']:,}"
        forks_formatted = f"{repo['forks']:,}"

        # Make the repo name a clickable-looking link (terminal hyperlinks)
        repo_name = repo["name"]

        table.add_row(
            f"{rank}{index}",
            repo_name,
            description,
            stars_formatted,
            repo["language"],
            forks_formatted,
        )

    console.print(table)

    # --- Topics footer (shown for top 3 repos) ---
    _display_topics(repos[:3])

    # --- Footer ---
    console.print()
    console.print(
        f"[dim]  💡 Tip: Use [bold]--duration day[/bold] for daily trends "
        f"or [bold]--duration month[/bold] for monthly. "
        f"Add [bold]--limit 20[/bold] to see more.[/dim]"
    )
    console.print()


def _get_rank_emoji(index: int) -> str:
    """Return a medal emoji for top 3, empty string otherwise."""
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    return medals.get(index, "  ")


def _display_topics(top_repos: list[dict]) -> None:
    """
    Show the topic tags for the top 3 repositories.
    Topics are like hashtags on GitHub — e.g. ['python', 'cli', 'tools']
    """
    has_topics = any(repo.get("topics") for repo in top_repos)
    if not has_topics:
        return

    console.print()
    console.print("  [bold dim]Top repo topics:[/bold dim]")

    for repo in top_repos:
        topics = repo.get("topics", [])
        if not topics:
            continue

        # Build colored topic pills
        topic_pills = "  ".join(
            f"[bold blue on bright_black] {t} [/bold blue on bright_black]"
            for t in topics[:6]   # Show max 6 topics per repo
        )
        short_name = repo["name"].split("/")[-1]  # Just the repo part, not 'user/repo'
        console.print(f"  [dim]{short_name}:[/dim] {topic_pills}")


def display_error(message: str) -> None:
    """Display a formatted error message in a red panel."""
    console.print()
    console.print(
        Panel(
            f"[bold red]Error:[/bold red] {message}",
            border_style="red",
            padding=(0, 2),
        )
    )
    console.print()


def display_loading(duration: str) -> None:
    """Show a brief loading message while the API call is in progress."""
    console.print(
        f"\n[dim]  Fetching trending repos from the last [bold]{duration}[/bold]...[/dim]"
    )
