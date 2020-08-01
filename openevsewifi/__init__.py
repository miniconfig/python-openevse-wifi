import re
import requests
import datetime
import json

from deprecated import deprecated
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


class BadChecksum(Exception):
    pass


class BadResponse(Exception):
    pass


class InvalidAuthentication(Exception):
    pass


def parse_checksum(s):
    """
    If there is a '^' in given string s, this checks that the xor of utf8 bytes
    before the '^' equal the hex value specified after '^'.  It returns the
    string before the '^' on success, and throws an BadChecksum exception on error.

    If there is no '^' in the string, the string is returned.
    """
    spl = s.rsplit('^', 1)
    if len(spl) == 1:
        return s
    try:
        check = int(spl[1], 16)
    except ValueError:
        raise BadChecksum(s)
    datsum = 0
    for c in spl[0].encode('utf-8'):
        datsum ^= c
    if datsum != check:
        raise BadChecksum(s)
    return spl[0]


def json_parser(s):
    """
    Parses the json string provided and checks that
    the "ret" field has a valid checksum.

    Throws JSONDecodeError if the json is invalid,
    openevsewifi.BadChecksum if the checksum is invalid,
    and openevsewifi.BadResponse if the expected "ret"
    element is not present in the json dictionary.
    """
    result = json.loads(s)
    if "ret" not in result:
        raise BadResponse(s)
    parsed = parse_checksum(result["ret"])
    # for compatibility with xml_parser, strip off the leading $.
    parsed = parsed[1:]
    return parsed.split()


def xml_parser(s):
    response = re.search('\\<p>&gt;\\$([^\\^]+)(\\^..)?<script', s)
    # If we are using version 1
    # https://github.com/OpenEVSE/ESP8266_WiFi_v1.x/blob/master/OpenEVSE_RAPI_WiFi_ESP8266.ino#L357
    if response is None:
        response = re.search('\\>\\>\\$(.+)\\<p>', s)
    return response.group(1).split()


