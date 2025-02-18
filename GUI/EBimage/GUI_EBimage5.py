#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
## @package GUI_EBimage.py
# @author Sebastien Ravel

##################################################
## Modules
##################################################
import argparse
import sys, os

# Python QT modules
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QApplication, QFileSystemModel, QTableWidget, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
from PyQt5.QtCore import Qt

#import rpy2
from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage

#exit()
##################################################
## Variables Globales
version = '1.0'
VERSION_DATE = '09/04/2018'

##################################################
## Functions

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative)
	return os.path.join(relative)


def existant_file(x):
	"""
	'Type' for argparse - checks that file exists but does not open by default.

	:param x: a file path
	:type x: str()
	:rtype: string
	:return: string

	"""
	if not os.path.exists(x):
		# Argparse uses the ArgumentTypeError to give a rejection message like:
		# error: argument input: x does not exist
		raise argparse.ArgumentTypeError("{0} does not exist".format(x))

	return x

filename = './includes/EBimage.ui'
myfontfile = resource_path(os.path.join(filename))
formEBimage,baseEBimage = uic.loadUiType(myfontfile)

def resource_path(relative_path):
	if hasattr(sys, '_MEIPASS'):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

# ************************************* CLASSE EBimage Gestion de l'affichage et de la récupération de donnée ****************************************************
## @class EBimage
# @brief Classe principale, fenêtre principale
class EBimage( formEBimage, baseEBimage ):
	""" Classe principale qui est aussi la fenêtre principale de la GUI
	"""
	def __init__(self,app,parent=None):
		super(EBimage,self).__init__(parent)
		self.app = app
		self.ui = self
		self.ui.setupUi(self)
		self.ui.setFocus(True)
		self.ui.setWindowTitle("GUI_EBimage")
		self.ui.show()
		self.setFocusPolicy(QtCore.Qt.StrongFocus)
		self.activateWindow()
		self.initializationCalibrationVariables()
		self.initializationAnalysisVariables()
		self.initializationCommonVariables()
		self.createWidgets()

	def initializationCalibrationVariables(self):
		"""Initialize calibration variables with defaults values"""
		self.calibrationInOutPath = None
		self.calibrationBasename = None
		self.calibrationOpenLineEdit.setText("")
		self.ui.runCalibrationFrame.hide()
		self.ui.calibrationOutFrame.hide()
		self.ui.runCalibrationPushButton.setDisabled(True)
		self.ui.treeView.reset()
		self.actualizeOutFiles()

	def initializationAnalysisVariables(self):
		"""Initialize analysis variables with defaults values"""
		self.dicoAnalysisValues = {	"leafSize" : 1000,
								"leafBorderSize" : 3,
								"lesionSize" : 10,
								"lesionBorderSize" : 3,
								"lesionColor" : 0					# 0 = black 1 = white
							}
		self.dicoObjectOpenLineEditAnalysis = {
								"leafSize" : self.leafSizeLineEdit,
								"leafBorderSize" : self.leafBorderSizeLineEdit,
								"lesionSize" : self.lesionSizeLineEdit,
								"lesionBorderSize" : self.lesionBorderLineEdit,
												}


		self.inputAnalyseFolder = ""
		self.outputAnalyseFolder = ""
		self.ui.runAnalysisPushButton.setDisabled(True)

	def initializationCommonVariables(self):
		"""Initialize common variables with defaults values"""
		#self.EBimageCalibration = EBimageCalibration
		#self.EBimageAnalysis = EBimageAnalysis
		self.tableWidget = QTableWidget()

	def actualizeOutFiles(self):
		"""actualise path of out files"""
		if self.calibrationInOutPath != None:
			self.calibrationFilesOut = {
								"RData": self.calibrationInOutPath+"/"+self.calibrationBasename+".RData",
								"png": self.calibrationInOutPath+"/"+self.calibrationBasename+".png",
								"txt": self.calibrationInOutPath+"/"+self.calibrationBasename+".txt",
								"info": self.calibrationInOutPath+"/"+self.calibrationBasename+"_info.txt"
								}

	def createWidgets(self):
		"""Mise en place du masquage des frames et des connections de l'interface"""
		self.setWindowIcon(QIcon(resource_path("./includes/icon.ico")))
		self.ui.statusbar.setStyleSheet("color: rgb(255, 107, 8);font: 8pt 'Arial Black';")

		## Edition des connect callibration:
		self.ui.loadCalibrationPushButton.clicked.connect(lambda: self.loadFolder(inputCat = "calibration", methode="clicked"))
		self.ui.calibrationOpenLineEdit.editingFinished.connect(lambda: self.loadFolder(inputCat = "calibration", methode="write"))

		self.ui.runCalibrationPushButton.clicked.connect(self.run)
		self.ui.resetCalibrationPushButton.clicked.connect(self.resetLoadFolder)

		## Edition des connect analysis:
		self.ui.leafSizeLineEdit.editingFinished.connect(lambda: self.actualizeAnalysisValues(inputLabel = "leafSize"))
		self.ui.leafBorderSizeLineEdit.editingFinished.connect(lambda: self.actualizeAnalysisValues(inputLabel = "leafBorderSize"))
		self.ui.lesionSizeLineEdit.editingFinished.connect(lambda: self.actualizeAnalysisValues(inputLabel = "lesionSize"))
		self.ui.lesionBorderLineEdit.editingFinished.connect(lambda: self.actualizeAnalysisValues(inputLabel = "lesionBorderSize"))
		self.ui.lesionColorComboBox.currentIndexChanged[int].connect(lambda: self.actualizeAnalysisValues(inputLabel = "lesionColor"))

		self.ui.loadAnalysisPushButton.clicked.connect(lambda: self.loadInputAnalysis(inputCat = "inputAnalysis", methode="clicked"))
		self.ui.analysisOpenLineEdit.editingFinished.connect(lambda: self.loadInputAnalysis(inputCat = "inputAnalysis", methode="write"))

		self.ui.loadPathOutPushButton.clicked.connect(lambda: self.loadOutputAnalysis(inputCat = "outputAnalysis", methode="clicked"))
		self.ui.pathOutlineEdit.editingFinished.connect(lambda: self.loadOutputAnalysis(inputCat = "outputAnalysis", methode="write"))

		self.ui.loadCalibrationFilePushButton.clicked.connect(lambda: self.loadFoldersAnalysis(inputCat = "calibrationAnalysis", methode="clicked"))
		self.ui.calibrationFileOpenLineEdit.editingFinished.connect(lambda: self.loadFoldersAnalysis(inputCat = "calibrationAnalysis", methode="write"))


	def testInt(self,inputLabel, value):
		try:
			return int(value)
		except:
			self.displayError(typeError="WARNING:", message = "\"%s\" is not a int value \n" % (value))
			self.dicoObjectOpenLineEditAnalysis[inputLabel].setText(str(self.dicoAnalysisValues[inputLabel]))

	def actualizeAnalysisValues(self, inputLabel = None):
		"""actualize values for analysis"""
		print(self.dicoAnalysisValues)
		if inputLabel == "lesionColor":
			dicoColor = {"Black":0, "White":1}
			self.dicoAnalysisValues[inputLabel] = dicoColor[self.lesionColorComboBox.currentText()]
		else:
			self.dicoAnalysisValues[inputLabel] = self.testInt(inputLabel, self.dicoObjectOpenLineEditAnalysis[inputLabel].text())

		print(inputLabel, self.dicoAnalysisValues[inputLabel])

	def resetLoadFolder(self):
		"""To reset if delete of change value"""
		self.actualizeRunButton()
		self.initializationCalibrationVariables()
		self.enableButtonsCalibration()
		self.ui.calibrationOutFrame.hide()
		self.viewLayout.removeWidget(self.tableWidget)

	def loadInputAnalysis(self,inputCat = None, methode = None):
		"""Méthode qui permet de charger un fichier et afficher dans le plainText"""
		directoryToOpen = os.getcwd()
		if methode == "clicked":
			pathdir = QFileDialog.getExistingDirectory(self, caption="Load the directory "+inputCat, directory=directoryToOpen)
			self.analysisOpenLineEdit.setText(pathdir)
		elif methode == "write":
			pathdir = str(self.analysisOpenLineEdit.text())
		if pathdir != "" and os.path.isdir(pathdir):
			print(pathdir)

	def loadOutputAnalysis(self,inputCat = None, methode = None):
		"""Méthode qui permet de charger un fichier et afficher dans le plainText"""
		directoryToOpen = os.getcwd()
		if methode == "clicked":
			pathdir = QFileDialog.getExistingDirectory(self, caption="Load the directory "+inputCat, directory=directoryToOpen)
			self.pathOutlineEdit.setText(pathdir)
		elif methode == "write":
			pathdir = str(self.pathOutlineEdit.text())
		if pathdir != "" and os.path.isdir(pathdir):
			print(pathdir)

	def loadFolder(self,inputCat = None, methode = None):
		"""Méthode qui permet de charger un fichier et afficher dans le plainText"""
		directoryToOpen = os.getcwd()
		if methode == "clicked":
			pathdir = QFileDialog.getExistingDirectory(self, caption="Load the directory "+inputCat, directory=directoryToOpen)
			self.calibrationOpenLineEdit.setText(pathdir)
		elif methode == "write":
			pathdir = str(self.calibrationOpenLineEdit.text())

		if pathdir != "" and os.path.isdir(pathdir):
			self.calibrationInOutPath = pathdir
			self.calibrationBasename = self.calibrationInOutPath.split("/")[-1]

			for root, dirs, files in os.walk(pathdir):
				if "leaf" in dirs and "background" in dirs and "lesion" in dirs:
					#-- Modèle
					self.myModel = QFileSystemModel()
					self.myModel.setReadOnly(True)
					self.myModel.setRootPath(pathdir)

					self.treeView.setModel(self.myModel)
					rootModelIndex = self.myModel.index(pathdir)
					self.treeView.setRootIndex(rootModelIndex)

					# ajuste to contents
					self.treeView.setColumnWidth(0,400)
					self.treeView.setSortingEnabled(True)
					self.treeView.setAlternatingRowColors(True)
					self.treeView.setAnimated(True)
					self.actualizeRunButton()
					break
				else:
					self.displayError(typeError="WARNING:", message = "\"%s\" not containt mandatory directory \n" % (pathdir))
					self.calibrationInOutPath = None
					self.calibrationOpenLineEdit.setText("")
					break


		else:
			self.calibrationInOutPath = None
			self.calibrationOpenLineEdit.setText("")
			self.displayError(typeError="WARNING:",message = "\"%s\" is not a valid Path \n" % (pathdir))
		#print(self.calibrationInOutPath)

	def actualizeRunButton(self):
		"""de grise le bouton run si rempli matrice et order"""
		if self.calibrationInOutPath != None:
			self.ui.runCalibrationPushButton.setEnabled(True)
		else:
			self.ui.runCalibrationPushButton.setDisabled(True)


	def infoDialogue(self, status): ## Method to open a message box
			infoBox = QMessageBox()
			infoBox.setFixedSize(10000,100000)
			infoBox.setIcon(QMessageBox.Information)
			infoBox.setText("Calibration OK")
			filestxt = "Files:\n"
			for key, path in self.calibrationFilesOut.items():
				filestxt += "- {}\n".format(path)
			if status == "new":
				infoBox.setInformativeText("All files created\n"+filestxt)
			if status == "already":
				infoBox.setInformativeText("All files already exist\n"+filestxt)
			infoBox.setWindowTitle("Good Calibration")
			infoBox.setStandardButtons(QMessageBox.Ok)
			infoBox.setEscapeButton(QMessageBox.Close)
			infoBox.exec_()
			self.openCalibrationTable()
			self.loadCalibrationPNG()

	def disalbledButtonsCalibration(self):
		"""Disable buttons when run calibration"""
		self.ui.runCalibrationPushButton.setDisabled(True)
		self.ui.loadCalibrationPushButton.setDisabled(True)
		self.ui.calibrationOpenLineEdit.setDisabled(True)


	def enableButtonsCalibration(self):
		"""enable buttons when finish run calibration or already do"""
		self.ui.runCalibrationPushButton.setDisabled(True)
		self.ui.loadCalibrationPushButton.setEnabled(True)
		self.ui.calibrationOpenLineEdit.setEnabled(True)


	def run(self):

		try:
			result = "0"
			# grise
			self.disalbledButtonsCalibration()
			self.ui.resetCalibrationPushButton.setDisabled(True)
			self.actualizeOutFiles()

			with open("fonctions_apprentissage.r", "r", encoding="utf-8") as apprentissageRopen:
				apprentissage = "".join(apprentissageRopen.readlines())

			apprentissage = SignatureTranslatedAnonymousPackage(apprentissage, "apprentissage")

			if args.debug: print("{}\n{}".format(apprentissage, dir(apprentissage)))

			# test if Rdata file already exist, if yes remove file if user say yes, or stop analyse
			if os.path.exists(self.calibrationFilesOut["RData"]):
				reply = QMessageBox.question(self, 'WARNING', 'File will be overwritten.\nDo you still want to proceed?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
				if reply == QMessageBox.Yes:
					for key, path in self.calibrationFilesOut.items():
						os.remove(path)
					reloadCalibration = True
				elif reply == QMessageBox.No:
					reloadCalibration = False
			else:
				reloadCalibration = True

			if reloadCalibration:
				self.ui.statusbar.showMessage(str("Running calibration, please waiting ...."),9600)
				#doivent être (dans cet ordre) le nom (relatif) des sous-répertoires fond, limbe, lésions
				result , good = apprentissage.apprentissage(self.calibrationInOutPath,"background", "leaf", "lesion").r_repr().replace('"','').replace("c(","").replace(")","").split(",")
				self.calibrationFileOpenLineEdit.setText(self.calibrationFilesOut["RData"])
				#print(result, good)
			if result == "1" and os.path.exists(self.calibrationFilesOut["RData"]):
				print(result, self.calibrationFilesOut["RData"])
				self.infoDialogue(status = "new")
				self.ui.statusbar.showMessage(str("FINISH, files were product on : %s" % self.calibrationInOutPath),9600)
				self.ui.resetCalibrationPushButton.setEnabled(True)
			elif  result == "0" and os.path.exists(self.calibrationFilesOut["RData"]):
				self.infoDialogue(status = "already")
				print(result, self.calibrationFilesOut["RData"])
				self.calibrationFileOpenLineEdit.setText("")
				self.ui.resetCalibrationPushButton.setEnabled(True)
				self.resetLoadFolder()
				self.enableButtonsCalibration()
			elif result == "0" and not os.path.exists(self.calibrationFilesOut["RData"]):
				self.displayError(typeError = "ERROR:", message = "Error when running R code....")
				self.resetLoadFolder()
		except Exception as e:
				self.displayError(typeError = "ERROR:", message = "Error when running R code....\n"+e)
				self.resetLoadFolder()
				self.ui.resetCalibrationPushButton.setEnabled(True)


	def openCalibrationTable(self):
		"""View result of calibration"""
		self.ui.calibrationOutFrame.show()
		with open(self.calibrationFilesOut["info"]) as tableFile:
			lines = [line.rstrip().split() for line in tableFile.readlines()]
		self.tableWidget.setRowCount(len(lines)-1)
		self.tableWidget.setColumnCount(4)
		row = 0
		print(lines[1:])
		for line in lines[1:]:
			print(line)
			if len(line) == 0:
				next
			if len(line) == 3:
				self.tableWidget.setItem(row,0, QTableWidgetItem(""))
				self.tableWidget.setItem(row,1, QTableWidgetItem(lines[row+1][0]))
				self.tableWidget.setItem(row,2, QTableWidgetItem(lines[row+1][1]))
				self.tableWidget.setItem(row,3, QTableWidgetItem(lines[row+1][2]))
			if len(line) == 4:
				self.tableWidget.setItem(row,0, QTableWidgetItem(lines[row+1][0]))
				self.tableWidget.setItem(row,1, QTableWidgetItem(lines[row+1][1]))
				self.tableWidget.setItem(row,2, QTableWidgetItem(lines[row+1][2]))
				self.tableWidget.setItem(row,3, QTableWidgetItem(lines[row+1][3]))
			row += 1
		self.viewLayout.addWidget(self.tableWidget)
		self.show()
		self.loadCalibrationPNG()

	def loadCalibrationPNG(self):
		"""Load png file if good calibration"""
		print(self.calibrationFilesOut["png"])
		pic = QPixmap(self.calibrationFilesOut["png"])
		pic = pic.scaled(480,480)
		self.ui.imgLabel.setPixmap(pic)


	def displayError(self,typeError,message):
		""" affiche les erreurs dans la zone de text"""
		if args.cmdMode:
			print(typeError,message)
		else:
			# Grise les cases pour ne pas relancer dessus et faire un reset
			#self.ui.runPushButton.setDisabled(True)
			print(typeError,message)
			txtError = str(message)
			self.ui.statusbar.showMessage(txtError,7200)
			self.errorPopUp(typeError, message)

	def errorPopUp(self, typeError, message): ## Method to open a message box
		infoBox = QMessageBox()
		infoBox.setFixedSize(10000,100000)
		infoBox.setWindowTitle(typeError)
		if "ERROR" in typeError:
			infoBox.setIcon(QMessageBox.Critical)
		else:
			infoBox.setIcon(QMessageBox.Warning)
		infoBox.setTextFormat(Qt.RichText)
		infoBox.setText("{} {}".format(typeError,message))
		infoBox.setTextInteractionFlags(Qt.TextSelectableByMouse)

		infoBox.exec_()


def main():

	#print sys.argv+["-cmd", "-gnome-terminal"]
	nargv = sys.argv

	# instanciation des objets principaux
	app = QApplication(nargv)
	myapp = EBimage(app)

	myapp.showMinimized()
	# les .app sous macos nécessitent cela pour que l'appli s'affiche en FG
	if "darwin" in sys.platform and ".app/" in sys.argv[0]:
		myapp.raise_()

	# lancement de la boucle Qt
	sys.exit(app.exec_())


def cmd():
	#print sys.argv+["-cmd", "-gnome-terminal"]
	nargv = sys.argv
	# instanciation des objets principaux
	app = QApplication(nargv)
	myapp = EBimage(app)

	# Load info arguments to Class
	# matrice file
	myapp.matricePathFile = relativeToAbsolutePath(args.matriceParam)
	# order file
	myapp.orderPathFile = relativeToAbsolutePath(args.orderMatriceParam)
	# PCA value
	myapp.PCAvalue = args.pcaParam
	# DA value
	myapp.DAvalue = args.daParam
	# pop min value
	myapp.popMinValue = args.nbpopiParam
	# pop max value
	myapp.popMaxValue = args.nbpopmParam
	# pgraph value
	myapp.graphType = args.graphParam

	# working dir path
	workingDir = "/".join(relativeToAbsolutePath(args.orderMatriceParam).encode("utf-8").split("/")[:-1])+"/"
	myapp.workingDir = workingDir.encode("utf-8")
	# basename
	basename = relativeToAbsolutePath(args.orderMatriceParam).encode("utf-8").split("/")[-1].split(".")[0]
	myapp.basename = basename.encode("utf-8")
	# pathFileOut dir path
	pathFileOut = workingDir+basename+"/"
	myapp.pathFileOut = pathFileOut.encode("utf-8")

	# rm old folder
	myapp.rmOld = args.rmOldParam


	# Run programme
	myapp.run()


if __name__ == '__main__':

	# Parameters recovery
	parser = argparse.ArgumentParser(prog='GUI_EBimage.py', description='''This Programme open GUI to produce EBimage script.\n
																				#If use on cluster you can run in commande line with option -c and args''')
	parser.add_argument('-v', '--version', action='version', version='You are using %(prog)s version: ' + version, help=\
						'display GUI_EBimage.py version number and exit')
	parser.add_argument('-d', '--debug',action='store_true', help='enter verbose/debug mode', dest = "debug", default = "False")

	filesReq = parser.add_argument_group('Input mandatory infos for running if -c use')
	filesReq.add_argument('-c', '--cmd', action='store_true', dest = 'cmdMode', help = 'If used, programme run in CMD without interface')
	filesReq.add_argument('-m', '--mat', metavar="<filename>",type=existant_file, required=False, dest = 'matriceParam', help = 'matrice file path')
	filesReq.add_argument('-o', '--order', metavar="<filename>",type=existant_file, required=False, dest = 'orderMatriceParam', help = 'file with re-order name of matrice')

	files = parser.add_argument_group('Input infos for running with default values')
	files.add_argument('-pca', '--pcanum', metavar="<int>", required=False, default = "NULL", dest = 'pcaParam', help = 'Number value of PCA retains (default = NULL)')
	files.add_argument('-da', '--danum', metavar="<int>", required=False, default = "NULL", dest = 'daParam', help = 'Number value of DA retains (default = NULL)')
	files.add_argument('-pi', '--popi', metavar="<int>", type = int, default=2, required=False, dest = 'nbpopiParam', help = 'Number of pop Min (default = 2)')
	files.add_argument('-pm', '--popm', metavar="<int>", type = int, default=10, required=False, dest = 'nbpopmParam', help = 'Number of pop Max (default = 10)')	## Check parameters
	files.add_argument('-r', '--rm', metavar="<True/False>", choices=("True","False"), default="False", required=False, dest = 'rmOldParam', help = 'if directory exist remove (default = False)')	## Check parameters
	files.add_argument('-g', '--graph', metavar="<1/2/3>", choices=("1","2","3"), default="1", required=False, dest = 'graphParam', help = 'type of graph (default = 1)')	## Check parameters
	args = parser.parse_args()

	if args.cmdMode:
		if args.matriceParam == "" or args.orderMatriceParam == "":
			print("ERROR: You must enter require arguments")
			exit()
		cmd()
	else:
		# run interface
		main()
