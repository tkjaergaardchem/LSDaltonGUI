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
class QHLine(QFrame):
    def __init__(self, *args, **kwargs):
        super(QHLine, self).__init__(*args, **kwargs)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

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
        #toplevel layout which have a single widget the scroll_widget
        #which contains the layoutWF layout 
        self.scroll_layoutWF = QVBoxLayout()
        self.layoutWF = QVBoxLayout()
        self.scroll_widgetWF = QWidget(self)
        self.scroll_widgetWF.setLayout(self.layoutWF)

        self.layoutWF.addWidget(QLabel("Select the Self-Consistent Field (SCF) Wave Function Model"))
        #Consider QbuttonGroup to have HF and DFT buttons be exclusive Check Boxes
        
        self.widgetHF = QCheckBox("Hartree-Fock (HF)")
        self.widgetHF.setStatusTip("Use the Hartree-Fock (HF) SCF method, recommended for Correlated calculations (see **CC and **DEC)")
        self.widgetHF.setWhatsThis("Whats This2")
        self.widgetHF.setChecked(True)
        self.widgetHF.stateChanged.connect(self.wavefunc_state2)
        self.layoutWF.addWidget(self.widgetHF)

        self.widgetDFT = QCheckBox("Density Functional Theory (DFT)")
        self.widgetDFT.setStatusTip("Use DFT as the SCF model, requires the specification of a DFT exchange-correlation (XC) functional")
