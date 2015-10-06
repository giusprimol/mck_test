# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 21:28:15 2015

@author: giuseppe
"""

import pandas as pd
import model,sys

from pandas.sandbox.qtpandas import DataFrameModel, DataFrameWidget
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


test_data = pd.DataFrame(index = ['A','B'], columns = ['2015','2016','2017'], data=[[100,101,102],[99,99,98]])
ld = model.loaded_data_model(test_data)
td = model.thresh_data_model()
cd = model.calc_data_model(ld,td)

from PyQt4 import QtCore, QtGui, uic
 
form_class = uic.loadUiType("mainWin.ui")[0]                 # Load the UI
 
class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, loaded_data, calc_data, thresh_data, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.fig = Figure()#(2.0, 4.0), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.findChild(QtGui.QWidget,'widget_plot'))        
        self.findChild(QtGui.QTableView,'table_calc_data').setModel(calc_data)
        axes = self.fig.add_subplot(111)
        cd.data[cd.data.columns[:-2]].T.plot(kind='bar', ax = axes)
        axes.legend(ncol=3)

        
        
        

app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(ld,cd,td,None)
myWindow.show()
app.exec_()






def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    #sys.exit(app.exec_())
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
