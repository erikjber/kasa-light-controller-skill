from mycroft import MycroftSkill, intent_file_handler
from kasa import SmartPlug, Discover
import asyncio
import time

class KasaLightController(MycroftSkill):
    def __init__(self):
        self.devices = {}
        MycroftSkill.__init__(self)

    def locate_all(self):
        """Find all devices on the network"""
        devs = asyncio.run(Discover.discover())
        self.devices = {}
        for addr,dev in devs.items():
            asyncio.run(dev.update())
            self.devices[dev.alias.lower()]=addr

    def turn_off(self,name):
        """Turn off a named device"""
        name = name.lower()
        if name in self.devices:
            addr = self.devices[name]
            plug = SmartPlug(addr)
            asyncio.run(plug.turn_off())
            return True
        return False

    def turn_on(self,name):
        """Turn on a named device"""
        name = name.lower()
        if name in self.devices:
            addr = self.devices[name]
            plug = SmartPlug(addr)
            asyncio.run(plug.turn_on())
            return True
        return False

    @intent_file_handler('controller.light.kasa.on.intent')
    def handle_controller_light_on(self, message):
        name = message.data.get('name')
        self.locate_all()
        if 'living room' in name:
            self.turn_on('moon')
            self.turn_on('window')
            self.turn_on('reading')
            self.turn_on('globe')
            self.turn_on('mirror')
        else:
            res = self.turn_on(name)
            if res == False:
                self.speak("Could not find " + name)

    @intent_file_handler('controller.light.kasa.off.intent')
    def handle_controller_light_off(self, message):
        name = message.data.get('name')
        self.locate_all()
        if 'living room' in name:
            self.turn_off('moon')
            self.turn_off('window')
            self.turn_off('reading')
            self.turn_off('globe')
            self.turn_off('mirror')
        else:
            res = self.turn_off(name)
            if res == False:
                self.speak("Could not find " + name)


def create_skill():
    return KasaLightController()

