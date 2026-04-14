"""
setup.py
--------
This file makes your tool installable as a real terminal command.

After running: pip install -e .
You can type:  trending-repos --duration week
...from ANYWHERE in your terminal, not just from the project folder.

HOW entry_points WORKS:
The magic is in 'entry_points'. It creates a script called 'trending-repos'
that calls the main() function from trending_repos/main.py.

'trending-repos = trending_repos.main:main' means:
  Command name      = trending-repos
  Python module     = trending_repos.main   (the main.py file)
  Function to call  = main                  (the main() function)
"""

from setuptools import setup, find_packages

setup(
    name="trending-repos",
    version="1.0.0",
    description="A CLI tool to discover trending GitHub repositories",
    author="Your Name",
    python_requires=">=3.10",

    # Automatically find all packages (folders with __init__.py)
    packages=find_packages(),

    # External libraries this project needs
    install_requires=[
        "requests>=2.28.0",   # For HTTP calls to GitHub API
        "rich>=13.0.0",        # For beautiful terminal output
    ],

    # THIS IS THE KEY PART — creates the 'trending-repos' terminal command
    entry_points={
        "console_scripts": [
            "trending-repos = trending_repos.main:main",
        ],
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
)
