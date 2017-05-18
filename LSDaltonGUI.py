#    LSDaltonGUI
#    Copyright May 2017 Thomas Kjaergaard 
#
#    LSDaltonGUI is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2.1 of the License, or (at your option) any later version.
#
#    LSDaltonGUI is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
#    USA
#
#    The the GNU Lesser General Public License is placed in file License
#    For electronic contact: Thomas Kjaergaard tkjaergaardchem@gmail.com
#
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys

#Icons have been imported from https://github.com/yusukekamiyamane/fugue-icons

#LSDalton GUI About Dialog Box 
class AboutDialog(QDialog):
    
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        #Titel
        self.setWindowTitle("About the LSDaltonGUI")

        title = QLabel("LSDaltonGUI")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)
        
        layout = QVBoxLayout()
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)

        #Logo
        logo = QLabel()
        watermark = QPixmap("john-dalton.jpg")
        newPixmap = watermark.scaled(QSize(100,100),Qt.KeepAspectRatio)
        logo.setPixmap(newPixmap)        
        logo.setAlignment(Qt.AlignHCenter)
        layout.addWidget(logo)

        #Version Number
        n1 = QLabel("Version 1.0.0.0")
        n1.setAlignment(Qt.AlignHCenter)
        layout.addWidget(n1)

        #Author 
        n2 = QLabel("Made by Thomas Kjaergaard")
        n2.setAlignment(Qt.AlignHCenter)
        layout.addWidget(n2)

        #OK and Cancel button
        QBtn = QDialogButtonBox.Ok # No Cancel 
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

# **WAVE FUNCTION TAB        
class WaveFunc(QWidget):

    def __init__(self, *args, **kwargs):
        super(WaveFunc, self).__init__(*args, **kwargs)

        layoutWF = QVBoxLayout()

        layoutWF.addWidget(QLabel("Select the Self-Consistent Field (SCF) Wave Function Model"))
        #Consider QbuttonGroup to have HF and DFT buttons be exclusive Check Boxes
        
        self.widgetHF = QCheckBox("Hartree-Fock (HF)")
        self.widgetHF.setStatusTip("Use the Hartree-Fock (HF) SCF method, recommended for Correlated calculations (see **CC and **DEC)")
        self.widgetHF.setWhatsThis("Whats This2")
        self.widgetHF.setChecked(True)
        self.widgetHF.stateChanged.connect(self.wavefunc_state2)
        layoutWF.addWidget(self.widgetHF)

        self.widgetDFT = QCheckBox("Density Functional Theory (DFT)")
        self.widgetDFT.setStatusTip("Use DFT as the SCF model, requires the specification of a DFT exchange-correlation (XC) functional")
#        self.widgetDFT.setToolTip("Use DFT as the SCF model")
        self.widgetDFT.setWhatsThis("Whats This1")
        self.widgetDFT.stateChanged.connect(self.wavefunc_state)
        layoutWF.addWidget(self.widgetDFT)

        self.widget4 = QComboBox()
        self.widget4.addItems(["LDA","SLATER","B3LYP"])
        #Set the default value to point to "B3LYP" 
        self.widget4.setCurrentIndex(2)
        self.widget4.setStatusTip("Select the DFT functional")
        #Signal
        self.widget4.currentIndexChanged[str].connect(self.DFTFUNCTextChanged)
        self.widget4.setVisible(False)
            
        layoutWF.addWidget(self.widget4)
        layoutWF.setAlignment(Qt.AlignTop| Qt.AlignVCenter)

        self.setLayout(layoutWF)

    def wavefunc_state(self, s):
        if(s == Qt.Checked):
            #Change to DFT with functional 
            self.widget4.setVisible(True)
            if(self.widgetHF.isChecked()):
                self.widgetHF.setChecked(False)
                
            self.parent().parent().RemoveText(".HF")
            self.parent().parent().AddText(".DFT","**WAVE FUNCTION")
            self.parent().parent().AddText("B3LYP",".DFT")
        else:
            #Change to HF without functional 
            self.widget4.setVisible(False)
            if(not self.widgetHF.isChecked()):
                self.widgetHF.setChecked(True)

            self.parent().parent().RemoveTextAndNext(".DFT")
            self.parent().parent().AddText(".HF","**WAVE FUNCTION")
            
    def wavefunc_state2(self, s):
        if(s == Qt.Checked):
            #Change to HF without functional 
            if(self.widgetDFT.isChecked()):
                self.widgetDFT.setChecked(False)
        else:
            #Change to DFT with functional 
            if(not self.widgetDFT.isChecked()):
                self.widgetDFT.setChecked(True)

    def DFTFUNCTextChanged(self,s):
        self.parent().parent().RemoveTextAndNext(".DFT")
        self.parent().parent().AddText(".DFT","**WAVE FUNCTION")
        self.parent().parent().AddText(s,".DFT")
        
            
