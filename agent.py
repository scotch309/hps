from bluez_peripheral.agent import BaseAgent, AgentCapability
from dbus_next.service import method

class MyAgent(BaseAgent):
    def __init__(self, capability: AgentCapability = AgentCapability.NO_INPUT_NO_OUTPUT):
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
