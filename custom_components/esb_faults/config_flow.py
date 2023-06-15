"""Platform for ESB Faults."""
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN


class ESBFaultsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for ESB Faults integration."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            # Validate and store the latitude, longitude, and proximity values
            latitude = user_input["latitude"]
            longitude = user_input["longitude"]
            proximity = user_input["proximity"]
            api_subscription_key = user_input[
                "api_subscription_key"
            ]  # Retrieve the API subscription key

            # Proceed to create the configuration entry
            return self.async_create_entry(
                title="ESB Faults",
                data={
                    "latitude": latitude,
                    "longitude": longitude,
                    "proximity": proximity,
                    "api_subscription_key": api_subscription_key,  # Include the API subscription key in the data
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("latitude"): str,
                    vol.Required("longitude"): str,
                    vol.Required("proximity"): vol.Coerce(float),
                    vol.Required("api_subscription_key"): str,
                }
            ),
        )
