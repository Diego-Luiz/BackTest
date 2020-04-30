from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

class strategy(bt.Strategy):
    params = (
        ('period', 2)
    )
    def __init__(self):
        self.data = self.datas[0]
        self.sma = bt.ind.SMA(self.data[0], period=self.p.period)
        

if __name__ == "__main__":
    cerebro = bt.Cerebro()

    datapath = 'MSFT.csv'
    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        fromdate = datetime.datetime(2019,10,21),
        todate = datetime.datetime(2020,3,23),
        
        dtformat = ('%Y-%m-%d'),
        nullvalue = 0.0,
        datetime = 0,
        open = 1,
        high = 2,
        low = 3,
        close = 4,
        volume = 6,
        openinterest = -1
    )

    cerebro.adddata(data)
    cerebro.addstrategy(strategy)

    cerebro.broker.setcash(10000.0)
    print('Initial value: %.2f' % cerebro.broker.get_value())
    cerebro.run()
    print('Final value: %.2f' % cerebro.broker.get_value())
