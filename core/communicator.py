# -*- encoding: utf-8 -*-

import socket
import errno
import struct
from collections import deque

from PyQt4 import QtCore

from core.messageData import MessageData


class Communicator(QtCore.QObject):
    def __init__(self, settings):
        super(Communicator, self).__init__()

        self._settings = settings
        self._messageSize = None
        self._messageMap = None

        self._directCommandSendBuffer = deque()
        self._pendingCommandSendBuffer = deque()

        self._sendTimer = QtCore.QTimer()
        self._sendTimer.setSingleShot(False)
        self._sendTimer.timeout.connect(self.sendPerTimer)
        self._sendTimer.start(settings.sendMessageIntervalLengthInMs)

    def setMessageMap(self, formatList):
        self._messageMap = formatList
        self._messageSize = self._messageMap[-1].positionInBytes + self._messageMap[-1].lengthInBytes

    def send(self, commandList):
        raise NotImplementedError()

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        raise NotImplementedError()

    def _packCommand(self, command):
        return struct.pack("<1i1f", command.id, command.getValue())

    def _unpack(self, rawPackets):
        # TODO - think about how to single source the packet configuration
        # TODO at the time being the source is in types.h -> messageOut in the microcontroller code

        unpackedMessages = list()

        for rawPacket in rawPackets:
            message = list()
            for messagePartInfo in self._messageMap:
                messagePart = MessageData()
                rawPart = rawPacket[messagePartInfo.positionInBytes : messagePartInfo.positionInBytes + messagePartInfo.lengthInBytes]

                # only these values are changed, the others are just copied
                messagePart.value = struct.unpack(messagePartInfo.unpackString, rawPart)[0]

                messagePart.positionInBytes = messagePartInfo.positionInBytes
                messagePart.lengthInBytes = messagePartInfo.lengthInBytes
                messagePart.dataType = messagePartInfo.dataType
                messagePart.unpackString = messagePartInfo.unpackString
                messagePart.name = messagePartInfo.name
                messagePart.isUserChannel = messagePartInfo.isUserChannel
                messagePart.userChannelId = messagePartInfo.userChannelId

                message.append(messagePart)

            unpackedMessages.append(message)

        return unpackedMessages


class UdpCommunicator(Communicator):
    def __init__(self, settings):
        super(UdpCommunicator, self).__init__(settings)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self._settings.computerIP, self._settings.udpPort))
        self.socket.setblocking(False)
        self.socket.settimeout(0)

    def send(self, commandList):
        if len(commandList.changedCommands) > 0:
            commandToSend = commandList.changedCommands.popleft()
            packedData = self._packCommand(commandToSend)
            self.socket.sendto(packedData, (self._settings.controllerIP, self._settings.udpPort))
            print "command send", commandToSend.id, commandToSend.name, commandToSend.getValue()

    def sendPerTimer(self):
        pass

    def sendPendingCommands(self):
        pass

    def receive(self):
        packets = list()
        while True:
            try:
                data, address = self.socket.recvfrom(self._messageSize)
                packets.append(data)
            except socket.timeout:
                break
            except socket.error, e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                else:
                    raise

        return self._unpack(packets)




class UsbHidCommunicator(Communicator):
    def __init__(self, settings):
        super(UsbHidCommunicator, self).__init__(settings)

    def send(self, commandList):
        pass

    def receive(self):
        pass