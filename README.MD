# trending-repos

A Python CLI tool to discover trending GitHub repositories filtered by time range.

---

## What It Does

Queries the GitHub Search API to find repositories created recently,
sorted by star count. Displays them in a clean terminal table.

---

## Installation

### Step 1 — Clone or download the project

```bash
git clone https://github.com/yourusername/trending-repos.git
cd trending-repos
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Install as a CLI command (optional but recommended)

```bash
pip install -e .
```

After this, you can use `trending-repos` from anywhere in your terminal.

---

## Usage

### Basic usage (defaults: week, 10 repos)

```bash
trending-repos
```

### Filter by time range

```bash
trending-repos --duration day      # Trending today
trending-repos --duration week     # Trending this week (default)
trending-repos --duration month    # Trending this month
trending-repos --duration year     # Trending this year
```

### Change number of results

```bash
trending-repos --duration month --limit 20
trending-repos --duration week --limit 5
```

### Filter by programming language

```bash
trending-repos --duration week --language python
trending-repos --duration month --language javascript --limit 15
trending-repos --duration day --language go
```

### Show help

```bash
trending-repos --help
```

---

## Without installing (run directly with Python)

```bash
cd trending-repos
python -m trending_repos.main --duration week --limit 10
```

---

## Arguments

| Argument     | Type   | Default | Options                         |
|--------------|--------|---------|---------------------------------|
| `--duration` | string | `week`  | `day`, `week`, `month`, `year`  |
| `--limit`    | int    | `10`    | 1–100                           |
| `--language` | string | None    | Any GitHub language name        |

---

## Example Output

```
╭─────────────────────────────────────────────────────────╮
│  🔥 GitHub Trending Repositories                        │
│  Showing top 10 repos from the last week                │
╰─────────────────────────────────────────────────────────╯

 #   Repository              Description                Stars    Language      Forks
 🥇1  user/awesome-project   A project that does X      12,345   Python        1,234
 🥈2  user/cool-tool         Another great tool          8,901   TypeScript      890
 🥉3  user/fast-api-starter  FastAPI boilerplate         7,200   Python          720
```

---

## Rate Limits

Without authentication, GitHub allows:
- **10 search requests per minute**
- **60 API requests per hour**

If you hit the limit, wait 1 minute and try again.

To increase limits, add a GitHub Personal Access Token:

```bash
export GITHUB_TOKEN=your_token_here
```

Then in `fetcher.py`, uncomment the Authorization header line.

---

## Project Structure

```
trending-repos/
├── trending_repos/
│   ├── __init__.py    ← Package marker
│   ├── main.py        ← Entry point + argparse
│   ├── fetcher.py     ← GitHub API logic
│   ├── display.py     ← Rich terminal output
│   └── utils.py       ← Date helpers
├── setup.py           ← CLI installation config
├── requirements.txt   ← Dependencies
└── README.md          ← This file
```

---

## Tech Stack

| Tool         | Purpose                              |
|--------------|--------------------------------------|
| Python 3.10+ | Language                             |
| `requests`   | HTTP calls to GitHub API             |
| `rich`       | Beautiful terminal tables and colors |
| `argparse`   | Command-line argument parsing        |
| `datetime`   | Calculating date ranges              |
