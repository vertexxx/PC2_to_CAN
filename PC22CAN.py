
from PCANBasic import *
import os
import sys
import threading
import urllib
import urllib.request
import json

debug_readfromfile = 0

class TimerRepeater(object):
    def __init__(self, name, interval, target):
        self._name = name
        self._thread = None
        self._event = None
        self._target = target
        self._interval = interval
    def _run(self):
        while not self._event.wait(self._interval):
            self._target()
        print("Timer stopped.")
    def start(self):
        if (self._thread == None):
            self._event = threading.Event()
            self._thread = threading.Thread(None, self._run, self._name)
            self._thread.start()
    def stop(self):
        if (self._thread != None):
            self._event.set()
            self._thread.join() 
            self._thread = None

class TimerWrite():
    PcanHandle = PCAN_USBBUS1
    Bitrate = PCAN_BAUD_1M
    TimerInterval = 10
    m_DLLFound = False
    sendcounter = 0
    jsondata = []
    roadFric=1

    def __init__(self):
        self.ShowConfigurationHelp()
        self.ShowCurrentConfiguration()
        try:
            self.m_objPCANBasic = PCANBasic()        
            self.m_DLLFound = self.CheckForLibrary()
        except:
            print("Unable to find the library: PCANBasic.dll !")
            self.getInput("Press <Enter> to quit...")
            self.m_DLLFound = False
            return
        stsResult = self.m_objPCANBasic.Initialize(self.PcanHandle,self.Bitrate)

        if stsResult != PCAN_ERROR_OK:
            print("Can not initialize. Please check the defines in the code.")
            self.ShowStatus(stsResult)
            print("")
            print("Press enter to close")
            input()
            return

        print("Successfully initialized.")
        self.m_objTimer = TimerRepeater("WriteMessages",float(self.TimerInterval)/1000, self.WriteMessages)
        self.m_objTimer.start()
        print("Started writing messages...")
        print("")
        self.getInput("Press <Enter> to stop timer...")
        self.m_objTimer.stop()
        self.getInput("Press <Enter> to exit...")

    def __del__(self):
        if self.m_DLLFound:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)

    def getInput(self, msg="Press <Enter> to continue...", default=""):
        res = default
        if sys.version_info[0] >= 3:
            res = input(msg + " ")
        else:
            res = raw_input(msg + " ")
        if len(res) == 0:
            res = default
        return res

    def updateJson(self):
        url='http://127.0.0.1:8180/crest2/v1/api'
        fileurl='api.json'
        if 1:#try:
            if debug_readfromfile:
                with open(fileurl, mode="rb") as fileasbytes:
                    jsonbytes = fileasbytes.read()
            else:
                try:
                    r = urllib.request.urlopen(url)
                    jsonbytes = r.read().decode(r.info().get_param('charset') or 'utf-8')
                except:
                    jsonbytes="{}"
            self.jsondata = json.loads(jsonbytes)
        #except:
        #    print('nope')
        if self.sendcounter==0 or (self.sendcounter%50)==0:
            print('#####################################Debugprint#################################')
            try:
                # print('carState.mRpm            ',self.jsondata['carState']['mRpm'])
                # print('carState.mSpeed          ',self.jsondata['carState']['mSpeed'])
                # print('carState.mBrake          ',self.jsondata['carState']['mBrake'])
                # print('carState.mThrottle       ',self.jsondata['carState']['mThrottle'])
                # print('carState.mAntiLockActive ',self.jsondata['carState']['mAntiLockActive'])
                # print('carState.mSteering       ',self.jsondata['carState']['mSteering'])
                # print(' ')
                # print('gameStates.mGameState    ',self.jsondata['gameStates']['mGameState'])
                # print('gameStates.mSessionState ',self.jsondata['gameStates']['mSessionState'])
                # print('gameStates.mRaceState    ',self.jsondata['gameStates']['mRaceState'])
                # print(' ')
                # print('part.mPI.0.mIsActive     ',self.jsondata['participants']['mParticipantInfo'][0]['mIsActive'])
                # print(' ')
                # print('aX                       ',self.jsondata['motionAndDeviceRelated']['mLocalAcceleration'][0])
                # print('aY                       ',self.jsondata['motionAndDeviceRelated']['mLocalAcceleration'][1])
                # print('aZ                       ',self.jsondata['motionAndDeviceRelated']['mLocalAcceleration'][2])
                # print(' ')
                # print('aX_W                     ',self.jsondata['motionAndDeviceRelated']['mWorldAcceleration'][0])
                # print('aY_W                     ',self.jsondata['motionAndDeviceRelated']['mWorldAcceleration'][1])
                # print('aZ_W                     ',self.jsondata['motionAndDeviceRelated']['mWorldAcceleration'][2])
                # print(' ')
                # print('mAngularVelocity         ',self.jsondata['motionAndDeviceRelated']['mAngularVelocity'][0])
                # print('mAngularVelocity         ',self.jsondata['motionAndDeviceRelated']['mAngularVelocity'][1])
                # print('mAngularVelocity         ',self.jsondata['motionAndDeviceRelated']['mAngularVelocity'][2])
                # print(' ')
                # print('mSuspensionTravel        ',self.jsondata['wheelsAndTyres']['mSuspensionTravel'][3])
                # print(' ')
                # print('mTyreRPS                 ',self.jsondata['wheelsAndTyres']['mTyreRPS'][0])
                # print('mTyreRPS                 ',self.jsondata['wheelsAndTyres']['mTyreRPS'][1])
                # print('mTyreRPS                 ',self.jsondata['wheelsAndTyres']['mTyreRPS'][2])
                # print('mTyreRPS                 ',self.jsondata['wheelsAndTyres']['mTyreRPS'][3])
                # print(' ')
                # print('mTyreY                   ',self.jsondata['wheelsAndTyres']['mTyreY'][0])
                # print('mTyreY                   ',self.jsondata['wheelsAndTyres']['mTyreY'][1])
                # print('mTyreY                   ',self.jsondata['wheelsAndTyres']['mTyreY'][2])
                # print('mTyreY                   ',self.jsondata['wheelsAndTyres']['mTyreY'][3])
                # print(' ')
                # print('mTyreTemp                ',self.jsondata['wheelsAndTyres']['mTyreTemp'][0])
                # print('mTyreTemp                ',self.jsondata['wheelsAndTyres']['mTyreTemp'][1])
                # print('mTyreTemp                ',self.jsondata['wheelsAndTyres']['mTyreTemp'][2])
                # print('mTyreTemp                ',self.jsondata['wheelsAndTyres']['mTyreTemp'][3])
                # print(' ')
                # print('timestamp                ',self.jsondata['timestamp'])
                # print(' ')
                # print('mUnfilteredSteering      ',self.jsondata['unfilteredInput']['mUnfilteredSteering'])
                # print(' ')
                # print('weather.mAmbientTemp     ',self.jsondata['weather']['mAmbientTemperature'])
                # print('weather.mRainDensity     ',self.jsondata['weather']['mRainDensity'])
                # print('weather.mSnowDensity     ',self.jsondata['weather']['mSnowDensity'])
                print('vX                       ',self.jsondata['motionAndDeviceRelated']['mLocalVelocity'][0])
                print('vY                       ',self.jsondata['motionAndDeviceRelated']['mLocalVelocity'][1])
                print('vZ                       ',self.jsondata['motionAndDeviceRelated']['mLocalVelocity'][2])
            except:
                print('API not fully available')

    def getMsgBytes(self, hexid, returnbytes):
        for i in range(8):
            returnbytes[i] = 0
        if hexid==0x50:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes, 8, 0,1,0,self.jsondata['gameStates']['mGameState'])
                returnbytes=self.writeSignalToBytes(returnbytes, 8, 8,1,0,self.jsondata['gameStates']['mSessionState'])
                returnbytes=self.writeSignalToBytes(returnbytes, 8,16,1,0,self.jsondata['gameStates']['mRaceState'])
                returnbytes=self.writeSignalToBytes(returnbytes, 8,24,1,0,self.jsondata['participants']['mParticipantInfo'][0]['mIsActive'])
                returnbytes=self.writeSignalToBytes(returnbytes,32,32,1,0,self.jsondata['timestamp'])
            except:
                print('Exception creating message for: ',hex(hexid))    
        if hexid==0x51:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes,16, 0,0.0039,-127.7874,self.jsondata['motionAndDeviceRelated']['mLocalVelocity'][2]*-1)
                returnbytes=self.writeSignalToBytes(returnbytes,16,16,0.000174532925199433,-5.71909489293502,self.jsondata['motionAndDeviceRelated']['mAngularVelocity'][1])
                returnbytes=self.writeSignalToBytes(returnbytes,16,32,3.19598837574497e-5,-1.0471975511966,self.jsondata['carState']['mSteering']*-1*360*1.3/13/180*3.14159)
                returnbytes=self.writeSignalToBytes(returnbytes,16,48,0.0039,-127.7874,self.jsondata['motionAndDeviceRelated']['mLocalVelocity'][0])
            except:
                print('Exception creating message for: ',hex(hexid))
        if hexid==0x52:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes,16, 0,0.005,-163.84,self.jsondata['motionAndDeviceRelated']['mLocalAcceleration'][0])
                returnbytes=self.writeSignalToBytes(returnbytes,16,16,0.005,-163.84,self.jsondata['motionAndDeviceRelated']['mLocalAcceleration'][2]*-1)
                returnbytes=self.writeSignalToBytes(returnbytes,16,32,0.005,-163.84,self.jsondata['motionAndDeviceRelated']['mLocalAcceleration'][1]*-1-9.81)
                returnbytes=self.writeSignalToBytes(returnbytes,16,48,0.000436252413289189,-14.2942465738336,self.jsondata['carState']['mSteering']*-1*360*1.3/180*3.14159)
            except:
                print('Exception creating message for: ',hex(hexid))
        if hexid==0x53:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes,16, 0,0.0039,-127.874,self.jsondata['wheelsAndTyres']['mTyreRPS'][0]*-1*(1/91*32))
                returnbytes=self.writeSignalToBytes(returnbytes,16,16,0.0039,-127.874,self.jsondata['wheelsAndTyres']['mTyreRPS'][1]*-1*(1/91*32))
                returnbytes=self.writeSignalToBytes(returnbytes,16,32,0.0039,-127.874,self.jsondata['wheelsAndTyres']['mTyreRPS'][2]*-1*(1/91*32))
                returnbytes=self.writeSignalToBytes(returnbytes,16,48,0.0039,-127.874,self.jsondata['wheelsAndTyres']['mTyreRPS'][3]*-1*(1/91*32))
            except:
                print('Exception creating message for: ',hex(hexid))
        if hexid==0x54:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes, 4, 0,1,0,0)
                returnbytes=self.writeSignalToBytes(returnbytes, 8, 8,1,-25,self.jsondata['wheelsAndTyres']['mTyreTemp'][0]/12*8)
                returnbytes=self.writeSignalToBytes(returnbytes, 8,16,1,-25,self.jsondata['wheelsAndTyres']['mTyreTemp'][1]/12*8)
                returnbytes=self.writeSignalToBytes(returnbytes, 8,24,1,-25,self.jsondata['wheelsAndTyres']['mTyreTemp'][2]/12*8)
                returnbytes=self.writeSignalToBytes(returnbytes, 8,32,1,-25,self.jsondata['wheelsAndTyres']['mTyreTemp'][3]/12*8)
                returnbytes=self.writeSignalToBytes(returnbytes, 8,40,0.01,0,self.estimateRoadFric())
            except:
                print('Exception creating message for: ',hex(hexid))
        if hexid==0x55:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes,12, 0,1,0,1500*0.55)
                returnbytes=self.writeSignalToBytes(returnbytes, 3,12,1,0,0)
                returnbytes=self.writeSignalToBytes(returnbytes,12,16,1,0,1500*0.45)
                returnbytes=self.writeSignalToBytes(returnbytes, 3,28,1,0,self.jsondata['carState']['mAntiLockActive'])
                returnbytes=self.writeSignalToBytes(returnbytes,12,32,1,0,self.jsondata['carState']['mBrake']*0.6*20475)
                returnbytes=self.writeSignalToBytes(returnbytes, 3,44,1,0,0)
                returnbytes=self.writeSignalToBytes(returnbytes, 4,48,1,0,1)
                returnbytes=self.writeSignalToBytes(returnbytes, 3,52,1,0,0)
                returnbytes=self.writeSignalToBytes(returnbytes, 8,56,1,0,self.jsondata['carState']['mThrottle']*100)
            except:
                print('Exception creating message for: ',hex(hexid))
        if hexid==0x57:
            try:
                returnbytes=self.writeSignalToBytes(returnbytes, 8, 0,50,0,self.jsondata['carState']['mRpm'])
                returnbytes=self.writeSignalToBytes(returnbytes, 8, 8,50,0,self.jsondata['carState']['mMaxRPM'])
                returnbytes=self.writeSignalToBytes(returnbytes, 8,16,1, 0,self.jsondata['carState']['mBrake']*100)
                returnbytes=self.writeSignalToBytes(returnbytes,16,32,0.005,-163.84,self.jsondata['wheelsAndTyres']['mSuspensionTravel'][3])
            except:
                print('Exception creating message for: ',hex(hexid))

        return returnbytes

        ####
        # mTerrain
        #   Straße:    0  1.1
        #   Gras:      7  0.6
        #   Erde:      19 0.6
        #   Schotter:  50 0.55
        #   Schnee     33 0.45
        #   Eis        45 0.25
        #   mRainDensity!=0  -0.3
    def estimateRoadFric(self):
        lroadFric=1
        t=[1,1,1,1]
        for i in range(len(t)):
            if self.jsondata['wheelsAndTyres']['mTerrain'][i]==0:
                t[i]=1.1
            if self.jsondata['wheelsAndTyres']['mTerrain'][i]==7:
                t[i]=0.6
            if self.jsondata['wheelsAndTyres']['mTerrain'][i]==19:
                t[i]=0.6
            if self.jsondata['wheelsAndTyres']['mTerrain'][i]==50:
                t[i]=0.55
            if self.jsondata['wheelsAndTyres']['mTerrain'][i]==33:
                t[i]=0.45
            if self.jsondata['wheelsAndTyres']['mTerrain'][i]==45:
                t[i]=0.25
        lroadFric=min(t)*0.5+0.5*0.25*(t[1]+t[2]+t[3]+t[0])
        if self.jsondata['weather']['mRainDensity']>0:
            lroadFric=lroadFric-0.2
        if self.jsondata['weather']['mSnowDensity']>0:
            lroadFric=lroadFric-0.2
        #mAmbientTemperature
        self.roadFric = self.roadFric + (lroadFric-self.roadFric)*0.05
        return self.roadFric


    def writeSignalToBytes(self,returnbytes,bitlength,bitoffset,sigfactor,sigoffset,signal):
        #print(list(returnbytes))
        tmpsignal=(float(signal)-sigoffset)*1/sigfactor
        #print(tmpsignal)
        tmpsignal=int(tmpsignal)%(2**bitlength)
        #print(tmpsignal)
        tmpbytes=tmpsignal.to_bytes((tmpsignal.bit_length() + 7) // 8, "big")
        if bitoffset%8 != 0:
            if len(tmpbytes)>1:
                print("Signal Shifting above uint8 not supported")
            else:
                if tmpbytes!=b'':
                    tmpbytes[0]<<bitoffset%8
        #print(tmpbytes)
        bofs = int((bitoffset-bitoffset%8)/8)
        for i in range(len(tmpbytes)):
            returnbytes[i+bofs]=returnbytes[i+bofs]|tmpbytes[len(tmpbytes)-1-i]
        #print(list(returnbytes))
        return returnbytes
        

    def WriteMessages(self):
        self.updateJson()
        stsResult = self.WriteMessage(0x50)
        stsResult = self.WriteMessage(0x51)
        stsResult = self.WriteMessage(0x52)
        stsResult = self.WriteMessage(0x53)
        if (self.sendcounter%5)==0:
            stsResult = self.WriteMessage(0x54)
            stsResult = self.WriteMessage(0x55)
            stsResult = self.WriteMessage(0x57)
        self.sendcounter = self.sendcounter+1
        if (stsResult != PCAN_ERROR_OK):
            self.ShowStatus(stsResult)
        #else:
        #    print("Message was successfully SENT")

    def WriteMessage(self, hexid):
        msgCanMessage = TPCANMsg()
        msgCanMessage.ID = hexid
        msgCanMessage.LEN = 8
        msgCanMessage.MSGTYPE = PCAN_MESSAGE_STANDARD #PCAN_MESSAGE_EXTENDED.value
        msgCanMessage.DATA=self.getMsgBytes(hexid,msgCanMessage.DATA)
        return self.m_objPCANBasic.Write(self.PcanHandle, msgCanMessage)

    def clear(self):
        if os.name=='nt':
            os.system('cls')
        else:
            os.system('clear')

    def CheckForLibrary(self):
        try:
            self.m_objPCANBasic.Uninitialize(PCAN_NONEBUS)
            return True
        except :
            return False 

    def ShowConfigurationHelp(self):
        print("")

    def ShowCurrentConfiguration(self):
        print("Parameter values used")
        print("----------------------")
        print("* PCANHandle= " + self.FormatChannelName(self.PcanHandle))
        print("* Bitrate= " + self.ConvertBitrateToString(self.Bitrate))
        print("* TimerInterval: " + str(self.TimerInterval))
        print("")

    def ShowStatus(self,status):
        print("=========================================================================================")
        print(self.GetFormattedError(status))
        print("=========================================================================================")
    
    def FormatChannelName(self, handle):
        handleValue = handle.value
        if handleValue < 0x100:
            devDevice = TPCANDevice(handleValue >> 4)
            byChannel = handleValue & 0xF
        else:
            devDevice = TPCANDevice(handleValue >> 8)
            byChannel = handleValue & 0xFF
        return ('%s: %s (%.2Xh)' % (self.GetDeviceName(devDevice.value), byChannel, handleValue))

    def GetFormattedError(self, error):
        stsReturn = self.m_objPCANBasic.GetErrorText(error,0x09)
        if stsReturn[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            message = str(stsReturn[1])
            return message.replace("'","",2).replace("b","",1)

    def GetDeviceName(self, handle):
        switcher = {
            PCAN_NONEBUS.value: "PCAN_NONEBUS",
            PCAN_PEAKCAN.value: "PCAN_PEAKCAN",
            PCAN_ISA.value: "PCAN_ISA",
            PCAN_DNG.value: "PCAN_DNG",
            PCAN_PCI.value: "PCAN_PCI",
            PCAN_USB.value: "PCAN_USB",
            PCAN_PCC.value: "PCAN_PCC",
            PCAN_VIRTUAL.value: "PCAN_VIRTUAL",
            PCAN_LAN.value: "PCAN_LAN"
        }
        return switcher.get(handle,"UNKNOWN")   

    def ConvertBitrateToString(self, bitrate):
        m_BAUDRATES = {PCAN_BAUD_1M.value:'1 MBit/sec', PCAN_BAUD_800K.value:'800 kBit/sec', PCAN_BAUD_500K.value:'500 kBit/sec', PCAN_BAUD_250K.value:'250 kBit/sec',
                       PCAN_BAUD_125K.value:'125 kBit/sec', PCAN_BAUD_100K.value:'100 kBit/sec', PCAN_BAUD_95K.value:'95,238 kBit/sec', PCAN_BAUD_83K.value:'83,333 kBit/sec',
                       PCAN_BAUD_50K.value:'50 kBit/sec', PCAN_BAUD_47K.value:'47,619 kBit/sec', PCAN_BAUD_33K.value:'33,333 kBit/sec', PCAN_BAUD_20K.value:'20 kBit/sec',
                       PCAN_BAUD_10K.value:'10 kBit/sec', PCAN_BAUD_5K.value:'5 kBit/sec'}
        return m_BAUDRATES[bitrate.value]

TimerWrite()
