# -*- coding: utf-8 -*-
"""
Created on Mon Oct 05 22:31:39 2015

Model file: collects the data items


@author: giuseppe
"""
import pandas as pd
from PyQt4.QtCore import QAbstractTableModel,QVariant, Qt


calc_labels = ['A/(A+B)', 'B/(A+B)', 'A/B'] #row labels for calculated data
threshold_labels = {False:'Basso', True:'Buono'} # labels for threshold comparison result

#loaded_data = pd.DataFrame(index = ['A','B'], columns = ['2015','2016','2017'], 
#    data=[[100,101,102],[99,99,98]])

class DataFrame_QAbstractTableModel(QAbstractTableModel):
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.data = pd.DataFrame()
    def rowCount(self, parent): return self.data.shape[0]
    def columnCount(self, parent): return self.data.shape[1]
    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return str(self.data.ix[index.row()][index.column()])
    def headerData(self, section, orientation,role) :  
        if (role == Qt.DisplayRole):  
            if (orientation == Qt.Horizontal):  
                return self.data.columns[section]
            elif (orientation == Qt.Vertical):                   
                return self.data.index[section]
        return None


class loaded_data_model(DataFrame_QAbstractTableModel):
    def __init__(self, start_data = None,parent=None, *args):
        DataFrame_QAbstractTableModel.__init__(self, parent, *args)
        self.data = start_data

class thresh_data_model(DataFrame_QAbstractTableModel):
    def __init__(self, parent=None, *args):
        DataFrame_QAbstractTableModel.__init__(self, parent, *args)
        self.data = pd.DataFrame(index = calc_labels, columns = ['thr'], data = [0.01, 0.0, 0.01])

class calc_data_model(DataFrame_QAbstractTableModel):
    def __init__(self, loaded, thresh, parent=None, *args):
        DataFrame_QAbstractTableModel.__init__(self, parent, *args)
        self.loaded = loaded
        self.thresh = thresh
        self.update_data()
    def update_data(self):
        """
        transforms loaded_data in calc_data if possible, otherwise returns None
        """
        if self.loaded.data is not None:
            res = pd.DataFrame.from_items([
                (calc_labels[0], self.loaded.data.ix['A']/self.loaded.data.sum()),
                (calc_labels[1], self.loaded.data.ix['B']/self.loaded.data.sum()),
                (calc_labels[2], self.loaded.data.ix['A']/self.loaded.data.ix['B'])]).T
            res['CAGR'] = pd.np.power((res.ix[:,-1]/res.ix[:,0]), 1./(self.loaded.data.shape[1]-1))-1
            res['Valutazione'] = (res.CAGR>self.thresh.data.thr).map(threshold_labels)
            self.data = res
        else:
            self.data = pd.DataFrame()

 