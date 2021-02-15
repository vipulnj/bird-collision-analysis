import json
from collections import Counter

def isValidJsonFile(jsonFile):
    """
    Checks if JSON file is a valid input or not
    """
    
    try:
        with open(jsonFile, 'r') as fh:
            jsonObj = json.load(fh)
    except ValueError as e:
        print(f"{jsonFile} could not be loaded since it's not a valid JSON file.")
        return False
    
    # if no issues so far, then it's a valid JSON file
    return True

def checkSerialNumbersInJsonFile(jsonFile):
    """
    Check for duplicated or mismatching serial numbers under each key in the json file
    """
    
    with open(jsonFile, 'r') as fh:
        jsonData = json.load(fh)
    
    keyNames = list(jsonData.keys()) # in input json file
    recSerNum_counterDictionaries = {} # dictionary of dictionaries
    
    # get record serial numbers as under each key of the JSON as a list
    for keyName in keyNames:
        recSerNumList = list(jsonData[keyName].keys())
        # gives record numbers under this key as list of strings
        # i.e. ["0", "1", "2" ...]
        
        recSerNum_counterDict = dict(Counter(recSerNumList)) # contains data of format
        # {"0": 1, "1": 1, "2": 1,  }
        
        # we apply Counter() on recSerNumList to count the number of occurences
        # of serial numbers. We know that, every serial number must occur only once,
        # therefore, we should see a count of 1 and only 1 for each serial number.
        
        if set(list(recSerNum_counterDict.values())) != {1}:
            print(f"FAILED! Some serial numbers occur more than once for the key {keyName} in {jsonFile}")
            return False
        
        # save the count dictionary with the key name we're extracting it from
        recSerNum_counterDictionaries[keyName] = recSerNum_counterDict
    
    # all the dictionaries must be same and must agree with each other 
    # in terms of the record numbers count dictionaries.
    # we test the count dictionary of first key with each of the 
    # remaining dictionaries. 
    # If they are no issues, then that completes our sanity check for record numbers.
    
    firstKeyName = keyNames[0]
    firstKeyName_counterDict = recSerNum_counterDictionaries[firstKeyName]
    
    for keyName in keyNames[1:]: # compare the firstKeyName_counterDict with rest of the keys' counterDictionaries
        if not firstKeyName_counterDict == recSerNum_counterDictionaries[keyName]:
            print(f"FAILED! {keyName} key's record serial number counter does not agree with {firstKeyName} counter in {jsonFile}")
            return False
    
    # if no issues so far,
    return True


def changeToTitleCase(inputString):
    """
    Change to title case
    """
    inputString = inputString.strip() # remove trailing and leading whitespace
    inputString = inputString.title()
    return inputString


def changeToLowerCase(inputString):
    """
    Chnage to lower case
    """
    inputString = inputString.strip() # remove trailing and leading whitespace
    inputString = inputString.lower()
    return inputString