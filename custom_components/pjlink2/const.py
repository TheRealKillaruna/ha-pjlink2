"""Provides the constants needed for component."""
from enum import StrEnum

DOMAIN = "pjlink2"

CONF_ENCODING = "encoding"
DEFAULT_ENCODING = "utf-8"
DEFAULT_PORT = 4352
DEFAULT_TIMEOUT = 2

ATTR_PRODUCT_NAME = "product_name"
ATTR_MANUFACTURER_NAME = "manufacturer_name"
ATTR_PROJECTOR_NAME = "projector_name"
ATTR_RESOLUTION_X = "x_resolution"
ATTR_RESOLUTION_Y = "y_resolution"
ATTR_LAMP_HOURS = "lamp_hours"

class ProjectorState(StrEnum):
    OFF = "off"
    ON = "on"
    COOLING = "cooling"
    WARMING = "warming"