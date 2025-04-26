"""Base class for Linksys Reboot entities."""

# pylint: disable=E0401, R0903

from homeassistant.helpers.device_registry import DeviceInfo # type: ignore
from homeassistant.helpers.update_coordinator import CoordinatorEntity # type: ignore

from .const import DOMAIN
from .coordinator import LinksysDataUpdateCoordinator

class LinksysEntity(CoordinatorEntity[LinksysDataUpdateCoordinator]):
    """Linksys Router entity."""
    _attr_has_entity_name = True

    def __init__(self, coordinator: LinksysDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Linksys Router"
        )
