import os, json, glob, sys
from time import sleep
from dhanhq import dhanhq, marketfeed
from datetime import datetime
import ssl, smtplib, asyncio
from email.message import EmailMessage

generic_directory = os.path.dirname(os.path.abspath(__file__))
flag_directory = rf"{generic_directory}\flags"
generic_script_name = os.path.splitext(os.path.basename(__file__))[0]
generic_logTime = datetime.now().strftime("%d%m%Y")
script_name = os.path.splitext(os.path.basename(__file__))[0]

if not os.path.exists(rf"{generic_directory}\logs"):
    # Create the folder if it doesn't exist
    os.makedirs(rf"{generic_directory}\logs")

def genericLog(text):
    with open(rf"{generic_directory}\logs\{generic_script_name}_{generic_logTime}.log","a") as log:
        log.write(f"{datetime.now()} - {text}\n")
        log.write(f"\n")

def userDetailsJson(script_name):

    genericLog(rf"userDetailsJson(): {script_name}")

    with open(rf"{generic_directory}\userDetails.json","r") as config:
        userDetails = json.load(config)

    processStartTime = userDetails.get('processStartTime')
    processStartTimeHour = int(processStartTime[0:2])
    processStartTimeMinute = int(processStartTime[3:5])
    processEndTime = userDetails.get('processEndTime')
    processEndTimeHour = int(processEndTime[0:2])
    processEndTimeMinute = int(processEndTime[3:5])
    currentTimeHour = datetime.now().hour
    currentTimeMinute = datetime.now().minute
    expiryLotSize = userDetails.get('expiryLotSize')
    breakOutLotSize = userDetails.get('breakOutLotSize')
    sleepTime = userDetails.get('sleepTime')
    instrumentToTrade_1 = userDetails.get('instrumentToTrade_1')
    instrumentToTrade_2 = userDetails.get('instrumentToTrade_2')
    isPrintEnabled = userDetails.get('enablePrint')
    tradeLimitPerInstrument = userDetails.get('tradeLimitPerInstrument')
    email = userDetails.get('email')
    emailSender = email['emailSender']
    emailReceiver = email['emailReceiver']
    emailPassword = email['emailPassword']
    emailTimeInterval = email['emailTimeInterval']
    downLoad = userDetails.get('downLoad')
    expirySL = userDetails.get('expirySL')
    deltaPrice = userDetails.get('deltaPrice')
    isHolidayInWeek = userDetails.get('isHolidayInWeek')

    return {
        "processStartTime" : processStartTime, "processStartTimeHour" : processStartTimeHour,
        "processStartTimeMinute" : processStartTimeMinute, "currentTimeHour" : currentTimeHour, "currentTimeMinute" : currentTimeMinute,
        "expiryLotSize" : expiryLotSize, "breakOutLotSize" : breakOutLotSize,
        "sleepTime" : sleepTime, "instrumentToTrade_1" : instrumentToTrade_1, "instrumentToTrade_2" : instrumentToTrade_2,
        "isPrintEnabled" : isPrintEnabled, "tradeLimitPerInstrument" : tradeLimitPerInstrument, "email" : email, "emailSender" : emailSender,
        "emailReceiver" : emailReceiver, "emailPassword" : emailPassword, "emailTimeInterval" : emailTimeInterval,
        "downLoad" : downLoad, "processEndTime": processEndTime, "processEndTimeHour" : processEndTimeHour, "processEndTimeMinute" : processEndTimeMinute,
        "expirySL" : expirySL, "deltaPrice" : deltaPrice, "isHolidayInWeek" : isHolidayInWeek
        }

userDetails = userDetailsJson(script_name)
sleepTime = userDetails['sleepTime']
expiryLotSize = userDetails['expiryLotSize']
breakOutLotSize = userDetails['breakOutLotSize']

def apiKey(script_name):
    genericLog(rf"apiKey(): {script_name}")
    with open(rf"{generic_directory}\credentials.json","r") as f:
        clientDetails = json.load(f)
        dataClient = clientDetails.get('dataClient')
        orderClient = clientDetails.get('orderClient')
        return dataClient, orderClient

dataClient, orderClient = apiKey(script_name)
dhanData = dhanhq(dataClient['clientId'],dataClient['accessToken'])
dhanOrder = dhanhq(orderClient['clientId'],orderClient['accessToken'])

