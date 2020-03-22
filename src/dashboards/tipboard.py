from . import Dashboard
import requests
import os
import json

# Note that this dashboard is intended to be paired with an associated layout_config.yaml defining the layout
class _TipboardDash(Dashboard):
    def __init__(self):
        # Get info for api calls
        if not "TB_API_KEY" in os.environ:
            raise ValueError("Missing Tipboard API key")
        api_key = os.environ["TB_API_KEY"]
        version = "v0.1" if "TB_API_VERS" not in os.environ else os.environ["TB_API_VERS"]
        host = "localhost" if "TB_HOST" not in os.environ else os.environ["TB_HOST"]
        port = "7272" if "TB_PORT" not in os.environ else os.environ["TB_PORT"]
        self.assembled_url = f"http://{host}:{port}/api/{version}/{api_key}"

    def update_weather(self, weather_data):
        # Assume weather data is a dictionary
        
        # Assignment function for easily pulling value from the dictionary
        def _assign(item): return weather_data[item] if item in weather_data else ""

        self._update_temp(_assign("current_temp"), _assign("temp_high"), _assign("temp_low"))
        self._update_precip_current(_assign("precip_type"), _assign("precip_prob"), _assign("max_intensity"))
        self._update_precip_hourly(_assign("hourly_precip_type"), _assign("hourly_precip"))
        self._update_general_weather_info(_assign("day_summary"), _assign("week_summary"))
        self._update_weather_alerts(_assign("alert_list"))


    def update_home(self, home_Data):
        # Assume home data is a dictionary

        # Assignment function for easily pulling value from the dictionary
        def _assign(item): return home_Data[item] if item in home_Data else ""

        self._update_network_status(_assign("internet"), _assign("gateway"), _assign("gfi"))

    def update_misc(self):
        pass

    def _update(self, post_data):
        response = requests.post(url = self.assembled_url + "/push", data = post_data)
        if response.status_code != 200:
            # TODO: Handle bad post
            pass
    
    def _update_config(self, config_type, tile_key, config_data):
        response = requests.post(url = self.assembled_url + "/{config_type}/{tile_key}", data = config_data)
        if response.status_code != 200:
            # TODO: Handle bad post
            pass

    def _update_temp(self, cur_temp, high_temp, low_temp):
        # Put the temp data into a single dict for json dumping
        temp_data = {
            "title": "Temperature",
            "description": "",
            "big-value": cur_temp,
            "upper-left-label": "High:",
            "upper-left-value": high_temp,
            "upper-right-label": "Low:",
            "upper-right-value": low_temp
        }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "big_value",
            "key": "weather_main",
            "data": json.dumps(temp_data)
        }

        self._update(data)

    def _update_precip_current(self, ptype, probability, max_intensity):
        # Put the temp data into a single dict for json dumping
        prob = probability if not probability == "" else "No"
        pt = ptype if not ptype == "" else "precipitation"
        maxp = max_intensity if not max_intensity == "" else "0"
        p_data = {
            "items":
            [
                f"{prob} chance of {pt}",
                f"Max intensity: {maxp}"
            ]
        }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "listing",
            "key": "weather_precipitation",
            "data": json.dumps(p_data)
        }

        self._update(data)
    
    def _update_precip_hourly(self, ptype, minute_array):
        # Put the temp data into a single dict for json dumping
        pt = ptype if not ptype == "None" else "No Precipitation"
        p_data = {
            "subtitle": f"{pt}",
            "description": f"Chance of {pt} this hour",
            "series_list": [ minute_array ]
        }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "line_chart",
            "key": "weather_precipitation_precision",
            "data": json.dumps(p_data)
        }

        # Disable trend line and update data
        self._update_config("tileconfig", "weather_precipitation_precision", 'value={"seriesDefaults": {"trendline": {"show": false}}}')
        self._update(data)

    def _update_general_weather_info(self, day_info, week_info):
        # Put the temp data into a single dict for json dumping
        info_data = {
            "text": f"Today: {day_info}\n\nThis week: {week_info}"
        }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "text",
            "key": "weather_misc",
            "data": json.dumps(info_data)
        }

        self._update(data)

    def _update_weather_alerts(self, alert_list):
        # Put the temp data into a single dict for json dumping
        a_data = {
            "items": alert_list
        }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "listing",
            "key": "weather_alerts",
            "data": json.dumps(a_data)
        }

        self._update(data)

    def _update_network_status(self, internet, gateway, gfi):
        # Put the temp data into a single dict for json dumping
        net_data = {
            "items": [
                f"Internet: {internet}",
                f"Gateway: {gateway}",
                f"GFI: {gfi}"
            ]
        }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "listing",
            "key": "network_status",
            "data": json.dumps(net_data)
        }

        self._update(data)

        # Put the temp data into a single dict for json dumping
        net_data = {
            "title": "GFI",
            "description": "",
            "big-value": gfi
            }

        # Dump data separately as json because that's what tipboard wants
        data = {
            "tile": "big_value",
            "key": "network_status_gfi",
            "data": json.dumps(net_data)
        }

        self._update(data)

_instance = _TipboardDash()
