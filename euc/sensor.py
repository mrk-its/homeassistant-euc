import logging
from homeassistant.helpers.entity import Entity
from .const import DOMAIN, DEVICE_INSTANCE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities) -> bool:
    device = hass.data[DOMAIN][DEVICE_INSTANCE][config_entry.entry_id]
    entities = [
        EUCSensor(device, "voltage", unit="V"),
        EUCSensor(device, "current", unit="A"),
        EUCSensor(device, "temperature", unit="°C"),
        EUCSensor(device, "total_distance", unit="m"),
        EUCBattery(device, "battery_level"),
    ]
    async_add_entities(entities, True)
    return True


class EUCSensor(Entity):
    def __init__(self, euc_device, kind, unit=None):
        self.euc_device = euc_device
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
        return f"{self.euc_device.name} {self.kind}"

    @property
    def state(self):
        return self._state

    def on_property_changed(self, euc_device, prop_name, value):
        self._state = value
        self.async_schedule_update_ha_state()


class EUCBattery(EUCSensor):
    unit_of_measurement = "%"
