from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, LOGGER
from .api import LinksysApiClient
from .coordinator import LinksysDataUpdateCoordinator

PLATFORMS = [Platform.SWITCH]

async def async_setup_entry(hass, entry):
    coordinator = LinksysDataUpdateCoordinator(hass=hass, logger=LOGGER)
    coordinator.config_entry = entry
    entry.runtime_data = type("obj", (object,), {
        "client": LinksysApiClient(entry.data["username"], entry.data["password"], async_get_clientsession(hass)),
        "coordinator": coordinator
    })()
    await coordinator.async_config_entry_first_refresh()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)