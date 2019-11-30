import logging

import ravel
import euc.device
import euc.utils

from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import CONF_NAME
from .const import DOMAIN, DEVICE_INSTANCE

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    hass.data[DOMAIN] = {}
    hass.data[DOMAIN][DEVICE_INSTANCE] = {}
    return True


async def async_setup_entry(hass, config_entry):
    # _LOGGER.info("async_setup_entry, %r", config_entry.as_dict())
    device_path = config_entry.data["device_path"]
    driver_name = config_entry.data["driver_name"]
    device_name = config_entry.data[CONF_NAME]
    # _LOGGER.info("device_path: %s", device_path)
    system_bus = ravel.system_bus()
    if not system_bus.connection.loop:
        system_bus.attach_asyncio(hass.loop)
    try:
        device = await euc.device.create_driver_instance(system_bus, driver_name, device_path)
    except euc.device.EUCError:
        raise ConfigEntryNotReady
    hass.data[DOMAIN][DEVICE_INSTANCE][config_entry.entry_id] = device
    euc.utils.create_task(device.run())
    _LOGGER.info("device %r is running", config_entry.data[CONF_NAME])
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(config_entry, "sensor")
    )
    return True
