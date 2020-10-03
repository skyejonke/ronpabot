import yaml
global source

# Main class for any piece of evidence
class evidence:
    def __init__(self, nameIn):
        self.name = nameIn
        self.text = "ERROR"
        self.subitems = []

def loadEvidence(active, triggered):
    itr = 0

    for i in active:
      if i == triggered:
        del active[itr]
      itr += 1

    active = active + triggered.subitems
    return active

def loadFile(url):
    locations = {}
    with open(url) as file:
        global source
        source = yaml.load(file, Loader=yaml.FullLoader)

    for i in source.keys():
        locations[i] = loadFileHelper(source[i])

    return locations

def loadFileHelper(start):
    out = []
    for i in start.keys():
        n = evidence(i)
        n.text = start[i]["Text"]
        if ("Next" in start[i]):
            n.subitems = loadFileHelper(start[i]["Next"])
        out.append(n)

    return out



loadFile(r'example.yaml')


# def parser(source, active, inpt):








