"""binary_sensor for hahm."""
import logging

from hahomematic.const import HA_PLATFORM_CLIMATE
from homeassistant.components.climate import ClimateEntity

from .const import DOMAIN
from .controlunit import ControlUnit
from .generic_entity import HaHomematicGenericEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities) -> None:
    """Set up the hahm climate platform."""
    cu: ControlUnit = hass.data[DOMAIN][entry.entry_id]
    entities: list[HaHomematicGenericEntity] = []
    # for hm_entity in cu.get_new_hm_entities(HA_PLATFORM_CLIMATE):
    #    entities.append(HaHomematicClimate(cu, hm_entity))
    async_add_entities(entities)


class HaHomematicClimate(HaHomematicGenericEntity, ClimateEntity):
    """Representation of the HomematicIP climate entity."""
