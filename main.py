
import datetime
import os.path
import sys

import backtrader as bt
from Strategies.RSI.RSIStrategy import RSIStrategy
from Strategies.MACD.MACD import MACDStrategy

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    
    data = bt.feeds.GenericCSVData(
        dataname = './/Datas//oracle.csv',
        fromdate = datetime.datetime(1995, 1, 3),
        todate = datetime.datetime(2014, 12, 31),
        nullvalue=0.0,

        dtformat=('%Y-%m-%d'),

        datetime = 0,
        high = 2,
        low = 3,
        open = 1,
        close = 4,
        volume = 6,
        openinterest=-1
    )

    # data = bt.feeds.YahooFinanceCSVData(dataname=".//Datas//MSFT.csv")

    cerebro.adddata(data)
    cerebro.broker.set_cash(5000.0)
    cerebro.addstrategy(MACDStrategy)

    print('Initial value: %.2f' % cerebro.broker.get_value())
    cerebro.run()
    print('Final value: %.2f' % cerebro.broker.get_value())
    cerebro.plot()
    
