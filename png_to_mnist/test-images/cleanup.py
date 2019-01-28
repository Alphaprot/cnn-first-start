import os

scriptPath = os.path.dirname(os.path.abspath(__file__))

def cleanUp():
    for filename in os.listdir(scriptPath):
        if os.path.isfile(filename) and not "-" in filename:
                os.remove(filename)
                print("Deleted file \"()\"" .format (filename))

cleanUp()
