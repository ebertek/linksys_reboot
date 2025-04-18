from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from .entity import LinksysEntity
import logging
import asyncio

_LOGGER = logging.getLogger(__name__)

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="linksys_reboot",
        name="Linksys Reboot Switch",
        icon="mdi:restart",
    ),
)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities(
        LinksysRebootSwitch(
            coordinator=entry.runtime_data.coordinator,
            entity_description=desc,
        )
        for desc in ENTITY_DESCRIPTIONS
    )

class LinksysRebootSwitch(LinksysEntity, SwitchEntity):
    def __init__(self, coordinator, entity_description):
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        _LOGGER.debug("LinksysRebootSwitch: async_turn_on called")
        success = await self.coordinator.config_entry.runtime_data.client.async_reboot_router()
        _LOGGER.debug(f"Reboot result: {success}")
        self._attr_is_on = success
        self.async_write_ha_state()
        await asyncio.sleep(5)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        _LOGGER.debug("LinksysRebootSwitch: async_turn_off called")
        self._attr_is_on = False
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        return self._attr_is_on