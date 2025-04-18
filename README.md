# Linksys Router Reboot for Home Assistant

A custom Home Assistant integration to remotely reboot your Linksys EA6350 (and compatible models) via the [Linksys Smart Wi-Fi](https://linksyssmartwifi.com) cloud API.

## Features

- Adds a momentary switch entity in Home Assistant
- Secure login using your Linksys cloud credentials
- Auto-resets after triggering
- Fully local configuration via the UI (Config Flow)
- No SNMP or local API access needed

## Installation

1. Copy the `linksys_reboot` folder to `config/custom_components/` in your Home Assistant setup.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration**, search for "Linksys Reboot".
4. Enter your Linksys account credentials.

## Credits

Developed by [@ebertek](https://github.com/ebertek)

## License

Apache License 2.0