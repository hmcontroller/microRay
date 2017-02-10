# -*- encoding: utf-8 -*-
import ConfigParser
import json
import collections

from core.settingsModel import Settings
from core.command import Command
from core.messageData import MessageData
from core.measurementData import MeasurementData
from core.valueChannel import ValueChannel


class ModelMaker():
    def __init__(self, configFilePath):
        self.configFilePath = configFilePath
        self.config = ConfigParser.SafeConfigParser(allow_no_value=True)
        self.config.optionxform = str
        self.config.read(self.configFilePath)

    def getCommands(self):
        commands = list()
        for i, name in enumerate(self.config.options('requestedControlledParameters')):
            cmd = Command()
            cmd.value = 0
            cmd.id = i
            cmd.name = name
            commands.append(cmd)
        return commands

    def getMeasurementDataModel(self):
        model = MeasurementData()

        bufferLength = self.config.getint("misc", "bufferSizePC")
        for i, channelName in enumerate(self.config.options('requestedFastParameters')):
            channel = ValueChannel()
            channel.id = i
            channel.name = channelName
            channel.values = collections.deque(maxlen=bufferLength)
            # channel.timeValues = collections.deque(maxlen=bufferLength)
            model.channels.append(channel)
            for n in range(0, bufferLength):
                channel.values.append(0.0)
                # channel.timeValues.append(0)

        model.timeValues = collections.deque(maxlen=bufferLength)
        for i in range(0, bufferLength):
            model.timeValues.append(0.0)

        return model

    def getMessageFormatList(self):
        messagePartsList = list()

        positionCounter = 0
        channelCounter = 0

        # value channels
        for i, channelName in enumerate(self.config.options('requestedFastParameters')):
            messageData = MessageData()
            # messageData.id = i
            messageData.bitPosition = positionCounter
            messageData.lengthInBytes = 4
            messageData.dataType = float
            messageData.unpackString = "<f"
            messageData.name = channelName
            messageData.isUserChannel = True
            messagePartsList.append(messageData)
            positionCounter += messageData.lengthInBytes
            channelCounter += 1

        # TODO dirty get the additional message stuff from some single source place

        # loopStartTime
        mData = MessageData()
        # mData.id = channelCounter
        channelCounter += 1
        mData.bitPosition = positionCounter
        mData.lengthInBytes = 4
        positionCounter += mData.lengthInBytes
        mData.dataType = int
        mData.unpackString = "<i"
        mData.name = "loopStartTime"
        messagePartsList.append(mData)

        # lastLoopDuration
        mData1 = MessageData()
        # mData1.id = channelCounter
        channelCounter += 1
        mData1.bitPosition = positionCounter
        mData1.lengthInBytes = 4
        positionCounter += mData1.lengthInBytes
        mData1.dataType = int
        mData1.unpackString = "<i"
        mData1.name = "lastLoopDuration"
        messagePartsList.append(mData1)

        # parameterNumber
        mData2 = MessageData()
        # mData2.id = channelCounter
        channelCounter += 1
        mData2.bitPosition = positionCounter
        mData2.lengthInBytes = 4
        positionCounter += mData2.lengthInBytes
        mData2.dataType = int
        mData2.unpackString = "<i"
        mData2.name = "parameterNumber"
        messagePartsList.append(mData2)

        # parameterValue
        mData3 = MessageData()
        # mData3.id = channelCounter
        channelCounter += 1
        mData3.bitPosition = positionCounter
        mData3.lengthInBytes = 4
        positionCounter += mData3.lengthInBytes
        mData3.dataType = float
        mData3.unpackString = "<f"
        mData3.name = "parameterValue"
        messagePartsList.append(mData3)

        return messagePartsList

    def getSensorMapping(self):
        mappingString = self.config.get("Sensors", "mapping")
        mappingString = mappingString.replace("\n", "").replace(" ", "")
        return json.loads(mappingString)

    def getMiscSettings(self):
        settingsModel = Settings()
        settingsModel.controllerLoopCycleTime = self.config.getint("misc", "loopCycleTimeUS")
        settingsModel.bufferLength = self.config.getint("misc", "bufferSizePC")
        settingsModel.plotUpdateTimeSpanInMs = self.config.getint("misc", "plotUpdateTimeSpanInMs")
        settingsModel.controlUpdateTimeSpanInMs = self.config.getint("misc", "controlUpdateTimeSpanInMs")
        return settingsModel
