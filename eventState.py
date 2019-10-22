eventDict = {}

def getState(id):
    try:
        return eventDict[id]
    except:
        eventDict[id] = False
        return False

def setState(id, state):
    eventDict[id] = state