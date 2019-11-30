import logging
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_NAME
from .const import DOMAIN, DEVICE_INSTANCE

_LOGGER = logging.getLogger(__name__)


UNITS = {
    "distance": "m",
    "total_distance": "m",
    "gps_speed": "km/h",
    "speed": "km/h",
    "voltage": "V",
    "current": "A",
    "power": "W",
    "battery_level": "%",
    "system_temp": "°C",
    "cpu_temp": "°C",
}
SELECTED_METRICS = {
    "gps_speed",
    "speed",
    "voltage",
    "current",
    "power",
    "battery_level",
    "total_distance",
    "system_temp",
    "cpu_temp",
    "mode",
    "alert",
}


async def async_setup_entry(hass, config_entry, async_add_entities) -> bool:
    device = hass.data[DOMAIN][DEVICE_INSTANCE][config_entry.entry_id]
    device_name = config_entry.data[CONF_NAME]
    entities = [
        EUCSensor(device, device_name, name, unit=UNITS.get(name))
        for name in SELECTED_METRICS
    ]
    async_add_entities(entities, True)
    return True


class EUCSensor(Entity):
    def __init__(self, euc_device, device_name, kind, unit=None):
        self.euc_device = euc_device
        self.device_name = device_name
        self.kind = kind
        self._unit_of_measurement = unit
        self._state = None
        self.euc_device.add_property_changed_callback(self.on_property_changed, prop_name=self.kind)

    should_poll = False

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def unique_id(self):
        return f"{self.euc_device.unique_id}-{self.kind}"

    @property
    def name(self):
        return f"{self.device_name} {self.kind}"

    @property
    def state(self):
        return self._state

    def on_property_changed(self, euc_device, prop_name, value):
        self._state = value
        self.async_schedule_update_ha_state()


class EUCBattery(EUCSensor):
    unit_of_measurement = "%"