class Charger:
    def __init__(self, host: str, json: bool = False, username: str = None, password: str = None):
        """A connection to an OpenEVSE charging station equipped with the wifi kit."""
        if json:
            self._url = 'http://' + host + '/r?json=1&'
            self._parseResult = json_parser
        else:
            self._url = 'http://' + host + '/r?'
            self._parseResult = xml_parser
        self._username = username
        self._password = password

    def _send_command(self, command: str) -> List[str]:
        """Sends a command through the web interface of the charger and parses the response"""
        data = {'rapi': command}
        if self._username and self._password:
            content = requests.post(self._url, data=data, auth=(self._username, self._password))
        else:
            content = requests.post(self._url, data=data)
        if content.status_code == 401:
            raise InvalidAuthentication
        else:
            return self._parseResult(content.text)

    @deprecated(reason='Use the status property')
    def getStatus(self) -> str:
        return self.status

    @property
    def status(self) -> str:
        """Returns the charger's charge status, as a string"""
        command = '$GS'
        status = self._send_command(command)
        return states[int(status[1])]

    @deprecated(reason='Use the charge_time_elapsed property')
    def getChargeTimeElapsed(self) -> int:
        return self.charge_time_elapsed

    @property
    def charge_time_elapsed(self) -> int:
        """Returns the charge time elapsed (in seconds), or 0 if is not currently charging"""
        command = '$GS'
        status = self._send_command(command)
        if int(status[1]) == 3:
            return int(status[2])
        else:
            return 0

    @deprecated(reason='Use time_limit property')
    def getTimeLimit(self) -> int:
        return self.time_limit

    @property
    def time_limit(self) -> int:
        """Returns the time limit in minutes or 0 if no limit is set"""
        command = '$G3'
        limit = self._send_command(command)
        return int(limit[1])*15

    @deprecated(reason='Use ammeter_scale_factor property')
    def getAmmeterScaleFactor(self) -> int:
        return self.ammeter_scale_factor

    @property
    def ammeter_scale_factor(self) -> int:
        """Returns the ammeter's current scale factor"""
        command = '$GA'
        settings = self._send_command(command)
        return int(settings[1])

    @deprecated(reason='Use ammeter_offset property')
    def getAmmeterOffset(self) -> int:
        return self.ammeter_offset

    @property
    def ammeter_offset(self) -> int:
        """Returns the ammeter's current offset"""
        command = '$GA'
        settings = self._send_command(command)
        return int(settings[2])

    @deprecated(reason='Use min_amps property')
    def getMinAmps(self) -> int:
        return self.min_amps

    @property
    def min_amps(self) -> int:
        """Returns the capacity range minimum, in amps"""
        command = '$GC'
        caprange = self._send_command(command)
        return int(caprange[1])

    @deprecated(reason='Use max_amps property')
    def getMaxAmps(self) -> int:
        return self.max_amps

    @property
    def max_amps(self) -> int:
        """Returns the capacity range maximum, in amps"""
        command = '$GC'
        caprange = self._send_command(command)
        return int(caprange[2])

    @deprecated(reason='Use current_capacity property')
    def getCurrentCapacity(self) -> int:
        return self.current_capacity

    @property
    def current_capacity(self) -> int:
        """Returns the current capacity, in amps"""
        command = '$GE'
        settings = self._send_command(command)
        return int(settings[1])

    @deprecated(reason='Use service_level property')
    def getServiceLevel(self) -> int:
        return self.service_level

    @property
    def service_level(self) -> int:
        """Returns the service level"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return (flags & 0x0001) + 1

    @deprecated(reason='Use diode_check_enabled property')
    def getDiodeCheckEnabled(self) -> bool:
        return self.diode_check_enabled

    @property
    def diode_check_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0002)

    @deprecated(reason='Use vent_required_enabled property')
    def getVentRequiredEnabled(self) -> bool:
        return self.vent_required_enabled

    @property
    def vent_required_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0004)

    @deprecated(reason='Use ground_check_enabled property')
    def getGroundCheckEnabled(self) -> bool:
        return self.ground_check_enabled

    @property
    def ground_check_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0008)

    @deprecated(reason='Use stuck_relay_check_enabled property')
    def getStuckRelayCheckEnabled(self) -> bool:
        return self.stuck_relay_check_enabled

    @property
    def stuck_relay_check_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0010)

    @deprecated(reason='Use auto_service_level_enabled property')
    def getAutoServiceLevelEnabled(self) -> bool:
        return self.auto_service_level_enabled

    @property
    def auto_service_level_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0020)

    @deprecated(reason='Use auto_start_enabled property')
    def getAutoStartEnabled(self) -> bool:
        return self.auto_start_enabled

    @property
    def auto_start_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0040)

    @deprecated(reason='Use serial_debug_enabled property')
    def getSerialDebugEnabled(self) -> bool:
        return self.serial_debug_enabled

    @property
    def serial_debug_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0080)

    @deprecated(reason='Use lcd_type property')
    def getLCDType(self) -> str:
        return self.lcd_type

    @property
    def lcd_type(self) -> str:
        """Returns LCD type as a string, either monochrome or rgb"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        if flags & 0x0100:
            lcdtype = 'monochrome'
        else:
            lcdtype = 'rgb'
        return lcdtype

    @deprecated(reason='Use gfi_self_test_enabled property')
    def getGFISelfTestEnabled(self) -> bool:
        return self.gfi_self_test_enabled

    @property
    def gfi_self_test_enabled(self) -> bool:
        """Returns True if enabled, False if disabled"""
        command = '$GE'
        settings = self._send_command(command)
        flags = int(settings[2], 16)
        return not (flags & 0x0200)

    @deprecated(reason='Use gfi_trip_count property')
    def getGFITripCount(self) -> int:
        return self.gfi_trip_count

    @property
    def gfi_trip_count(self) -> int:
        """Returns GFI Trip Count, as integer"""
        command = '$GF'
        faults = self._send_command(command)
        return int(faults[1])

    @deprecated(reason='Use no_gnd_trip_count property')
    def getNoGndTripCount(self) -> int:
        return self.no_gnd_trip_count

    @property
    def no_gnd_trip_count(self) -> int:
        """Returns No Ground Trip Count, as integer"""
        command = '$GF'
        faults = self._send_command(command)
        return int(faults[2])

    @deprecated(reason='Use stuck_relay_trip_count property')
    def getStuckRelayTripCount(self) -> int:
        return self.stuck_relay_trip_count

    @property
    def stuck_relay_trip_count(self) -> int:
        """Returns Stuck Relay Trip Count, as integer"""
        command = '$GF'
        faults = self._send_command(command)
        return int(faults[3])

    @deprecated(reason='Use charging_current property')
    def getChargingCurrent(self) -> float:
        return self.charging_current

    @property
    def charging_current(self) -> float:
        """Returns the charging current, in amps, or 0.0 of not charging"""
        command = '$GG'
        current_and_voltage = self._send_command(command)
        amps = float(current_and_voltage[1])/1000
        return amps if amps > 0 else 0.0

    @deprecated(reason='Use charging_voltage property')
    def getChargingVoltage(self) -> float:
        return self.charging_voltage

    @property
    def charging_voltage(self) -> float:
        """Returns the charging voltage, in volts, or 0.0 of not charging"""
        command = '$GG'
        current_and_voltage = self._send_command(command)
        volts = float(current_and_voltage[2])/1000
        return volts if volts > 0 else 0.0

    @deprecated(reason='Use charge_limit property')
    def getChargeLimit(self) -> int:
        return self.charge_limit

    @property
    def charge_limit(self) -> int:
        """Returns the charge limit in kWh"""
        command = '$GH'
        limit = self._send_command(command)
        return int(limit[1])

    @deprecated(reason='Use volt_meter_scale_factor property')
    def getVoltMeterScaleFactor(self) -> int:
        return self.volt_meter_scale_factor

    @property
    def volt_meter_scale_factor(self) -> int:
        """Returns the voltmeter scale factor, or 0 if there is no voltmeter"""
        command = '$GM'
        volt_meter_settings = self._send_command(command)
        if volt_meter_settings[0] == 'NK':
            return 0
        else:
            return int(volt_meter_settings[1])

    @deprecated(reason='Use volt_meter_offset property')
    def getVoltMeterOffset(self) -> int:
        return self.volt_meter_offset

    @property
    def volt_meter_offset(self) -> int:
        """Returns the voltmeter offset, or 0 if there is no voltmeter"""
        command = '$GM'
        volt_meter_settings = self._send_command(command)
        if volt_meter_settings[0] == 'NK':
            return 0
        else:
            return int(volt_meter_settings[2])

    @deprecated(reason='Use ambient_threshold property')
    def getAmbientThreshold(self) -> float:
        return self.ambient_threshold

    @property
    def ambient_threshold(self) -> float:
        """Returns the ambient temperature threshold in degrees Celcius, or 0 if no Threshold is set"""
        command = '$GO'
        threshold = self._send_command(command)
        if threshold[0] == 'NK':
            return 0.0
        else:
            return float(threshold[1])/10

    @deprecated(reason='Use ir_threshold property')
    def getIRThreshold(self) -> float:
        return self.ir_threshold

    @property
    def ir_threshold(self) -> float:
        """Returns the IR temperature threshold in degrees Celcius, or 0 if no Threshold is set"""
        command = '$GO'
        threshold = self._send_command(command)
        if threshold[0] == 'NK':
            return 0.0
        else:
            return float(threshold[2])/10

    @deprecated(reason='Use rtc_temperature property')
    def getRTCTemperature(self) -> float:
        return self.rtc_temperature

    @property
    def rtc_temperature(self) -> float:
        """Returns the temperature of the real time clock sensor (DS3231), in degrees Celcius, or 0.0 if sensor is not
        installed"""
        command = '$GP'
        temperature = self._send_command(command)
        return float(temperature[1])/10

    @deprecated(reason='Use ambient_temperature property')
    def getAmbientTemperature(self) -> float:
        return self.ambient_temperature

    @property
    def ambient_temperature(self) -> float:
        """Returns the temperature of the ambient sensor (MCP9808), in degrees Celcius, or 0.0 if sensor is not
        installed"""
        command = '$GP'
        temperature = self._send_command(command)
        return float(temperature[2])/10

    @deprecated(reason='Use ir_temperature property')
    def getIRTemperature(self) -> float:
        return self.ir_temperature

    @property
    def ir_temperature(self) -> float:
        """Returns the temperature of the IR remote sensor (TMP007), in degrees Celcius, or 0.0 if sensor is not
        installed"""
        command = '$GP'
        temperature = self._send_command(command)
        return float(temperature[3])/10

    @deprecated(reason='Use the time property')
    def getTime(self) -> Optional[datetime.datetime]:
        return self.time

    @property
    def time(self) -> Optional[datetime.datetime]:
        """Get the RTC time.  Returns a datetime object, or NULL if the clock is not set"""
        command = '$GT'
        time = self._send_command(command)
        if time == ['OK', '165', '165', '165', '165', '165', '85']:
            return None
        else:
            return datetime.datetime(year=int(time[1])+2000,
                                     month=int(time[2]),
                                     day=int(time[3]),
                                     hour=int(time[4]),
                                     minute=int(time[5]),
                                     second=int(time[6]))

    @deprecated(reason='Use usage_session property')
    def getUsageSession(self) -> float:
        return self.usage_session

    @property
    def usage_session(self) -> float:
        """Get the energy usage for the current charging session.  Returns the energy usage in Wh"""
        command = '$GU'
        usage = self._send_command(command)
        return float(usage[1])/3600

    @deprecated(reason='Use usage_total property')
    def getUsageTotal(self) -> float:
        return self.usage_total

    @property
    def usage_total(self) -> float:
        """Get the total energy usage.  Returns the energy usage in Wh"""
        command = '$GU'
        usage = self._send_command(command)
        return float(usage[2])

    @deprecated(reason='Use firmware_version property')
    def getFirmwareVersion(self) -> str:
        return self.firmware_version

    @property
    def firmware_version(self) -> str:
        """Returns the Firmware Version, as a string"""
        command = '$GV'
        version = self._send_command(command)
        return version[1]

    @deprecated(reason='Use protocol_version property')
    def getProtocolVersion(self) -> str:
        return self.protocol_version

    @property
    def protocol_version(self) -> str:
        """Returns the Protocol Version, as a string"""
        command = '$GV'
        version = self._send_command(command)
        return version[2]
