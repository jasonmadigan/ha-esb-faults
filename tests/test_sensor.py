"""Test ESB Faults sensor states."""
from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from custom_components.esb_faults.sensor import ESBFaultsSensor

mock_outages_response = [
        {
            "i": "2258859",
            "t": "Restored",
            "p": {"c": "53.452609350776,-8.063591288851"},
        },
        {
            "i": "2258603",
            "t": "Restored",
            "p": {"c": "53.45492895512,-8.011282794926"},
        },
        {
            "i": "2258623",
            "t": "Restored",
            "p": {"c": "53.453450506359,-8.062050296445"},
        },
        {
            "i": "2258635",
            "t": "Restored",
            "p": {"c": "53.858356264493,-8.639909087399"},
        },
        {
            "i": "2258618",
            "t": "Restored",
            "p": {"c": "53.409884502789,-7.331046556344"},
        },
        {
            "i": "2258619",
            "t": "Restored",
            "p": {"c": "53.409327439741,-7.310882618153"},
        },
        {
            "i": "2258637",
            "t": "Restored",
            "p": {"c": "53.419851634242,-7.298411269891"},
        },
        {
            "i": "2258646",
            "t": "Restored",
            "p": {"c": "53.401632552166,-7.341897425629"},
        },
        {
            "i": "2258647",
            "t": "Restored",
            "p": {"c": "53.403738255159,-7.288073840105"},
        },
        {"i": "2258642", "t": "Fault", "p": {"c": "53.58842,-7.82331"}},
        {
            "i": "2258616",
            "t": "Restored",
            "p": {"c": "54.536696117514,-8.074364083407"},
        },
        {
            "i": "2258589",
            "t": "Restored",
            "p": {"c": "53.188981515725,-8.005984930568"},
        },
        {
            "i": "2258645",
            "t": "Restored",
            "p": {"c": "53.923846354672,-8.111801998247"},
        },
        {
            "i": "2258675",
            "t": "Restored",
            "p": {"c": "53.923846354672,-8.111801998247"},
        },
        {
            "i": "2258685",
            "t": "Restored",
            "p": {"c": "54.139108231507,-8.64041896672"},
        },
        {
            "i": "2258518",
            "t": "Restored",
            "p": {"c": "53.296635849453,-6.377596350802"},
        },
        {
            "i": "2258571",
            "t": "Restored",
            "p": {"c": "53.786231722217,-9.15298777383"},
        },
        {"i": "2258697", "t": "Fault", "p": {"c": "54.21481,-8.98743"}},
        {"i": "2258701", "t": "Fault", "p": {"c": "54.20994,-8.99091"}},
        {
            "i": "2258583",
            "t": "Restored",
            "p": {"c": "53.880558629667,-7.476678981358"},
        },
        {
            "i": "2258643",
            "t": "Restored",
            "p": {"c": "53.881184324279,-7.475302841941"},
        },
        {
            "i": "2258644",
            "t": "Restored",
            "p": {"c": "53.794511194785,-7.405704741683"},
        },
        {
            "i": "2258652",
            "t": "Restored",
            "p": {"c": "53.894108678451,-7.488717718682"},
        },
        {"i": "2257991", "t": "Planned", "p": {"c": "53.09191,-6.11529"}},
        {"i": "2258524", "t": "Fault", "p": {"c": "52.27089,-6.62613"}},
        {
            "i": "2258600",
            "t": "Restored",
            "p": {"c": "53.436593298415,-6.183094663519"},
        },
        {"i": "2257809", "t": "Fault", "p": {"c": "53.33258,-6.28401"}},
        {"i": "2258673", "t": "Fault", "p": {"c": "53.33258,-6.28398"}},
        {"i": "2258457", "t": "Fault", "p": {"c": "53.35537,-6.35323"}},
        {"i": "2258718", "t": "Fault", "p": {"c": "52.70886,-8.8784"}},
        {
            "i": "2258672",
            "t": "Restored",
            "p": {"c": "54.026086192653,-8.932771671475"},
        },
        {
            "i": "2258658",
            "t": "Restored",
            "p": {"c": "54.062115652614,-8.712206381223"},
        },
    ]

mock_detailed_data = {
  'outageId': '2258859', 
  'outageType': 'Planned',
  'point': {'c': '52.46626,-6.76333'}, 
  'location': 'Clonroche', 
  'plannerGroup': 'Enniscorthy', 
  'numCustAffected': 35, 
  'startTime': '16/06/2023 10:16', 
  'estRestoreTime': '16/06/2023 17:00', 
  'statusMessage': 'We apologise for the loss of supply.  We are carrying out essential improvement / maintenance works in your area and will restore power as quickly as possible.', 
  'restoreTime': ''
}

@pytest.mark.asyncio
async def test_async_update_success(hass, aioclient_mock):
    with patch('custom_components.esb_faults.sensor.fetch_data_from_api', new_callable=AsyncMock) as mock_fetch, \
         patch('custom_components.esb_faults.sensor.fetch_detailed_outage_data', new_callable=AsyncMock) as mock_detailed_fetch:

        # Prepare some mock data to return from your mock functions
        mock_fetch.return_value = mock_outages_response
        mock_detailed_fetch.return_value = mock_detailed_data  # Use the renamed variable

        sensor = ESBFaultsSensor(53.349804, -6.260310, 50, 'test')
        await sensor.async_update()

        print('lenny', len(sensor._attributes['outages']))

        assert len(sensor._attributes['outages']) == 6 # 6 outages in specified area
        assert sensor.available is True

@pytest.mark.asyncio
async def test_async_update_outage_outside_proximity(hass, aioclient_mock):
    with patch('custom_components.esb_faults.sensor.fetch_data_from_api', new_callable=AsyncMock) as mock_fetch, \
          patch('custom_components.esb_faults.sensor.calculate_distance') as mock_distance:

        # Prepare the mock data to return one outage from your mock function
        mock_fetch.return_value = [{
            "i": "test_outage_id",
            "t": "test_outage_type",
            "p": {"c": "55.000000, -6.000000"},  # outage location outside of the defined proximity
        }]

        # Ensure that calculate_distance function returns a value greater than the defined proximity
        mock_distance.return_value = 100  # value greater than the defined proximity (50)

        sensor = ESBFaultsSensor(53.349804, -6.260310, 50, 'test')
        await sensor.async_update()

        # Check if sensor state is 0 when there are no outages within the defined proximity
        assert sensor.state == 0
        assert sensor.extra_state_attributes['outages'] == []
        assert sensor.available is True