#        self.widgetDFT.setToolTip("Use DFT as the SCF model")
        self.widgetDFT.setWhatsThis("Whats This1")
        self.widgetDFT.stateChanged.connect(self.wavefunc_state)
        self.layoutWF.addWidget(self.widgetDFT)

        self.widget4 = QComboBox()
        self.widget4.addItems(["LDA","SLATER","B3LYP"])
        #Set the default value to point to "B3LYP" 
        self.widget4.setCurrentIndex(2)
        self.widget4.setStatusTip("Select the DFT functional")
        #Signal
        self.widget4.currentIndexChanged[str].connect(self.DFTFUNCTextChanged)
        self.widget4.setVisible(False)
        self.layoutWF.addWidget(self.widget4)

        self.layoutWF.addWidget(QHLine())
        
        #*DENSOPT
        self.layoutWF.addWidget(QLabel("Density Matrix Optimization (SCF optimization) Keywords:"))

        self.widgetConvdyn = QCheckBox("Dynamic Density Optimization Threshold (recommended for large molecules)")
        self.widgetConvdyn.stateChanged.connect(self.convdyn_select)
        self.layoutWF.addWidget(self.widgetConvdyn)

        self.widgetConvdynL = QComboBox()
        self.widgetConvdynL.addItems(["SLOPP","STAND","TIGHT","VTIGH"])
        #Set the default value to point to "STAND" 
        self.widgetConvdynL.setCurrentIndex(1)
        self.widgetConvdynL.currentIndexChanged[str].connect(self.convdyn_selectL)
        self.layoutWF.addWidget(self.widgetConvdynL)

        self.widgetConvthr = QCheckBox("Static Density Optimization Threshold (recommended for small molecules)")
        self.widgetConvthr.stateChanged.connect(self.convthr_select)
        self.layoutWF.addWidget(self.widgetConvthr)

        self.widgetConvthrD = QDoubleSpinBox()
        self.widgetConvthrD.setMinimum(0.0)
        self.widgetConvthrD.setMaximum(10000.0)
        self.widgetConvthrD.setDecimals(10)
        self.widgetConvthrD.setValue(0.0001)
        self.widgetConvthrD.setSingleStep(0.00000001)
        self.widgetConvthrD.valueChanged.connect(self.convthr_value)
        self.layoutWF.addWidget(self.widgetConvthrD)

        self.layoutWF.addWidget(QHLine())

        self.layoutWF.addWidget(QLabel("Initial Starting Guess for Density Optimization:"))

        self.widgetStart = QCheckBox("Choose Starting Guess for Density Optimization")
        self.widgetStart.stateChanged.connect(self.start_select)
        self.layoutWF.addWidget(self.widgetStart)

        self.widgetStartL = QComboBox()
        self.widgetStartL.addItems(["H1DIAG","ATOMS","TRILEVEL"])
        #Set the default value to point to "ATOMS" 
        self.widgetStartL.setCurrentIndex(1)
        self.widgetStartL.currentIndexChanged[str].connect(self.start_selectL)
        self.layoutWF.addWidget(self.widgetStartL)

        self.layoutWF.addWidget(QHLine())

        self.layoutWF.addWidget(QLabel("Density Optimization Algorithm:"))

        self.widgetARH = QCheckBox("Augmented Roothaan-Hall optimization (Recommended and default)")
        self.widgetARH.stateChanged.connect(self.ARH_select)
        self.layoutWF.addWidget(self.widgetARH)

        self.widgetARHD = QCheckBox("Augmented Roothaan-Hall optimization using Davidson Solver")
        self.widgetARHD.stateChanged.connect(self.ARHD_select)
        self.layoutWF.addWidget(self.widgetARHD)

        self.widgetRH = QCheckBox("Roothaan-Hall optimization (standard method in many codes)")
        self.widgetRH.stateChanged.connect(self.RH_select)
        self.layoutWF.addWidget(self.widgetRH)

        self.widgetDIIS = QCheckBox("Activate Direct inversion in the iterative subspace (DIIS) accelaration (Require .RH)")
        self.widgetDIIS.stateChanged.connect(self.DIIS_select)
        self.layoutWF.addWidget(self.widgetDIIS)

        self.widgetrestart = QCheckBox("Restart from previous density matrix dens.restart")
        self.widgetrestart.stateChanged.connect(self.restart_select)
        self.layoutWF.addWidget(self.widgetrestart)
        
        self.layoutWF.setAlignment(Qt.AlignTop| Qt.AlignVCenter)

        self.layoutWF.addWidget(QHLine())

        #*DFT INPUT
        self.layoutWF.addWidget(QLabel("Density Functional Theory Input: Nummerical Grid Input"))
        self.layoutWF.addWidget(QLabel("Grid Type (Radial and partitioning)"))
        self.widgetGridTypeL0 = QCheckBox("Specify Radial Grid and partitioning")
        self.widgetGridTypeL0.stateChanged.connect(self.GridTypeL0_select)
        self.layoutWF.addWidget(self.widgetGridTypeL0)

        self.widgetGridTypeL1 = QComboBox()
        self.widgetGridTypeL1.addItems(["GC2","LMG","TURBO"])
        #Set the default value to point to "TURBO" 
        self.widgetGridTypeL1.setCurrentIndex(2)
        self.widgetGridTypeL1.currentIndexChanged[str].connect(self.GridTypeL12_select)
        self.layoutWF.addWidget(self.widgetGridTypeL1)
        self.widgetGridTypeL2 = QComboBox()
        self.widgetGridTypeL2.addItems(["SSF","BECKE","BECKEORIG","BLOCK","BLOCKSSF"])
        #Set the default value to point to "BLOCKSSF" 
        self.widgetGridTypeL2.setCurrentIndex(4)
        self.widgetGridTypeL2.currentIndexChanged[str].connect(self.GridTypeL12_select)
        self.layoutWF.addWidget(self.widgetGridTypeL2)

        self.widgetGRID0 = QCheckBox("Use TurboMole type Grids")
        self.widgetGRID0.stateChanged.connect(self.GRID0_select)
        self.layoutWF.addWidget(self.widgetGRID0)

        self.widgetGRIDL = QComboBox()
        self.widgetGRIDL.addItems([".GRID1",".GRID2",".GRID3",".GRID4",".GRID5"])
        #Set the default value to point to "GRID3" 
        self.widgetGRIDL.setCurrentIndex(2)
        self.widgetGRIDL.currentIndexChanged[str].connect(self.GRIDL_select)
        self.layoutWF.addWidget(self.widgetGRIDL)

        self.widgetGRIDD0 = QCheckBox("Use Dalton type Grids")
        self.widgetGRIDD0.stateChanged.connect(self.GRIDD0_select)
        self.layoutWF.addWidget(self.widgetGRIDD0)

        self.widgetGRIDDL = QComboBox()
        self.widgetGRIDDL.addItems([".ULTRAC",".COARSE",".NORMAL",".FINE",".ULTRAF"])
        #Set the default value to point to "NORMAL" 
        self.widgetGRIDDL.setCurrentIndex(2)
        self.widgetGRIDDL.currentIndexChanged[str].connect(self.GRIDDL_select)
        self.layoutWF.addWidget(self.widgetGRIDDL)
        
        self.layoutWF.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
        #Scroll area which contains scroll_widget which contains the
        #layoutWF layout
        self.scroll_areaWF = QScrollArea()
        self.scroll_areaWF.setWidget(self.scroll_widgetWF)
        self.scroll_layoutWF.addWidget(self.scroll_areaWF)
        
        self.setLayout(self.scroll_layoutWF)
        
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
        
    def convdyn_select(self, s):