def securityDetails_1(script_name):
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
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 25
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 1:
        security_id = 27
        strikePriceGap = 50
        nickname = "FINNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 40
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 35
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 2:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 3:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 25
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 4:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    else:
        genericLog("securityDetails_1(): {script_name} - Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50

    return [security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss]

def securityDetails_2(script_name):
    current_datetime = datetime.now()
    weekday_number = current_datetime.weekday()
    weekday_name = current_datetime.strftime("%A")

    if weekday_number == 0:
        security_id = 69
        strikePriceGap = 100
        nickname = "BANKEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 1:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 2:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 50
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 3:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 25
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 4:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    else:
        genericLog("securityDetails_2(): {script_name} - Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = 50

    return [security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss]

async def securityPrice(secId, exchangeSegment, instrumentType, script_name):
    try:
        secId != '13' and genericLog(rf"securityPrice(): {script_name} - Security Id --> {secId}")
        subscription_code = marketfeed.Ticker
        secId != '13' and genericLog(rf"Subscription code : {subscription_code}")

        if exchangeSegment == 'NSE_FNO':
            securitiesToTrade = [(2, rf"{str(secId)}")]
        elif exchangeSegment == 'BSE_FNO':
            securitiesToTrade = [(8, rf"{str(secId)}")]
        elif exchangeSegment == 'IDX':
            securitiesToTrade = [(0, rf"{str(secId)}")]
        else:
            genericLog(rf"Exchange Segment not in configured list - {exchangeSegment}.. process will exit !")
            sys.exit(0)
        secId != '13' and genericLog(rf"securities to trade: {securitiesToTrade}")

        async def on_connect(instance):
            secId != '13' and genericLog(rf"Connected to websocket")

        async def on_message(instance, message):
            if message['type'] == 'Ticker Data':
                secId != '13' and genericLog(message)
                instance.LTP = float(message["LTP"])
                secId != '13' and genericLog(rf"LTP: {instance.LTP}")

        feed = marketfeed.DhanFeed(
            dataClient['clientId'],
            dataClient['accessToken'],                                                                                          
            securitiesToTrade,
            subscription_code,
            on_connect=on_connect,
            on_message=on_message
            )
        await feed.run_once()
        return feed.LTP
    except Exception as e:
        genericLog(rf"securityPrice(): Something went wrong.. Please Check !")
        print(rf"securityPrice(): Something went wrong.. Please Check !")
        genericLog(rf"{e}")

def indexOpenPrice(security_id, nickname, script, script_name):
    global sleepTime
    genericLog("#################################################################################################################################################")
    genericLog(rf"indexOpenPrice(): {script_name} - Security Id --> {security_id}")
    openPrice = None
    try:
        liveIndexPrice = dhanData.intraday_daily_minute_charts(
            security_id = f"{security_id}",
            exchange_segment = 'IDX_I',
            instrument_type = 'INDEX'
        )
        openPrice = liveIndexPrice['data']['close'][-1]
    except Exception as e:
        genericLog(rf"indexOpenPrice(): {script_name} - indexOpenPrice() --> Error while calling API, will attempt again..")
        print(rf"indexOpenPrice(): {script_name} - indexOpenPrice() --> Error while calling API, will attempt again..")
        genericLog(e)
        #sleep(sleepTime)
        openPrice = asyncio.run(securityPrice(security_id, 'IDX', '_', script_name))
    finally:
        if not os.path.exists(rf"{flag_directory}\{nickname}_{script}.flag") or (os.path.exists(rf"{flag_directory}\{nickname}_{script}.flag") and os.path.getsize(rf"{flag_directory}\{nickname}_{script}.flag") == 0):
            with open(rf"{flag_directory}\{nickname}_{script}.flag","w") as flag:
                #openPrice = liveIndexPrice['data']['close'][-1]
                json.dump({"openPrice" : openPrice}, flag, indent = 4)
        else:
            with open(rf"{flag_directory}\{nickname}_{script}.flag","r") as config:
                price = json.load(config)
                openPrice = price.get('openPrice')
        genericLog(f"indexOpenPrice(): {script_name} - indexOpenPrice() --> {nickname}_{script} opened at --> {openPrice}")
        return openPrice

def apiCall(secId, exchangeSegment, instrumentType, script_name):
    genericLog(rf"apiCall() - {script_name} - {secId}")
    try:
        sleep(sleepTime)
        price = dhanData.intraday_daily_minute_charts(
        security_id = f"{secId}",
        exchange_segment = f"{exchangeSegment}",
        instrument_type = f"{instrumentType}"
        )
        optionPrice = price['data']['close'][-1]
        return optionPrice
    except Exception as e:
        genericLog(rf"apiCall(): {script_name} - Error while calling API, will try through websocket..")
        print(rf"apiCall(): {script_name} - Error while calling API, will try through websocket..")
        genericLog(e)
        genericLog(rf"apiCall({secId}, {exchangeSegment}, {instrumentType}, {script_name})")
        return asyncio.run(securityPrice(secId, exchangeSegment, instrumentType, script_name))

def sendEmail(emailSender, emailReceiver, emailPassword, subject, script_name):
    genericLog(rf"sendEmail(): {script_name} - Initiating mail notification")
    try:
        em = EmailMessage()
        em['From'] = emailSender
        em['To'] = emailReceiver
        em['Subject'] = subject
        #em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
            smtp.login(emailSender, emailPassword)
            smtp.sendmail(emailSender, emailReceiver, em.as_string())
    except Exception as e:
        genericLog("sendEmail(): {script_name} - Error: {e}")

def delFile(fileDirectory, pattern, script_name):
    genericLog(rf"delFile() - {script_name}")
    try:
        files_to_delete = glob.glob(rf"{fileDirectory}\{pattern}")
        for file in files_to_delete:
            os.remove(rf"{file}")
            genericLog(rf"delFile(): {script_name} - {file} file removed")
    except Exception as e:
        genericLog(rf"delFile(): {script_name} - INFO: {file} deletion failed.. Please check.. Process will exit !")
        genericLog(rf"{e}")
        sys.exit(0)

def checkOpenPositions(secId, script_name):
    #genericLog(rf"checkOpenPositions() - {script_name}")
    while True:
        try:
            sleep(sleepTime)
            existingPositions = dhanOrder.get_positions()
            if existingPositions['status'].upper() == 'SUCCESS':
                for el in existingPositions['data']:
                    if secId == str(el['securityId']) and el['positionType'].upper() in ['LONG', 'SHORT']:
                        return True
                return False
            else:
                genericLog(rf"checkOpenPositions(): {script_name} - get_positions() did not return success status, returned data is- {existingPositions}")
                sleep(sleepTime)

        except Exception as e:
            genericLog(rf"checkOpenPositions(): {script_name} - Something went wrong while checking existing positions! will try again..")
            genericLog(rf"existingPositions: {existingPositions}")
            genericLog(rf"Error: {e}")
            sleep(sleepTime)

def costPrice(secId, script_name):
    genericLog(rf"costPrice() - {script_name}")
    while True:
        try:
            sleep(sleepTime)
            existingPositions = dhanOrder.get_positions()
            if existingPositions['status'].upper() == 'SUCCESS':
                for el in existingPositions['data']:
                    if secId == str(el['securityId']) and el['positionType'].upper() in ['LONG', 'SHORT']:
                        return el['costPrice']
                genericLog(rf"Cost Price of secId {secId} {el['tradingSymbol']} not returned. Please check immediately !!")
                genericLog(rf"existingPositions['data']: {existingPositions['data']}")
            else:
                genericLog(rf"checkOpenPositions(): {script_name} - get_positions() did not return success status, returned data is- {existingPositions}")
                sleep(sleepTime)

        except Exception as e:
            genericLog(rf"checkOpenPositions(): {script_name} - Something went wrong while checking existing positions! will try again..")
            genericLog(rf"{e}")

def momentumSecDetails(script_name):
    securitiesToTrade = []
    current_datetime = datetime.now()
    weekday_number = current_datetime.weekday()
    weekday_name = current_datetime.strftime("%A")

    if weekday_number != 7:
        security_id = 69
        strikePriceGap = 100
        trailingStopLoss = [100, 100]
        nickname = "BANKEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        itmPoints = strikePriceGap * 4
        isTradeCePe = ['CE', 'PE']
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints, isTradeCePe])
    if weekday_number != 7:
        security_id = 442
        strikePriceGap = 25
        trailingStopLoss = [50, 50]
        nickname = "MIDCPNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 75
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        itmPoints = strikePriceGap * 4
        isTradeCePe = ['CE', 'PE']
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints, isTradeCePe])
    if weekday_number != 7:
        security_id = 27
        strikePriceGap = 50
        trailingStopLoss = [75, 75]
        nickname = "FINNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 40
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        itmPoints = strikePriceGap * 4
        isTradeCePe = ['CE', 'PE']
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints, isTradeCePe])
    if weekday_number != 7:
        security_id = 25
        strikePriceGap = 100
        trailingStopLoss = [200, 200]
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        itmPoints = strikePriceGap * 5
        isTradeCePe = ['CE', 'PE']
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints, isTradeCePe])
    if weekday_number != 7:
        security_id = 13
        strikePriceGap = 50
        trailingStopLoss = [70, 70]
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 25
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        itmPoints = strikePriceGap * 5
        isTradeCePe = ['CE', 'PE']
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints, isTradeCePe])
    if weekday_number == 7:
        security_id = 51
        strikePriceGap = 100
        trailingStopLoss = [150, 150]
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        itmPoints = strikePriceGap * 4
        isTradeCePe = ['CE', 'PE']
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints, isTradeCePe])

    return securitiesToTrade

