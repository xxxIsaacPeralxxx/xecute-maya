#Cutpaste this code to a new file and save it near the main python file (G:\Kumaresan\MyPython\LBR\LBR.py)
#After that save and run the cutpasted file with arguments as shown below.. (Else Use the tool to do it ...)
#Python.exe setup.py py2exe --includes sip

from py2exe.build_exe import py2exe
from distutils.core import setup
import py2exe
MAINFILE = "XecuteMaya.py"
MICON = "icon.ico"

setup(
    windows = [
        {
            "script": MAINFILE,
            "icon_resources": [(0, MICON)],

        }
    ],
    options = {
                "py2exe": {
                            "bundle_files":1,
                            "compressed": 1
                          }

              }

)
