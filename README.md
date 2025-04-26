# Linksys Reboot - Home Assistant Integration

A custom Home Assistant integration to remotely reboot your Linksys EA6350 (and compatible models) via the [Linksys Smart Wi-Fi](https://linksyssmartwifi.com) cloud API.

## Features

- Adds a momentary switch entity in Home Assistant.
- Secure login using your Linksys cloud credentials.
- Auto-resets after triggering.
- Fully local configuration via the UI (Config Flow).
- No SNMP or local API access needed.

## Installation
### HACS (Recommended)
1. Go to **HACS**.
2. Click on the three-dot menu (top right) and select **Custom repositories**.
    1. Set **Repository** to:

        ```
        https://github.com/ebertek/linksys_reboot
        ```

    2. Set **Type** to **Integration**.
    3. Click **ADD**.
3. Search for and select **Linksys Reboot**, click **Download**, and click **Download** again.
4. Restart Home Assistant.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ebertek&repository=linksys_reboot&category=Integration)

### Manual Installation  
1. Copy the `custom_components/linksys_reboot` folder into your own `config/custom_components/`.
2. Restart Home Assistant.

## Configuration
1. Navigate to **Settings > Devices & services**.
2. Click **Add integration** and search for `Linksys Reboot`.
3. Enter your **Email** and **Password** for Linksys Smart Wi-Fi.

## License
This project is licensed under the [Apache License 2.0](LICENSE).
