import sys
import time

from sortMd import sortAll
from utils import *


def rebase(*args, **kwargs):
    """If dirty want to ignore this particular rebase, we should avoid raising an exception"""
    if currentlyRebasingOn(r):
        raise Exception("Attempt to do a rebase during a rebase")
    if currentlyMergingOn(r):
        raise Exception("Attempt to do a rebase during a merge")
    try:
        r.git.rebase(*args, **kwargs)
    except GitCommandError:
        ignoreSomeRebase()
        sortAll()
        if r.is_dirty():
            raise

rebaseOver = [
    "b1fe8fa2546f613a3d470245ce636304ae820fba", #explode fix integrity
    "a7543df6ec64f5341ec5ab1f3397fb15e3453491", #baseFork
]

def rebaseOnto(parent, child):
    if r.is_ancestor(parent, child):
        print(f"{child} already rebased on {parent}")
        return
    execute(f"checkout parent {parent}", lambda: r.git.checkout(parent))
    testAndRaise()
    if "/" not in parent and r.is_ancestor(f"milchior/{parent}", child):
        execute(f"checkout {child}", lambda: r.git.checkout(child))
        execute(f"rebase {child} onto {parent}", lambda: rebase("--onto", parent, f"milchior/{parent}", child))
        return
    execute(f"checkout {child}", lambda: r.git.checkout(child))
    print(f"Can't rebase {child} onto {parent} as it's not descendant of milchior/{parent}, and not of {parent} either")
    rebaseChildOnParent(parent, child, parentTested=True)

def rebaseChildOnParent(parent, child, parentTested=False):
    if not parentTested:
        testAndRaise()
    if r.is_ancestor(parent, child):
        print(f"{child} already rebased on {parent}")
    else:
        time.sleep(1)
        execute(f"checkout {child}", lambda: r.git.checkout(child))
        execute(f"rebase {child} on some fixed baseFork", lambda: rebase(parent))
    update(child)
