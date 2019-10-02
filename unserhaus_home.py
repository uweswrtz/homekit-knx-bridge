"""Starts a fake fan, lightbulb, garage door and a TemperatureSensor
"""
import logging
import signal
import random

from pyhap.accessory import Accessory, Bridge
from pyhap.accessory_driver import AccessoryDriver
from pyhap.const import (CATEGORY_FAN,
                         CATEGORY_LIGHTBULB,
                         CATEGORY_GARAGE_DOOR_OPENER,
                         CATEGORY_SENSOR,
                         CATEGORY_PROGRAMMABLE_SWITCH,
                         CATEGORY_SWITCH
                        )


"""
From XKNX example_switch.py
Example for Switch device.
"""
import asyncio

from xknx import XKNX
from xknx.devices import Switch

logging.basicConfig(level=logging.INFO, format="[%(module)s] %(message)s")


class TemperatureSensor(Accessory):
    """Fake Temperature sensor, measuring every 3 seconds."""

    category = CATEGORY_SENSOR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_temp = self.add_preload_service('TemperatureSensor')
        self.char_temp = serv_temp.configure_char('CurrentTemperature')

    @Accessory.run_at_interval(3)
    async def run(self):
        self.char_temp.set_value(random.randint(18, 26))

class ProgrammableSwitch(Accessory):
    """Fake Temperature sensor, measuring every 3 seconds."""

    category = CATEGORY_PROGRAMMABLE_SWITCH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_sps = self.add_preload_service('StatelessProgrammableSwitch')
        self.char_sps = serv_sps.configure_char('ProgrammableSwitchEvent',setter_callback=self.set_bulb)

    # @Accessory.run_at_interval(3)
    # async def run(self):
    #     self.char_temp.set_value(random.randint(18, 26))

    
    def __setstate__(self, state):
        self.__dict__.update(state)
        #self._gpio_setup(self.pin)

    def set_bulb(self, value):
        if value:
            logging.debug("set_bulb: %s", value)
        else:
            logging.debug("set_bulb: %s", value)

    # def stop(self):
    #     super().stop()
    #     GPIO.cleanup()

class HapSwitch(Accessory):
    """Fake Temperature sensor, measuring every 3 seconds."""

    category = CATEGORY_SWITCH

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_switch = self.add_preload_service('Switch')
        self.char_switch = serv_switch.configure_char('On',setter_callback=self.set_switch)

    # @Accessory.run_at_interval(3)
    # async def run(self):
    #     self.char_temp.set_value(random.randint(18, 26))

    
    def __setstate__(self, state):
        self.__dict__.update(state)
        #self._gpio_setup(self.pin)

    def set_switch(self, value):
        if value:
            logging.debug("set_switch: %s", value)
            print("set_switch: %s" %  value)
        else:
            logging.debug("set_switch: %s", value)
            print("set_switch: %s" % value)

    # def stop(self):
    #     super().stop()
    #     GPIO.cleanup()




class FakeFan(Accessory):
    """Fake Fan, only logs whatever the client set."""

    category = CATEGORY_FAN

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the fan service. Also add optional characteristics to it.
        serv_fan = self.add_preload_service(
            'Fan', chars=['RotationSpeed', 'RotationDirection'])

        self.char_rotation_speed = serv_fan.configure_char(
            'RotationSpeed', setter_callback=self.set_rotation_speed)
        self.char_rotation_direction = serv_fan.configure_char(
            'RotationDirection', setter_callback=self.set_rotation_direction)

    def set_rotation_speed(self, value):
        logging.debug("Rotation speed changed: %s", value)

    def set_rotation_direction(self, value):
        logging.debug("Rotation direction changed: %s", value)

class LightBulb(Accessory):
    """Fake lightbulb, logs what the client sets."""

    category = CATEGORY_LIGHTBULB

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        serv_light = self.add_preload_service('Lightbulb')
        self.char_on = serv_light.configure_char(
            'On', setter_callback=self.set_bulb)

    def set_bulb(self, value):
        logging.info("Bulb value: %s", value)

class GarageDoor(Accessory):
    """Fake garage door."""

    category = CATEGORY_GARAGE_DOOR_OPENER

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_preload_service('GarageDoorOpener')\
            .configure_char(
                'TargetDoorState', setter_callback=self.change_state)

    def change_state(self, value):
        logging.info("Bulb value: %s", value)
        self.get_service('GarageDoorOpener')\
            .get_characteristic('CurrentDoorState')\
            .set_value(value)

class KnxSwitch(Accessory):
    """KNX Switch"""

    category = CATEGORY_SWITCH

    def __init__(self, *args, xknx, **kwargs):
        super().__init__(*args, **kwargs)

        serv_switch = self.add_preload_service('Switch')
        self.char_switch = serv_switch.configure_char('On',setter_callback=self.set_switch)
        
        self.switch = Switch(xknx,
                    name='HK_00ZE_JZH',
                    group_address='0/3/5')
    
    # @Accessory.run_at_interval(3)
    # async def run(self):
    #     self.char_temp.set_value(random.randint(18, 26))

    
    def __setstate__(self, state):
        self.__dict__.update(state)
        #self._gpio_setup(self.pin)

    def set_switch(self, value):
        if value:
            # await self.switch.set_on()
            self.switch.set_on()
            logging.debug("set_switch: %s", value)
            print("set_switch: %s" %  value)
        else:
            logging.debug("set_switch: %s", value)
            # await self.switch.set_off()
            self.switch.set_off()
            print("set_switch: %s" % value)

    # def stop(self):
    #     super().stop()
    #     GPIO.cleanup()

def get_bridge(driver,xknx):
    print('get_bridge')
    bridge = Bridge(driver, 'Homekit KNX Bridge')

    # bridge.add_accessory(LightBulb(driver, 'Fake Lightbulb'))
    # bridge.add_accessory(FakeFan(driver, 'Fake Big Fan'))
    # bridge.add_accessory(GarageDoor(driver, 'Fake Garage'))
    # bridge.add_accessory(TemperatureSensor(driver, 'Fake Sensor'))
    bridge.add_accessory(KnxSwitch(driver, 'Jemand@Home', xknx=xknx))

    return bridge

async def get_xknx():
    print("get_xknx")
    xknx = XKNX(config='xknx.yaml')
    #await xknx.start()

    return xknx

if __name__ == "__main__":
    # pylint: disable=invalid-name
    try:
        print("dummy")
        xknx = asyncio.run(get_xknx())
    except Exception as e:
        print('Exception: ',e)
        print('Exiting...')
        exit()

    driver = AccessoryDriver(port=51826, persist_file='unserhaus_home.state')
    driver.add_accessory(accessory=get_bridge(driver,xknx))
    signal.signal(signal.SIGTERM, driver.signal_handler)

    driver.start()