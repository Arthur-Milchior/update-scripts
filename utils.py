import os

from git import Repo
from git.exc import GitCommandError

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
    with open(rebase_head_file, "tr") as f:
        return f.readline().strip()

def currentlyMergingOn(r):
    """
    :return: The hash of the commit which is currently being replayed while rebasing.

    None if we are not currently rebasing.
    """
    rebase_head_file = os.path.join(r.git_dir, "MERGE_HEAD")
    if not os.path.isfile(rebase_head_file):
        return None
    with open(rebase_head_file, "tr") as f:
        return f.readline().strip()


r = Repo("../source")
def ignoreSomeRebase():
    while True:
        rebasingOn = currentlyRebasingOn(r)
        if rebasingOn is None:
            return
        #print(f"Rebasing on «{rebasingOn}»")
        if rebasingOn in toIgnoreRebase:
            print(f"skipping {rebasingOn}")
            try:
                r.git.rebase("--skip")
            except GitCommandError:
                pass
        else:
            print(f"rebasing: not skipping {rebasingOn}")
            return
ignoreSomeRebase()

def ignoreSomeMerge():
    while True:
        mergingOn = currentlyMergingOn(r)
        if mergingOn is None:
            return
        if mergingOn in toIgnoreMerge:
            print(f"skipping {mergingOn}")
            try:
                r.git.add("-u")
                r.git.apply("--reverse --index -p0 --ignore-space-change -")
                r.git.apply("--reverse --index -p0 --ignore-space-change -")
            except GitCommandError:
                pass
        else:
            print(f"merging: not skipping {mergingOn}")
            return
ignoreSomeMerge()

def execute(tag, callable):
    print(f"Trying to do {tag}")
    ignoreSomeRebase()
    ignoreSomeMerge()
    isort()
    if r.is_dirty():
        print("It's dirty")
        raise Dirty
    print(f"""Calling {tag}""")
    ret =callable()
    print(f"{tag}: {ret}")


with open("../update/tested", "rt") as f:
    testeds = [tested.rstrip() for tested in f.readlines()]
# print(f"""tested are:""")
# for tested in testeds:
#     print(f"«{tested}»")


def testSucceed():
    os.chdir("../source")
    if 0==os.system("""grep -qR "<<<<<<" * """):
        print("Some <<<<<< found")
        return False
    if 0==os.system("""grep -qR ">>>>>>>" * """):
        print("Some >>>>>>> found")
        return False

    currentHash = str(r.head.commit.binsha)
    if currentHash in testeds:
        print(f"{currentHash} was already succesfully testeds")
        return True
    print(f"{currentHash} is not yet succesfully testeds")
    os.system("./tools/build_ui.sh")
    # returned = os.system("./tools/tests.sh")
    # if returned != 0:
    #     return False

    os.chdir("../update")
    print(f"{currentHash} is succesfully tested")
    with open("tested", "at") as f:
        testeds.append(currentHash)
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

def isort():
    if not r.is_ancestor("factorized", "HEAD"):
        return
    os.system("isort -rc -y -s runanki -s aqt/forms")
