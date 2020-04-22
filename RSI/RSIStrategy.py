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

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None

        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.datas[0], 
            period=self.params.period,
            upperband=self.params.upperband,
            lowerband=self.params.lowerband
        )
        print('Hello world')


    def next(self):
        
         # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            print('Analisando close: {} e rsi: {}'.format(self.dataclose[0], self.rsi[0]))
            if self.rsi >=60:
                self.order = self.sell()
            elif self.rsi <= 40:
                self.order = self.buy()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                print('BUY EXECUTED, Price: %.2f, Cost: %.2f' % (order.executed.price, order.executed.value))

                self.buyprice = order.executed.price
               
            else:  # Sell
                 print('SELL EXECUTED, Price: %.2f, Cost: %.2f' % (order.executed.price, order.executed.value))

            
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print('Order Canceled/Margin/Rejected')

        self.order = None
        print('Setou o order = None')