#!/usr/bin/env python3
import os
import sys
import time

from git import Repo
from git.exc import GitCommandError

from consts import push
from data import *
from mergeMethods import *
from rebaseMethods import *
from sortMd import sortAll
from utils import *

rebased = set()


#execute("fetch", lambda: r.git.fetch("elmes"))


for parent, child in pairs:
    if child in rebased:
        print(f"{child} already rebased once, thus we merge {parent} in it instead of rebasing it")
        mergeParentInChild(parent, child)
    else:
        rebased.add(child)
        print(f"rebasing (if necessary) {parent} into {child} if needed")
        rebaseOnto(parent, child)
        sortAll()

execute("checkout fork", lambda: r.git.checkout("fork"))
for branch in leaves:
    if r.is_ancestor(branch, "fork"):
        print(f"{branch} is contained in fork")
        continue
    testAndRaise()
    try:
        execute(f"merge {branch}", lambda: r.git.merge(branch, "-m", f"merge {branch}", "--no-ff"))
        sortAll()
    except GitCommandError:
        sortAll()
        isort()
        testAndRaise()
        r.git.add("-u", ".")
        if 0==os.system("""grep -qR "<<<<<<" * """):
            print("Merge can't be automated because of <<<<")
            raise
        r.git.commit(file=".git/MERGE_MSG")

testAndRaise()
if not r.is_ancestor("fork", f"milchior/fork"):
    if push:
        execute("push", lambda: r.git.push("--force", "milchior", "fork"))
