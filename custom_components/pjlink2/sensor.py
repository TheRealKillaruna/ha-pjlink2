"""GitHub sensor platform."""
from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
import logging
from typing import Any

from aiopjlink import PJLink, PJLinkException, PJLinkProjectorError, Power, Sources, Lamp, Information 

from homeassistant import config_entries, core
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME, CONF_PASSWORD, CONF_TIMEOUT

import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType, HomeAssistantType

import voluptuous as vol

from .const import DOMAIN, CONF_ENCODING, DEFAULT_ENCODING, DEFAULT_PORT, DEFAULT_TIMEOUT, ATTR_PRODUCT_NAME, ATTR_MANUFACTURER_NAME, ATTR_PROJECTOR_NAME, ATTR_RESOLUTION_X, ATTR_RESOLUTION_Y, ATTR_LAMP_HOURS, ProjectorState


_LOGGER = logging.getLogger(__name__)
# Time between updating data from projector
SCAN_INTERVAL = timedelta(seconds=3)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_ENCODING, default=DEFAULT_ENCODING): cv.string,
        vol.Optional(CONF_PASSWORD) : cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT) : cv.positive_float
    }
)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    host = config.get(CONF_HOST)
    port =  config.get(CONF_PORT)
    password = config.get(CONF_PASSWORD)
    timeout = config.get(CONF_TIMEOUT)
    name = config.get(CONF_NAME)
    pjl = PJLink(host, port, password, timeout)
    sensors = [PJLink2Sensor(pjl, name)]
    async_add_entities(sensors, update_before_add=False)


class PJLink2Sensor(Entity):
    """Representation of a PJLink2 sensor."""

    def __init__(self, pjl, name):
        super().__init__()
        self._projector = pjl
        self.attrs: dict[str, Any] = {}
        self._name = name
        self._state = None
        self._available = False
        self._connectionErrorLogged = False

    async def async_will_remove_from_hass(self) -> None:
        """Close connection."""
        await super().async_will_remove_from_hass()
        if self._available:
            try:
                await self._projector.__aexit__(0,0,0)
            except (PJLinkException, OSError) as err:
                _LOGGER.error("PJLink2 ERROR when closing connection to %s: %s", self._name, repr(err))
            else:
                _LOGGER.info("PJLink2 INFO for %s: Connection closed.", self._name)

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._projector._address

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> str | None:
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.attrs

    async def async_update(self) -> None:
        """Update all sensors."""
        try:
            if not self._available:
                # connect and init static information
                await self._projector.__aenter__()
                self._available = True
                info = await Information(self._projector).table()
                self.attrs[ATTR_PRODUCT_NAME] = info["product_name"]
                self.attrs[ATTR_MANUFACTURER_NAME] = info["manufacturer_name"]
                self.attrs[ATTR_PROJECTOR_NAME] = info["projector_name"]
                if self._name == None: self._name = info["projector_name"]
                _LOGGER.info("PJLink2 INFO for %s: Connection opened.", self._name)
                
            pwr = await Power(self._projector).get()
            if pwr == Power.State.OFF: self._state = ProjectorState.OFF
            elif pwr == Power.State.ON: self._state = ProjectorState.ON
            elif pwr == Power.State.COOLING: self._state = ProjectorState.COOLING
            elif pwr == Power.State.WARMING: self._state = ProjectorState.WARMING
            
            if pwr==Power.ON:
                res = await Sources(self._projector).resolution()
                self.attrs[ATTR_RESOLUTION_X] = res[0]
                self.attrs[ATTR_RESOLUTION_Y] = res[1]
                lmpHrs = await Lamp(self._projector).hours()
                self.attrs[ATTR_LAMP_HOURS] = lmpHrs
            else:
                if ATTR_RESOLUTION_X in self.attrs: del self.attrs[ATTR_RESOLUTION_X]
                if ATTR_RESOLUTION_Y in self.attrs: del self.attrs[ATTR_RESOLUTION_Y]
                
            self._connectionErrorLogged = False # after successful update, enable error logging for next connection issue
        
        except PJLinkProjectorError:
            # resolution cannot be queried due to no input
            if ATTR_RESOLUTION_X in self.attrs: del self.attrs[ATTR_RESOLUTION_X]
            if ATTR_RESOLUTION_Y in self.attrs: del self.attrs[ATTR_RESOLUTION_Y]
            _LOGGER.info("PJLink2 INFO for %s: Cannot get resolution", self._name)
        except (PJLinkException, OSError) as err:
            if not self._connectionErrorLogged: 
                _LOGGER.error("PJLink2 ERROR for %s: %s", self._name, repr(err))
                self._connectionErrorLogged = True # do not spam logfile with same error message
            self._state = None
            if self._available:
                self._available = False # only call exit function once after disconnect
                try:
                    await self._projector.__aexit__(0,0,0)
                except (PJLinkException, OSError) as err:
                    _LOGGER.error("PJLink2 ERROR when closing connection to %s: %s", self._name, repr(err))
                else:
                    _LOGGER.info("PJLink2 INFO for %s: Connection closed.", self._name)
