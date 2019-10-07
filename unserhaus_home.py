"""Starts a fake fan, lightbulb, garage door and a TemperatureSensor
"""
import logging
import signal
import random
import getopt
import sys

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

    def __init__(self, *args, xknx, objname, group_address, **kwargs):
        super().__init__(*args, **kwargs)

        serv_switch = self.add_preload_service('Switch')
        self.char_switch = serv_switch.configure_char('On',setter_callback=self.set_switch)
        
        self.switch = Switch(xknx,
                    name=objname,
                    group_address=group_address)

    
    # @Accessory.run_at_interval(3)
    # async def run(self):
    #     self.char_temp.set_value(random.randint(18, 26))

    
    def __setstate__(self, state):
        self.__dict__.update(state)
        #self._gpio_setup(self.pin)

    def set_switch(self, value):
        #print(xknx)
        if value:
            logging.debug("set_switch: %s", value)
            #loop.run_until_complete(self.switch.set_on())
            #asyncio.run(self.switch.set_on()) 
            #asyncio.create_task(self.switch.set_on())
            #await self.switch.set_on()
            self.driver.add_job(self.switch.set_on())
            #self.driver.loop.create_task(self.switch.set_on())
            #asyncio.get_event_loop().run_until_complete(self.switch.set_on())
            #print("set_switch: %s" %  value)
        else:
            logging.debug("set_switch: %s", value)
            #loop.run_until_complete(self.switch.set_off())
            #asyncio.run(self.switch.set_off())
            self.driver.add_job(self.switch.set_off())
            #self.driver.loop.create_task(self.switch.set_off())
            #print("set_switch: %s" % value)




class KNXBridge(Bridge):
    def __init__(self, *args, xknx, **kwargs):
        super().__init__(*args, **kwargs)

    async def stop(self):
        await xknx.stop()
        await super().stop()
        

def get_bridge(driver,bridge_name,xknx):
    #print('get_bridge')
    bridge = KNXBridge(driver, bridge_name, xknx=xknx)
    #bridge = Bridge(driver, 'Homekit KNX Bridge')
    # bridge.add_accessory(LightBulb(driver, 'Fake Lightbulb'))
    # bridge.add_accessory(FakeFan(driver, 'Fake Big Fan'))
    # bridge.add_accessory(GarageDoor(driver, 'Fake Garage'))
    # bridge.add_accessory(TemperatureSensor(driver, 'Fake Sensor'))
    bridge.add_accessory(KnxSwitch(driver, 'Anwesend', xknx=xknx, objname='HK_00ZE_JZH',group_address='0/3/5'))
    bridge.add_accessory(KnxSwitch(driver, 'Licht', xknx=xknx, objname='L_03DI_1',group_address='3/0/5'))
    

    return bridge

def show_help():
    """Print Help."""
    print("HomeKit KNX Bridge")
    print("")
    print("Usage:")
    print("")
    print(__file__, "                            Start with defaults")
    print(__file__, "-n --name                   Set bridge name")
    print(__file__, "-h --help                   Print help")
    print("")

async def telegram_received_cb(telegram):
    print("Telegram received: {0}".format(telegram))

async def get_xknx():
    #print("get_xknx")
    xknx = XKNX(config="xknx.yaml")
    await xknx.start()

    return xknx

if __name__ == "__main__":

    # pylint: disable=invalid-name

    bridge_name = "HomeKit KNX Bridge"

    """Parse command line arguments."""
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "hn:", ["help", "name="])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    address_filters = None
    for opt, arg in opts:
        if opt in ['-h', '--help']:
            show_help()
            sys.exit()
        if opt in ['-n', '--name']:
            bridge_name = arg

    logging.info("Bridge name: %s", bridge_name)
    
    loop = asyncio.get_event_loop()

    try:
        xknx = loop.run_until_complete(get_xknx())
    except Exception as e:
        logging.info('Exception for KNX: %s',e)
        logging.info('Exiting...')
        sys.exit(1)
    
    driver = AccessoryDriver(loop=loop, port=51826, persist_file='unserhaus_home.state')
    
    driver.add_accessory(accessory=get_bridge(driver, bridge_name, xknx))

    signal.signal(signal.SIGTERM, driver.signal_handler)

    driver.start()
    #driver.async_add_job(xknx.start())
    
    #driver.add_job(xknx.stop())
    #loop.run_until_complete(xknx.stop())
   # driver.stop()