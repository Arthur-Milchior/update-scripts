#!/usr/bin/env python3

import os
import sys
import time

from git.exc import GitCommandError

from data import *
from mergeMethods import *
from utils import *

# try:
#     for parent, child in pairs:
#         mergeParentInChild(parent, child)
# except Dirty:
#     pass


for commit in children:
    if not r.is_ancestor(f"milchior/{commit}", commit):
        r.git.checkout(commit)
        testAndRaise()
        print(f"Trying to push {commit} on github")
        execute("push", lambda: r.git.push("--force", "milchior", commit))
        print(f"pushed {commit}")
    else:
        print(f"«{commit}» already pushed")

if not r.is_ancestor("fork", f"milchior/fork"):
    testAndRaise()
    execute("push", lambda: r.git.push( "milchior", "fork"))