#            self.widgetConvdyn.setChecked(True)
        if(s == Qt.Checked):
            if(self.widgetConvthr.isChecked()):
                self.widgetConvthr.setChecked(False)
            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".CONVDYN","*DENSOPT")
            self.parent().parent().AddText(self.widgetConvdynL.currentText(),".CONVDYN")
        else:
            self.parent().parent().RemoveTextAndNext(".CONVDYN")

    def convdyn_selectL(self,s):
        if(self.widgetConvdyn.isChecked()):
            self.parent().parent().RemoveTextAndNext(".CONVDYN")
            self.parent().parent().AddText(".CONVDYN","*DENSOPT")
            self.parent().parent().AddText(s,".CONVDYN")

    def convthr_select(self, s):
        if(s == Qt.Checked):
            if(self.widgetConvdyn.isChecked()):
                self.widgetConvdyn.setChecked(False)
            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".CONVTHR","*DENSOPT")
            self.parent().parent().AddDouble(str(self.widgetConvthrD.value()),".CONVTHR")
        else:
            self.parent().parent().RemoveTextAndNext(".CONVTHR")

    def convthr_value(self, d):
        if(self.widgetConvthr.isChecked()):
            self.parent().parent().RemoveTextAndNext(".CONVTHR")
            self.parent().parent().AddText(".CONVTHR","*DENSOPT")
            self.parent().parent().AddDouble(str(d),".CONVTHR")

    def start_select(self, s):
        if(s == Qt.Checked):
            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".START","*DENSOPT")
            self.parent().parent().AddText(self.widgetStartL.currentText(),".START")
        else:
            self.parent().parent().RemoveTextAndNext(".START")

    def start_selectL(self,s):
        if(self.widgetStart.isChecked()):
            self.parent().parent().RemoveTextAndNext(".START")
            self.parent().parent().AddText(".START","*DENSOPT")
            self.parent().parent().AddText(s,".START")

    def ARH_select(self, s):
        if(s == Qt.Checked):
            self.widgetARHD.setChecked(False)
            self.widgetRH.setChecked(False)
            self.widgetDIIS.setChecked(False)

            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".ARH","*DENSOPT")
        else:
            self.parent().parent().RemoveText(".ARH")

    def ARHD_select(self, s):
        if(s == Qt.Checked):
            self.widgetARH.setChecked(False)
            self.widgetRH.setChecked(False)
            self.widgetDIIS.setChecked(False)

            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".ARH DAVID","*DENSOPT")
        else:
            self.parent().parent().RemoveText(".ARH DAVID")

    def RH_select(self, s):
        if(s == Qt.Checked):
            self.widgetARH.setChecked(False)
            self.widgetARHD.setChecked(False)

            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".RH","*DENSOPT")
            if(self.widgetDIIS.isChecked()):
                self.parent().parent().AddText(".DIIS",".RH")                

        else:
            self.parent().parent().RemoveText(".RH")
            if(self.widgetDIIS.isChecked()):
                self.widgetDIIS.setChecked(False)

    def DIIS_select(self, s):
        if(s == Qt.Checked):
            if(self.widgetRH.isChecked()):
                self.parent().parent().AddText(".DIIS",".RH")
        else:
            self.parent().parent().RemoveText(".DIIS")

    def restart_select(self, s):
        if(s == Qt.Checked):
            self.parent().parent().AddNewBlock("*DENSOPT")
            self.parent().parent().AddText(".RESTART","*DENSOPT")
        else:
            self.parent().parent().RemoveText(".RESTART")


    def GRID0_select(self, s):
        if(s == Qt.Checked):
            self.widgetGRIDD0.setChecked(False)

            self.parent().parent().AddNewBlock("*DFT INPUT")
            self.parent().parent().AddText(self.widgetGRIDL.currentText(),"*DFT INPUT")
        else:
            self.parent().parent().RemoveText(".GRID")

    def GRIDL_select(self,s):
        if(self.widgetGRID0.isChecked()):
            self.parent().parent().RemoveText(".GRID")
            self.parent().parent().AddText(self.widgetGRIDL.currentText(),"*DFT INPUT")

    def GRIDD0_select(self, s):
        if(s == Qt.Checked):
            self.widgetGRID0.setChecked(False)

            self.parent().parent().AddNewBlock("*DFT INPUT")
            self.parent().parent().AddText(self.widgetGRIDDL.currentText(),"*DFT INPUT")
        else:
            self.parent().parent().RemoveText(self.widgetGRIDDL.currentText())

    def GRIDDL_select(self,s):
        if(self.widgetGRIDD0.isChecked()):
            self.parent().parent().RemoveText(".ULTRAC")
            self.parent().parent().RemoveText(".COARSE")
            self.parent().parent().RemoveText(".NORMAL")
            self.parent().parent().RemoveText(".FINE")
            self.parent().parent().RemoveText(".ULTRAF")
            self.parent().parent().AddText(self.widgetGRIDDL.currentText(),"*DFT INPUT")

    def GridTypeL0_select(self):
        if(self.widgetGridTypeL0.isChecked()):
            self.parent().parent().AddNewBlock("*DFT INPUT")
            self.parent().parent().AddText(".GRID TYPE","*DFT INPUT")
            self.parent().parent().AddText(" " + self.widgetGridTypeL1.currentText() + " " + self.widgetGridTypeL2.currentText(),".GRID TYPE")
        else:
            self.parent().parent().RemoveTextAndNext(".GRID TYPE")

    def GridTypeL12_select(self,s):
        if(self.widgetGridTypeL0.isChecked()):
            self.parent().parent().RemoveTextAndNext(".GRID TYPE")
            self.parent().parent().AddText(".GRID TYPE","*DFT INPUT")
            self.parent().parent().AddText(" " + self.widgetGridTypeL1.currentText() + " " + self.widgetGridTypeL2.currentText(),".GRID TYPE")


            
