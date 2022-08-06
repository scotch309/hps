from bluez_peripheral.gatt.descriptor import descriptor, DescriptorFlags as DescFlags
from bluez_peripheral.util import *
from bluez_peripheral.util import get_message_bus
from bluez_peripheral.advert import Advertisement
import asyncio, subprocess
from bluez_peripheral.gatt.service import Service
from agent import MyAgent
from service import HPS

async def main():
    bus = await get_message_bus()
    service = HPS()
    await service.register(bus)
    agent = MyAgent()
    await agent.register(bus)
    adapter = await Adapter.get_first(bus)
    advert = Advertisement(localName='hps', serviceUUIDs=[service.service_uuid], appearance=0, timeout=60)
    await advert.register(bus, adapter)
    while True:
        await asyncio.sleep(5)
    await bus.wait_for_disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('KeyboardInterrupt END')