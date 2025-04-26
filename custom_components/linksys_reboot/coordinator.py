"""Data coordinator for the Linksys Reboot integration."""

# pylint: disable=C0301, E0401, R0903

from homeassistant.exceptions import ConfigEntryAuthFailed # type: ignore
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed # type: ignore

from .api import LinksysApiClientAuthenticationError, LinksysApiClientError

class LinksysDataUpdateCoordinator(DataUpdateCoordinator):
    """Manage fetching and refreshing data from the Linksys cloud API."""
    def __init__(self, hass, logger):
        super().__init__(hass, logger=logger, name="Linksys Reboot")
        self.config_entry = None

    async def _async_update_data(self):
        """Fetch latest data from the API, or raise appropriate errors."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except LinksysApiClientAuthenticationError as e:
            raise ConfigEntryAuthFailed(e) from e
        except LinksysApiClientError as e:
            raise UpdateFailed(e) from e
