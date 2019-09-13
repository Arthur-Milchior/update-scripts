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

sortDifference()
