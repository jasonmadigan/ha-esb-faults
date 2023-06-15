"""Sensor for ESB Faults."""

import logging

import aiohttp
from geopy.distance import geodesic

from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


def calculate_distance(known_location, outage_location):
    """Calculate proximity from faults to specified location."""
    user_location = (float(known_location[0]), float(known_location[1]))
    outage_location = (
        float(outage_location.split(",")[0]),
        float(outage_location.split(",")[1]),
    )
    distance = geodesic(user_location, outage_location).kilometers
    return distance


def filter_outages_by_proximity(outages, known_location, max_distance):
    """Filter outages."""
    filtered_outages = []

    if max_distance is not None:
        if known_location is None or not all(known_location):
            _LOGGER.warning("Invalid known_location: %s", known_location)
            return filtered_outages

        for outage in outages:
            outage_location = outage.get("p", {}).get("c")
            if outage_location is not None and "," in outage_location:
                try:
                    distance = calculate_distance(known_location, outage_location)
                    if distance is not None and distance <= max_distance:
                        filtered_outages.append(outage)
                except ValueError:
                    _LOGGER.warning("Invalid outage_location: %s", outage_location)
            else:
                _LOGGER.warning("Invalid outage_location: %s", outage_location)
    else:
        filtered_outages = outages

    return filtered_outages


async def fetch_detailed_outage_data(outage_id, api_subscription_key):
    url = f"https://api.esb.ie/esbn/powercheck/v1.0/outages/{outage_id}"
    headers = {"api-subscription-key": api_subscription_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # Extract the desired detailed outage data from the response
                detailed_outage_data = {
                    "outageType": data["outageType"],
                    "location": data["location"],
                    "plannerGroup": data["plannerGroup"],
                    "numCustAffected": data["numCustAffected"],
                    "startTime": data["startTime"],
                    "estRestoreTime": data["estRestoreTime"],
                    "statusMessage": data["statusMessage"],
                    "restoreTime": data["restoreTime"],
                }
                return detailed_outage_data
            else:
                return None


async def fetch_data_from_api(api_subscription_key):
    """Fetch latest faults via ESB Powercheck API."""
    url = "https://api.esb.ie/esbn/powercheck/v1.0/outages"
    headers = {"api-subscription-key": api_subscription_key}
    _LOGGER.warning("Headers: %s", headers)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                # Perform necessary processing and return the desired state
                # Example code:
                return data.get("outageMessage")

            return None


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the ESB Faults sensor."""
    latitude = entry.data.get("latitude")
    longitude = entry.data.get("longitude")
    proximity = entry.data.get("proximity")
    api_subscription_key = entry.data.get("api_subscription_key")

    sensor = ESBFaultsSensor(latitude, longitude, proximity, api_subscription_key)
    await sensor.async_update()
    async_add_entities([sensor])


class ESBFaultsSensor(Entity):
    """Representation of an ESB Faults sensor."""

    def __init__(self, latitude, longitude, proximity, api_subscription_key):
        """Init with specicied location, and valid key."""
        self._latitude = latitude
        self._longitude = longitude
        self._proximity = proximity
        self._api_subscription_key = api_subscription_key
        self._state = None
        self._attributes = {}

    async def async_update(self):
        """Update the sensor data."""
        outages = await fetch_data_from_api(self._api_subscription_key)
        if outages is not None:
            known_location = (self._latitude, self._longitude)
            max_distance = self._proximity

            filtered_outages = filter_outages_by_proximity(
                outages, known_location, max_distance
            )

            self._state = len(filtered_outages)
            self._attributes = {"outages": []}

            for outage in filtered_outages:
                outage_location = outage["p"]["c"]
                outage_latitude, outage_longitude = map(
                    float, outage_location.split(",")
                )

                outage_distance = geodesic(
                    (self._latitude, self._longitude),
                    (outage_latitude, outage_longitude),
                ).kilometers

                outage_data = {
                    "id": outage["i"],
                    "type": outage["t"],
                    "location": outage_location,
                    "distance": round(outage_distance, 2),
                }

                # Fetch detailed outage data for the outage ID
                detailed_outage_data = await fetch_detailed_outage_data(
                    outage["i"], self._api_subscription_key
                )
                if detailed_outage_data is not None:
                    outage_data.update(detailed_outage_data)

                self._attributes["outages"].append(outage_data)
        else:
            self._state = None
            self._attributes = {}

    @property
    def unique_id(self):
        """Return the unique ID of the sensor."""
        return "esb_faults_outages"

    @property
    def name(self):
        """Return the name of the sensor."""
        return "ESB Faults Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return "problem"

    @property
    def extra_state_attributes(self):
        """Return the sensor attributes."""
        return self._attributes
