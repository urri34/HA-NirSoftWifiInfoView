#!python.exe
# -*- coding: utf-8 -*-
from os import path
from math import log10
import pandas as pd
import matplotlib.pyplot as plt
FileName='Scan-Dorm1.csv'
Tabulate=False
JustLowerThan=36
ZigBee={2405:11, 2410:12, 2415:13, 2420:14, 2425:15, 2430:16, 2435:17, 2440:18, 2445:19, 2450:20, 2455:21, 2460:22, 2465:23, 2470:24, 2475:25, 2480:26} 
ZigBeeWidth=2
ZigBeeDown=0.1
ZigBeeOverWifi=1
#https://en.wikipedia.org/wiki/List_of_WLAN_Channels
WiFiWith=20
WiFiDown=1

if(path.isfile(FileName)):
    data = pd.read_csv(FileName)
    MyHeaders=["SSID", "Average Signal Quality", "Frequency", "Channel"]
    df = pd.DataFrame(data, columns=MyHeaders)
    df = df.reset_index()
    #For each Frequency just add all the "Average Signal mW" and generate Spectrum matrix
    Spectrum={}
    for index, row in df.iterrows():
        Channel=int(row['Channel'])
        Frequency=float(str(row['Frequency']).replace(',','').replace('.',''))
        if Channel < JustLowerThan:
            Power=pow(10,((float(row['Average Signal Quality'])/2)-100))
            if Frequency in Spectrum:
                Spectrum[Frequency][0]+=Power
            else:
                Spectrum[Frequency]=[Power,Channel]


    #We will show how data is build step by step if Tabulate is True
    if Tabulate:
        from tabulate import tabulate
        #Import all data from csv files ["SSID", "Average Signal Quality", "Frequency", "Channel"]
        MyData=[]
        for index, row in df.iterrows():
            Channel=int(row['Channel'])
            if Channel < JustLowerThan:
                Ssid=row['SSID']
                Quality=row['Average Signal Quality']
                Frequency=float(str(row['Frequency']).replace(',','').replace('.',''))
                MyData.append([Ssid, Quality, Frequency, Channel])
        print('Data from your capture(%):')
        print(tabulate(MyData, headers=MyHeaders, tablefmt="grid"))
        input('--Press any key to continue--')

        #Convert all data from "Average Signal Quality" -> "Average Signal dBm"
        #https://learn.microsoft.com/ca-es/windows/win32/api/wlanapi/ns-wlanapi-wlan_association_attributes?redirectedfrom=MSDN"
        MyHeaders=["SSID", "AverageSignalPw(dBm)", "Frequency", "Channel"]
        MyData=[]
        for index, row in df.iterrows():
            Channel=int(row['Channel'])
            if Channel < JustLowerThan:
                Ssid=row['SSID']
                dBm=(float(row['Average Signal Quality'])/2)-100
                Frequency=float(str(row['Frequency']).replace(',','').replace('.',''))
                MyData.append([Ssid, dBm, Frequency, Channel])
        print('Data from your capture(dBm):')
        print(tabulate(MyData, headers=MyHeaders, tablefmt="grid"))
        input('--Press any key to continue--')

        #Convert all data from "Average Signal dBm" to "Average Signal mW"
        MyHeaders=["SSID", "AverageSignalPw(mW)", "Frequency", "Channel"]
        MyData=[]
        for index, row in df.iterrows():
            Channel=int(row['Channel'])
            if Channel < JustLowerThan:
                Ssid=row['SSID']
                mW=pow(10,((float(row['Average Signal Quality'])/2)-100))
                Frequency=float(str(row['Frequency']).replace(',','').replace('.',''))                
                MyData.append([Ssid, mW, Frequency, Channel])
        print('Data from your capture(mW):')
        print(tabulate(MyData, headers=MyHeaders, tablefmt="grid"))
        input('--Press any key to continue--')

        #Get all added mW from spectrum
        MyData=[]
        MyHeaders=["Frequency", "Power(mW)", "Channel"]
        for Freq in Spectrum:
            MyData.append([Freq, Spectrum[Freq][0], Spectrum[Freq][1]])
        print('Data for you(mW):')
        print(tabulate(MyData, headers=MyHeaders, tablefmt="grid"))
        input('--Press any key to continue--')

        #For each Frequency in the Spectrum matrix convert "Average Signal mW" to "Average Signal dbm+100"
        MyHeaders=["Frequency", "Power(dBm)+100", "Channel"]
        MyData=[]
        for Freq in Spectrum:
            Channel=Spectrum[Freq][1]
            if Channel < JustLowerThan:
                MyData.append([Freq, (log10(Spectrum[Freq][0])+100), Channel])
        print('Data for you(dBm)+100:')
        print(tabulate(MyData, headers=MyHeaders, tablefmt="grid"))
        input('--Press any key to continue--')

    #ax1 contains the graph of each wifi
    ax1= plt.subplots()[1]
    plt.xlabel("MHz")
    plt.ylabel("mW")
    #ax2 contains the graph of the Spectrum matrix with the added power of each wifi dbm+100
    ax2= plt.subplots()[1]
    plt.xlabel("MHz")
    plt.ylabel("dBm+100")

    ZigBeePw=0
    for Freq in Spectrum:
        ActualFreq=float(str(Freq).replace(',',''))
        if ActualFreq > min(ZigBee) and ActualFreq < max(ZigBee):
            globals()[str(Freq)+'X']=[]
            globals()[str(Freq)+'Y']=[]
            globals()[str(Freq)+'X'].append(ActualFreq-WiFiWith/2-WiFiDown)
            globals()[str(Freq)+'Y'].append(0)
            globals()[str(Freq)+'X'].append(ActualFreq-WiFiWith/2)
            globals()[str(Freq)+'Y'].append(log10(Spectrum[Freq][0])+100)
            globals()[str(Freq)+'X'].append(ActualFreq)
            globals()[str(Freq)+'Y'].append(log10(Spectrum[Freq][0])+100)
            globals()[str(Freq)+'X'].append(ActualFreq+WiFiWith/2)
            globals()[str(Freq)+'Y'].append(log10(Spectrum[Freq][0])+100)
            globals()[str(Freq)+'X'].append(ActualFreq+WiFiWith/2+WiFiDown)
            globals()[str(Freq)+'Y'].append(0)
            if ZigBeePw < max(globals()[str(Freq)+'Y']):
                ZigBeePw=max(globals()[str(Freq)+'Y'])
            ax1.plot(globals()[str(Freq)+'X'],globals()[str(Freq)+'Y'], label=str(Freq)+'GHz')

    WiFiX=[]
    WiFiY=[]
    for FreqZigBee in ZigBee:
        for FreqZigBeeActual in [(FreqZigBee-ZigBeeWidth/2), (FreqZigBee+ZigBeeWidth/2)]:
            Power=0
            for FreqWifi in Spectrum:
                FreqWifiActual=float(str(FreqWifi).replace(',',''))
                if (FreqWifiActual-(WiFiWith/2))<=FreqZigBeeActual:
                    if (FreqWifiActual+(WiFiWith/2))>=FreqZigBeeActual:
                        Power+=log10(Spectrum[FreqWifi][0])+100
            WiFiX.append(FreqZigBeeActual)
            WiFiY.append(Power)
    ax2.plot(WiFiX,WiFiY, label='WiFi')

    ZigBeePw=ZigBeePw*ZigBeeOverWifi
    for Freq in ZigBee:
        globals()['Zigbee'+str(ZigBee[Freq])+'X']=[]
        globals()['Zigbee'+str(ZigBee[Freq])+'Y']=[]
        globals()['Zigbee'+str(ZigBee[Freq])+'X'].append(Freq-(ZigBeeWidth/2)-ZigBeeDown)
        globals()['Zigbee'+str(ZigBee[Freq])+'Y'].append(0)
        globals()['Zigbee'+str(ZigBee[Freq])+'X'].append(Freq-(ZigBeeWidth/2))
        globals()['Zigbee'+str(ZigBee[Freq])+'Y'].append(ZigBeePw)
        globals()['Zigbee'+str(ZigBee[Freq])+'X'].append(Freq+(ZigBeeWidth/2))
        globals()['Zigbee'+str(ZigBee[Freq])+'Y'].append(ZigBeePw)
        globals()['Zigbee'+str(ZigBee[Freq])+'X'].append(Freq+(ZigBeeWidth/2)+ZigBeeDown)
        globals()['Zigbee'+str(ZigBee[Freq])+'Y'].append(0)
        ax1.plot(globals()['Zigbee'+str(ZigBee[Freq])+'X'],globals()['Zigbee'+str(ZigBee[Freq])+'Y'], label='Zigbee'+str(ZigBee[Freq]))
        ax2.plot(globals()['Zigbee'+str(ZigBee[Freq])+'X'],globals()['Zigbee'+str(ZigBee[Freq])+'Y'], label='Zigbee'+str(ZigBee[Freq]))

    ax1.legend(loc="upper left")
    ax2.legend(loc="upper left")
    plt.show()
    plt.close()

else:
    print('ERROR: Unable to open '+str(FileName))
exit(0)