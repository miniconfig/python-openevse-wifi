import re
import requests
import datetime

from typing import (
  List,
  Optional
)


states = {
        0: 'unknown',
        1: 'not connected',
        2: 'connected',
        3: 'charging',
        4: 'vent required',
        5: 'diode check failed',
        6: 'gfci fault',
        7: 'no ground',
        8: 'stuck relay',
        9: 'gfci self-test failure',
        10: 'over temperature',
        254: 'sleeping',
        255: 'disabled'
}

colors = ['off', 'red', 'green', 'yellow', 'blue', 'violet', 'teal', 'white']


class Charger:
    def __init__(self, host: str):
        """A connection to an OpenEVSE charging station equipped with the wifi kit."""
        self.url = 'http://' + host + '/r?'

    def sendCommand(self, command: str) -> List[str]:
        """Sends a command through the web interface of the charger and parses the response"""
        data = {'rapi': command}
        content = requests.post(self.url, data=data)
        response = re.search('\\<p>&gt;\\$([^\\^]+)(\\^..)?<script', content.text)
        # If we are using version 1
        # https://github.com/OpenEVSE/ESP8266_WiFi_v1.x/blob/master/OpenEVSE_RAPI_WiFi_ESP8266.ino#L357
        if response is None:
            response = re.search('\\>\\>\\$(.+)\\<p>', content.text)
        return response.group(1).split()

    def getStatus(self) -> str:
        """Returns the charger's charge status, as a string"""
        command = '$GS'
        status = self.sendCommand(command)
        return states[int(status[1])]

    def getChargeTimeElapsed(self) -> int:
        """Returns the charge time elapsed (in seconds), or 0 if is not currently charging"""
        command = '$GS'
        status = self.sendCommand(command)
        if int(status[1]) == 3:
            return int(status[2])
        else:
            return 0

    def getTimeLimit(self) -> int:
        """Returns the time limit in minutes or 0 if no limit is set"""
        command = '$G3'
        limit = self.sendCommand(command)
        return int(limit[1])*15

    def getAmmeterScaleFactor(self) -> int:
        """Returns the ammeter's current scale factor"""
        command = '$GA'
        settings = self.sendCommand(command)
        return int(settings[1])

    def getAmmeterOffset(self) -> int:
        """Returns the ammeter's current offset"""
        command = '$GA'
        settings = self.sendCommand(command)
        return int(settings[2])

    def getMinAmps(self) -> int:
        """Returns the capacity range minimum, in amps"""
        command = '$GC'
        caprange = self.sendCommand(command)
        return int(caprange[1])

    def getMaxAmps(self) -> int:
        """Returns the capacity range maximum, in amps"""
        command = '$GC'
        caprange = self.sendCommand(command)
        return int(caprange[2])

    def getCurrentCapacity(self) -> int:
        """Returns the current capacity, in amps"""
        command = '$GE'
        settings = self.sendCommand(command)
        return int(settings[1])

    def getServiceLevel(self) -> int:
        """Returns the service level"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return (flags & 0x0001) + 1

    def getDiodeCheckEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0002)

    def getVentRequiredEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0004)

    def getGroundCheckEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0008)

    def getStuckRelayCheckEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0010)

    def getAutoServiceLevelEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0020)

    def getAutoStartEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0040)

    def getSerialDebugEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0080)

    def getLCDType(self) -> str:
        """Returns LCD type as a string, either monochrome or rgb"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        if flags & 0x0100:
            lcdtype = 'monochrome'
        else:
            lcdtype = 'rgb'
        return lcdtype

    def getGFISelfTestEnabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self.sendCommand(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0200)

    def getGFITripCount(self) -> int:
        """Returns GFI Trip Count, as integer"""
        command = '$GF'
        faults = self.sendCommand(command)
        return int(faults[1])

    def getNoGndTripCount(self) -> int:
        """Returns No Ground Trip Count, as integer"""
        command = '$GF'
        faults = self.sendCommand(command)
        return int(faults[2])

    def getStuckRelayTripCount(self) -> int:
        """Returns Stuck Relay Trip Count, as integer"""
        command = '$GF'
        faults = self.sendCommand(command)
        return int(faults[3])

    def getChargingCurrent(self) -> float:
        """Returns the charging current, in amps, or 0.0 of not charging"""
        command = '$GG'
        current_and_voltage = self.sendCommand(command)
        amps = float(current_and_voltage[1])/1000
        return amps if amps > 0 else 0.0

    def getChargingVoltage(self) -> float:
        """Returns the charging voltage, in volts, or 0.0 of not charging"""
        command = '$GG'
        current_and_voltage = self.sendCommand(command)
        volts = float(current_and_voltage[2])/1000
        return volts if volts > 0 else 0.0

    def getChargeLimit(self) -> int:
        """Returns the charge limit in kWh"""
        command = '$GH'
        limit = self.sendCommand(command)
        return int(limit[1])

    def getVoltMeterScaleFactor(self) -> int:
        """Returns the voltmeter scale factor, or 0 if there is no voltmeter"""
        command = '$GM'
        volt_meter_settings = self.sendCommand(command)
        if volt_meter_settings[0] == 'NK':
            return 0
        else:
            return int(volt_meter_settings[1])

    def getVoltMeterOffset(self) -> int:
        """Returns the voltmeter offset, or 0 if there is no voltmeter"""
        command = '$GM'
        volt_meter_settings = self.sendCommand(command)
        if volt_meter_settings[0] == 'NK':
            return 0
        else:
            return int(volt_meter_settings[2])

    def getAmbientThreshold(self) -> float:
        """Returns the ambient temperature threshold in degrees Celcius, or 0 if no Threshold is set"""
        command = '$GO'
        threshold = self.sendCommand(command)
        if threshold[0] == 'NK':
            return 0.0
        else:
            return float(threshold[1])/10

    def getIRThreshold(self) -> float:
        """Returns the IR temperature threshold in degrees Celcius, or 0 if no Threshold is set"""
        command = '$GO'
        threshold = self.sendCommand(command)
        if threshold[0] == 'NK':
            return 0.0
        else:
            return float(threshold[2])/10

    def getRTCTemperature(self) -> float:
        """Returns the temperature of the real time clock sensor (DS3231), in degrees Celcius, or 0.0 if sensor is not
        installed"""
        command = '$GP'
        temperature = self.sendCommand(command)
        return float(temperature[1])/10

    def getAmbientTemperature(self) -> float:
        """Returns the temperature of the ambient sensor (MCP9808), in degrees Celcius, or 0.0 if sensor is not
        installed"""
        command = '$GP'
        temperature = self.sendCommand(command)
        return float(temperature[2])/10

    def getIRTemperature(self) -> float:
        """Returns the temperature of the IR remote sensor (TMP007), in degrees Celcius, or 0.0 if sensor is not
        installed"""
        command = '$GP'
        temperature = self.sendCommand(command)
        return float(temperature[3])/10

    def getTime(self) -> Optional[datetime.datetime]:
        """Get the RTC time.  Returns a datetime object, or NULL if the clock is not set"""
        command = '$GT'
        time = self.sendCommand(command)
        if time == ['OK', '165', '165', '165', '165', '165', '85']:
            return None
        else:
            return datetime.datetime(year=int(time[1])+2000,
                                     month=int(time[2]),
                                     day=int(time[3]),
                                     hour=int(time[4]),
                                     minute=int(time[5]),
                                     second=int(time[6]))

    def getUsageSession(self) -> float:
        """Get the energy usage for the current charging session.  Returns the energy usage in Wh"""
        command = '$GU'
        usage = self.sendCommand(command)
        return float(usage[1])/3600

    def getUsageTotal(self) -> float:
        """Get the total energy usage.  Returns the energy usage in Wh"""
        command = '$GU'
        usage = self.sendCommand(command)
        return float(usage[2])

    def getFirmwareVersion(self) -> str:
        """Returns the Firmware Version, as a string"""
        command = '$GV'
        version = self.sendCommand(command)
        return version[1]

    def getProtocolVersion(self) -> str:
        """Returns the Protocol Version, as a string"""
        command = '$GV'
        version = self.sendCommand(command)
        return version[2]
