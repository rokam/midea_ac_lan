import logging
from .message import (
    MessageQuery,
    MessageSet,
    MessageE2Response,
    MessagePower
)
from ...core.device import MiedaDevice
from ...backports.enum import StrEnum

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    power = "power"
    heating = "heating"
    heat_insulating = "heat_insulating"
    current_temperature = "current_temperature"
    target_temperature = "target_temperature"
    mode = "mode"
    whole_tank_heating = "whole_tank_heating"
    variable_heating = "variable_heating"
    protection = "protection"
    heating_power = "heating_power"
    auto_cut_out = "auto_cut_out"


class MideaE2Device(MiedaDevice):
    def __init__(
            self,
            name: str,
            device_id: int,
            ip_address: str,
            port: int,
            token: str,
            key: str,
            protocol: int,
            model: str
    ):
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=0xE2,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            protocol=protocol,
            model=model
        )
        self._attributes = {
            DeviceAttributes.power: False,
            DeviceAttributes.heating: False,
            DeviceAttributes.heat_insulating: False,
            DeviceAttributes.current_temperature: None,
            DeviceAttributes.target_temperature: 40,
            DeviceAttributes.mode: 0,
            DeviceAttributes.whole_tank_heating: False,
            DeviceAttributes.variable_heating: False,
            DeviceAttributes.protection: False,
            DeviceAttributes.heating_power: None,
            DeviceAttributes.auto_cut_out: False
        }

    def build_query(self):
        return [MessageQuery(self._device_protocol_version)]

    def process_message(self, msg):
        message = MessageE2Response(msg)
        _LOGGER.debug(f"[{self.device_id}] Received: {message}")
        new_status = {}
        for status in self._attributes.keys():
            if hasattr(message, status.value):
                self._attributes[status] = getattr(message, status.value)
                new_status[status.value] = getattr(message, status.value)
        return new_status

    def make_message_set(self):
        message = MessageSet(self._device_protocol_version)
        message.mode = self._attributes[DeviceAttributes.mode]
        message.whole_tank_heating = self._attributes[DeviceAttributes.whole_tank_heating]
        message.protection = self._attributes[DeviceAttributes.protection]
        message.target_temperature = self._attributes[DeviceAttributes.target_temperature]
        message.variable_heating = self._attributes[DeviceAttributes.variable_heating]
        message.auto_cut_out = self._attributes[DeviceAttributes.auto_cut_out]
        return message

    def set_attribute(self, attr, value):
        if attr not in [DeviceAttributes.heating,
                        DeviceAttributes.heat_insulating,
                        DeviceAttributes.current_temperature,
                        DeviceAttributes.protection,
                        DeviceAttributes.heating_power]:
            if attr == DeviceAttributes.power:
                message = MessagePower(self._device_protocol_version)
                message.power = value
            else:
                message = self.make_message_set()
                setattr(message, str(attr), value)
            self.build_send(message)


class MideaAppliance(MideaE2Device):
    pass
