from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
import requests

requests_functions = {
    b'\x01': requests.get,
    b'\x03': requests.post,
    b'\x04': requests.put,
    b'\x06': requests.get,
    b'\x08': requests.post,
    b'\x09': requests.put,
}

class WebClient:
    default_request = {
        'uri': None,
        'headers': None,
        'body': None
    }
    default_response = {
        'headers': None,
        'body': None
    }
    def __init__(self):
        self.request = self.default_request
        self.response = self.default_response

class HPS(Service):
    def __init__(self):
        self.service_uuid = '1823'
        super().__init__(self.service_uuid, True)

    @characteristic('2AB6', CharFlags.WRITE).setter
    def URI_write(self, value, options):
        print(value)

    @characteristic('2AB7', CharFlags.READ)
    def Headers_read(self, options):
        return bytes('headers', 'utf-8')
    @characteristic('2AB7', CharFlags.WRITE).setter
    def Headers_write(self, value, options):
        print(value)

    @characteristic('2AB9', CharFlags.READ)
    def Entity_Body_read(self, options):
        return bytes('entity body', 'utf-8')
    @characteristic('2AB9', CharFlags.WRITE).setter
    def Entity_Body_write(self, value, options):
        print(value)

    @characteristic('2ABC', CharFlags.WRITE).setter
    def Control_Point_write(self, value, options):
        print(value)
        print(tables[value])

    @characteristic('2AB8', CharFlags.NOTIFY)
    def Status_Code_notify(self, options):
        pass

    @characteristic('2ABB', CharFlags.READ)
    def Security(self, options):
        return bytes('security', 'utf-8')