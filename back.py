from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import os.path
import sys

import backtrader as bt

class Test(bt.Strategy):
    params = (
        ('period', 5),
    )

    def __init__(self):
        self.data = self.datas[0]
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # Add SimpleMovingAverage indicator for use in the trading strategy
        self.sma = bt.indicators.SMA(self.data[0],period=self.p.period)
        
    def log(self,txt,dt=None):
        dt= dt or self.data.datetime.date(0)
        print('%s %s' % (dt.isoformat(), txt))
    
    def next(self):
        self.log('Close, %.2f' % self.data.close[0])
        if self.order:
            return 
    
        if not self.position:
            # Not yet ... we MIGHT BUY if ...
            if self.data.close[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.data.close[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()       

        else:
            if self.data.close[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def notify_order(self,order):           
        if order.status in [order.Submitted, order.Accepted]: #se a ordem foi submetida para o broker ou foi aceita pelo broker
            return
        
        if order.status in [order.Completed]: #se a ordem foi completamente executada pelo broker
            if order.isbuy():
                self.log('Buy executed, Price: %.2f, Cost: %.2f, Comm: %.2f' % (order.executed.price, order.executed.value, order.executed.comm) )
                self.buyprice = order.executed.price
                self.comm = order.executed.comm

            else:
                self.log('Sell executed, Price: %.2f, Cost: %.2f, Comm: %.2f' % (order.executed.price, order.executed.value, order.executed.comm) )

            self.bar_executed = len(self)
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' % (trade.pnl, trade.pnlcomm))

if __name__ == "__main__":
    cerebro = bt.Cerebro()

    datapath = 'MSFT.csv'
    data = bt.feeds.GenericCSVData(
        dataname = datapath,
        fromdate = datetime.datetime(2019,8,21),
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
    cerebro.addstrategy(Test)
    cerebro.broker.set_cash(100000.0)

    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    # Set the commission - 0.1% ... divide by 100 to remove the %
    cerebro.broker.setcommission(commission=0.0)
    
    print('Initial value: %.2f' % cerebro.broker.get_value())
    cerebro.run()
    print('Final value: %.2f' % cerebro.broker.get_value())
    # cerebro.plot()