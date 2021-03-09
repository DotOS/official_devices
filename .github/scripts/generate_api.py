import os
import sys
import json


def report_error(message):
    print(message)
    sys.exit(1)


def read_json_file(filepath):
    try:
        _file = open(filepath).read()
    except:
        report_error(f'{filepath} not found')

    try:
        return json.loads(_file)
    except:
        report_error(f'{filepath} is not a valid json')


devices = read_json_file('master/devices.json')
teams = read_json_file('master/teams.json')


def generate_device_list():
    brands = {}
    for device in devices:
        if device['brand'] not in brands.keys():
            brands[device['brand']] = {}

        brands[device['brand']][device['codename']] = device['name']

    res = json.dumps(brands, indent=3, sort_keys=True)

    device_list_filepath = 'api/devices/devices.json'
    device_list_file = open(device_list_filepath, 'w+')
    device_list_file.write(res)
    device_list_file.close()


def generate_device_api():

    DEVICE_PARAMS = ['name', 'brand', 'codename', 'xda_thread', 'version_info']
    TEAM_PARAMS = ['_id', 'name', 'url', 'devices']
    BUILD_PARAMS = ['datetime', 'filename', 'id',
                    'romtype', 'size', 'url', 'version', 'changelog']

    for device in devices:
        for param in DEVICE_PARAMS:
            if param not in device.keys():
                report_error(f"'{param}' not found in {device}")

        codename = device['codename']

        api = device.copy()
        del api['version_info']

        api['builds'] = {}
        api['maintainers'] = []
        for team in teams:
            _team = team.copy()
            for param in TEAM_PARAMS:
                if param not in _team.keys():
                    report_error(f"'{param}' not found in {team}")

            if codename in _team['devices']:
                del _team['devices']
                api['maintainers'].append(_team)

        gapps_build = device['version_info'].get('has_gapps_builds')
        if gapps_build is True:
            gapps_ota_path = f'master/builds/{codename}/builds_gapps.json'
            gapps_ota = read_json_file(gapps_ota_path)
            response = gapps_ota['response']

            for index, resp in enumerate(response):
                _keys = list(resp.keys())
                for param in BUILD_PARAMS:
                    if param not in _keys:
                        report_error(f"'{param}' not found in {resp}")
                del response[index]['changelog']

            api['builds']['gapps'] = response

        vanilla_build = device['version_info'].get('has_vanilla_builds')
        if vanilla_build is True:
            vanilla_ota_path = f'master/builds/{codename}/builds.json'
            vanilla_ota = read_json_file(vanilla_ota_path)
            response = vanilla_ota['response']

            for index, resp in enumerate(response):
                _keys = list(resp.keys())
                for param in BUILD_PARAMS:
                    if param not in _keys:
                        report_error(f"'{param}' not found in {resp}")

                del response[index]['changelog']
            api['builds']['vanilla'] = response

        api_filepath = f'api/devices/{codename}.json'
        api_json = json.dumps(api, indent=3, sort_keys=False)
        api_file = open(api_filepath, 'w+')
        api_file.write(api_json + '\n')
        api_file.close()


def main():
    generate_device_api()
    generate_device_list()


if __name__ == "__main__":
    main()