# **INTEGRAL TAB        
class Integral(QWidget):

    def __init__(self, *args, **kwargs):
        super(Integral, self).__init__(*args, **kwargs)
        
        layoutInt = QVBoxLayout()

        layoutInt.addWidget(QLabel("Integral and Performance Specific Keywords"))

        widget2 = QCheckBox("Use density-fitting for Coulomb Integrals")
# 1. option
#        widget2.setChecked(True)
# 2. option
#        widget2.setCheckState(Qt.Checked)
# 3. option
#        widget2.setCheckState(Qt.PartiallyChecked)
# 4. option
#        widget2.setCheckState(Qt.Checked)
#        widget2.setTristate(True)
        #connect signal to show_state function defined below
        widget2.setStatusTip("Recommended for performance reasons")
        widget2.stateChanged.connect(self.show_state)
        layoutInt.addWidget(widget2)

        layoutInt.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
        self.setLayout(layoutInt)
#        self.setCentralWidget(self)
        

    def show_state(self, s):
        if(s == Qt.Checked):
#            print( s == Qt.Checked )
            # add DENSFIT else            
            self.parent().parent().AddNewBlock("**INTEGRAL")
            self.parent().parent().AddText(".DENSFIT","**INTEGRAL")
        else:
            self.parent().parent().RemoveText(".DENSFIT")
            
        
# **Other TAB        
class Other(QWidget):

    def __init__(self, *args, **kwargs):
        super(Other, self).__init__(*args, **kwargs)
        
        layout = QVBoxLayout()

        widget2 = QCheckBox("Dynamic Density Optimization Threshold")
        widget2.stateChanged.connect(self.show_convdyn_state)
        layout.addWidget(widget2)

        widget4 = QComboBox()
        widget4.addItems(["SLOPP","STAND","TIGHT","VTIGH"])
        #Set the default value to point to "STAND" 
        widget4.setCurrentIndex(1)
        #Signal
        widget4.currentIndexChanged.connect(self.DynThresholdIndexChanged)
        widget4.currentIndexChanged[str].connect(self.DynThresholdTextChanged)
        layout.addWidget(widget4)

        widget5 = QListWidget()
        widget5.addItems(["One","Two","Three"])
        #Signal
        widget5.currentItemChanged.connect(self.ItemChanged)
        widget5.currentTextChanged[str].connect(self.TextChanged)
        layout.addWidget(widget5)

        #Single line of text
        widget6 = QLineEdit()
        widget6.setMaxLength(10)
        widget6.setPlaceholderText("Enter your text (max 10 characters)")
        #make the line read only
        widget6.returnPressed.connect(self.return_pressed)
        widget6.selectionChanged.connect(self.selection_changed)
        widget6.textChanged.connect(self.text_changed)
        #text Edited only give signal when the user changes the text
        #not when the program changes the text. 
        widget6.textEdited.connect(self.text_edited)
#        widget6.setReadOnly(True)
        layout.addWidget(widget6)

        widget9 = QSpinBox()
        widget9.setMinimum(-10)
        widget9.setMaximum(3)
        widget9.setPrefix("$")
        widget9.setSuffix("c")
        widget9.setSingleStep(1)
#        widget9.valueChanged.connect(self.value_changed)
#        widget9.valueChanged[str].connect(self.value_changed_str)
        layout.addWidget(widget9)

        widget10 = QDoubleSpinBox()
        widget10.setMinimum(-10.0)
        widget10.setMaximum(3.0)
        widget10.setPrefix("$")
        widget10.setSuffix("c")
        widget10.setSingleStep(0.3)