def secIdToTradeFromJson(data, keys_to_exclude, script_name):
    genericLog(rf"secIdToTradeFromJson() - {script_name}")
    uniqueSecurityIdCheck = []
    securitiesToTrade = []
    for key, value in data.items():
        if isinstance(value, dict) and key not in keys_to_exclude:
            for sub_key, sub_value in value.items():
                if sub_key not in keys_to_exclude:
                    genericLog(f"{sub_key}: {sub_value}")
        elif isinstance(value, list) and key not in keys_to_exclude:
            for item in value:
                for sub_key, sub_value in item.items():
                    if sub_key not in keys_to_exclude:
                        genericLog(f"{sub_key}: {sub_value}")
        elif key not in keys_to_exclude:
            genericLog(f"{key}: {value}")

        if key == 'instrument':

            for el in value:
                uniqueSecurityIdCheck.append(el['securityId'])
                genericLog(rf"{el}")

                if el['exchangeSegment'] == 'IDX_I':
                    securitiesToTrade.append((0,el['securityId']))

                elif el['exchangeSegment'] == 'NSE_EQ':
                    securitiesToTrade.append((1,el['securityId']))

                elif el['exchangeSegment'] == 'NSE_FNO':
                    securitiesToTrade.append((2,el['securityId']))

                elif el['exchangeSegment'] == 'NSE_CURR':
                    securitiesToTrade.append((3,el['securityId']))

                elif el['exchangeSegment'] == 'BSE_EQ':
                    securitiesToTrade.append((4,el['securityId']))

                elif el['exchangeSegment'] == 'MCX':
                    securitiesToTrade.append((5,el['securityId']))

                elif el['exchangeSegment'] == 'BSE_CURR':
                    securitiesToTrade.append((7,el['securityId']))

                elif el['exchangeSegment'] == 'BSE_FNO':
                    securitiesToTrade.append((8,el['securityId']))
    return uniqueSecurityIdCheck, securitiesToTrade

