import math
import backtrader as bt

class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), ('order_percentage', 0.95), ('ticker', 'SPY'))

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.p.fast, plotname='50 day moving average'
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.p.slow, plotname='200 day moving average'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average,self.slow_moving_average)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.p.order_percentage * self.broker.cash)#dinheiro a ser investido
                self.size = math.floor(amount_to_invest/self.data.close)#quantidade de ações que vao ser compradas de acordo com o dinheiro e o preço de fechamento 

                print('Buy {} shares of {} at {}'.format(self.size,self.p.ticker, self.data.close[0]))

                self.buy(size=self.size)  #compre 'size' ações
            
        if self.position.size > 0:
            if self.crossover < 0:
                print('Sell {} shares of {} at {}'.format(self.size,self.p.ticker, self.data.close[0])) 
                self.close()   