#        widget9.valueChanged.connect(self.value_changed)
#        widget9.valueChanged[str].connect(self.value_changed_str)
        layout.addWidget(widget10)

#        layoutStack.addLayout(layout)
        layout.setAlignment(Qt.AlignTop| Qt.AlignVCenter)

        self.setLayout(layout)
#        self.setCentralWidget(self)
        

    def show_convdyn_state(self, s):
        print(s)
        if(s == Qt.Checked):
            print( s == Qt.Checked )
            # add DENSFIT else
            print("add CONVDYN")
        else:
            print("remove CONVDYN")
            
    def wavefunc_state(self, s):
        if(s == Qt.Checked):
            print("DFT chosen")
        else:
            print("HF chosen")            

    def show_state(self, s):
        print( s == Qt.Checked )
        print(s)

    def DynThresholdIndexChanged(self,i):
        print(i)

    def DynThresholdTextChanged(self,s):
        print(s)

    def ItemChanged(self, i):
        print(i)

    def TextChanged(self,s):
        print(s)

    def return_pressed(self):
        print("return pressed!")
#        print(self.centralWidget().setText("Boom"))

    def selection_changed(self):
        print("selection changed")
#        print(self.centralWidget().selectedText())
# DO NOT KNOW HOW TO ACCESS selectedText of instance of the central widget - widget instance 

    def text_changed(self,s):
        print("text changed")
        print(s)

    def text_edited(self,s):
        print("text edited")
        print(s)

        
# The Main GUI 
# Subclass QMainWindow to customise the application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.outfile = open('GUILSDALTON.INP', 'w') 
        f2 = open('TMPGUILSDALTON.INP', 'w') 
        self.setWindowTitle("LSDalton GUI")

        #create instance of toolbar 
        toolbar = QToolBar("The main LSDalton toolbar")
        toolbar.setIconSize(QSize(16,16))
        #add toolbar to qmainwindow
        self.addToolBar(toolbar)

        #Create instance of menu
        menu = self.menuBar()
        #add menu to menu -- name of menu
        #The & define keyboard shortcuts to menu entry
        #Here "F" selects this File menu
        file_menu = menu.addMenu(u"&File")

        #Qaction instance create from Q object to act as parent of the action
        #here the mainwindow is passed as the parent action
        save_action = QAction(QIcon("disk-black.png"),"Save", self)
        #
        save_action.setStatusTip("Save LSDALTON.INP file")
        #"triggered" signal is sent when Qaction is clicked
        #save_action.triggered.connect(lambda outfile=outfile: self.onSaveLSDALTON(outfile))
        save_action.triggered.connect(self.onSaveLSDALTON)
        #add key short-cut to action
        #save_action.setShortcut(QKeySequence("Ctrl+s"))
        save_action.setShortcut(QKeySequence.Save)
        #set button checkable 
        #save_action.setCheckable(True)
        #add button to toolbar 
        toolbar.addAction(save_action)

        #add action (same as for toolbar)
        file_menu.addAction(save_action)
        #horisontal line to seperate menu items
        #        file_menu.addSeparator()
        #        file_submenu = file_menu.addMenu("Submenu")
        #        file_submenu.addAction(save_action)

        #Whats this
        self.WhatsThisCustomAction = QWhatsThis.createAction() #QAction(QIcon("cursor-question.png"),"Help Cursor", self)
        self.WhatsThisCustomAction.setStatusTip("Obtain additional info for each keyword")
        #WhatsThisCustomAction.triggered.connect(self.WhatIsThisModeCustomAction.enterWhatsThisMode())
        self.WhatsThisCustomAction.setCheckable(True)
        toolbar.addAction(self.WhatsThisCustomAction)
        
        
        help_menu = self.menuBar().addMenu("&Help")
        
        about_action = QAction(QIcon("question-white.png"),"About LSDaltonGUI", self)
        about_action.setStatusTip("Find out more about LSDaltonGUI")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
        help_menu.addAction(self.WhatsThisCustomAction)
        toolbar.addAction(about_action)

        
        #adds a label with "Hello" along with Checkbox