def scalpSecDetails(script_name):
    securitiesToTrade = []
    current_datetime = datetime.now()
    weekday_number = current_datetime.weekday()
    weekday_name = current_datetime.strftime("%A")

    if weekday_number != 7:
        security_id = 69
        strikePriceGap = 100
        nickname = "BANKEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [100, 100]
        itmPoints = strikePriceGap * 4
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])
    if weekday_number != 7:
        security_id = 442
        strikePriceGap = 25
        nickname = "MIDCPNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 75
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [50, 50]
        itmPoints = strikePriceGap * 4
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])
    if weekday_number != 7:
        security_id = 27
        strikePriceGap = 50
        nickname = "FINNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 40
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [75, 75]
        itmPoints = strikePriceGap * 4
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])
    if weekday_number != 7:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [100, 100]
        itmPoints = strikePriceGap * 10
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])
    if weekday_number != 7:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 25
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [50, 50]
        itmPoints = strikePriceGap * 8
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])
    if weekday_number != 7:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [100, 50]
        itmPoints = strikePriceGap * 4
        genericLog(rf"momentumSecDetails(): {script_name} - quantity entered by user --> {quantity}")
        genericLog(rf"momentumSecDetails(): {script_name} - {weekday_name} --> {nickname}")
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])
    else:
        genericLog("momentumSecDetails(): {script_name} - Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        if "expiry_" in script_name:
            quantity = expiryLotSize * unit
        elif "breakout_" in script_name:
            quantity = breakOutLotSize * unit
        else:
            quantity = breakOutLotSize * unit
        breakOutPriceSlippage = 15
        trailingStopLoss = [50, 50]
        itmPoints = strikePriceGap * 5
        securitiesToTrade.append([security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity, breakOutPriceSlippage, trailingStopLoss, itmPoints])

    return securitiesToTrade
