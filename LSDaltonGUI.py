from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
class WaveFunc(QWidget):

    def __init__(self, *args, **kwargs):
        super(WaveFunc, self).__init__(*args, **kwargs)

        layoutWF = QVBoxLayout()

        layoutWF.addWidget(QLabel("Select the SCF Wave Function Model"))
        #Consider QbuttonGroup to have HF and DFT buttons be exclusive Check Boxes
        self.widgetWF = QCheckBox("Density Functional Theory (DFT)")
        self.widgetWF.setStatusTip("The default is Hartree-Fock (HF) when not checked")
        self.widgetWF.stateChanged.connect(self.wavefunc_state)
        layoutWF.addWidget(self.widgetWF)

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
            print("DFT chosen")
            self.widget4.setVisible(True)
            #Change to DFT with functional 
        else:
            print("HF chosen")
            self.widget4.setVisible(False)
            #Change to HF without functional 

    def DFTFUNCTextChanged(self,s):
        print("DFT Functional")
        #Change DFT functional in File   if DFT chosen
        print(s)

            
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

#        widget2 = QLabel()
#        widget2.setPixmap(QPixmap("john-dalton.jpg") )
#        widget2.setScaledContents(True)
#        layout.addWidget(widget2)
#        layout.addWidget(widget2)
        layoutInt.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
        self.setLayout(layoutInt)
#        self.setCentralWidget(self)
        

    def show_state(self, s):
        print(s)
        if(s == Qt.Checked):
            print( s == Qt.Checked )
            # add DENSFIT else
            print("add DENSFIT")
        else:
            print("remove DENSFIT")
            
        
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

        
# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.outfile = open('GUILSDALTON.INP', 'w') 
        # set title of window
        self.setWindowTitle("LSDalton GUI")

        #create instance of toolbar 
        toolbar = QToolBar("The main LSDalton toolbar")
        toolbar.setIconSize(QSize(16,16))
        #add toolbar to qmainwindow
        self.addToolBar(toolbar)
        
        #Qaction instance create from Q object to act as parent of the action
        #here the mainwindow is passed as the parent action
        #Icons from fugue.......        
        save_action = QAction(QIcon("disk-black.png"),"Save", self)
        #
        save_action.setStatusTip("Save LSDALTON.INP file")
        #"triggered" signal is sent when Qaction is clicked
#        save_action.triggered.connect(lambda outfile=outfile: self.onSaveLSDALTON(outfile))
        save_action.triggered.connect(self.onSaveLSDALTON)
        #add key short-cut to action
        #save_action.setShortcut(QKeySequence("Ctrl+s"))
        save_action.setShortcut(QKeySequence.Save)
        #set button checkable 
        #save_action.setCheckable(True)
        #add button to toolbar 
        toolbar.addAction(save_action)

        

        
        #adds a label with "Hello" along with Checkbox
#        toolbar.addWidget(QLabel("Hello"))
#        toolbar.addWidget(QCheckBox())

        #add status bar
        self.setStatusBar(QStatusBar(self))

        #Create instance of menu
        menu = self.menuBar()
        #add menu to menu -- name of menu
        #The & define keyboard shortcuts to menu entry
        #Here "F" selects this File menu
        file_menu = menu.addMenu(u"&File")
        #add action (same as for toolbar)
        file_menu.addAction(save_action)

        #horisontal line to seperate menu items
        file_menu.addSeparator()


        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(save_action)


        layoutMain = QHBoxLayout()

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        layoutS = QStackedLayout()

        layout1 = QVBoxLayout()
        widget = QLabel("LSDALTON.INP")
        font = widget.font()
        font.setPointSize(20)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignHCenter| Qt.AlignVCenter)
        layout1.addWidget(widget)

        widget7 = QTextEdit()
        widget7.setText("**WAVE FUNCTION")
        self.outfile.write("**WAVE FUNCTION")
        self.outfile.write("\n")
        widget7.append(".HF")
        self.outfile.write(".HF")
        self.outfile.write("\n")
        widget7.append("*END OF INPUT")
        self.outfile.write("*END OF INPUT")
        self.outfile.write("\n")
        widget7.setStatusTip("The current LSDALTON.INP file, generated by this program")
        widget7.setReadOnly(True)
        layout1.addWidget(widget7)

        layoutMain.addLayout(layout1)

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

            
    def onSaveLSDALTON(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save LSDALTON.INP as", "",
                                                  "All files (*.*)")
        print(filename)
        if filename:
            print("filename success")
            self.outfile.close()
            self.outfile = open('GUILSDALTON.INP', 'r') 
            f=open(filename, 'w')
            for line in self.outfile:
                print(line)
                f.write(line)
            f.close()
        
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
# Read LSDALTON.INP and set the checkboxed etc accordingly!
# Push Label of CheckBox to get more detailed info - citations etc. 
# Update Display
# Add Block of Code to LSDALTON.INP file
# Read xyz file and Create MOLECULE.INP
# 
# Create Bottons based on the Source code.

#Consider QbuttonGroup to have HF and DFT buttons be exclusive Check Boxes
