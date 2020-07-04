import pytest

from tests.utils import load_fixture


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/status_unplugged.txt', 'not connected'),
                          ('v1_responses/status_charging.txt', 'charging')])
def test_get_status(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    status = test_charger.getStatus()
    assert status == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/status_unplugged.txt', 0),
                          ('v1_responses/status_charging.txt', 568)])
def test_get_charge_time_elapsed(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    charge_time = test_charger.getChargeTimeElapsed()
    assert charge_time == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/time_limit_unset.txt', 0),
                          ('v1_responses/time_limit_set.txt', 630)])
def test_get_time_limit(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    time_limit = test_charger.getTimeLimit()
    assert time_limit == expected


def test_get_ammeter_scale_factor(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/ammeter.txt'))
    scale_factor = test_charger.getAmmeterScaleFactor()
    assert scale_factor == 220


def test_get_ammeter_offsset(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/ammeter.txt'))
    offset = test_charger.getAmmeterOffset()
    assert offset == 0


def test_get_min_amps(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/capacity_range.txt'))
    amps = test_charger.getMinAmps()
    assert amps == 6


def test_get_max_amps(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/capacity_range.txt'))
    amps = test_charger.getMaxAmps()
    assert amps == 80


def test_get_current_capacity(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    amps = test_charger.getCurrentCapacity()
    assert amps == 50


def test_get_service_level(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    level = test_charger.getServiceLevel()
    assert level == 2


def test_get_diode_check_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getDiodeCheckEnabled()
    assert enabled is True


def test_get_vent_required_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getVentRequiredEnabled()
    assert enabled is True


def test_get_ground_check_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getGroundCheckEnabled()
    assert enabled is True


def test_get_stuck_relay_check_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getGroundCheckEnabled()
    assert enabled is True


def test_get_auto_service_level_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getAutoServiceLevelEnabled()
    assert enabled is False


def test_get_auto_start_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getAutoStartEnabled()
    assert enabled is True


def test_get_serial_debug_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getDiodeCheckEnabled()
    assert enabled is True


def test_get_lcd_type(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    lcd_type = test_charger.getLCDType()
    assert lcd_type == 'rgb'


def test_get_gfi_self_test_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.getGFISelfTestEnabled()
    assert enabled is False


def test_get_gfi_trip_count(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/faults.txt'))
    count = test_charger.getGFITripCount()
    assert count == 0


def test_get_no_ground_trip_count(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/faults.txt'))
    count = test_charger.getNoGndTripCount()
    assert count == 9


def test_get_stuck_relay_trip_count(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/faults.txt'))
    count = test_charger.getStuckRelayTripCount()
    assert count == 0


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/charging_values_unplugged.txt', 0.0),
                          ('v1_responses/charging_values_charging.txt', 10.34)])
def test_get_charging_current(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    current = test_charger.getChargingCurrent()
    assert current == expected
    assert type(current) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/charging_values_unplugged.txt', 0.0),
                          ('v1_responses/charging_values_charging.txt', 0.0)])
def test_get_charging_voltage(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    voltage = test_charger.getChargingVoltage()
    assert voltage == expected
    assert type(voltage) == float


def test_get_charge_limit(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/charge_limit.txt'))
    limit = test_charger.getChargeLimit()
    assert limit == 0


def test_get_voltmeter_scale_factor(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/voltmeter_settings.txt'))
    scale = test_charger.getVoltMeterScaleFactor()
    assert scale == 0


def test_get_voltmeter_offset(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/voltmeter_settings.txt'))
    offset = test_charger.getVoltMeterOffset()
    assert offset == 0


def test_get_ambient_threshold(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/temperature_settings.txt'))
    threshold = test_charger.getAmbientThreshold()
    assert threshold == 0.0
    assert type(threshold) == float


def test_get_ir_threshold(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/temperature_settings.txt'))
    threshold = test_charger.getIRThreshold()
    assert threshold == 0.0
    assert type(threshold) == float


def test_get_rtc_temperature(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/temperature_values.txt'))
    temperature = test_charger.getRTCTemperature()
    assert temperature == 59.2
    assert type(temperature) == float


def test_get_ambient_temperature(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/temperature_values.txt'))
    temperature = test_charger.getAmbientTemperature()
    assert temperature == 0.0
    assert type(temperature) == float


def test_get_ir_temperature(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/temperature_values.txt'))
    temperature = test_charger.getIRTemperature()
    assert temperature == 23.0
    assert type(temperature) == float


def test_get_time(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/time.txt'))
    time = test_charger.getTime()
    assert str(time) == '2000-01-20 08:34:29'


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/usage_unplugged.txt', 0.0),
                          ('v1_responses/usage_charging.txt', 779.8663888888889)])
def test_get_usage_session(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    usage = test_charger.getUsageSession()
    assert usage == expected
    assert type(usage) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/usage_unplugged.txt', 12419994.0),
                          ('v1_responses/usage_charging.txt', 12419994.0)])
def test_get_usage_total(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger.url, text=load_fixture(fixture))
    usage = test_charger.getUsageTotal()
    assert usage == expected
    assert type(usage) == float


def test_get_firmware_version(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/version.txt'))
    version = test_charger.getFirmwareVersion()
    assert version == '3.11.3'
    assert type(version) == str


def test_get_protocol_version(test_charger, requests_mock):
    requests_mock.post(test_charger.url, text=load_fixture('v1_responses/version.txt'))
    version = test_charger.getProtocolVersion()
    assert version == '1.0.3'
    assert type(version) == str

def test_checksum():
    import openevsewifi
    strings = ["$OK 1 0^21", "$OK 220 0^20", "$OK 30 0001^22", "$OK 0 -1^0C"]
    for s in strings:
        assert openevsewifi.parse_checksum(s) == s.split('^', 1)[0]
    bad_checksums = ["$OK 1 0^22", "$OK 220 0^30", "$OK 30 0001^f2", "$OK 0 -1^1C"]
    for s in bad_checksums:
        assert openevsewifi.parse_checksum(s) is None
    no_checksums = ["$OK 1 0", "$OK 220 0", "$OK 30 0001", "$OK 0 -1"]
    for s in no_checksums:
        assert openevsewifi.parse_checksum(s) == s
