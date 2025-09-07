#! /usr/bin/env python

"""
    This script takes a list of repositories and tries to push them.
"""
import os
import sys
from pathlib import Path
import subprocess
from rich import print
import yaml


def branch_ahead(remote: str, branch: str) -> bool:
    """Return True if local branch is ahead of remote."""
    result = subprocess.run(['git', 'rev-list', f"{branch}..HEAD", "--count"],
                            check=True, capture_output=True, text=True)
    return int(result.stdout.strip()) > 0

def current_branch() -> str:
    """Return the current branch."""
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                            check=True, capture_output=True, text=True)
    return result.stdout.strip()

def working_tree_clean() -> bool:
    """Return if the working tree is clean."""
    result = subprocess.run(['git', 'status', '--porcelain'],
                            check=True, capture_output=True, text=True)
    return result.stdout.strip() == ""

def get_repositories() -> list:
    """ Returns the list of repositories from the configuration file.
        Halts on error. """
    specs_path_dir = Path("~/.config/repos").expanduser().absolute()

    if not specs_path_dir.is_dir():
        print(f"[red]ERROR[/]: {specs_path_dir} does not exist")
        sys.exit(1)

    repos_file = specs_path_dir / "repositories.yaml"
    if not repos_file.is_file():
        print(f"[red]ERROR[/]: {repos_file} does not exist")
        sys.exit(1)

    with open(specs_path_dir / "repositories.yaml", "r") as f:
        repositories = yaml.safe_load(f)
    return repositories

def main():
    repositories = get_repositories()
    for path_str, remote, branch in repositories:
        print()
        print("#" * 100)
        print("# " + path_str)
        print("#" * 100)
        path = Path(path_str).expanduser()
        print(f"pulling {path} from {remote} {branch}")
        os.chdir(path)
        result = subprocess.run(["git", "status"], check=True, capture_output=True, text=True)
        if working_tree_clean():
            initial_branch = current_branch()
            if not branch_ahead(remote, branch):
                print(f"[green]INFO[/]: Nothing to push")
                continue
            if initial_branch != branch:
                subprocess.run(["git", "checkout", branch], check=True)
            try:
                subprocess.run(['git', 'push', remote, branch], check=True)
                print(f"[green]INFO[/]: pushed {path_str}:{branch}")
            finally:
                if current_branch() != initial_branch:
                    subprocess.run(["git", "checkout", initial_branch], check=True)
            continue
        print("[yellow]WARNING[/]: Repo dirty, skipping: {path_str}")
        print(result.stdout)

if __name__ == "__main__":
    main()
