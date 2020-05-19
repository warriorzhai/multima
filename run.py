# -*- coding: utf-8 -*-
"""
Created on Mon May 18 18:13:02 2020

@author: nantypeobject
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:50:52 2020

@author: nantypeobject
"""













import pandas as pd
import math
from okex import Okex
import time


'''
/*backtest
start: 2016-01-30        
end: 2016-12-30           
period: 1440
periodBase: 60
mode: 0                 
*/
'''
import datetime



def get_ma(line,span):
    line=pd.Series(line)
    return line.rolling(span).mean()

def get_ema(line,span):
    line=pd.Series(line)
    return line.ewm(span=span,min_periods=0,adjust=False,ignore_na=False).mean()

def kline_smoothing(line,method,span):
    ma_funcs={'ema':get_ema,'ma':get_ma}
    return ma_funcs[method](line,span)

class Trader:
    def __init__(self,apikey,secretkey,passphrase,symbol,currency):

        self.position = 0
        self.isPending = False
        self.lasttime=datetime.datetime.now()
        self.macd_winlen1=144
        self.macd_winlen2=89
        self.macd_winlen3=21
        self.macd_method1='ma'
        self.macd_method2='ema'
        self.macd_method3='ma'
        self.currency=currency
        self.symbol=symbol
        self.minbal=500
        self.margin=3
        self.stoprate=5.0
        self.okex=Okex(apikey,secretkey,passphrase,'1')
#        self.okex.set_leverage(self.symbol,self.currency,self.margin,'long')
#        self.okex.set_leverage(self.symbol,self.currency,self.margin,'short')

    def set_order(self,symbol,side,price,hands):

        odinfo=self.okex.place_order(self.symbol,
                              side, None,hands,match_price='0',order_type='4')
        time.sleep(30)
        self.check_orderdone(symbol,odinfo['order_id'])
#        depth = exchange.GetDepth()
#        if side  in ('buy','closesell'):
#            depthdf=pd.DataFrame(depth["Asks"])
#        else:
#            depthdf=pd.DataFrame(depth["Bids"])
#        Log(depthdf)
#        amtcumsum=depthdf['Amount'].cumsum()
#        validprice=depthdf['Price'][(amtcumsum>=hands)]
#        if validprice.empty:
#            Log('深度不足')
#            price=depthdf['Price'].iloc[-1]*0.9
#        else:
#            price=validprice.iloc[-1]
#        exchange.SetContractType("quarter")
#        exchange.SetMarginLevel(10)
#        exchange.SetDirection(side)
#        if side in ('buy','closesell'):
#            exchange.Buy(price,hands)
#        else:
#            exchange.Sell(price,hands)

    def check_capvalable(self,acctbal):

        if acctbal<=self.minbal:
            raise('账户资金小于设定开仓本金')
        #if int_money==0:
        #    int_money=accont.Stocks*price
        #if int_money<cap:
        #    raise('账户资金小于设定开仓本金')
        
    def onBuySig(self,price):
        price=float(price)
        position = self.okex.position(self.symbol)
        accont=float(self.okex.futures_account(self.currency)['equity'])
     
        if 'USD' in self.currency:
            hands=math.floor(accont/100.0)
        else:
            hands=math.floor((accont*price)/100.0)
        
        if float(position["long_qty"])+float(position["short_qty"])> 0:
            if float(position["short_avail_qty"])>0:
                print('当前做空，买入平仓，开仓做多'+str(position["short_avail_qty"]))
                closehands=float(position["short_avail_qty"])
                self.set_order(self.symbol, '4', price, closehands)

                self.set_order(self.symbol, '1',price,hands)
            print('当前多仓，不处理')
        else:
            print('当前无仓位，开仓做多')
            self.check_capvalable(accont)
            self.set_order(self.symbol, '1',price,hands)
            
    def onSellSig(self,price):
        position = self.okex.position(self.symbol)
        accont=self.okex.futures_account(self.currency)['equity']
        price=float(price)
        if self.currency[:3]=='USD':
            hands=math.floor(accont/100.0)
        else:
            hands=math.floor((accont*price)/100.0)
        
        if float(position["long_qty"])+float(position["short_qty"]) > 0:
            if float(position["long_avail_qty"])>0:
                print('当前做多，卖出平仓，开仓做空'+str(position["long_avail_qty"]))
                closehands=float(position["long_avail_qty"])
                self.set_order(self.symbol, '3', price, closehands)
