"""Config flow for the Linksys Reboot integration."""

# pylint: disable=E0401, R0903, W0718

import voluptuous as vol # type: ignore

from homeassistant import config_entries # type: ignore
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD # type: ignore

from .const import DOMAIN
from .api import LinksysApiClient

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for the Linksys Reboot integration."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Show the config form and handle user input."""
        errors = {}
        if user_input:
            client = LinksysApiClient(
                user_input[CONF_USERNAME],
                user_input[CONF_PASSWORD],
                self.hass.helpers.aiohttp_client.async_get_clientsession()
            )
            try:
                await client.async_get_data()
                return self.async_create_entry(title="Linksys Router", data=user_input)
            except Exception:
                errors["base"] = "auth"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str
            }),
            errors=errors,
        )
