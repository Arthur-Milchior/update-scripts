from utils import *


def mergeParentInChild(parent, child):
    if  r.is_ancestor(parent, child):
        print(f"{parent} is contained in {child}")
    else:
        print(f"starting to merge {parent} in {child}")
        execute(f"checkout parent {parent} to test", lambda: r.git.checkout(parent))
        testAndRaise()
        execute(f"checkout child {child} to merge", lambda: r.git.checkout(child))
        execute(f"merge {child} on {parent}", lambda: r.git.merge(parent, "--no-ff"))
    update(child)
