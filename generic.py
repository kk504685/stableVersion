import os, json, glob, sys
from time import sleep
from dhanhq import dhanhq
from datetime import datetime
import ssl, smtplib
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

    genericLog(rf"userDetailsJson(): {script_name} - userDetailsJson function invoked")

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
    lotSize = userDetails.get('lotSize')
    sleepTime = userDetails.get('sleepTime')
    instrumentToTrade = userDetails.get('instrumentToTrade')
    isPrintEnabled = userDetails.get('enablePrint')
    tradeLimitPerInstrument = userDetails.get('tradeLimitPerInstrument')
    email = userDetails.get('email')
    emailSender = email['emailSender']
    emailReceiver = email['emailReceiver']
    emailPassword = email['emailPassword']
    emailTimeInterval = email['emailTimeInterval']
    downLoad = userDetails.get('downLoad')

    return {
        "processStartTime" : processStartTime, "processStartTimeHour" : processStartTimeHour,
        "processStartTimeMinute" : processStartTimeMinute, "currentTimeHour" : currentTimeHour, "currentTimeMinute" : currentTimeMinute, "lotSize" : lotSize,
        "sleepTime" : sleepTime, "instrumentToTrade" : instrumentToTrade,
        "isPrintEnabled" : isPrintEnabled, "tradeLimitPerInstrument" : tradeLimitPerInstrument, "email" : email, "emailSender" : emailSender,
        "emailReceiver" : emailReceiver, "emailPassword" : emailPassword, "emailTimeInterval" : emailTimeInterval,
        "downLoad" : downLoad, "processEndTime": processEndTime, "processEndTimeHour" : processEndTimeHour, "processEndTimeMinute" : processEndTimeMinute
        }

userDetails = userDetailsJson(script_name)
sleepTime = userDetails['sleepTime']

def apiKey(script_name):
    genericLog(rf"apiKey(): {script_name}")
    with open(rf"{generic_directory}\credentials.json","r") as f:
        clientDetails = json.load(f)
        dataClient = clientDetails.get('dataClient')
        orderClient = clientDetails.get('orderClient')
        return [dataClient, orderClient]

clientDetails = apiKey(script_name)
dataClient = clientDetails[0]
orderClient = clientDetails[1]

dhan = dhanhq(dataClient[0]['clientId'],dataClient[0]['accessToken'])

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
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 1:
        security_id = 27
        strikePriceGap = 50
        nickname = "FINNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 40
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 2:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 3:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 50
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 4:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_1(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_1(): {script_name} - {weekday_name} --> {nickname}")
    else:
        genericLog("securityDetails_1(): {script_name} - Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = userDetails['lotSize'] * unit

    return [security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity]

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
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 1:
        security_id = 25
        strikePriceGap = 100
        nickname = "BANKNIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 15
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 2:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 50
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 3:
        security_id = 13
        strikePriceGap = 50
        nickname = "NIFTY"
        exchangeSegment = 'NSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 50
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    elif weekday_number == 4:
        security_id = 51
        strikePriceGap = 100
        nickname = "SENSEX"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = userDetails['lotSize'] * unit
        genericLog(rf"securityDetails_2(): {script_name} - quantity entered by user --> {userDetails['lotSize']} * {unit} = {quantity}")
        genericLog(rf"securityDetails_2(): {script_name} - {weekday_name} --> {nickname}")
    else:
        genericLog("securityDetails_2(): {script_name} - Market might be closed today, so assigning any security id for testing")
        security_id = 51
        strikePriceGap = 100
        nickname = "sensex_DUMMY"
        exchangeSegment = 'BSE_FNO'
        instrumentType = 'OPTIDX'
        unit = 10
        quantity = userDetails['lotSize'] * unit

    return [security_id, strikePriceGap, nickname, exchangeSegment, instrumentType, unit, quantity]

def indexOpenPrice(security_id, nickname, script, script_name):
    global sleepTime
    genericLog("#################################################################################################################################################")
    genericLog(rf"indexOpenPrice(): {script_name} - Security Id --> {security_id}")
    openPrice = None
    while True:
        try:
            liveIndexPrice = dhan.intraday_daily_minute_charts(
                security_id = f"{security_id}",
                exchange_segment = 'IDX_I',
                instrument_type = 'INDEX'
            )
            if not os.path.exists(rf"{flag_directory}\{nickname}_{script}.flag"):
                with open(rf"{flag_directory}\{nickname}_{script}.flag","w") as flag:
                    openPrice = liveIndexPrice['data']['close'][-1]
                    json.dump({"openPrice" : openPrice}, flag, indent = 4)
            else:
                with open(rf"{flag_directory}\{nickname}_{script}.flag","r") as config:
                    price = json.load(config)
                    openPrice = price.get('openPrice')
            genericLog(f"indexOpenPrice(): {script_name} - indexOpenPrice() --> {nickname}_{script} opened at --> {openPrice}")
            return openPrice
        except Exception as e:
            genericLog(rf"indexOpenPrice(): {script_name} - indexOpenPrice() --> Error while calling API, will attempt again..")
            genericLog(e)
            sleep(sleepTime)

def apiCall(secId, exchangeSegment, instrumentType, script_name):
    try:
        optionPrice = dhan.intraday_daily_minute_charts(
        security_id = f"{secId}",
        exchange_segment = f"{exchangeSegment}",
        instrument_type = f"{instrumentType}"
        ) 
        return optionPrice
    except Exception as e:
        print(rf"apiCall(): {script_name} - Error while calling API, will attempt again..")
        print(e)

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
    while True:
        try:
            sleep(sleepTime/2)
            existingPositions = dhan.get_positions()
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
            genericLog(rf"{e}")

