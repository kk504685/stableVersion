import os, json
from time import sleep
from dhanhq import dhanhq
from datetime import datetime

generic_directory = os.path.dirname(os.path.abspath(__file__))
generic_script_name = os.path.splitext(os.path.basename(__file__))[0]
generic_logTime = datetime.now().strftime("%d%m%Y%H%M%S")

def userDetailsJson():
    with open(rf"{generic_directory}\userDetails.json","r") as config:
        userDetails = json.load(config)

    clientId = userDetails.get('clientId')
    accessToken = userDetails.get('accessToken')
    processStartTime = userDetails.get('processStartTime')
    processStartTimeHour = int(processStartTime[0:2])
    processStartTimeMinute = int(processStartTime[3:5])
    currentTimeHour = datetime.now().hour
    currentTimeMinute = datetime.now().minute
    lotSize = userDetails.get('lotSize')
    clientIdToPlaceOrder = userDetails.get('clientIdToPlaceOrder')
    accessTokenToPlaceOrder = userDetails.get('accessTokenToPlaceOrder')
    sleepTime = userDetails.get('sleepTime')
    instrumentToTrade = userDetails.get('instrumentToTrade')
    isPrintEnabled = userDetails.get('enablePrint')
    tradeLimitPerInstrument = userDetails.get('tradeLimitPerInstrument')
    email = userDetails.get('email')
    emailSender = email['emailSender']
    emailReceiver = email['emailReceiver']
    emailPassword = email['emailPassword']
    emailTimeInterval = email['emailTimeInterval']
    subject = email['subject']
    dataClient = userDetails.get('dataClient')
    orderClient = userDetails.get('orderClient')
    downLoad = userDetails.get('downLoad')

    return {
        "clientId" : clientId, "accessToken" : accessToken, "processStartTime" : processStartTime, "processStartTimeHour" : processStartTimeHour,
        "processStartTimeMinute" : processStartTimeMinute, "currentTimeHour" : currentTimeHour, "currentTimeMinute" : currentTimeMinute, "lotSize" : lotSize,
        "clientIdToPlaceOrder" : clientIdToPlaceOrder,"accessTokenToPlaceOrder" : accessTokenToPlaceOrder, "sleepTime" : sleepTime, "instrumentToTrade" : instrumentToTrade,
        "isPrintEnabled" : isPrintEnabled, "tradeLimitPerInstrument" : tradeLimitPerInstrument, "email" : email, "emailSender" : emailSender, "emailReceiver" : emailReceiver,
        "emailPassword" : emailPassword, "emailTimeInterval" : emailTimeInterval, "subject" : subject, "dataClient" : dataClient, "orderClient" : orderClient,
        "downLoad" : downLoad
        }

userDetails = userDetailsJson()

dhan = dhanhq(userDetails['dataClient'][0]['clientId'],userDetails['dataClient'][0]['accessToken'])

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
            if userDetails['isPrintEnabled'].lower() == "true":
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
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 1:
        security_id = 27
        strikePriceGap = 50
        nickname = "FINNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 40
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 2:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 3:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 50
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    elif weekday_number == 4:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"{weekday_name} --> {nickname}")
    else:
        genericLog("Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = userDetails['lotSize'] * unit

    return [security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity]

def apiCall(secId, exchangeSegment, instrumentType):
    try:
        optionPrice = dhan.intraday_daily_minute_charts(
        security_id = f"{secId}",
        exchange_segment = f"{exchangeSegment}",
        instrument_type = f"{instrumentType}"
        ) 
        return optionPrice
    except Exception as e:
        print(rf"apiCall() --> Error while calling API, will attempt again..")
        print(e)
