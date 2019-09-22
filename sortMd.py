import os.path


def newSection(line):
    return line.startswith("## ")

def toDelete(line):
    for stri in {"<<<<<<< HEAD\n", "=======\n", ">>>>>>>"}:
        if stri in line:
            return True

def sort(fileName):
    if not os.path.isfile(fileName):
        return
    with open(fileName, "r") as f:
        lines = f.readlines()
    sections = {}
    currentSectionName = ""
    sections[currentSectionName] = ""
    for line in lines:
        if toDelete(line):
            continue
        if newSection(line):
            if not sections[currentSectionName].endswith("\n\n"):
                sections[currentSectionName] += "\n"
            currentSectionName = line
            sections[currentSectionName] = ""
        sections[currentSectionName] += line
    if not sections[currentSectionName].endswith("\n\n"):
        sections[currentSectionName] += "\n"

    output = "".join([sections[key] for key in sorted(sections)])
    with open(fileName, "w") as f:
        f.write(output)

def sortDifference():
    sort("../source/difference.md")


def sortBetween(fileName, firstLine, lastLine):
    if not os.path.isfile(fileName):
        return
    with open(fileName, "r") as f:
        lines = f.readlines()
    step = "first"
    first = []
    toSort = []
    last = []
    current = first
    for line in lines:
        if step == "toSort":
            if lastLine in line:
                step = "last"
                current = last
            if line in current:
                continue
            found=False
            for s in {"<<<<<", "=====", ">>>>>"}:
                if s in line:
                    found=True
            if found:continue
        current.append(line)
        if step == "first" and firstLine in line:
            step = "toSort"
            current = toSort
    middle = sorted(toSort)
    output = "".join(first+middle+last)
    with open(fileName, "w") as f:
        f.write(output)
    
def sortAll():
    sortDifference()
    sortBetween("../source/anki/incorporatedAddons.py", "incorporatedAddonsSet = {", "}\n")
    sortBetween("../source/aqt/preferences.py", """{"name":"pastePNG", "sync":False}""", "]\n")
    
sortAll()
