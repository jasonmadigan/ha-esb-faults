# ESB Networks PowerCheck Faults integration for Home Assistant

This repository contains a Home Assistant integration for  [ESB Networks PowerCheck](https://powercheck.esbnetworks.ie/) display notable service interruptions for a given location, within a configured proximity. The integration relies upon a connection to ESB Network's PowerCheck API.

##  Installation

You will need [HACS](https://hacs.xyz) installed in your Home Assistant server. Install the integration by installing this repository as a Custom Respository (working on adding this to the default HACS integration set). Then, navigate to Integrations, Add an Integration and select ESB Faults. You will then be asked to enter:

* Latitude: Your location latitude
* Longitude: Your location longitude
* Proximity: Filters alerts to within `X` kilometers of your lat/lon.
* API Key: I won't include this here, but you can find it by inspecting requests on the PowerCheck website. Look for the `Api-Subscription-Key` key.

[![Open your Home Assistant instance and add this integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=esb_faults)


## Entities

The integration reads data 5 minutes. It exposes one entity, `sensor.esb_faults_sensor`. The *State* of the sensor is a numeric value, indiciating how many total faults (be they Planned Outages, Recent Restorations or Current Unplanned Faults) are present nearby. The attributes for the sensor include a an `outages` array, which contains details of individual outages present. Fields for these individual outages include:

| Outage Field    | Description                                                  |
|-----------------|--------------------------------------------------------------|
| outageType      | Outage type (e.g. 'Planned', 'Fault', 'Restored')            |
| location        | Outage location                                              |
| plannerGroup    | Region                                                       |
| numCustAffected | Number of customers affected                                 |
| startTime       | Outage start time                                            |
| estRestoreTime  | Estimated restoration time                                   |
| statusMessage   | Status Message                                               |
| restoreTime     | Restoration time (only for outages of outageType `Restored`) |
| numCustAffected | Number of customers affected                                 |