#        toolbar.addWidget(QLabel("Hello"))
#        toolbar.addWidget(QCheckBox())

        #add status bar
        self.setStatusBar(QStatusBar(self))



        layoutMain = QHBoxLayout()

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        layoutS = QStackedLayout()

        layout1 = QVBoxLayout()

        widgetDal = QLabel()
        watermark = QPixmap("john-dalton.jpg")
        newPixmap = watermark.scaled(QSize(50,50),Qt.KeepAspectRatio)
        widgetDal.setPixmap(newPixmap)        
#        widgetDal.setPixmap(QPixmap("john-dalton.jpg") )        
#        widgetDal.setScaledContents(True)
        layout1.addWidget(widgetDal)


        widget = QLabel("LSDALTON.INP")
        font = widget.font()
        font.setPointSize(20)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
        layout1.addWidget(widget)

        self.widgetOutFile = QTextEdit()
        self.widgetOutFile.setText("**WAVE FUNCTION")
        self.outfile.write("**WAVE FUNCTION\n")
        self.widgetOutFile.append(".HF")
        self.outfile.write(".HF\n")
        self.widgetOutFile.append("*END OF INPUT")
        self.outfile.write("*END OF INPUT\n")
        self.outfile.close()
        f2.write("TmpFile\n")
        f2.close()
        self.widgetOutFile.setStatusTip("The current LSDALTON.INP file, generated by this program")
        self.widgetOutFile.setReadOnly(True)
        layout1.addWidget(self.widgetOutFile)

        layoutMain.addLayout(layout1)

        #TAB INSTEAD
        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(layoutS)

        btn1 = QPushButton( "**WAVE FUNCTION")
        btn1.pressed.connect( lambda n=0: layoutS.setCurrentIndex(0) )
        btn1.setStatusTip("Select the SCF wave function model")
        button_layout.addWidget(btn1)
        layoutS.addWidget(WaveFunc())

        btn2 = QPushButton( "**INTEGRALS")
        btn2.pressed.connect( lambda n=1: layoutS.setCurrentIndex(1) )
        btn2.setStatusTip("Select the integral evaluation specifications")
        button_layout.addWidget(btn2)
        layoutS.addWidget(Integral())

        btn3 = QPushButton( "**Other")
        btn3.pressed.connect( lambda n=2: layoutS.setCurrentIndex(2) )
        button_layout.addWidget(btn3)
        layoutS.addWidget(Other())

        layoutS.setCurrentIndex(0)
        layoutMain.addLayout(pagelayout)
        
        #Widget which consist of the widgets in the layout
        widget3 = QWidget()
        widget3.setLayout(layoutMain)
        self.setCentralWidget(widget3)
        
#        #layout with 10 buttons 
#        
#        # QHBoxLayout is a horizontally stacking layout with new widgets
#        # added to the right of previous widgets.
#        layout = QHBoxLayout()
#
#        for n in range(10):
#            # Create a push button labeled with the loop number 0-9
#            btn = QPushButton(str(n))
#            # SIGNAL: The .pressed signal fires whenever the button is pressed.
#            # We connect this to self.my_custom_fn via a lambda to pass in
#            # additional data.
#            # IMPORTANT: You must pass the additional data in as a named 
#            # parameter on the lambda to create a new namespace. Otherwise
#            # the value of n will be bound to the final value in the parent
#            # for loop (always 9).
#            btn.pressed.connect( lambda n=n: self.my_custom_fn(n) )
# 
#            # Add the button to the layout. It will go to the right by default.
#            layout.addWidget(btn)
#
#        # Create a empty widget to hold the layout containing our buttons.
#        widget = QWidget()
#        
#        # Set the layout containing our buttons onto the blank widget. We only
#        # need to do this here because we can't set a layout on a QMainWindow.
#        # So instead we're setting a layout on a widget, and then adding that 
#        # widget to the window(!)
#        widget.setLayout(layout)
#        
#        # Set the central widget of the Window. Widget will expand
#        # to take up all the space in the window by default.
#        self.setCentralWidget(widget)


#        #Old Label Widget 
#        label = QLabel("THIS IS AWESOME!!!")
#
#        # The `Qt` namespace has a lot of attributes to customise
#        # widgets. See: http://doc.qt.io/qt-5/qt.html
#        label.setAlignment(Qt.AlignCenter)
#        
#        # Set the central widget of the Window. Widget will expand
#        # to take up all the space in the window by default.
#        self.setCentralWidget(label)

