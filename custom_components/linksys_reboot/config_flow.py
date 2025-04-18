from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import voluptuous as vol
from .const import DOMAIN
from .api import LinksysApiClient

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
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