import datetime
import os.path
import sys
import math
import backtrader as bt


class RSIStrategy(bt.Strategy):
    params = (
        ('period', 14),
        ('upperband', 70),
        ('lowerband', 30)
    )

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.order = None
        self.rsi = bt.indicators.RelativeStrengthIndex(
            self.dataclose, 
            period=self.params.period,
            upperband= self.params.upperband,
            lowerband = self.params.lowerband
        )
        
    def next(self):
        if self.order:
            return
        
        else:   
            if self.position.size == 0: #se a quantidade de ações for 0
                if self.rsi[0] < self.params.lowerband: # e o RSI for menor que 30, entao compra
                    amount_to_invest = (0.50 * self.broker.cash) #vai investir 50% do dinheiro q tem no broker
                    self.size = math.floor(amount_to_invest/self.dataclose[0]) #quantidade de ações que vao ser compradas de acordo com o dinheiro e o preço de fechamento 
                    self.order = self.buy(size=self.size) 

            if self.position.size > 0: #se a quantidade de ações for MAIOR que 0
                if self.rsi[0] > self.params.upperband: # e o RSI for maior que 70, entao vende
                    self.order = self.sell(size=self.position.size)

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
        