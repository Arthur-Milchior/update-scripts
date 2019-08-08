#!/usr/bin/env python3

import os
import sys
import time
from git.exc import GitCommandError
from data import *
from utils import *
from mergeMethods import *

try:
    for parent, child in pairs:
        mergeParentInChild(parent, child)
except Dirty:
    pass


for commit in children:
    if not r.is_ancestor(commit, "fork"):
        r.git.checkout(commit)
        testAndRaise()
        r.git.checkout("fork")
        testAndRaise()
        print(f"Trying to merging {commit} into fork")
        r.git.merge(commit)
        print(f"Merge {commit} into fork suceeded")

if not r.is_ancestor("fork", f"milchior/fork"):
    testAndRaise()
    execute("push", lambda: r.git.push( "milchior", "fork"))
