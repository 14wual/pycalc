# ██╗    ██╗██╗   ██╗ █████╗ ██╗     
# ██║    ██║██║   ██║██╔══██╗██║     
# ██║ █╗ ██║██║   ██║███████║██║     (code by wual)
# ██║███╗██║██║   ██║██╔══██║██║     
# ╚███╔███╔╝╚██████╔╝██║  ██║███████╗
#  ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝

# See proyect >> https://github.com/14wual/pycalc
# Follow me >> https://twitter.com/14wual

from pycalc.windows import WinStartUp
from pycalc.linux import LinStartUp
from tkinter import messagebox
import platform

def whichSystem():
    return platform.system()

if __name__ == '__main__':
    if whichSystem() == 'Linux':app = LinStartUp();app.run()
    elif whichSystem() == 'Windows':app = WinStartUp();app.run()
    else:messagebox.Message("Alert!", "Unrecognized Operating System.")
