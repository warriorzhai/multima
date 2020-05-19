# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:30:43 2019

@author: Administrator
"""

import common.base as base

pair='BTCUSD'
symbol=pair[:3]
teststart='20170716'
testend='20170916'
inittime=base.str_toTimestamp(teststart)
ultra_timeframe='3h'
macro_timeframe='30m'
mid_timeframe='5m'
micro_timeframe='1m'
base_timeframe='1m'
usedb='multimacd_tim'
ultra_timeframe_as_minute=180
macro_timeframe_as_minute=30
micro_timeframe_as_minute=1
mid_timeframe_as_minute=5
ultra_timeframe_minute=0
macro_timeframe_minute=30
micro_timeframe_minute=1
mid_timeframe_minute=5

ultra_timeframe_as_hour=3
macro_timeframe_as_hour=0
mid_timeframe_as_hour=0
micro_timeframe_as_hour=0
base_timeframe_as_minute=1
tftree=['1m','5m','30m','3h']
tfmintree={'1m':1,'5m':5,'30m':30,'3h':180}
tftree=list(tfmintree.keys())
path=r'C:\Users\Administrator.ZX-201608042013\Desktop\mystragedy\ver1.3b'

bollmove_tb='BOLLMOVE'
bollpoint_tb='BOLLLINE'
layer_tb='LAYER'
upline_tb='UPLINE'
uplinetwist_tb='UPLINETWIST'
breaklayer_tb='BREAKLAYER'
breaklayerend_tb='BREAKLAYEREND'
diffcross_tb='DIFFCROSS'
utwist_db='UTWIST'
trend_db='TREND'
trendtd_db='TRENDTD'
transtrendtd_tb='TRANS_TRANDTD'
trendwv_db='TRANS_TRANDWV'
diffdeacross_tb='DIFFDEACROSS'
diffdeadep_tb='DIFFDEADEP'
diffdeafade_tb='DIFFDEAFADE'
bs3_tb='BS3'
bs1_tb='BS1'
bs2_tb='BS2'
bs3macd_tb='BS3MACD'
orders_tb='ORDERS'
resislayer_tb='RESISLAYER'
hspeak_tb='HSPEAK'


targetlayer_db='TARGETLAYER'
bsdowntf_tb='BSDOWNTF'

trend_db='TREND'

sigtb_dict={
       'BOLLMOVE':{
               'trackbollpoint':1.0,
               'track_utwist':1.0
               } ,
       'BOLLLINE':{
               'process_bollline':1.0,
               'tracklayer':1.0,
               'track_expandlayer':1.0,
               'update_layer_breakstatend':1.0,
               'track_trendtd_bs1':1.0,
               'track_trendtd_bs1_downtf':1.0,
               'track_trendtd_bs2':1.0,
               'track_diffdea_depend':1.0,
               'layerposwatch':1.0,
               'track_hspeak':1.0
               },
        'DIFFCROSS':{
               'track_utwist':1.0},
        'DIFFDEAFADE':{
                'track_diffdea_dep':1.0
                },
        'UPLINETWIST':{
                'track_expandlayer':1.0,
                'track_upline_twist':1.0,
                'track_transtrendwave':1.0,
                'track_trandwvupdate':1.0
                },
        'BREAKLAYER':{
                'check_ktwist':1.0,
                'track_transtrendtrend':1.0,
                'update_trendlayer_breakstat':1.0,
                'track_bs3':1.0,
                'update_layerrealstat':1.0,
                'track_macd_bs3':1.0
                },
        'BREAKLAYEREND':{'STH':1.0},
        'BS1':{
                'track_transtrendwave':1.0,
                'handle_bs1':1.0
                },
        'BS2':{
                'track_trandwvupdate':1.0,
                'handle_bs2':1.0
                },

        'BSDOWNTF':{
                'track_trendtd_bs1':1.0,
                'track_trendtd_bs2':1.0
                },
        'BS3':{
                'track_transtrendtrend':1.0,
                'track_trendtd_bs2':1.0,
                'track_transtrendwave':1.0,
                'track_trandwvupdate':1.0,
                'track_upline_twist':1.0,
                'track_diffdea_depend':1.0
                },
        'BS3MACD':{
                'track_transtrendtrend':1.0,
                'track_trendtd_bs2':1.0,
                'track_transtrendwave':1.0,
                'track_trandwvupdate':1.0
                },
        'TRANS_TRANDTD':{
                'build_trendtd':1.0
                },
        'DIFFDEACROSS':{
                'track_trendtd_bs1':1.0,
                'track_diffdea_dep':1.0,
                'track_trandwv_bs':1.0,
                'track_diffdea_depend':1.0,
                'track_macd_bs3':1.0
                },
        'DIFFDEADEP':{
                'track_trendtd_bs1':1.0,
                'track_trandwv_bs':1.0
                },
        'TARGETLAYER':{'handle_wavetargetlayer':1.0},
#        'RESISLAYER':{
#                'handle_bs2':1.0
#                }
        'UPLINE':
            {
                'STH':1.0
                },
        'LAYER':{
                'STH':1.0
                }
            
        
        }