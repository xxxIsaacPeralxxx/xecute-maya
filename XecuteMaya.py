from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Sub_DragDropMods import *
from Sub_INIReader import *
from WIN import Ui_MainWindow
from time import gmtime, strftime,localtime
import re, os, sys, sip
import xtools

def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    app.exec_()
    del(app)
    sys.exit()

class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.setupUi(self, *args)
        self.setGeometry(100,100,700,500)


        self.presets = []
        self.allexepath = []
        self.allargpath = []

        self.myqp = QProcess(self)
        self.skinbox.addItems(QtGui.QStyleFactory.keys())
        self.addDockWidget(Qt.RightDockWidgetArea,self.dockWidget_2)
        self.addDockWidget(Qt.TopDockWidgetArea,self.dockWidget)
        xtools.appstyle(self)


        self.configs = configINI("Settings.ini")
        self.read_settings()
        self.windowx = None

        batchtotalfiles=0
        batchcurrentfile=0
        batchtotaldone=0
        batchtotalerror=0
        batchtotalskip=0

        self.lastsearch=""

        #Replacing old QObjectS with new DRAG/DROPABLE QObjects

        xtools.updaterchk(self,"Execute.exe")


        #List widget for collecting Drag Dropped filesfor Batch Process....
        sip.delete(self.listWidget)
        self.listWidget = DroppableListWidget(self.tab_batch)
        self.listWidget.setFrameShape(QtGui.QFrame.Box)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_5.addWidget(self.listWidget, 1, 0, 1, 1)
        self.listWidget.__class__.dropEvent = self.batchdragdropped


        QObject.connect(self.pushButton, SIGNAL("clicked()"), self.mysignalrunner)
        QObject.connect(self.myqp,SIGNAL("finished(int)"),self.endofprocess)
        QObject.connect(self.myqp,SIGNAL("readyRead()"),self.processcapture)
        QObject.connect(self.myqp,SIGNAL("started()"),self.started)
        QObject.connect(self.myqp,SIGNAL("stateChanged()"),self.stateChanged)
        QObject.connect(self.myqp,SIGNAL("error(QProcess::ProcessError)"),self.someerror)
        QObject.connect(self.myqp,SIGNAL("readyReadStandardError()"),self.errorcatcher)

        self.do_listscripts()
        self.toolButton_4.setEnabled(0)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        self.textEdit.setReadOnly(True)
        self.displayer.setReadOnly(True)
        self.lineEdit.setReadOnly(True)
        self.infodisp.clear()
        self.do_changeskin(self.skinbox.currentText())
        self.do_smoothtab(self.checkBox_3.checkState())
        self.do_bgstyle(self.skinbox_2.currentText())
        self.infodisp.hide()



        #Loading CommandLine presets
        self.xm_presetDesign()

        #Adding Default Preset
        if self.presets.count("Default")==0:
            mpath = str(xtools.getString(self.ui_mayapath))
            margs = str(xtools.getString(self.ui_basecommand))
            self.xm_addpreset("Default",mpath,margs)


    def xm_presetDesign(self):

        self.presets = eval(xtools.INIReadValue("PRESETS.ini","COMMANDLINE","PRESETLIST",True,"[]"))
        self.allexepath = eval(xtools.INIReadValue("PRESETS.ini","COMMANDLINE","EXELIST",True,"[]"))
        self.allargpath = eval(xtools.INIReadValue("PRESETS.ini","COMMANDLINE","ARGLIST",True,"[]"))

        self.listWidget_3.clear()
        self.listWidget_3.addItems(self.presets)


    def do_presetLoad(self,q):

        rn = self.listWidget_3.currentRow()

        prname = self.presets[rn]
        exepname = self.allexepath[rn]
        argpath = self.allargpath[rn]

        xtools.putString(self.ui_mayapath,exepname)
        xtools.putString(self.ui_basecommand,argpath)



    def do_presetAdd(self):

        newpre = xtools.showInputBox(self,"Add Preset","Preset Name","")
        mpath = xtools.getString(self.ui_mayapath)
        margs = xtools.getString(self.ui_basecommand)

        if newpre!=0 and mpath!="" and margs!="":
            self.xm_addpreset(newpre,mpath,margs)


    def xm_addpreset(self,presetname,exepath,baseargument):

            if self.presets.count(str(presetname))==0 or self.allexepath.count(str(exepath))==0:

                self.presets.append(str(presetname))
                self.allexepath.append(str(exepath))
                self.allargpath.append(str(baseargument))

                xtools.INISetValue("PRESETS.ini","COMMANDLINE","PRESETLIST",str(self.presets))
                xtools.INISetValue("PRESETS.ini","COMMANDLINE","EXELIST",str(self.allexepath))
                xtools.INISetValue("PRESETS.ini","COMMANDLINE","ARGLIST",str(self.allargpath))

                self.xm_presetDesign()


    def do_presetRemove(self):
        #x = str(xtools.getString(self.listWidget_3))
        rn = self.listWidget_3.currentRow()

        prname = self.presets[rn]
        exepname = self.allexepath[rn]
        argpath = self.allargpath[rn]

        self.presets.remove(prname)
        self.allexepath.remove(exepname)
        self.allargpath.remove(argpath)

        itm = self.listWidget_3.item(rn)
        self.listWidget_3.removeItemWidget(itm)

        xtools.INISetValue("PRESETS.ini","COMMANDLINE","PRESETLIST",str(self.presets))
        xtools.INISetValue("PRESETS.ini","COMMANDLINE","EXELIST",str(self.allexepath))
        xtools.INISetValue("PRESETS.ini","COMMANDLINE","ARGLIST",str(self.allargpath))

        self.xm_presetDesign()


    def url_b1(self):
        print self.checkBox_4.checkState()
        import webbrowser
        webbrowser.open("http://www.google.com/profiles/kaymatrix")

    def url_b2(self):
        import webbrowser
        webbrowser.open("http://in.linkedin.com/pub/kumaresan-laxman/12/9b6/89b")

    def url_b3(self):
        import webbrowser
        webbrowser.open("http://thekumaresan.blogspot.com/")

    def url_b4(self):
        import webbrowser
        webbrowser.open("http://www.box.net/kumarsprofession")


    def do_findinscript(self):

        st = QtGui.QInputDialog.getText(self,"Find in Script","Search for...",QLineEdit.Normal,str(self.lastsearch))

        self.lastsearch = st[0]
        if self.ui_disp_script.find(str(st[0]))==0:
            xtools.messagebox(self,"Sorry!","Nothing found!")



    def do_loadfreshscript(self):

        fileName = QtGui.QFileDialog.getOpenFileName(self,"Open a mel script file...","Mel","Maya MEL (*.mel);;All Files (*)")

        if os.path.exists(fileName):

            self.ui_loadedscriptpath.setText(fileName)

            ff = open(fileName, 'r').read()
            self.ui_disp_script.setText(str(ff))
            self.infodisp.setText("Custom Script is loaded!")
            self.saydisplayer("<font size=3 color=green>Script loaded! If file(s) are added you can proceed clicking RUN.</font>",False)


    def do_newscript(self):
        fileName = QtGui.QFileDialog.getSaveFileName(self,"Save your new script to...","Mel","Maya MEL (*.mel);;All Files (*)")

        if str(fileName)!="":

            self.ui_loadedscriptpath.setText(fileName)

            s = """
                /*
                New Custom Script - Created with XecuteMaya
                */
                """
            xtools.putString(self.ui_disp_script,str(s))

            if (self.ui_loadedscriptpath.text()!="" and self.ui_disp_script.toPlainText()!=""):
                f = open(self.ui_loadedscriptpath.text(), 'w')
                f.write(self.ui_disp_script.toPlainText())

            self.infodisp.setText("New Script is loaded!")
            self.saydisplayer("<font size=3 color=green>Script loaded! If file(s) are added you can proceed clicking RUN.</font>",False)

        self.do_listscripts()


    def do_bgstyle(self, color):

        self.setStyleSheet("")
        if color == "Green":
            self.setStyleSheet("border-bottom-color: rgb(0, 0, 0);border-color: rgb(57, 105, 126);background-color: qlineargradient(spread:pad, x1:0.505682, y1:0, x2:0.528, y2:1, stop:0 rgba(195, 216, 179, 255), stop:1 rgba(182, 182, 182, 255));")
        if color == "Gray":
            self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.505682, y1:0, x2:0.528, y2:1, stop:0 rgba(216, 216, 216, 255), stop:1 rgba(182, 182, 182, 255));")
        if color == "Red":
            self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.511545, y1:1, x2:0.517, y2:0, stop:0 rgba(216, 169, 169, 255), stop:1 rgba(180, 180, 180, 255));")
        if color == "Blue":
            self.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.505682, y1:0, x2:0.528, y2:1, stop:0 rgba(182, 192, 216, 255), stop:1 rgba(185, 185, 185, 255));")


    def do_smoothtab(self, i):
        if i==2:
            self.tabWidget.setTabShape(QtGui.QTabWidget.Triangular)
        else:
            self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)

    def do_changeskin(self, style):
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(style))
        QtGui.QApplication.setPalette(QtGui.QApplication.style().standardPalette())

    def do_setdefaultpath(self):

        genscript = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Scripts") + QDir.separator () + str("General Scripts"))
        advscript = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Scripts") + QDir.separator () + str("Advance Scripts"))
        tempscript = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Scripts") + QDir.separator () + str("Temp Scripts"))
        processlogpath = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Log") + QDir.separator () + str("ProcessLog"))
        outlogpath = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Log") + QDir.separator () + str("OutputLog"))

        self.ui_genscpth.setText(genscript)
        self.ui_advscpth.setText(advscript)
        self.ui_tmpscpth.setText(tempscript)

        self.ui_processlogpath.setText(processlogpath)
        self.ui_outlogpath.setText(outlogpath)
        self.do_listscripts()

        if not os.path.exists(genscript):
            QtCore.QDir().mkpath(genscript)

        if not os.path.exists(advscript):
            QtCore.QDir().mkpath(advscript)

        if not os.path.exists(tempscript):
            QtCore.QDir().mkpath(tempscript)

        if not os.path.exists(processlogpath):
            QtCore.QDir().mkpath(processlogpath)

        if not os.path.exists(outlogpath):
            QtCore.QDir().mkpath(outlogpath)


    def do_tabchange(self,i):
        self.infodisp.clear()

    def do_logclear(self):
        self.lineEdit.clear()
        self.textEdit.clear()
        self.infodisp.clear()

    def do_statussave(self):
        if os.path.exists(self.ui_processlogpath.text()):
            timestmp = strftime("%d%m%Y%H%M%S", localtime())
            newfile = self.ui_processlogpath.text() + "\\Status-" + timestmp + ".txt"
            self.saydisplayer("<font size=3 color=blue>Status Log Saved:  </font><br><b><font size=3 color=purple>" + newfile + "<br></b></font>",False)

            f = open(newfile, 'w')
            try:
                f.write(self.displayer.toPlainText())
                self.infodisp.setText("Status Saved!")
            finally:
                f.close()
        else:
            self.saydisplayer("<font size=3 color=red>ProcessLog Save Location not found!Check Settings!</font>",False)


    def do_logsave(self):

       if os.path.exists(self.lineEdit.text()) == 0:
            self.saydisplayer("<font size=3 color=red>No file has been processed. DragDrop list of file(s) to be processed.</font>",False)

       if os.path.exists(self.ui_outlogpath.text())==0:
            self.saydisplayer("<font size=3 color=red>Output Log save location not found! Check Settings!</font>",False)


       if os.path.exists(self.lineEdit.text()) and os.path.exists(self.ui_outlogpath.text()):

            cfile = QtCore.QFileInfo(self.lineEdit.text())
            filename = cfile.fileName()
            filenameNoext = cfile.completeBaseName()
            fileext = cfile.completeSuffix()
            filepath = cfile.path()
            timestmp = strftime("%d%m%Y%H%M%S", localtime())

            newfile = self.ui_outlogpath.text() + "\\" + str(filenameNoext + "-" + timestmp + ".txt")
            self.saydisplayer("<font size=3 color=red>Log Saved:  </font><br><b><font size=3 color=purple>" + newfile + "<br></b></font>",False)

            f = open(newfile, 'w')
            try:
                f.write(self.textEdit.toPlainText())
                self.infodisp.setText("Log Saved!")
            finally:
                f.close()



    def read_settings(self):

        lst1 = self.configs.read_settings("General")
        lst2 = self.configs.read_settings("Scripts")
        if lst1==None or lst2==None:
            self.saydisplayer("<font size=3 color=red>Settings file not found! Creating Default settings!</font>",False)
            self.default_settings()
            self.configs = configINI("Settings.ini")
            self.read_settings()
        else:
            self.ui_mayapath.setText(lst1["exepath"])
            self.ui_basecommand.setText(lst1["commandlines"])
            self.checkBox.setChecked(int(lst1["autosave"]))
            self.checkBox_2.setChecked(int(lst1["autoclear"]))
            self.skinbox.setCurrentIndex(int(lst1["skin"]))
            self.skinbox_2.setCurrentIndex(int(lst1["colortheme"]))
            self.checkBox_3.setChecked(int(lst1["smoothtab"]))
            self.checkBox_4.setChecked(int(lst1["dispcommandline"]))
            self.ui_genscpth.setText(lst2["genscript"])
            self.ui_advscpth.setText(lst2["advscript"])
            self.ui_tmpscpth.setText(lst2["tempscript"])

            self.ui_processlogpath.setText(lst2["processlogpath"])
            self.ui_outlogpath.setText(lst2["outlogpath"])

    def save_settings(self):
        exepath = self.ui_mayapath.text()
        commandlines = self.ui_basecommand.text()
        autosave = self.checkBox.checkState()
        autoclear = self.checkBox_2.checkState()
        skin = self.skinbox.currentIndex()
        colortheme = self.skinbox_2.currentIndex()
        smoothtab = self.checkBox_3.checkState()
        dispcommandline = self.checkBox_4.checkState()
        genscript =self.ui_genscpth.text()
        advscript = self.ui_advscpth.text()
        tempscript = self.ui_tmpscpth.text()
        processlogpath = self.ui_processlogpath.text()
        outlogpath = self.ui_outlogpath.text()

        mylist1={
                "exepath":exepath,
                "commandlines":commandlines,
                "skin":skin,
                "colortheme":colortheme,
                "smoothtab":smoothtab,
                "dispcommandline":dispcommandline,
                "autosave":autosave,
                "autoclear":autoclear
                }

        mylist2={
                "genscript":genscript,
                "advscript":advscript,
                "tempscript":tempscript,
                "processlogpath":processlogpath,
                "outlogpath":outlogpath
                }


        self.configs.write_settings("General",mylist1,"w")
        self.configs.write_settings("Scripts",mylist2,"a")
        self.infodisp.setText("Settings Saved!")
        self.saydisplayer("<font size=3 color=green>Settings Saved!</font>",False)

    def default_settings(self):

        exepath = r"C:\Program Files\Autodesk\Maya2009\bin\mayabatch.exe"
        commandlines = "-noAutoloadPlugins -script [SCRIPTFILE] -file [MBFILE]"
        autosave = 0
        autoclear = 0
        skin = 4
        colortheme = 0
        smoothtab = 0


        genscript = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Scripts") + QDir.separator () + str("General Scripts"))
        advscript = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Scripts") + QDir.separator () + str("Advance Scripts"))
        tempscript = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Scripts") + QDir.separator () + str("Temp Scripts"))
        processlogpath = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Log") + QDir.separator () + str("ProcessLog"))
        outlogpath = QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Log") + QDir.separator () + str("OutputLog"))
        pluginpath =  QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Plugins"))

        mylist1={
                "exepath":exepath,
                "commandlines":commandlines,
                "skin":skin,
                "smoothtab":smoothtab,
                "colortheme":colortheme,
                "autosave":autosave,
                "autoclear":autoclear
                }

        mylist2={
                "genscript":genscript,
                "advscript":advscript,
                "tempscript":tempscript,
                "processlogpath":processlogpath,
                "outlogpath":outlogpath
                }


        self.configs.write_settings("General",mylist1,"w")
        self.configs.write_settings("Scripts",mylist2,"a")
        self.infodisp.setText("Default Settings Saved!")
        self.saydisplayer("<font size=3 color=green>Default Settings Saved!</font>",False)

        if not os.path.exists(genscript):
            QtCore.QDir().mkpath(genscript)

        if not os.path.exists(advscript):
            QtCore.QDir().mkpath(advscript)

        if not os.path.exists(tempscript):
            QtCore.QDir().mkpath(tempscript)

        if not os.path.exists(processlogpath):
            QtCore.QDir().mkpath(processlogpath)

        if not os.path.exists(outlogpath):
            QtCore.QDir().mkpath(outlogpath)

        if not os.path.exists(pluginpath):
            QtCore.QDir().mkpath(pluginpath)

    def do_pluginstart(self,qm):

