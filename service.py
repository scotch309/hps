from bluez_peripheral.gatt.service import Service
from bluez_peripheral.gatt.characteristic import characteristic, CharacteristicFlags as CharFlags
import requests

request_functions = {
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
        self.req = self.default_request
        self.res = self.default_response
    def request(self, method):
        if (func:=request_functions.get(method,None)) is None:
            return
        response = func(self.req['uri'], proxies={'http':None, 'https':None}, params=self.req['body'], headers=self.req['headers'])
        self.req = self.default_request
        data_status = self.getDataStatus(response)
        return (response.status_code).to_bytes(2,byteorder='little',signed=True)+(data_status).to_bytes(1,byteorder='little',signed=True)

    def getDataStatus(self, response):
        data_status = 0x00

        self.res['headers'] = response.headers
        if len(str(self.res['headers'])) > 512:
            data_status += 0x02
        elif self.res['headers'] is not None:
            data_status += 0x01

        self.res['body'] = response.text
        if len(str(self.res['body'])) > 512:
            data_status += 0x08
        elif self.res['body'] is not None:
            data_status += 0x04
        return data_status

class HPS(Service):
    READ_PROPERTY = CharFlags.READ
    WRITE_PROPERTY = CharFlags.WRITE
    def __init__(self):
        self.service_uuid = '1823'
        self.webclient = WebClient()
        super().__init__(self.service_uuid, True)

    @characteristic('2AB6', WRITE_PROPERTY)
    def URI_write(self, options):
        pass
    @URI_write.setter
    def URI_write(self, value, options):
        self.webclient.req['uri'] = value.decode()
        print(self.webclient.req['uri'])

    @characteristic('2AB7', READ_PROPERTY)
    def Headers_read(self, options):
        res = str(self.webclient.res['headers']) if self.webclient.res['headers'] is not None else ''
        return bytes(res, 'utf-8')
    @characteristic('2AB7', CharFlags.WRITE)
    def Headers_write(self, options):
        pass
    @Headers_write.setter
    def Headers_write(self, value, options):
        self.webclient.req['headers'] = value.decode()
        print(self.webclient.req['headers'])

    @characteristic('2AB9', READ_PROPERTY)
    def Entity_Body_read(self, options):
        res = str(self.webclient.res['body']) if self.webclient.res['body'] is not None else ''
        return bytes(res, 'utf-8')
    @characteristic('2AB9', CharFlags.WRITE)
    def Entity_Body_write(self, options):
        pass
    @Entity_Body_write.setter
    def Entity_Body_write(self, value, options):
        self.webclient.req['body'] = value.decode()
        print(self.webclient.req['body'])

    @characteristic('2ABC', CharFlags.WRITE)
    def Control_Point_write(self, options):
        pass
    @Control_Point_write.setter
    def Control_Point_write(self, value, options):
        self.Status_Code_notify.changed(self.webclient.request(value))

    @characteristic('2AB8', CharFlags.NOTIFY)
    def Status_Code_notify(self, options):
        pass

    @characteristic('2ABB', READ_PROPERTY)
    def Security(self, options):
        return bytes('security', 'utf-8')