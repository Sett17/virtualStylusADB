import subprocess
import signal
import sys
import pynput
from win32api import GetSystemMetrics

# INIT

# catch close signal, stop adb server cause why not
def signal_handler(signal, frame): 
     print('Stopping ADB Server')
     subprocess.call(['adb.exe', 'kill-server'])
     sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

mouse = pynput.mouse.Controller()
left = pynput.mouse.Button.left
right = pynput.mouse.Button.right
display = 0
displayDir = 1 # 1 = right, -1 = left
size = (GetSystemMetrics(0), GetSystemMetrics(1))

scrollMode = False
#  INIT end

def exec(msg):
    global display
    global size
    global scrollMode

    # print(msg)
    if msg[0] == 'm':
        pos = msg[1:].split(',')
        xOffset = size[0] * display
        mouse.position = (int(pos[0]) + xOffset, int(pos[1]))
    elif msg[0] == 'l':
        if msg[1] == 'd':
            mouse.press(left)
        elif msg[1] == 'u':
            mouse.release(left)
            pass
    elif msg[0] == '1':
        if msg[1] == 'd':
            pass
        elif msg[1] == 'u':
            pass
    elif msg[0] == '2':
        if msg[1] == 'd':
            pass
        elif msg[1] == 'u':
            if display > 0:
                display = 0
            elif display < 1:
                display = 1
        pos = mouse.position
        xOffset = size[0] * display
        mouse.position = (pos[0] + xOffset, pos[1])

        

subprocess.call(['adb.exe', 'connect', '192.168.178.39']) # dbg

subprocess.call(['adb.exe', 'devices'])
subprocess.call(['adb.exe', 'shell', 'am', 'start', '-n', 'm.sett.virtualstyluswired/m.sett.virtualstyluswired.MainActivity'])
subprocess.call(['adb.exe', 'logcat', '-c'])

# sp = subprocess.Popen(['adb', 'logcat', 'm.sett.virtualstyluswired:D', '-s', '"VSW"'], stdout=subprocess.PIPE, universal_newlines=True).communicate()

with subprocess.Popen(['adb', 'logcat', 'm.sett.virtualstyluswired:D', '-s', 'VSW'], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
    for line in p.stdout:
        exec(line.split(': ')[-1])

if p.returncode != 0:
    raise subprocess.CalledProcessError(p.returncode, p.args)

# subprocess.run(["adb", "shell am start -n m.sett.virtualstyluswired/m.sett.virtualstyluswired.MainActivity"], shell=True, check=True)
# output = subprocess.run(["adb", "logcat m.sett.virtualstyluswired:D -s \"VSW\""])

# print(output)

subprocess.call(['adb.exe', 'kill-server'])