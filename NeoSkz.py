#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This script reads ~/.NeoSkz and processes each line (ignoring ^#)
# of the form «path» «direction» «repository name» [«branch name»]
# Where «branch name» is optional and defaults to *master*

# The script tries to find «path» and, when available, it cds to it
# If it corresponds to the root of a git repository, it:
# 1. adds everything new to stage
# 2. commits changes with argv[1] message if present or a default
# missage otherwise.
# 3. if direction is '<' or '<>' pulls changes from repository name
# 4. if direction is '>' or '<>' pushes changes to repository name
#   Note: if direction is not specified, it is assumed <>

# XXX TODO: offer a way to dissable autocommit on all files! e.g. add
# a repo type at the begining of the line

import sys, os, datetime, re
import subprocess

_CONFIG_FILE = os.path.expanduser("~/.NeoSkz")
_LINE_COMMENT = "^\s*#"
_LINE_FORMAT = "^(?:[\"'])?(\S+?)(?:[\"'])?\s+(\<|\>|(?:\<\>))?\s*(\w+)(\s+(\w+))?\s*$"
_COMMAND_COMMIT = 'git add -A && git commit -am "%s"'
_COMMAND_PULL   = 'git pull %s %s'
_COMMAND_PUSH   = 'git push %s %s'

_WORKING_DIRECTORY_CLEAN = 'nothing to commit (working directory clean)'
_FATAL = 'fatal: '
_ERROR = 'remote: error: '

_commits_in_path = {} # { path: bool_something_to_push }

def run_command(command):
    """ runs a command appending exit 0 and returning stdout&&stderr """
    print ("$ %s"%command)
    return subprocess.check_output("%s; exit 0"%command,
                                   stderr=subprocess.STDOUT,
                                   shell=True).decode('utf-8')

def has_error(message):
    """ returns true if an error is present in the message """
    return _FATAL in message or _ERROR in message

def do_commit_on_path(path, message):
    """ tries to commit on path.
        First it checks if path has been already commited """
    if path not in _commits_in_path:
        _commits_in_path[path]=False
        if os.path.exists(path):
            os.chdir(path)
            res = run_command(_COMMAND_COMMIT%message)
            if _WORKING_DIRECTORY_CLEAN not in res:
                _commits_in_path[path]=True
        else:
            print("Warning: path not found '%s'"%path)

def do_pull(path, repo, branch):
    """ tries to pull from repo """
    if os.path.exists(path):
        os.chdir(path)
        command = _COMMAND_PULL%(repo, branch)
        res = run_command(command)
        if has_error(res):
            print(res)
    else:
        print("Warning: path not found '%s'"%path)

def do_push(path, repo, branch):
    """ tries to push to repo """
    if os.path.exists(path):
        os.chdir(path)
        command = _COMMAND_PUSH%(repo, branch)
        res = run_command(command)
        if has_error(res):
            print(res)
    else:
        print("Warning: path not found '%s'"%path)

def processa(path, direction, repo, branch, message):
    print("\nOn path: %s"%path)
    if '<' in direction:
        do_pull(path, repo, branch)
    do_commit_on_path(path, message)
    if _commits_in_path[path] and '>' in direction:
        do_push(path, repo, branch)

def main():
    if not os.path.exists(_CONFIG_FILE):
        print("ERROR: missing config file %s."%_CONFIG_FILE, file=sys.stderr)
        sys.exit(1)

    if len(sys.argv)>1:
        message = sys.argv[1]
    else:
        message = datetime.datetime.today().isoformat()

    commentregex = re.compile(_LINE_COMMENT)
    lineregex = re.compile(_LINE_FORMAT)
    with open(_CONFIG_FILE) as f:
        for line in f:
            if commentregex.match(line):
                continue
            m = lineregex.match(line.strip())
            if m:
                path = os.path.expanduser(m.group(1))
                direction = m.group(2)
                repo = m.group(3)
                branch = m.group(4)
                if direction == None:
                    direction = "<>"
                if branch == None:
                    branch = "master"
                processa(path, direction, repo, branch, message)

if __name__=="__main__":
    sys.exit(main())

