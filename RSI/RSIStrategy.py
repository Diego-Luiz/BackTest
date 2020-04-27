import datetime
import os.path
import sys
import backtrader as bt


class RSIStrategyy(bt.Strategy):
    params = (
        ('period', 14),
        ('upperband', 70.0),
        ('lowerband', 30.0)
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.dataclose, 
            period=self.params.period
        )
        print('Hello world')


    def next(self):
        if self.order:
            return
        else:
            if self.rsi[0] >=71.0 and self.rsi[0]<=74.0:
                # self.order = self.sell(size=20)
                self.order = self.sell()
            elif self.rsi[0] <= 30.0:
                # self.order = self.buy(size=1000)
                self.order = self.buy()

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
        print('Self.order = {}'.format(self.order))