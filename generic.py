import os, json
from time import sleep
from dhanhq import dhanhq
from datetime import datetime

generic_directory = os.path.dirname(os.path.abspath(__file__))
generic_script_name = os.path.splitext(os.path.basename(__file__))[0]
generic_logTime = datetime.now().strftime("%d%m%Y%H%M%S")

with open(rf"{generic_directory}\userDetails.json","r") as config:
    userDetails = json.load(config)
dataClient = userDetails.get('dataClient')
isPrintEnabled = userDetails.get('enablePrint')
sleepTime = userDetails.get('sleepTime')
trade = userDetails.get('trade')
lotSize = userDetails.get('lotSize')

dhan = dhanhq(dataClient[0]['clientId'],dataClient[0]['accessToken'])

def genericLog(text):
    with open(rf"{generic_directory}\logs\{generic_script_name}_{generic_logTime}.log","a") as log:
        log.write(f"{datetime.now()} - {text}\n")
        log.write(f"\n")

def indexOpenPrice(security_id, nickname):
    global sleepTime
    genericLog("#################################################################################################################################################")
    genericLog(rf"Security Id --> {security_id}")
    openPrice = None
    while True:
        try:
            liveIndexPrice = dhan.intraday_daily_minute_charts(
                security_id = f"{security_id}",
                exchange_segment = 'IDX_I',
                instrument_type = 'INDEX'
            )
            openPrice = liveIndexPrice['data']['open'][0]
            #openPrice = liveIndexPrice
            genericLog(f"indexOpenPrice() --> {nickname} opened at --> {openPrice}")
            return openPrice
        except Exception as e:
            if isPrintEnabled.lower() == "true":
                genericLog(rf"indexOpenPrice() --> Error while calling API, will attempt again..")
                genericLog(e)
            sleep(sleepTime)

def securityDetails():
    current_datetime = datetime.now()
    weekday_number = current_datetime.weekday()
    weekday_name = current_datetime.strftime("%A")

    if weekday_number == 0:
        security_id = 442
        strikePriceGap = 25
        nickname = "MIDCPNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 75
        quantity = lotSize * unit
        genericLog(rf"quantity entered by user --> {lotSize} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 1:
        security_id = 27
        strikePriceGap = 50
        nickname = "FINNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 40
        quantity = lotSize * unit
        genericLog(rf"quantity entered by user --> {lotSize} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 2:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        quantity = lotSize * unit
        genericLog(rf"quantity entered by user --> {lotSize} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 3:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 50
        quantity = lotSize * unit
        genericLog(rf"quantity entered by user --> {lotSize} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 4:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = lotSize * unit
        genericLog(rf"quantity entered by user --> {lotSize} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    else:
        genericLog("Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = lotSize * unit

    return [security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity]
