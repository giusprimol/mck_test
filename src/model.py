# -*- coding: utf-8 -*-
"""
Model for data being loaded from disk. 
Class deals with data loading and validation.
Also, inherits from DataFrame_QAbstractTableModel so that it can emit signals 
when data is updated
    

@author: giuseppe
"""
from PyQt4.QtCore import Signal,QObject
import os, pandas as pd


test_data = pd.DataFrame(index = ['A','B'], columns = ['2015','2016','2017'], data=[[100,101,102],[99,99,98]])

calc_labels = ['A/(A+B)', 'B/(A+B)', 'A/B'] #row labels for calculated data
threshold_labels = {False:'Basso', True:'Buono'} # labels for threshold comparison result

class loaded_data(QObject):
    loaded_data_changed = Signal()    
    def __init__(self, start_data = None):
        super(loaded_data, self).__init__()        
        self.data = start_data if start_data is not None else pd.DataFrame()
        
    def update_data(self,data):
        self.validate_data(data)
        self.data = data
        self.loaded_data_changed.emit()
        
    def loadfile(self,filename):      
        ext = os.path.splitext(filename)[1]
        if ext in ('.txt','.csv'):
            data = pd.DataFrame.from_csv(filename)
        elif ext in ('*.'):
            data = pd.read_excel(filename,index_col = 0)
        else:
            raise Exception('Estensione file sconosciuta: %s'%ext)
        self.update_data(data)

    def validate_data(self,data):
        if data.shape[1]<2:
            raise Exception('Sono necessarie almeno 2 colonne di dati, il file ne contiene solo %d'%data.shape[1])
        if data.index.duplicated().any():
            raise Exception('Sono presenti serie con nome duplicato: %s'%', '.join(data.index[data.index.duplicated()]))
        if data.shape[0]<2:
            raise Exception('Sono necessarie almeno 2 serie di dati, il file ne contiene solo %d'%data.shape[0])

class calc_data(QObject):
    calc_data_changed = Signal()    
    def __init__(self):
        super(calc_data, self).__init__()       
        self.data = pd.DataFrame()        
        
    def update_data(self, df_loaded_data, idxA, idxB):
        if (df_loaded_data is not None) and (len(df_loaded_data)>0):        
            tmp = pd.DataFrame({'A' : df_loaded_data.ix[idxA], 'B' : df_loaded_data.ix[idxB]}).T
            self.data = pd.DataFrame.from_items([
                (calc_labels[0], tmp.ix['A']/tmp.sum()),
                (calc_labels[1], tmp.ix['B']/tmp.sum()),
                (calc_labels[2], tmp.ix['A']/tmp.ix['B'])]).T
        else:
            self.data = pd.DataFrame()
        self.calc_data_changed.emit()
        
class summary_data(QObject):
    summary_data_changed = Signal()    
    def __init__(self):
        super(summary_data, self).__init__()       
        self.data = pd.DataFrame()        
    def update_data(self,df_calc_data, s_tresh):
        if (df_calc_data is not None) and (len(df_calc_data)>0):
            self.data = pd.DataFrame()
            self.data['CAGR'] = pd.np.power((df_calc_data.ix[:,-1]/df_calc_data.ix[:,0]), 1./(df_calc_data.shape[1]-1))-1
            self.data['Valutazione'] = (self.data.CAGR>s_tresh).map(threshold_labels)
        else:
            self.data = pd.DataFrame()
        self.summary_data_changed.emit()

class thresh_data(QObject):
    thresh_data_changed = Signal()    
    def __init__(self):
        super(thresh_data, self).__init__()       
        self.data = pd.Series(dict(zip(calc_labels,[0,0,0])))
        
    def update_data(self,t1,t2,t3):
        self.data = pd.Series(dict(zip(calc_labels,[t1,t2,t3])))
        self.thresh_data_changed.emit()

class model_data():
    def __init__(self):
        self.loaded_data = loaded_data()
        self.calc_data = calc_data()
        self.thresh_data = thresh_data()
        self.summary_data = summary_data()
