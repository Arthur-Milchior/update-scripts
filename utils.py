import os
from git.exc import GitCommandError
from git import Repo
from data import *

class Dirty(Exception):
    pass

def currentlyRebasingOn(r):
    """
    :return: The hash of the commit which is currently being replayed while rebasing.

    None if we are not currently rebasing.
    """
    rebase_head_file = os.path.join(r.git_dir, "REBASE_HEAD")
    if not os.path.isfile(rebase_head_file):
        return None
    with open(rebase_head_file, "tw") as f:
        return f.readline().strip()


r = Repo("source")
def ignoreSomeRebase():
    while True:
        rebasingOn = currentlyRebasingOn(r)
        #print(f"Rebasing on «{rebasingOn}»")
        if rebasingOn in toIgnoreRebase:
            print(f"skipping {rebasingOn}")
            try:
                r.git.rebase("--skip")
            except GitCommandError:
                pass
        else:
            print(f"not skipping {rebasingOn}")
            return
ignoreSomeRebase()

def execute(tag, callable):
    print(f"Trying to do {tag}")
    ignoreSomeRebase()
    if r.is_dirty():
        print("It's dirty")
        raise Dirty
    print(f"""Calling {tag}""")
    ret =callable()
    print(f"{tag}: {ret}")


with open("tested", "rt") as f:
    tested = f.readlines()
print(f"""tested are:
{tested}""")


def testSucceed():
    currentHash = str(r.head.commit.binsha)
    if currentHash in tested:
        print(f"{currentHash} was already succesfully tested")
        return True
    print(f"{currentHash} is not yet succesfully tested")
    os.chdir("source")
    os.system("./tools/build_ui.sh")
    returned = os.system("./tools/tests.sh")
    if returned != 0:
        return False

    if 0==os.system("""grep -qR "<<<<" * """) or 0==os.system("""grep -qR ">>>>>" * """):
        print("Some <<<< found")
        return False

    os.chdir("..")
    print(f"{currentHash} is succesfully tested")
    with open("tested", "at") as f:
        tested.append(currentHash)
        f.write(f"{currentHash}\n")
    return True

def testAndRaise():
    if not testSucceed():
        raise Exception("Test error")

def update(child):
    try:
        isAncestor = r.is_ancestor(child, f"milchior/{child}")
    except GitCommandError:
        isAncestor = False
    if isAncestor:
        print(f"{child} is contained in milchior/{child}")
    else:
        execute(f"checkout {child}", lambda: r.git.checkout(child))
        try:
            #if int(time.strftime("%H",time.localtime(time.time())))>10: #debugging fails before 10h
            testAndRaise()
            execute("push", lambda: r.git.push("--force", "milchior", child))
            pass
        except GitCommandError:
            #execute("set-upstream", lambda: r.git.branch(f"--set-upstream-to=milchior/{child}"))
            #execute("push", lambda: r.git.push("-u", "milchior", child))
            pass
