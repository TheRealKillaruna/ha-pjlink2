# PJLink2 for Home Assistant

[Home Assistant](https://www.home-assistant.io) custom component to integrate video projectors via the [PJLink](https://pjlink.jbmia.or.jp/english/index.html) network protocol.
In contrast to the official [PJLink integration](https://www.home-assistant.io/integrations/pjlink), it also supports PJLink class-2 features, notably querying the current resolution of the projector.
The projector is integrated as a sensor that shows the current state (ON/OFF), all other data fields are attributes to the entity.

## Tested devices

The component has been developed and tested with an Epson LS12000 projector, but should work with all models and brands that support the PJLink protocol, among them Sony, NEC, Panasonic, Optoma, BenQ, and many more.


## Installation

**Manually**

Copy `pjlink2` folder from [latest release](https://github.com/TheRealKillaruna/pjlink2/releases/latest) to `custom_components` folder in your config folder.


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