#    # SLOT: This function will receive the single value passed from the signal
#    def my_custom_fn(self, a):
#        print(a)

    def WhatIsThisModeCustomActionF(self, s):
        if(s == Qt.Checked):
            self.WhatIsThisModeCustomAction.leaveWhatsThisMode()
        else:
            self.WhatIsThisModeCustomAction.enterWhatsThisMode()
            
    def onSaveLSDALTON(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save LSDALTON.INP as", "",
                                                  "All files (*.*)")
        print(filename)
        if filename:
            print("filename success")
            self.outfile = open('GUILSDALTON.INP', 'r') 
            f=open(filename, 'w')
            for line in self.outfile:
                f.write(line)
#                f.write("\n")
            f.close()
            self.outfile.close()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def RemoveText(self, s):
        self.outfile = open('GUILSDALTON.INP', 'r') 
        f=open('TMPGUILSDALTON.INP', 'r+')
        for line in self.outfile:
            if(not s in line):
                f.write(line)
        f.truncate()
        self.outfile.close()
        self.CopyTmpFileToFile(f)
        f.close
        self.UpdateWidgetOutFile()

    def CopyTmpFileToFile(self,f):
        f.seek(0)
        self.outfile = open('GUILSDALTON.INP', 'w') 
        self.outfile.seek(0)
        for line in f:
            self.outfile.write(line)
        self.outfile.truncate()
        self.outfile.close()

    def RemoveTextAndNext(self, s):
        self.outfile = open('GUILSDALTON.INP', 'r') 
        f=open('TMPGUILSDALTON.INP', 'r+')
        f.seek(0)
        skip = False
        for line in self.outfile:
            if(s in line):
                skip = True
            else:
                if(skip):
                    skip = False
                else:
                    f.write(line)
                    
        f.truncate()
        self.outfile.close()
        self.CopyTmpFileToFile(f)
        f.close()
        self.UpdateWidgetOutFile()

    def AddNewBlock(self, s):
        self.outfile = open('GUILSDALTON.INP', 'r') 
        f=open('TMPGUILSDALTON.INP', 'r+')
        f.seek(0)
        NotAlreadyExist = True
        for line in self.outfile:
            if(s in line):
                NotAlreadyExist = False
            
            if("*END OF INPUT" in line):
                if(NotAlreadyExist):
                    f.write(s)   
                    f.write("\n")
                    f.write(line)
            else:
                f.write(line)

        if(NotAlreadyExist):
            f.truncate()
            self.outfile.close()
            self.CopyTmpFileToFile(f)
            self.UpdateWidgetOutFile()
        else:
            self.outfile.close()
            
        f.close()
        

    def AddText(self, s, s2):
        self.outfile = open('GUILSDALTON.INP', 'r') 
        f=open('TMPGUILSDALTON.INP', 'r+')
        f.seek(0)
        for line in self.outfile:
            if(s2 in line):
                f.write(line)
                f.write(s)
                f.write("\n")
            else:
                f.write(line)
        f.truncate()
        self.outfile.close()
        self.CopyTmpFileToFile(f)
        f.close()
        self.UpdateWidgetOutFile()

    def UpdateWidgetOutFile(self):
        self.widgetOutFile.clear()
        self.outfile = open('GUILSDALTON.INP', 'r') 
        for line in self.outfile:
            self.widgetOutFile.append(line.strip())
        self.outfile.close()

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

window = MainWindow()
window.show() # IMPORTANT OTHERWISE SEE NOTHING

# Start the event loop.
app.exec_()

# Your application won't reach here until you exit and the event 
# loop has stopped.



# TODO
#1. Done
#2. Done
#  Update Display func
# add text to GUILSDALTON.INP (Add Block of Code to LSDALTON.INP file) - Structured!!
#            addKeyword(".DENSFIT")
#            addKeyword(".CONVDYN",Real)
#            etc 
# remove text to GUILSDALTON.INP (Remove Block of Code to LSDALTON.INP file)
# 
# Read xyz file and Create MOLECULE.INP
# Run lsdalton.x (provide path to lsdalton.x, path to basis set)
# display run command
#
# Create Bottons based on the Source code - increase version ID by 1.
#
# Read LSDALTON.INP and set the checkboxed etc accordingly!
#
