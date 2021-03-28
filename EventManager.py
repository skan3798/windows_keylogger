'''
Handles storing of keyevents and pushing to backend
'''

class EventManager:
    def __init__ (self):
        # self.caps = False # is capslock/shift currently activated?
        self.history = []
        self.historyCount = 0 # len(self.history)
        self.historyThreshold = 100
    
    
    def addEvent(self, asciiCode, asciiChar, caps, windowName, processedKey, time):
        event = KeyEvent(asciiCode, asciiChar, caps, windowName, processedKey, time)
        self.__pushEvent(event)
    
    def addEvent(self, keyEvent):
        if type(keyEvent) == KeyEvent:
            self.__pushEvent(keyEvent)
        else:
            pass    
    '''
        event: KeyEvent
        pushes
    '''
    def __pushEvent(self, event):
        # append event to history
        # if historythreshold is hit, push to backend
        
        self.history.append(event)
        
        if self.historyCount >= self.historyThreshold:
            self.__pushHistoryToBackend()
            
    def __pushHistoryToBackend(self):
        try:
            print("Pushing data to backend")
            # TODO: push to api (POST to hotchips)
            payload = {}
            i = 0
            for e in self.history:
                payload[i] = e.toJSON()
            
            
            return 0
        except Exception:
            print("Error pushing to backend")
            return 1

class KeyEvent:
    def __init__(self,datetime, epochTime, messageName, windowName, asciiCode, asciiChar, keyName, caps, processedKey):
        self.datetime = datetime # datetime in format "%d/%m/%Y %H:%M:%S"
        self.epochTime = epochTime # epoch seconds
        self.messageName = messageName # e.g. 'key up' or 'key down'
        self.windowName = windowName # Name of the foreground window at the time of the event
        self.asciiCode = asciiCode # integer
        self.asciiChar = asciiChar # char
        self.keyName = keyName # string
        self.caps = caps # isCapital?
        self.processedKey = processedKey # `asciiChar` after parsing with caps
        
    def __str__(self):
        return f"KeyEvent(\n\tdatetime: {self.datetime}\n\tepochTime: {self.epochTime}\n\tmessageName: {self.messageName}\n\twindowName: {self.windowName}\n\tasciiCode: {self.asciiCode}\n\tasciiChar: {self.asciiChar}\n\tkeyName: {self.keyName}\n\tcaps: {self.caps}\n\tprocessedKey: {self.processedKey}\n)"
        
    def toJSON(self):
        res = {}
        res["datetime"] = self.datetime
        res["epochTime"] = self.epochTime
        res["messageName"] = self.messageName
        res["windowName"] = self.windowName
        res["asciiCode"] = self.asciiCode
        res["asciiChar"] = self.asciiChar
        res["keyName"] = self.keyName
        res["caps"] = self.caps
        res["processedKey"] = self.processedKey
        return res