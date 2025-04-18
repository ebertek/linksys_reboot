"""Switch platform for the Linksys Reboot integration."""
import logging
import asyncio
from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from .entity import LinksysEntity

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
    """Switch that triggers a Linksys router reboot."""
    def __init__(self, coordinator, entity_description):
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_is_on = False

    async def async_turn_on(self, **kwargs):
        """Send reboot command and reset switch state."""
        _LOGGER.debug("LinksysRebootSwitch: async_turn_on called")
        success = await self.coordinator.config_entry.runtime_data.client.async_reboot_router()
        _LOGGER.debug(f"Reboot result: {success}")
        self._attr_is_on = success
        self.async_write_ha_state()
        await asyncio.sleep(5)
        self._attr_is_on = False
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Force switch to off state (used by UI reset)."""
        _LOGGER.debug("LinksysRebootSwitch: async_turn_off called")
        self._attr_is_on = False
        self.async_write_ha_state()

    @property
    def is_on(self) -> bool:
        """Return True if the switch is currently on (reboot was triggered)."""
        return self._attr_is_on