# **INTEGRAL TAB        
class Integral(QWidget):

    def __init__(self, *args, **kwargs):
        super(Integral, self).__init__(*args, **kwargs)

        self.scroll_layoutInt = QVBoxLayout()
        self.layoutInt = QVBoxLayout()
        self.scroll_widgetInt = QWidget(self)
        self.scroll_widgetInt.setLayout(self.layoutInt)

        self.layoutInt.addWidget(QLabel("Integral and Performance Specific Keywords"))

        self.widgetDF = QCheckBox("Use density-fitting for Coulomb Integrals")
        self.widgetDF.setStatusTip("Recommended for performance reasons")
        self.widgetDF.stateChanged.connect(self.show_state)
        self.layoutInt.addWidget(self.widgetDF)

        self.widgetINTTHR = QCheckBox("Integral Screening Threshold")
        self.widgetINTTHR.setStatusTip("The overall screening threshold for integral evaluation.")
        self.widgetINTTHR.setWhatsThis("The overall screening threshold for integral evaluation. The various integral-evaluation thresholds (below) are set according to this Threshold. The Screening threshold used for Coulomb is this Threshold multiplied by 10e-2 (Default: 10e-10). The Screening threshold used for Exchange is this Threshold (Default: 10e-8). The Screening threshold used for One-electron operators is this Threshold multiplied by 10e-7 (Default: 10e-15)")
        self.widgetINTTHR.stateChanged.connect(self.INTTHR_select)
        self.layoutInt.addWidget(self.widgetINTTHR)

        self.widgetINTTHRVAL = QDoubleSpinBox()
        self.widgetINTTHRVAL.setMinimum(0.0)
        self.widgetINTTHRVAL.setMaximum(10000.0)
        self.widgetINTTHRVAL.setDecimals(16)
        self.widgetINTTHRVAL.setValue(0.00000001)
        self.widgetINTTHRVAL.setSingleStep(0.0000000001)
        self.widgetINTTHRVAL.valueChanged.connect(self.INTTHR_value)
        self.layoutInt.addWidget(self.widgetINTTHRVAL)
        

        self.widgetNOCS = QCheckBox("Deactivate Cauchy-Schwarz screening")
        self.widgetNOCS.setStatusTip("Not Recommended as this will slow down the code.")
        self.widgetNOCS.stateChanged.connect(self.NOCS_select)
        self.layoutInt.addWidget(self.widgetNOCS)
        
        self.layoutInt.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
        #self.setLayout(self.layoutInt)

        self.scroll_areaInt = QScrollArea()
        self.scroll_areaInt.setWidget(self.scroll_widgetInt)
        self.scroll_layoutInt.addWidget(self.scroll_areaInt)
        
        self.setLayout(self.scroll_layoutInt)
        

    def show_state(self, s):
        if(s == Qt.Checked):
            self.parent().parent().AddNewBlock("**INTEGRAL")
            self.parent().parent().AddText(".DENSFIT","**INTEGRAL")
        else:
            self.parent().parent().RemoveText(".DENSFIT")

    def NOCS_select(self, s):
        if(s == Qt.Checked):
            self.parent().parent().AddNewBlock("**INTEGRAL")
            self.parent().parent().AddText(".NO SCREEN","**INTEGRAL")
        else:
            self.parent().parent().RemoveText(".NO SCREEN")

    def INTTHR_select(self, s):
        if(s == Qt.Checked):
            self.parent().parent().AddNewBlock("**INTEGRAL")
            self.parent().parent().AddText(".THRESH","**INTEGRAL")
            self.parent().parent().AddDouble(str(self.widgetINTTHRVAL.value()),".THRESH")
        else:
            self.parent().parent().RemoveTextAndNext(".THRESH")

    def INTTHR_value(self, d):
        if(self.widgetINTTHR.isChecked()):
            self.parent().parent().RemoveTextAndNext(".THRESH")
            self.parent().parent().AddText(".THRESH","**INTEGRAL")
            self.parent().parent().AddDouble(str(self.widgetINTTHRVAL.value()),".THRESH")

