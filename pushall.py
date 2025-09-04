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
        print(f"pushing {path} from {remote} {branch}")
        os.chdir(path)
        result = subprocess.run(["git", "status"], check=True, capture_output=True, text=True)
        if 'working tree clean' in result.stdout:
            initial_branch = result.stdout.split('\n')[0].split("On branch ")[1]
            print(f"[green]INFO[/]: initial branch is {initial_branch}")
            try:
                subprocess.run(["git", "checkout", branch], check=True)
                result = subprocess.run(["git", "status"], check=True, capture_output=True, text=True)
                if f"Your branch is ahead of '{remote}/{branch}'" not in result.stdout:
                    print("[green]INFO[/]: nothing to push")
                    continue
                result = subprocess.run(["git", "push", remote, branch], check=True, capture_output=True, text=True)
                print(f"[green]INFO[/]: pushed {path_str}")
                print(result.stdout)
            finally:
                subprocess.run(["git", "checkout", initial_branch], check=True)
                result = subprocess.run(["git", "status"], check=True, capture_output=True, text=True)
                final_branch = result.stdout.split('\n')[0].split("On branch ")[1]
                print(f"[green]INFO[/]: final branch is {final_branch}")

            continue
        print("[yellow]WARNING[/]: Review the changes before pushing")
        print(result.stdout)

if __name__ == "__main__":
    main()
