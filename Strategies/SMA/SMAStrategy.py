import datetime
import os.path
import sys
import math
import backtrader as bt


class SMAStrategy(bt.Strategy):
    params=(
        ('period1',50), #media curta
        ('period2',200)  #media longa
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.lastSMA = None
        self.smacurta = bt.indicators.MovingAverageSimple(
            self.dataclose,
            period=self.params.period1,
            plotname= 'SMA curta'
        )
        self.smalonga = bt.indicators.MovingAverageSimple(
            self.dataclose,
            period=self.params.period2,
            plotname = 'SMA longa'
            
        )
        self.crossMedias = bt.indicators.CrossOver(self.smacurta, self.smalonga)
    
    def next(self):
        if self.order:
            return
        
        if self.position.size > 0 and self.crossMedias[0] == -1.0: #se tem ações e se da para comprar
            self.order = self.sell()
            self.lastSMA = 'V'
        elif self.crossMedias[0] == 1.0: #se der para comprar
            self.order = self.buy()
            self.lastSMA = 'C'

    def notify_order(self,order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                print(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                print('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print('Order Canceled/Margin/Rejected')

        self.order = None
        
    