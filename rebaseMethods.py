from utils import *
import sys

def rebase(*args, **kwargs):
    """If dirty want to ignore this particular rebase, we should avoid raising an exception"""
    try:
        r.git.rebase(*args, **kwargs)
    except GitCommandError:
        ignoreSomeRebase()
        if r.is_dirty():
            raise

def rebaseOnto(parent, child):
    if r.is_ancestor(parent, child):
        print(f"{child} already rebased on {parent}")
        return
    execute(f"checkout parent {parent}", lambda: r.git.checkout(parent))
    testAndRaise()
    if "/" not in parent and r.is_ancestor(f"milchior/{parent}", child):
        execute(f"checkout {child}", lambda: r.git.checkout(child))
        execute(f"rebase {child} onto {parent}", lambda: rebase("--onto", parent, f"milchior/{parent}", child))
    # elif parent=="baseFork":
    #     execute(f"rebase {child} on some fixed baseFork", lambda: rebase("--onto", parent, "5fc67d5515fb2d9db66f57ae9db92e5475e20f4e", child))
    else:
        execute(f"checkout {child}", lambda: r.git.checkout(child))
        print(f"Can't rebase {child} onto {parent} as it's not descendant of milchior/{parent}, and not of {parent} either")
        rebaseChildOnParent(parent, child, parentTested=True)
        #sys.exit(1)#execute(f"rebase {child} on {parent}", lambda:rebase(parent))

def rebaseChildOnParent(parent, child, parentTested=False):
    if not parentTested:
        testAndRaise()
    if r.is_ancestor(parent, child):
        print(f"{child} already rebased on {parent}")
    else:
        execute(f"checkout {child}", lambda: r.git.checkout(child))
        execute(f"rebase {child} on some fixed baseFork", lambda: rebase(parent))
    update(child)