##        from PyQt4 import uic
##
##          THIS ONE IS ERROR ON EXE PREPERATION
##
##        pluginpath =  QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Plugins"))
##        plugname = qm.text()
##        ldscript =  pluginpath + "\\" + plugname
##
##        self.windowx = loadUi(ldscript)
##
##        self.connect(self.windowx.pushButton, QtCore.SIGNAL("clicked()"), self.melGenereater)
##        self.connect(self.windowx.pushButton_2, QtCore.SIGNAL("clicked()"), self.previews)
##
##
##        self.windowx.show()

#        TODO THIS SECTION IS TO LOAD UIs Dynamically
          xtools.messagebox(self,"Under Construction","This Section is still under development!")


    def previews(self):
        x = ""
        x = xtools.getString(self.windowx.textEdit)

        IN1 = xtools.getString(self.windowx.lineEdit_1)
        IN2 = xtools.getString(self.windowx.lineEdit_2)
        IN3 = xtools.getString(self.windowx.lineEdit_3)
        IN4 = xtools.getString(self.windowx.lineEdit_4)
        IN5 = xtools.getString(self.windowx.lineEdit_5)

        if IN1!=None:        x = x.replace("[INPUT1]",IN1)
        if IN2!=None:        x = x.replace("[INPUT2]",IN2)
        if IN3!=None:        x = x.replace("[INPUT3]",IN3)
        if IN4!=None:        x = x.replace("[INPUT4]",IN4)
        if IN5!=None:        x = x.replace("[INPUT5]",IN5)

        x = x.replace("\\","/")

        xtools.putString(self.windowx.textEdit_2,x)




    def melGenereater(self):
        x = ""
        x = xtools.getString(self.windowx.textEdit)

        IN1 = xtools.getString(self.windowx.lineEdit_1)
        IN2 = xtools.getString(self.windowx.lineEdit_2)
        IN3 = xtools.getString(self.windowx.lineEdit_3)
        IN4 = xtools.getString(self.windowx.lineEdit_4)
        IN5 = xtools.getString(self.windowx.lineEdit_5)
        IN5 = xtools.getString(self.windowx.lineEdit_5)

        if IN1!=None:        x = x.replace("[INPUT1]",IN1)
        if IN2!=None:        x = x.replace("[INPUT2]",IN2)
        if IN3!=None:        x = x.replace("[INPUT3]",IN3)
        if IN4!=None:        x = x.replace("[INPUT4]",IN4)
        if IN5!=None:        x = x.replace("[INPUT5]",IN5)

        x = x.replace("\\","/")

        fileName = QtGui.QFileDialog.getSaveFileName(self,"Save Customized Script to...","CustomizedMEL","Maya MEL (*.mel);;All Files (*)")


        if fileName!="" and x!="":

                fileObj = open(fileName,"w")
                fileObj.write(x)
                fileObj.close()

                xtools.messagebox(self,"Done!","Customized Script Generated and Saved. Please... Reload the script, if needed!")

        self.do_listscripts()


    def do_savesettings(self):
        self.save_settings()

    def do_gotoscripts(self):
          self.tabWidget.setCurrentIndex(1)

    def do_gotofiles(self):
          self.tabWidget.setCurrentIndex(0)

    def do_clearlist(self):
        self.listWidget.clear()

    def batchdragdropped(self, event):
        if event.mimeData().hasUrls() == True:
            urllist = event.mimeData().urls()
            for url in urllist:
                self.listWidget.addItem(url.toLocalFile())
            self.infodisp.setText(str(urllist.__len__() ) + " file(s) added to the list! If Script is loaded you can proceed clicking RUN.")
            self.saydisplayer("<font size=3 color=green>" + str(urllist.__len__() ) + " file(s) added to the list! If Script is loaded you can proceed clicking RUN.</font>",False)

    def do_listscripts(self):
        genscripts = self.ui_genscpth.text()
        advscripts = self.ui_advscpth.text()
        tempscripts = self.ui_tmpscpth.text()
        pluginpath =  QDir.toNativeSeparators ( QDir.currentPath() + QDir.separator () + str("Plugins"))

        self.ui_gensclst.clear()
        self.ui_advsclst.clear()
        self.ui_tmpsclst.clear()
        self.listWidget_2.clear()

        if os.path.exists(genscripts) and os.path.exists(advscripts) and os.path.exists(tempscripts) and os.path.exists(pluginpath):

            for fls in os.listdir(genscripts):
                self.ui_gensclst.addItem(fls)

            for fls in os.listdir(advscripts):
                self.ui_advsclst.addItem(fls)

            for fls in os.listdir(tempscripts):
                self.ui_tmpsclst.addItem(fls)

            for fls in os.listdir(pluginpath):
                self.listWidget_2.addItem(fls)



    def do_loadscript(self,qm):
        qm = QListWidgetItem(qm)
        scriptpath = self.get_scriptpath(self.toolBox.currentIndex())
        scriptname = qm.text()
        ldscript =  scriptpath + "\\" + scriptname

        self.ui_loadedscriptpath.setText(ldscript)

        if os.path.exists(ldscript):
            ff = open(ldscript, 'r').read()
            self.ui_disp_script.setText(str(ff))

        self.tabWidget.setCurrentIndex(1)
        self.infodisp.setText("Script is loaded!")
        self.saydisplayer("<font size=3 color=green>Script loaded! If file(s) are added you can proceed clicking RUN.</font>",False)


    def do_tempsave(self):
            if (self.ui_loadedscriptpath.text()!="" and self.ui_disp_script.toPlainText()!=""):
                f = open(self.ui_loadedscriptpath.text(), 'w')
                f.write(self.ui_disp_script.toPlainText())
                self.saydisplayer("<font size=3 color=green>Script Updated! If file(s) are added you can proceed clicking RUN.</font>",False)

    def get_scriptpath(self,i):

        if (i==0):
            return self.ui_genscpth.text()

        if (i==1):
            return self.ui_advscpth.text()

        if (i==2):
            return self.ui_tmpscpth.text()


    def terminator(self):
        self.saydisplayer("<font size=3 color=red><b>Process terminate requested!</b></font>")

    def someerror(self, err):
        self.saydisplayer("Process Error:" + str(err))

    def errorcatcher(self):
        self.saydisplayer("<font size=3 color=red><b>Process execution error occured...</b></font>")

    def stateChanged(self):
        self.saydisplayer("Process changing...")

    def started(self):
        #self.saydisplayer("Process Started!")
        pass

    def endofprocess(self, qs):

        self.myqp.close()
        self.myqp.kill()
        self.myqp.terminate()
        self.enabler(1)
        self.toolButton_4.setEnabled(0)
        self.saydisplayer("<b>File Process completed with Exit Code: " + str(qs) + "------------------</b>" )
        self.saydisplayer("",False)

        if self.checkBox.checkState()==2:
            self.do_logsave()

        if self.checkBox_2.checkState()==2:
            self.textEdit.clear()

        if (self.batchcurrentfile+1)<=self.batchtotalfiles:
                self.batchcurrentfile = self.batchcurrentfile + 1
                self.saydisplayer("<b>Started Processing file " + str(self.batchcurrentfile) + "/" + str(self.batchtotalfiles) + "---------------------------------<b>")
                self.setfilefromlist(self.batchcurrentfile)
                self.singlefilerunner()


    def setfilefromlist(self, nox):

        self.listWidget.setCurrentRow(nox-1)
        itm = self.listWidget.currentItem()
        self.lineEdit.setText(itm.text())
        self.saydisplayer("<font size=3 color=blue><b>" + itm.text() + "</b></font>",False)

    def mysignalrunner(self):

        self.batchtotalfiles=0
        self.batchtotaldone=0
        self.batchtotalerror=0
        self.batchtotalskip=0
        self.batchcurrentfile=0

        #PERFORM BATCH FILE PROCESS

        #QtGui.QListWidget.count()
        self.batchtotalfiles = self.listWidget.count()
        if self.batchtotalfiles > 0:
            self.displayer.clear()
            self.textEdit.clear()
            self.batchcurrentfile = self.batchcurrentfile + 1
            self.do_tempsave()
            self.saydisplayer("<b><font size=4 color=red>Batch Process Started...\nTotal file(s) to be processed: </font><font size=5 color=blue>" + str(self.batchtotalfiles)+ "</font></b>")
            self.saydisplayer("",False)
            self.saydisplayer("<b>Started Processing file " + str(self.batchcurrentfile) + "/" + str(self.batchtotalfiles) + "---------------------------------<b>")
            self.setfilefromlist(self.batchcurrentfile)
            self.tabWidget.setCurrentIndex(2)
            self.singlefilerunner()
        else:
            self.saydisplayer("<font size=3 color=red>No file(s) found in process list. Drag Drop some files!</font>",False)


    def filenamealone(self,f):
        z = f
        z = z.replace(os.path.dirname(z),"")
        z = z.replace(os.path.splitext(z)[1],"")
        z = z[1:]
        return z



    def singlefilerunner(self):

        mybasecomm = ""
        myfile = self.lineEdit.text()
        mymaya = self.ui_mayapath.text()
        mybasecomm = self.ui_basecommand.text()
        myscript = self.ui_loadedscriptpath.text()

        myfilex = os.path.normpath(str(myfile))
        myfilename = os.path.basename(myfilex)
        myfilepath = os.path.dirname(myfilex)
        myfileexe = os.path.splitext(myfilex)[1][1:]
        myfilenamalone = self.filenamealone(myfilex)

        if os.path.exists(myfile)==0:
            self.saydisplayer("<font size=3 color=red> Can't access the file: "+ myfile+ "</font>",False)

        if os.path.exists(mymaya)==0:
            self.saydisplayer("<font size=3 color=red> Can't access the mayabatch file:  "+ mymaya+ "</font>",False)

        if os.path.exists(myscript)==0:
            self.saydisplayer("<font size=3 color=red> Can't access the script file: "+ myscript+ "</font>",False)



        if (os.path.exists(myfile) and os.path.exists(mymaya) and os.path.exists(myscript)):

            mybasecomm = mybasecomm.replace("[SCRIPTFILE]", myscript)
            mybasecomm = mybasecomm.replace("[MBFILE]", myfile)

            mybasecomm = mybasecomm.replace("[MBFILENAME]", myfilename )
            mybasecomm = mybasecomm.replace("[MBFILENAME-NOEXT]", myfilenamalone )
            mybasecomm = mybasecomm.replace("[MBFILEEXT]", myfileexe)
            mybasecomm = mybasecomm.replace("[MBFILEPATH]", myfilepath )



            formd = "\"" + mymaya + "\" " + mybasecomm

            #Disable for safty....
            self.enabler(0)

            #Display the Show COmmands
            if self.checkBox_4.checkState()==2:
                self.saydisplayer("<font size=3 color=red>" + formd + "</font>",False)


            #Enable for usability....
            self.toolButton_4.setEnabled(1)

            #PROCESS START.......
            self.myqp.start (formd)


    def processcapture(self):

        xx = ""
        if self.myqp.canReadLine():
            xx = self.myqp.readAll()
            self.textEdit.append(str(xx))
            sb = self.textEdit.verticalScrollBar()
            sb.setValue(sb.maximum())


    def saydisplayer(self,disp,timeneeded=True):
        #self.tabWidget.setCurrentIndex(0)
        if timeneeded:
            #t = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
            t = strftime("%d-%b-%Y %H:%M:%S", localtime())
            self.displayer.append(str(t) + ": " + str(disp))
        else:
            self.displayer.append(str(disp))


    def enabler(self,b):
        self.pushButton.setEnabled(b)
        self.pushButton_3.setEnabled(b)
        self.pushButton_2.setEnabled(b)
        self.toolBox.setEnabled(b)
        self.listWidget.setEnabled(b)



if __name__ == "__main__":
    main()



