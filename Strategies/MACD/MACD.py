import datetime
import os.path
import sys
import math
import backtrader as bt

class MACDStrategy(bt.Strategy):
    params = (
        ('period_me1',12),
        ('period_me2',26),
        ('period_signal',9)
    )
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None

        
        self.macd = bt.indicators.MACD(
            self.dataclose,
            period_me2 = self.params.period_me2, 
            period_me1 = self.params.period_me1, 
            period_signal = self.params.period_signal
        )
        #Esse indicardo CrossOver vai verficar quando o macd cruzou com o signal. Ai dependendo se cruzou indo pra baixo ou indo pra cima
        self.macdsig = bt.ind.CrossOver(self.macd.macd, self.macd.signal)
    
    def next(self):
        if self.order:
            return
        # print('Next, self.signal?: {}'.format(self.signal[0]))
        if (self.macdsig[0] > 0 ):
            print('BUY ?')
            self.order = self.buy()
        else:
            print('SELL ?')
            self.order = self.sell()
       

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
