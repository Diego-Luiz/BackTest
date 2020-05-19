import datetime
import os.path
import sys
import math
import backtrader as bt

class MACDStrategy(bt.Strategy):
    params = (
        ('period_me1',50),
        ('period_me2',200),
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
        self.crossMacdSignal = bt.indicators.CrossOver(self.macd, self.macd.signal)
   
    def next(self):
        if self.order:
            return

        if self.crossMacdSignal[0] == 1.0: #quer dizer que o MACD cruzou o signal pra cima
            self.order = self.sell(size = self.position.size) #vende tudo
        elif self.crossMacdSignal[0] == -1.0: #MACD cruzou com signal para baixo
            amount_to_invest = (0.50 * self.broker.cash) #vai investir 50% do dinheiro q tem no broker
            self.size = math.floor(amount_to_invest/self.dataclose[0]) #quantidade de ações que vao ser compradas de acordo com o dinheiro e o preço de fechamento 
            self.order = self.buy(size = self.size) #compra self.size qtd de ações
        
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
