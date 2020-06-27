
import datetime
import os.path
import sys

import backtrader as bt

from Strategies.RSI.RSIStrategy import RSIStrategy
from Strategies.MACD.MACD import MACDStrategy
from Strategies.SMA.SMAStrategy import SMAStrategy

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    
    # data = bt.feeds.GenericCSVData(
    #     dataname = './/Datas//oracle.csv',
    #     fromdate = datetime.datetime(1995, 1, 3),
    #     todate = datetime.datetime(2014, 12, 31),
    #     nullvalue=0.0,

    #     dtformat=('%Y-%m-%d'),

    #     datetime = 0,
    #     high = 2,
    #     low = 3,
    #     open = 1,
    #     close = 4,
    #     volume = 6,
    #     openinterest=-1
    # )

    # data = bt.feeds.YahooFinanceCSVData(dataname=".//Datas//MSFT.csv")
    nomeEmpresa = "Lojas Renner"
    data = bt.feeds.YahooFinanceCSVData(dataname = ".//Datas//Lojas Renner//Frequencia5anosdaily//LREN3.SA.csv")
    

    cerebro.adddata(data)
    
    #RSI
    cerebro.broker.set_cash(5000.0)
    cerebro.addstrategy(RSIStrategy)
    print('Initial value: %.2f' % cerebro.broker.get_value())
    retorno = cerebro.run()
    print('Final value: %.2f' % cerebro.broker.get_value())

    #MACD
    cerebro.broker.set_cash(5000.0)
    cerebro.addstrategy(MACDStrategy)
    print('Initial value: %.2f' % cerebro.broker.get_value())
    retorno = cerebro.run()
    print('Final value: %.2f' % cerebro.broker.get_value())

    #SMA
    cerebro.broker.set_cash(5000.0)
    cerebro.addstrategy(SMAStrategy)
    print('Initial value: %.2f' % cerebro.broker.get_value())
    retorno = cerebro.run()
    print('Final value: %.2f' % cerebro.broker.get_value())
    
    arquivo = open('Resultados.txt','a+')

    legenda = "     Legenda\nC: Compra       V: Venda\nURSI: Ultima operacao RSI   ARSI atual: RSI atual\nUMACD: Ultima operacao MACD  AMACD: MACD atual\nUSMA: Ultima operacao SMA    ASMA: SMA atual\nS: Sugestão\n"
    print(legenda)
    arquivo.writelines(legenda)

    dictionary = { 'URSI':retorno[0].lastRSI, 'ARSI':round(retorno[0].rsi[0],2),
                   'UMACD':retorno[1].lastMACD, 'AMACD': retorno[1].crossMacdSignal[0],
                   'USMA':retorno[2].lastSMA, 'ASMA':retorno[2].crossMedias[0]
                 }
    decision_dictt = {'V':0, 'C':0}

    # Preenchendo os valores dos indices do dicionário de decisao (compra ou venda), de acordo com os valores retornados pelas estratégias 
    decision_dictt[dictionary['URSI']] += 1
    decision_dictt[dictionary['UMACD']] += 1
    decision_dictt[dictionary['USMA']] += 1

    if dictionary['ARSI'] >= 70.0:
        decision_dictt['V'] += 1
    elif dictionary['ARSI'] <= 30.0:
        decision_dictt['C'] += 1
    
    if dictionary['AMACD'] == 1.0:
        decision_dictt['V'] += 1
    elif dictionary['AMACD'] == -1.0:
        decision_dictt['C'] += 1

    if dictionary['ASMA'] == -1.0:
        decision_dictt['V'] += 1
    elif dictionary['ASMA'] == 1.0:
        decision_dictt['C'] += 1

    decision_dictt_true = sorted(decision_dictt) #ordenando de forma q a chave('V' ou 'C') com maior resultado fique na ultima posicao 
    
    stringtowrite1 = []
    stringtowrite2 = []
    
    for i in dictionary:
        stringtowrite1.append('|{}|'.format(i)+" ")
        stringtowrite2.append(str(dictionary[i]) +"      ")

    stringtowrite1.append('     |{}|'.format('S')+" ")
    stringtowrite2.append((decision_dictt_true[len(decision_dictt_true)-1]) +"      ")

    stringtowrite1.append('\n')
    stringtowrite2.append('\n')
    
    for i in stringtowrite1:
        print(i,end="")
    for i in stringtowrite2:
        print(i,end="")
    
    arquivo.write("\n\n     Resultados\nEmpresa: {}\n".format(nomeEmpresa))     
    arquivo.writelines(stringtowrite1)   
    arquivo.writelines(stringtowrite2)
    arquivo.write("\n\n")
    cerebro.plot(style='candlesticks')
    
