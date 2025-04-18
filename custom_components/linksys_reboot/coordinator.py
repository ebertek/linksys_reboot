from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.exceptions import ConfigEntryAuthFailed
from .api import (
    LinksysApiClientAuthenticationError,
    LinksysApiClientError
)

class LinksysDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, logger):
        super().__init__(hass, logger=logger, name="Linksys Reboot")
        self.config_entry = None

    async def _async_update_data(self):
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except LinksysApiClientAuthenticationError as e:
            raise ConfigEntryAuthFailed(e) from e
        except LinksysApiClientError as e:
            raise UpdateFailed(e) from e