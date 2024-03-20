# Small config
MID_CONFIG = {
    "SCOUT_TRIGGER_1": 10000000,
    "SCOUT_TRIGGER_2": 40000000,
    "SCOUT_TRIGGER_3": 80000000,
    "TRIGGER_1": 30000000,
    "TRIGGER_2": 70000000,
    "TRIGGER_3": 100000000,
    "CANCEL_1": 180000000,
    "CANCEL_2": 150000000,
    "CANCEL_3": 130000000,
    "CANCEL_LARGE_1": 350000000,
    "CANCEL_LARGE_2": 330000000,
    "CANCEL_LARGE_3": 300000000,
}

LARGE_CONFIG = {
    "SCOUT_TRIGGER_1": 70000000,
    "SCOUT_TRIGGER_2": 140000000,
    "SCOUT_TRIGGER_3": 200000000,
    "TRIGGER_1": 100000000,
    "TRIGGER_2": 200000000,
    "TRIGGER_3": 300000000,
    "CANCEL_1": 550000000,
    "CANCEL_2": 500000000,
    "CANCEL_3": 450000000,
    "CANCEL_LARGE_1": 800000000,
    "CANCEL_LARGE_2": 700000000,
    "CANCEL_LARGE_3": 650000000
}


ROW_TEMPLETE = { 
                "SecurityID": 000000,
                "ExchangeID": 0,
                "BuyTriggerVolume": 0,
                "CancelVolume":0,
                "Position":10000, # 元
                "MaxTriggerTimes": 3,
                "LowerTimeLimit": 2000000000,
                "ScoutBuyTriggerCashLim": 0,
                "ScoutMonitorDuration" : 600000000000, 
                "Cond2Percent" : -0.35,
                "Cond2HighTime": 180000000000,
                "Cond2TrackDuration": 3000000000,
                "CancelTriggerVolumeLarge": 0 ,
                "Cond4LowTime": 4000000000,
                "Cond4HighTime": 600000000000
              }
