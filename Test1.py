import numpy as np
import pandas as pd
import matplotlib as plt
from scipy.stats import probplot, t
import statsmodels.api as sm
import sys
sys.path.append(r'D:\OneDrive\My_ML_Trading\LSTM')
import stock_Feat_Eng


class MyClass:
    
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            exec('self.%s = %s' %(k,v))

    def exec_all(self):
        self.get_data()
        self.plots()
    
    def get_data(self):
        S = stock_Feat_Eng.stockDF_Constr(self.ohlc_folder, self.ticker)
        S.exec_all()
        self.stock_DF = S.stock_DF.iloc[-250:]
        self.stock_DF['Prev_Close'] = self.stock_DF['Close'].shift(1)
        self.stock_DF['Return'] = (self.stock_DF['Close']/self.stock_DF['Prev_Close'])-1
        self.stock_DF['Log_Return'] = np.log(1 + self.stock_DF['Return'])

    def plots(self):
        self.stock_DF['Return'].plot(kind='hist', bins=100)
        print('Mean: %f\nSkewness: %f\nKurt: %f' %(self.stock_DF['Return'].mean(), self.stock_DF['Return'].skew(), self.stock_DF['Return'].kurtosis()))
        # probplot(self.stock_DF['Return'].dropna(), dist='norm', fit=True, plot=plt.pyplot)
        # sm.qqplot(self.stock_DF['Return'].dropna(), dist=t, line='s')
        # sm.qqplot(self.stock_DF['Log_Return'].dropna(), dist=t, line='s')

if __name__ == '__main__':
    ohlc_folder = 'D:\OneDrive\Trading\Hist_Data\Stock OHLC'
    ticker = 'HDFC'
    C = MyClass(ohlc_folder="r'%s'"%ohlc_folder, ticker="r'%s'"%ticker)
    C.exec_all()