#                if len(exchange.GetPosition())>0:
#                    Log(exchange.GetPosition())
#                    Log('平仓失败')
#                    assert False,'平仓失败'
                self.set_order(self.symbol, '2', price, hands)
        else:
            print('当前无仓位，开仓做空')
            self.check_capvalable(accont)
            self.set_order(self.symbol, '2', price, hands)
            
    def check_stop(self,price,ask,bid,stoprate):
        position = self.okex.position(self.symbol)
        stoprate=self.stoprate/100.0
        price=float(price)
        if float(position["long_qty"])+float(position["short_qty"]) > 0:
        
            if (float(position["long_avail_qty"])>0 and price<float(position['long_avg_cost'])*(1-stoprate)):
                closehands=float(position["long_avail_qty"])
                self.set_order(self.symbol, '3', price, closehands)
                print('多仓止损')
                return
                
            if (float(position["short_avail_qty"])>0 and price>float(position['short_avg_cost'])*(1+stoprate)):
             
                closehands=float(position["short_avail_qty"])
                self.set_order(self.symbol, '4',price, closehands)
                print('空仓止损')
                return 
            if float(position["long_avail_qty"])>0:
                print('当前仓位方向=做多'+',仓位大小'+position["long_avail_qty"]+',均价='+position['long_avg_cost']+',盈利='+position['long_pnl_ratio'])
            else:
                print('当前仓位方向=做空'+',仓位大小'+position["short_avail_qty"]+',均价='+position['short_avg_cost']+',盈利='+position['short_pnl_ratio'])
        else:
            print(datetime.datetime.now(),'非整点未开仓')
               
    def check_orderdone(self,symbol,orderid):
        odinfo=self.okex.get_order_details(orderid, symbol)
        if int(odinfo['status'])>0 and odinfo['status']!='2':
            self.okex.cancel_order(orderid, symbol)
            
    
    def onTick(self):
        
        nowtime=datetime.datetime.now()
        ishour=(nowtime.hour!=self.lasttime.hour)
        ticker = self.okex.get_ticker(self.symbol)
        #整的小时，进行信号计算；否则计算止损
        if ishour:
            print ('整点时间',self.lasttime,nowtime)
            self.lasttime=nowtime
            
            records1 = self.okex.get_candles(self.symbol,granularity=60*60).sort_values('time')
            records2 = self.okex.get_candles(self.symbol,granularity=60*60*4).sort_values('time')
            records3 = self.okex.get_candles(self.symbol,granularity=60*60*24).sort_values('time')
            
            if (records1.shape[0])<self.macd_winlen1:                
                return
            if (records2.shape[0])<self.macd_winlen2:
                return
            if (records3.shape[0])<self.macd_winlen3:
                return
        
            close1=records1["close"].astype(float)
            close2=records2["close"].astype(float)
            close3=records3["close"].astype(float)
            
            ma0=close1.iloc[-1]
            ma1 = kline_smoothing(close1,self.macd_method1,self.macd_winlen1).iloc[-1]
            ma2 = kline_smoothing(close2,self.macd_method2,self.macd_winlen2).iloc[-1]
            ma3 = kline_smoothing(close3,self.macd_method3,self.macd_winlen3).iloc[-1]
            print ('三ma',ma0,ma1,ma2,ma3)
            #Log(str(ma0)+'_'+str(ma1)+'_'+str(ma2)+'_'+str(ma3))
            if ma0>ma1 and ma0>ma2 and ma0>ma3:
                print('买入信号'+str(ma0)+'_'+str(ma1)+'_'+str(ma2)+'_'+str(ma3))
                self.onBuySig(ticker['best_ask'])
            else:
                if ma0<ma1 and ma1<ma2:
                    print('卖出信号')
                    self.onSellSig(ticker['best_bid'])
        else:
            self.check_stop(ticker['last'],ticker['best_ask'],ticker['best_bid'],5) 
            
                  

'''def main():
    q = ext.NewTaskQueue()
    Log(_C(exchange.GetAccount))
    tasks = []
    for symbol in ContractList.split(','):
        tasks.append(Trader(q, symbol.strip()))
    while True:
        if exchange.IO("status"):
            for t in tasks:
                t.onTick()
            q.poll()
            Sleep(1000)'''
def main():
    apikey = ""
    secretkey = ""
    passphrase=""
    symbol,currency='BTC-USDT-200626','BTC-USDT'
    print('公主陛下你的你的男朋友2号小鹿鹿上线了..')
    t=Trader(apikey,secretkey,passphrase,symbol,currency)
    while True:
        t.onTick()
        time.sleep(5)

if __name__ == '__main__':
    main()

