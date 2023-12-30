# PJLink2 for Home Assistant

[Home Assistant](https://www.home-assistant.io) custom component to integrate video projectors via the [PJLink](https://pjlink.jbmia.or.jp/english/index.html) network protocol.
In contrast to the official [PJLink integration](https://www.home-assistant.io/integrations/pjlink), it also supports PJLink class-2 features, notably querying the current resolution of the projector.
The projector is integrated as a sensor that shows the current state (ON/OFF), all other data fields are attributes to the entity.

## Tested devices

The component has been developed and tested with an Epson LS12000 projector, but should work with all models and brands that support the PJLink protocol, among them Sony, NEC, Panasonic, Optoma, BenQ, and many more.


## Installation

**HACS**

1. In HACS, select `Integrations`
2. Select `Custom Repositories` from the three dots in top right corner
3. Enter `https://github.com/TheRealKillaruna/ha-pjlink2` as repository and select `Integration` as category
4. Click `Add`
5. Open `Custom Repositories` again and you should see `PJLink2` at the top of the list, click it
6. Click `Download` in lower right corner
7. Select the latest version and click `Download`
8. Configure your settings as described below
9. Restart Home Assistant

**Manually**

1. Copy `pjlink2` folder from [latest release](https://github.com/TheRealKillaruna/pjlink2/releases/latest) to `custom_components` folder in your config folder.
2. Configure your settings as described below
3. Restart Home Assistant


## Configuration
All settings are specified in your Home Assistant configuration via [YAML](https://www.home-assistant.io/docs/configuration/).

Add your projector as a sensor and configure like this:

```yaml
sensor:
  - platform: pjlink2
    host: 192.168.0.123       # IP address of the projector
    port: 1234                # projector port for communication (optional, default is 4352)
    name: "My Projector"      # name under which projector appears in HA (optional)
    encoding: "utf-16"        # encoding for communication (optional, default is utf-8)
    password: "secret%123"    # password to establish connection (optional)
    timeout: 1.5              # timeout to establish connection in seconds (optional, default is 4 sec)
```
