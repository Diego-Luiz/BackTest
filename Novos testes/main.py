import os,sys, argparse
import pandas as pd
import backtrader as bt

from GoldenCross import GoldenCross

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

spy_prices = pd.read_csv('oracle.csv', index_col='Date', parse_dates=True)

feed = bt.feeds.PandasData(dataname=spy_prices)

cerebro.adddata(feed)
cerebro.addstrategy(GoldenCross)  
print('Initial portfolio value: ', cerebro.broker.getvalue())
cerebro.run()    
print('Final portfolio value: ', cerebro.broker.getvalue())
cerebro.plot()