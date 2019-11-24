"""Adds config flow for EUC."""
import asyncio
import voluptuous as vol

import homeassistant.helpers.config_validation as cv  # noqa
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback

from .const import DEFAULT_NAME, DOMAIN

import euc.device
import ravel


@callback
def configured_instances(hass):
    """Return a set of configured EUC instances."""
    return set(
        entry.data[CONF_NAME] for entry in hass.config_entries.async_entries(DOMAIN)
    )


class EUCFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for EUC"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            if user_input[CONF_NAME] in configured_instances(self.hass):
                self._errors[CONF_NAME] = "name_exists"

            if not self._errors:
                user_input["device_path"] = (
                    user_input["device"].rsplit("|", 1)[1]
                ).strip()
                return self.async_create_entry(
                    title=user_input[CONF_NAME], data=user_input
                )

        system_bus = ravel.system_bus()
        if not system_bus.connection.loop:
            system_bus.attach_asyncio(asyncio.get_event_loop())
        devices = await euc.device.get_devices(system_bus)
        driver_names = [name for name, _ in euc.device.get_device_drivers()]

        return self._show_config_form(
            name=DEFAULT_NAME,
            driver_names=driver_names,
            devices=[
                f"{obj.get('Name', 'unknown')} | {device_path}"
                for device_path, obj in devices
            ],
        )

    def _show_config_form(self, name=None, driver_names=(), devices=()):
        """Show the configuration form to edit data."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_NAME, default=name): str,
                    vol.Required("driver_name"): vol.In(driver_names),
                    vol.Required("device"): vol.In(devices),
                }
            ),
            errors=self._errors,
        )
