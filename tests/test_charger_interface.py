import pytest

from tests.utils import load_fixture


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/status_unplugged.txt', 'not connected'),
                          ('v1_responses/status_charging.txt', 'charging')])
def test_get_status_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        status = test_charger.getStatus()
    assert status == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/status_unplugged.txt', 'not connected'),
                          ('v1_responses/status_charging.txt', 'charging')])
def test_get_status(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    status = test_charger.status
    assert status == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/status_unplugged.txt', 0),
                          ('v1_responses/status_charging.txt', 568)])
def test_get_charge_time_elapsed_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        charge_time = test_charger.getChargeTimeElapsed()
    assert charge_time == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/status_unplugged.txt', 0),
                          ('v1_responses/status_charging.txt', 568)])
def test_get_charge_time_elapsed(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    charge_time = test_charger.charge_time_elapsed
    assert charge_time == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/time_limit_unset.txt', 0),
                          ('v1_responses/time_limit_set.txt', 630)])
def test_get_time_limit_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        time_limit = test_charger.getTimeLimit()
    assert time_limit == expected


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/time_limit_unset.txt', 0),
                          ('v1_responses/time_limit_set.txt', 630)])
def test_get_time_limit(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    time_limit = test_charger.time_limit
    assert time_limit == expected


def test_get_ammeter_scale_factor_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/ammeter.txt'))
    with pytest.deprecated_call():
        scale_factor = test_charger.getAmmeterScaleFactor()
    assert scale_factor == 220


def test_get_ammeter_scale_factor(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/ammeter.txt'))
    scale_factor = test_charger.ammeter_scale_factor
    assert scale_factor == 220


def test_get_ammeter_offset_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/ammeter.txt'))
    with pytest.deprecated_call():
        offset = test_charger.getAmmeterOffset()
    assert offset == 0


def test_get_ammeter_offset(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/ammeter.txt'))
    offset = test_charger.ammeter_offset
    assert offset == 0


def test_get_min_amps_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/capacity_range.txt'))
    with pytest.deprecated_call():
        amps = test_charger.getMinAmps()
    assert amps == 6


def test_get_min_amps(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/capacity_range.txt'))
    amps = test_charger.min_amps
    assert amps == 6


def test_get_max_amps_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/capacity_range.txt'))
    with pytest.deprecated_call():
        amps = test_charger.getMaxAmps()
    assert amps == 80


def test_get_max_amps(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/capacity_range.txt'))
    amps = test_charger.max_amps
    assert amps == 80


def test_get_current_capacity_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        amps = test_charger.getCurrentCapacity()
    assert amps == 50


def test_get_current_capacity(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    amps = test_charger.current_capacity
    assert amps == 50


def test_get_service_level_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        level = test_charger.getServiceLevel()
    assert level == 2


def test_get_service_level(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    level = test_charger.service_level
    assert level == 2


def test_get_diode_check_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getDiodeCheckEnabled()
    assert enabled is True


def test_get_diode_check_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.diode_check_enabled
    assert enabled is True


def test_get_vent_required_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getVentRequiredEnabled()
    assert enabled is True


def test_get_vent_required_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.vent_required_enabled
    assert enabled is True


def test_get_ground_check_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getGroundCheckEnabled()
    assert enabled is True


def test_get_ground_check_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.ground_check_enabled
    assert enabled is True


def test_get_stuck_relay_check_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getStuckRelayCheckEnabled()
    assert enabled is True


def test_get_stuck_relay_check_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.stuck_relay_check_enabled
    assert enabled is True


def test_get_auto_service_level_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getAutoServiceLevelEnabled()
    assert enabled is False


def test_get_auto_service_level_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.auto_service_level_enabled
    assert enabled is False


def test_get_auto_start_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getAutoStartEnabled()
    assert enabled is True


def test_get_auto_start_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.auto_start_enabled
    assert enabled is True


def test_get_serial_debug_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getSerialDebugEnabled()
    assert enabled is True


def test_get_serial_debug_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.serial_debug_enabled
    assert enabled is True


def test_get_lcd_type_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        lcd_type = test_charger.getLCDType()
    assert lcd_type == 'rgb'


def test_get_lcd_type(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    lcd_type = test_charger.lcd_type
    assert lcd_type == 'rgb'


def test_get_gfi_self_test_enabled_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    with pytest.deprecated_call():
        enabled = test_charger.getGFISelfTestEnabled()
    assert enabled is False


def test_get_gfi_self_test_enabled(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/settings.txt'))
    enabled = test_charger.gfi_self_test_enabled
    assert enabled is False


def test_get_gfi_trip_count_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/faults.txt'))
    with pytest.deprecated_call():
        count = test_charger.getGFITripCount()
    assert count == 0


def test_get_gfi_trip_count(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/faults.txt'))
    count = test_charger.gfi_trip_count
    assert count == 0


def test_get_no_ground_trip_count_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/faults.txt'))
    with pytest.deprecated_call():
        count = test_charger.getNoGndTripCount()
    assert count == 9


def test_get_no_ground_trip_count(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/faults.txt'))
    count = test_charger.no_gnd_trip_count
    assert count == 9


def test_get_stuck_relay_trip_count_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/faults.txt'))
    with pytest.deprecated_call():
        count = test_charger.getStuckRelayTripCount()
    assert count == 0


def test_get_stuck_relay_trip_count(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/faults.txt'))
    count = test_charger.stuck_relay_trip_count
    assert count == 0


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/charging_values_unplugged.txt', 0.0),
                          ('v1_responses/charging_values_charging.txt', 10.34)])
def test_get_charging_current_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        current = test_charger.getChargingCurrent()
    assert current == expected
    assert type(current) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/charging_values_unplugged.txt', 0.0),
                          ('v1_responses/charging_values_charging.txt', 10.34)])
def test_get_charging_current(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    current = test_charger.charging_current
    assert current == expected
    assert type(current) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/charging_values_unplugged.txt', 0.0),
                          ('v1_responses/charging_values_charging.txt', 0.0)])
def test_get_charging_voltage_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        voltage = test_charger.getChargingVoltage()
    assert voltage == expected
    assert type(voltage) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/charging_values_unplugged.txt', 0.0),
                          ('v1_responses/charging_values_charging.txt', 0.0)])
def test_get_charging_voltage(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    voltage = test_charger.charging_voltage
    assert voltage == expected
    assert type(voltage) == float


def test_get_charge_limit_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/charge_limit.txt'))
    with pytest.deprecated_call():
        limit = test_charger.getChargeLimit()
    assert limit == 0


def test_get_charge_limit(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/charge_limit.txt'))
    limit = test_charger.charge_limit
    assert limit == 0


def test_get_voltmeter_scale_factor_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/voltmeter_settings.txt'))
    with pytest.deprecated_call():
        scale = test_charger.getVoltMeterScaleFactor()
    assert scale == 0


def test_get_voltmeter_scale_factor(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/voltmeter_settings.txt'))
    scale = test_charger.volt_meter_scale_factor
    assert scale == 0


def test_get_voltmeter_offset_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/voltmeter_settings.txt'))
    with pytest.deprecated_call():
        offset = test_charger.getVoltMeterOffset()
    assert offset == 0


def test_get_voltmeter_offset(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/voltmeter_settings.txt'))
    offset = test_charger.volt_meter_offset
    assert offset == 0


def test_get_ambient_threshold_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_settings.txt'))
    with pytest.deprecated_call():
        threshold = test_charger.getAmbientThreshold()
    assert threshold == 0.0
    assert type(threshold) == float


def test_get_ambient_threshold(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_settings.txt'))
    threshold = test_charger.ambient_threshold
    assert threshold == 0.0
    assert type(threshold) == float


def test_get_ir_threshold_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_settings.txt'))
    with pytest.deprecated_call():
        threshold = test_charger.getIRThreshold()
    assert threshold == 0.0
    assert type(threshold) == float


def test_get_ir_threshold(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_settings.txt'))
    threshold = test_charger.ir_threshold
    assert threshold == 0.0
    assert type(threshold) == float


def test_get_rtc_temperature_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_values.txt'))
    with pytest.deprecated_call():
        temperature = test_charger.getRTCTemperature()
    assert temperature == 59.2
    assert type(temperature) == float


def test_get_rtc_temperature(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_values.txt'))
    temperature = test_charger.rtc_temperature
    assert temperature == 59.2
    assert type(temperature) == float


def test_get_ambient_temperature_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_values.txt'))
    with pytest.deprecated_call():
        temperature = test_charger.getAmbientTemperature()
    assert temperature == 0.0
    assert type(temperature) == float


def test_get_ambient_temperature(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_values.txt'))
    temperature = test_charger.ambient_temperature
    assert temperature == 0.0
    assert type(temperature) == float


def test_get_ir_temperature_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_values.txt'))
    with pytest.deprecated_call():
        temperature = test_charger.getIRTemperature()
    assert temperature == 23.0
    assert type(temperature) == float


def test_get_ir_temperature(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/temperature_values.txt'))
    temperature = test_charger.ir_temperature
    assert temperature == 23.0
    assert type(temperature) == float


def test_get_time_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/time.txt'))
    with pytest.deprecated_call():
        time = test_charger.getTime()
    assert str(time) == '2000-01-20 08:34:29'


def test_get_time(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/time.txt'))
    time = test_charger.time
    assert str(time) == '2000-01-20 08:34:29'


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/usage_unplugged.txt', 0.0),
                          ('v1_responses/usage_charging.txt', 779.8663888888889)])
def test_get_usage_session_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        usage = test_charger.getUsageSession()
    assert usage == expected
    assert type(usage) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/usage_unplugged.txt', 0.0),
                          ('v1_responses/usage_charging.txt', 779.8663888888889)])
def test_get_usage_session(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    usage = test_charger.usage_session
    assert usage == expected
    assert type(usage) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/usage_unplugged.txt', 12419994.0),
                          ('v1_responses/usage_charging.txt', 12419994.0)])
def test_get_usage_total_deprecated(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    with pytest.deprecated_call():
        usage = test_charger.getUsageTotal()
    assert usage == expected
    assert type(usage) == float


@pytest.mark.parametrize('fixture, expected',
                         [('v1_responses/usage_unplugged.txt', 12419994.0),
                          ('v1_responses/usage_charging.txt', 12419994.0)])
def test_get_usage_total(test_charger, requests_mock, fixture, expected):
    requests_mock.post(test_charger._url, text=load_fixture(fixture))
    usage = test_charger.usage_total
    assert usage == expected
    assert type(usage) == float


def test_get_firmware_version_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/version.txt'))
    with pytest.deprecated_call():
        version = test_charger.getFirmwareVersion()
    assert version == '3.11.3'
    assert type(version) == str


def test_get_firmware_version(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/version.txt'))
    version = test_charger.firmware_version
    assert version == '3.11.3'
    assert type(version) == str


def test_get_protocol_version_deprecated(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/version.txt'))
    with pytest.deprecated_call():
        version = test_charger.getProtocolVersion()
    assert version == '1.0.3'
    assert type(version) == str


def test_get_protocol_version(test_charger, requests_mock):
    requests_mock.post(test_charger._url, text=load_fixture('v1_responses/version.txt'))
    version = test_charger.protocol_version
    assert version == '1.0.3'
    assert type(version) == str
