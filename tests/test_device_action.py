"""The tests for Homematic(IP) Local device actions."""

from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_get_device_automations,
    async_mock_service,
    mock_device_registry,
    mock_registry,
)

from custom_components.homematicip_local import DOMAIN as HMIP_DOMAIN
from homeassistant.components import automation
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry, entity_registry
from homeassistant.setup import async_setup_component


@pytest.fixture
def device_reg(hass: HomeAssistant) -> device_registry.DeviceRegistry:
    """Return an empty, loaded, registry."""
    return mock_device_registry(hass)


@pytest.fixture
def entity_reg(hass: HomeAssistant) -> entity_registry.EntityRegistry:
    """Return an empty, loaded, registry."""
    return mock_registry(hass)


async def no_test_get_actions(
    hass: HomeAssistant,
    device_reg: device_registry.DeviceRegistry,
    entity_reg: entity_registry.EntityRegistry,
) -> None:
    """Test we get the expected actions from a Homematic(IP) Local."""
    config_entry = MockConfigEntry(domain="test", data={})
    config_entry.add_to_hass(hass)
    device_entry = device_reg.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        connections={(device_registry.CONNECTION_NETWORK_MAC, "12:34:56:AB:CD:EF")},
    )
    entity_reg.async_get_or_create(HMIP_DOMAIN, "test", "5678", device_id=device_entry.id)
    await async_get_device_automations(hass, "action", device_entry.id)
    # assert_lists_same(actions, expected_actions)


async def no_test_action(hass: HomeAssistant) -> None:
    """Test for turn_on and turn_off actions."""
    assert await async_setup_component(
        hass,
        automation.DOMAIN,
        {
            automation.DOMAIN: [
                {
                    "trigger": {
                        "platform": "event",
                        "event_type": "test_event_turn_off",
                    },
                    "action": {
                        "domain": HMIP_DOMAIN,
                        "device_id": "abcdefgh",
                        "entity_id": "homematicip_local.entity",
                        "type": "turn_off",
                    },
                },
                {
                    "trigger": {
                        "platform": "event",
                        "event_type": "test_event_turn_on",
                    },
                    "action": {
                        "domain": HMIP_DOMAIN,
                        "device_id": "abcdefgh",
                        "entity_id": "homematicip_local.entity",
                        "type": "turn_on",
                    },
                },
            ]
        },
    )

    turn_off_calls = async_mock_service(hass, "homematicip_local", "turn_off")
    turn_on_calls = async_mock_service(hass, "homematicip_local", "turn_on")

    hass.bus.async_fire("test_event_turn_off")
    await hass.async_block_till_done()
    assert len(turn_off_calls) == 1
    assert len(turn_on_calls) == 0

    hass.bus.async_fire("test_event_turn_on")
    await hass.async_block_till_done()
    assert len(turn_off_calls) == 1
    assert len(turn_on_calls) == 1
