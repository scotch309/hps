from bluez_peripheral.gatt.service import Service
from dbus_next.service import method
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
from bluez_peripheral.util import *
from bluez_peripheral.util import get_message_bus
from bluez_peripheral.advert import Advertisement
from bluez_peripheral.agent import BaseAgent, AgentCapability
import asyncio, subprocess
from bluez_peripheral.gatt.service import Service

class MyAgent(BaseAgent):
    def __init__(self, capability: AgentCapability):
        super().__init__(capability)
    @method()
    def Cancel():
        pass
    @method()
    def Release():
        pass
    @method()
    def RequestPinCode(self, device: "o") -> "s": # type: ignore
        return "1234567890123456"
    @method()
    def DisplayPinCode(self, device: "o", pincode: "s"): # type: ignore
        pass
    @method()
    def RequestPasskey(self, device: "o") -> "u": # type: ignore
        return 1234567890123456
    @method()
    def DisplayPasskey(self, device: "o", passkey: "u", entered: "q"): # type: ignore
        print(passkey)
    @method()
    def RequestConfirmation(self, device: "o", passkey: "u"): # type: ignore
        print(passkey)
    @method()
    def RequestAuthorization(self, device: "o"): # type: ignore
        pass
    @method()
    def AuthorizeService(self, device: "o", uuid: "s"): # type: ignore
        pass

class MyService(Service):
    def __init__(self):
        self._some_value = None
        super().__init__("BEEF", True)
    @characteristic("BEF0", CharFlags.READ)
    def my_readonly_characteristic(self, options):
        return bytes("Hello World!", "utf-8")
    @characteristic("BEF1", CharFlags.WRITE)
    def my_writeonly_characteristic(self, options):
        pass
    @my_readonly_characteristic.setter
    def my_writeonly_characteristic(self, value, options):
        self._some_value = value
    @descriptor("BEF2", my_readonly_characteristic, DescFlags.READ)
    def my_readonly_descriptors(self, options):
        return bytes("This characteristic is completely pointless!", "utf-8")

def run_command(command_line):
    sproc = subprocess.Popen(command_line,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            bufsize = -1, shell = True)
    stdout, stderr = sproc.communicate()
    rtncode = sproc.returncode
    return rtncode, stdout, stderr

async def main():
    my_service_ids = ["BEEF"]
    my_appearance = 0
    my_timeout = 60

    cmd = 'sudo hciconfig hci0 piscan'
    rtc_code, stdout, stderr = run_command(cmd)
    if rtc_code != 0:
        print(f'{cmd} command failed. rtncode={rtc_code}')
        return

    bus = await get_message_bus()

    service = MyService()
    await service.register(bus)

    agent = MyAgent(AgentCapability.NO_INPUT_NO_OUTPUT)
    await agent.register(bus)

    adapter = await Adapter.get_first(bus)
    advert = Advertisement("hps", my_service_ids, my_appearance, my_timeout)
    await advert.register(bus, adapter)
    while True:
        await asyncio.sleep(5)
    await bus.wait_for_disconnect()

if __name__ == '__main__':
    asyncio.run(main())