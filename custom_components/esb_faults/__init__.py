"""Platform for ESB Faults."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN
from .sensor import ESBFaultsSensor

# Define the platforms supported by the component
PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the ESB Faults sensor."""

    # Set up the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    latitude = entry.data.get("latitude")
    longitude = entry.data.get("longitude")
    proximity = entry.data.get("proximity")
    api_subscription_key = entry.data.get("api_subscription_key")

    sensor = ESBFaultsSensor(latitude, longitude, proximity, api_subscription_key)
    await sensor.async_update()

    async def async_update_sensor(event_time):
        """Update the sensor data."""
        await sensor.async_update()

    # Schedule periodic updates
    async_track_time_interval(
        hass, async_update_sensor, timedelta(minutes=5)
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = sensor

    async def async_remove_entry(hass, entry):
        """Handle removal of the entry."""
        await sensor.async_remove()

    entry.async_on_unload(entry.add_update_listener(async_remove_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
