#! /usr/bin/env python

"""
    This script takes a list of repositories and tries to pull them.
"""
import os
from pathlib import Path
import subprocess
from rich import print
import pushall

def main():
    repositories = pushall.get_repositories()
    for path_str, remote, branch in repositories:
        print()
        print("#" * 100)
        print("# " + path_str)
        print("#" * 100)
        path = Path(path_str).expanduser()
        print(f"pulling {path} from {remote} {branch}")
        os.chdir(path)
        result = subprocess.run(["git", "status"], check=True, capture_output=True, text=True)
        if pushall.working_tree_clean():
            initial_branch = pushall.current_branch()
            if initial_branch != branch:
                subprocess.run(["git", "checkout", branch], check=True)
            try:
                subprocess.run(['git', 'pull', remote, branch], check=True)
                print(f"[green]INFO[/]: pulled {path_str}:{branch}")
            finally:
                if pushall.current_branch() != initial_branch:
                    subprocess.run(["git", "checkout", initial_branch], check=True)
            continue
        print("[yellow]WARNING[/]: Repo dirty, skipping: {path_str}")
        print(result.stdout)

if __name__ == "__main__":
    main()
