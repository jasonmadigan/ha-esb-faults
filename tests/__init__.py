"""Tests for the ESB Faults integration."""
from __future__ import annotations

from datetime import timedelta
from typing import Any
from unittest.mock import AsyncMock, patch

from aiohttp import web
from pytest_homeassistant_custom_component.common import (
    MockConfigEntry,
    async_fire_time_changed,
)

from custom_components.esb_faults.const import DOMAIN
from homeassistant.config_entries import RELOAD_AFTER_UPDATE_DELAY, ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant