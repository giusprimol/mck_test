# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 21:28:15 2015

@author: giuseppe
"""

import pandas as pd, sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui, uic
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from model import *

#==============================================================================
# 
# test_data = pd.DataFrame(index = ['A','B'], columns = ['2015','2016','2017'], data=[[100,101,102],[99,99,98]])
# ld = model.loaded_data_model(test_data)
# td = model.thresh_data_model()
# cd = model.calc_data_model(ld,td)
#==============================================================================


 
# load the main, show and help windows
mainwindow_class = uic.loadUiType("mainWin.ui")[0]
#helpwindow_class = uic.loadUiType("helpWin.ui")[0]
#showwindow_class = uic.loadUiType("showWin.ui")[0]
 
# Adding the matplotlib canvas and application logic
class MyWindowClass(QtGui.QMainWindow, mainwindow_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.model = model_data()
        self.setupUi(self)
        self.setupFigure()
        self.setupSignals()
    
    def setupFigure(self):        
        self.figure = Figure()#(2.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.findChild(QtGui.QWidget,'widget_plot'))
                
    def setupSignals(self):
        # connecting signals from the data model...        
        self.model.loaded_data.loaded_data_changed.connect(self.handle_loaded_data_changed)
        self.model.calc_data.calc_data_changed.connect(self.handle_calc_data_changed)
        self.model.thresh_data.thresh_data_changed.connect(self.handle_thresh_data_changed)
        self.model.summary_data.summary_data_changed.connect(self.summary_data_data_changed)
    
        # ... and from the GUI
        self.findChild(QtGui.QWidget,'but_load').clicked.connect(self.handle_press_loadData)
        self.connect(self.findChild(QtGui.QWidget,'combo_serA'), QtCore.SIGNAL("currentIndexChanged(const QString&)"), 
                    self.handle_combo_selection_change)
        self.connect(self.findChild(QtGui.QWidget,'combo_serB'), QtCore.SIGNAL("currentIndexChanged(const QString&)"), 
                    self.handle_combo_selection_change)
        self.findChild(QtGui.QWidget,'spb_thr1').valueChanged.connect(self.handle_thresh_box_change)
        self.findChild(QtGui.QWidget,'spb_thr2').valueChanged.connect(self.handle_thresh_box_change)
        self.findChild(QtGui.QWidget,'spb_thr3').valueChanged.connect(self.handle_thresh_box_change)
        

    def handle_loaded_data_changed(self):
        # update list boxes
        data_series = sorted(self.model.loaded_data.data.index)
        comboA = self.findChild(QtGui.QWidget,'combo_serA')
        comboA.blockSignals(True)        
        comboA.clear()
        comboA.insertItems(0,data_series)
        comboA.setCurrentIndex(0)
        comboA.blockSignals(False)
        
        comboB = self.findChild(QtGui.QWidget,'combo_serB')
        comboB.blockSignals(True)         
        comboB.clear()
        comboB.insertItems(0,data_series)
        comboB.setCurrentIndex(1)
        comboB.blockSignals(False)
        self.handle_combo_selection_change(None)

    
    def handle_thresh_data_changed(self):
        
        pass
    
    def summary_data_data_changed(self):
        # update interface
        pass
    
    def handle_calc_data_changed(self):
        # update summary data
        # update interface
        pass
        
    def handle_press_loadData(self):
        try:        
            (filename, filetype) = QtGui.QFileDialog.getOpenFileNameAndFilter(parent = None, 
                caption = 'Select file...', directory = '.', 
                filter= "Comma Separed Text (*.csv;*.txt);;Excel (*.xls;*.xlsm;*.xlsx)")
            if filename:
                self.model.loaded_data.loadfile(filename)
        except Exception as e:
            QtGui.QErrorMessage(self, 'Errore', e.message)
    
    def handle_combo_selection_change(self, dummy):
        # update calc data
        print "selChange"
        comboA = self.findChild(QtGui.QWidget,'combo_serA')
        comboB = self.findChild(QtGui.QWidget,'combo_serB')
        self.model.calc_data.update_data(self.model.loaded_data.data, 
            str(comboA.currentText()), str(comboB.currentText()))
    
    def handle_thresh_box_change(self, dummy):
        self.model.summary_data.update_data(self.model.calc_data,        
            self.findChild(QtGui.QWidget,'spb_thr1').value,
            self.findChild(QtGui.QWidget,'spb_thr2').value,
            self.findChild(QtGui.QWidget,'spb_thr3').value)
        
        
        
#==============================================================================
#         self.findChild(QtGui.QTableView,'table_calc_data').setModel(calc_data)
#         axes = self.fig.add_subplot(111)
#         cd.data[cd.data.columns[:-2]].T.plot(kind='bar', ax = axes)
#         axes.legend(ncol=3)
#==============================================================================

        
        
        

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()


    
    
#==============================================================================
#     
# class MyWindow(QWidget):
#     def __init__(self, *args):
#         QWidget.__init__(self, *args)
# 
#         
#         tableview_l = QTableView()
#         tableview_l.setModel(ld)
#         tableview_t = QTableView()
#         tableview_t.setModel(td)
#         tableview_c = QTableView()
#         tableview_c.setModel(cd)
#         
#         lay_l = QHBoxLayout(None)
#         lay_l.addWidget(tableview_l)
#         
#         lay_tc = QHBoxLayout(None) 
#         lay_tc.addWidget(tableview_t)
#         lay_tc.addWidget(tableview_c)
#         
#         layout = QVBoxLayout(None)
#         
#         layout.addWidget(tableview_l)
#         layout.addLayout(lay_tc)
#         self.setLayout(layout)
#==============================================================================

#==============================================================================
# 
# 
# if __name__ == "__main__":
#     main()
#==============================================================================
