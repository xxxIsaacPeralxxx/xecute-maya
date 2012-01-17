
from distutils.core import setup
import py2exe
import sys
import os
import shutil


#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()

####Adjust these Parent Folder to reach root folder####
    parentFolder1 = os.path.dirname(currentFolder)
    parentFolder2 = os.path.dirname(parentFolder1)

####Pass parentFolder Level to reach Root folder####
    rootFolder = os.path.dirname(parentFolder2)
    rootFolderParent = os.path.dirname(rootFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                      parentFolder1 + '/lra',
                      parentFolder1 + '/lra/lib',
                      parentFolder1 + '/lra/uis',
                      parentFolder1 + '/lra/res',
                      parentFolder1 + '/opl',
                      ##'F:\PYTHON\LIB',
                      "F:\\Kumaresan\\Dev\\Python\\opl",
                      "F:\\Kumaresan\\Dev\\Python\\lib",
                      "F:/Tools/TweakNow PowerPack 2009/Module32"
                     ]

    for modulePath in modulePathList:
        if os.path.abspath(modulePath) not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(os.path.abspath(modulePath))


import warnings
warnings.simplefilter('ignore')

#PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = "XecuteMaya.py"
APPNAME = 'Execute Maya'
DESCRIPTION = 'Execute Maya'
COMPANY_NAME = 'Kumaresan '
COPYRIGHT = 'GNU'
VERSION = '0.0.1'
USE_ICON = False
ICON_FILE = 'icon.ico'
FOLDER_SUFFIX = 'bin'
RELEASE_OWNER = 'LKUMARESAN'
BUNDLE_LEVEL = 1                        # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = True
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip']
PACKAGES = []

#PY2EXE PROCESS...
appVariable = {
                'name': APPNAME,
                'version': VERSION,
                'company_name': COMPANY_NAME,
                'copyright': COPYRIGHT,
                'description': DESCRIPTION
              }

if MAIN_SCRIPT_FILE: appVariable['script'] = MAIN_SCRIPT_FILE
if USE_ICON: appVariable['icon_resources'] = [(0, ICON_FILE)]

opVars = {
            "py2exe":{
                        "packages":PACKAGES,
                        "includes":INCLUDES,
                        "bundle_files": BUNDLE_LEVEL,
                        "compressed": DO_COMPRESS,
                        "dist_dir":str(MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE)-3])+'_'+FOLDER_SUFFIX,
                     }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable],options=opVars,zipfile=1,version="0.0.0.1",author='LKUMARESAN')
    else:
        setup(console=[appVariable],options=opVars,version="0.0.0.1",author='LKUMARESAN')
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable],options=opVars,zipfile=1)
    else:
        setup(windows=[appVariable],options=opVars)

print "\n\nEvery thing is fine!"
