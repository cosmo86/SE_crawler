# Small config
MID_CONFIG = {
    "SCOUT_TRIGGER_1": 1000,
    "SCOUT_TRIGGER_2": 4000,
    "SCOUT_TRIGGER_3": 8000,
    "TRIGGER_1": 3000,
    "TRIGGER_2": 7000,
    "TRIGGER_3": 10000,
    "CANCEL_1": 18000,
    "CANCEL_2": 15000,
    "CANCEL_3": 13000,
    "CANCEL_LARGE_1": 35000,
    "CANCEL_LARGE_2": 33000,
    "CANCEL_LARGE_3": 30000,
}

LARGE_CONFIG = {
    "SCOUT_TRIGGER_1": 7000,
    "SCOUT_TRIGGER_2": 14000,
    "SCOUT_TRIGGER_3": 20000,
    "TRIGGER_1": 10000,
    "TRIGGER_2": 20000,
    "TRIGGER_3": 30000,
    "CANCEL_1": 55000,
    "CANCEL_2": 50000,
    "CANCEL_3": 45000,
    "CANCEL_LARGE_1": 80000,
    "CANCEL_LARGE_2": 70000,
    "CANCEL_LARGE_3": 65000
}


ROW_TEMPLETE = { 
                "SecurityID": 000000,
                "ExchangeID": 0,
                "BuyTriggerVolume": 0,
                "CancelVolume":0,
                "Position":10,
                "MaxTriggerTimes": 3,
                "LowerTimeLimit": 0,
                "ScoutBuyTriggerCashLim": 0,
                "ScoutMonitorDuration" : 600000000000, 
                "Cond2Percent" : -0.35,
                "Cond2HighTime": 180000000000,
                "Cond2TrackDuration": 3000000000,
                "CancelTriggerVolumeLarge": 0 ,
                "Cond4LowTime": 4000000000,
                "Cond4HighTime": 600000000000
              }