# **Other TAB        
class Other(QWidget):

    def __init__(self, *args, **kwargs):
        super(Other, self).__init__(*args, **kwargs)

        pass
#        layout = QVBoxLayout()
#        layoutStack.addLayout(layout)
#        layout.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
#
#        self.setLayout(layout)

# **Other TAB        
class DEC(QWidget):

    def __init__(self, *args, **kwargs):
        super(DEC, self).__init__(*args, **kwargs)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Divide-Expand-Consolidate Keywords"))
        
        layout.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
        
        self.setLayout(layout)
        
# **Other TAB        
class CC(QWidget):

    def __init__(self, *args, **kwargs):
        super(CC, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Conventional Coupled Cluster Keywords"))
        
        layout.setAlignment(Qt.AlignTop| Qt.AlignVCenter)
        
        self.setLayout(layout)

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

#        widgetDal = QLabel()
#        watermark = QPixmap("john-dalton.jpg")
#        newPixmap = watermark.scaled(QSize(50,50),Qt.KeepAspectRatio)
#        widgetDal.setPixmap(newPixmap)        
#        widgetDal.setPixmap(QPixmap("john-dalton.jpg") )        
#        widgetDal.setScaledContents(True)
#        layout1.addWidget(widgetDal)


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

        btn3 = QPushButton( "**CC")
        btn3.pressed.connect( lambda n=2: layoutS.setCurrentIndex(2) )
        button_layout.addWidget(btn3)
        layoutS.addWidget(CC())

        btn3 = QPushButton( "**DEC")
        btn3.pressed.connect( lambda n=2: layoutS.setCurrentIndex(3) )
        button_layout.addWidget(btn3)
        layoutS.addWidget(DEC())

        #Set tab to point to WAVE FUNCTION
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

    def AddDouble(self, d, s2):
        self.outfile = open('GUILSDALTON.INP', 'r') 
        f=open('TMPGUILSDALTON.INP', 'r+')
        f.seek(0)
        for line in self.outfile:
            if(s2 in line):
                f.write(line)
                f.write(d)
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
#3. Done
#4. Done
#5. Keyword and Threshold or     addTextReal(".CONVTHR",Real)
#6. Keyword and List Variable    addKeyword(".CONVDYN",List)
#6. SubTab *DENSOPT
#7. Read xyz file and Create MOLECULE.INP
#8. Run lsdalton.x (provide path to lsdalton.x, path to basis set)
#9.  display run command
#
# Create Bottons based on the Source code - increase version ID by 1.
#
# Read LSDALTON.INP and set the checkboxed etc accordingly!
#
