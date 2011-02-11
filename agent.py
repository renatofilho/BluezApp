import dbus
import dbus.service

class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"

class BluezAgent(dbus.service.Object):
    exit_on_release = True

    def __init__(self, bus, path, parent, pinCode = None):
        super(BluezAgent, self).__init__(bus, path)
        self._pinCode = pinCode
        self._parent = parent

    def set_exit_on_release(self, exit_on_release):
        self.exit_on_release = exit_on_release

    @dbus.service.method("org.bluez.Agent",
                    in_signature="", out_signature="")
    def Release(self):
        self._parent._connectionFinish(self._device)
        self._device = None
        print "Release"

    @dbus.service.method("org.bluez.Agent",
                    in_signature="os", out_signature="")
    def Authorize(self, device, uuid):
        print "Authorize (%s, %s)" % (device, uuid)
        authorize = raw_input("Authorize connection (yes/no): ")
        if (authorize == "yes"):
            return
        raise Rejected("Connection rejected by user")

    @dbus.service.method("org.bluez.Agent",
                    in_signature="o", out_signature="s")
    def RequestPinCode(self, device):
        print "RequestPinCode (%s)" % (device)
        self._device = device
        return self._pinCode

    @dbus.service.method("org.bluez.Agent",
                    in_signature="o", out_signature="u")
    def RequestPasskey(self, device):
        print "RequestPasskey (%s)" % (device)
        passkey = raw_input("Enter passkey: ")
        return dbus.UInt32(passkey)

    @dbus.service.method("org.bluez.Agent",
                    in_signature="ou", out_signature="")
    def DisplayPasskey(self, device, passkey):
        print "DisplayPasskey (%s, %d)" % (device, passkey)

    @dbus.service.method("org.bluez.Agent",
                    in_signature="ou", out_signature="")
    def RequestConfirmation(self, device, passkey):
        print "RequestConfirmation (%s, %d)" % (device, passkey)
        confirm = raw_input("Confirm passkey (yes/no): ")
        if (confirm == "yes"):
            return
        raise Rejected("Passkey doesn't match")

    @dbus.service.method("org.bluez.Agent",
                    in_signature="s", out_signature="")
    def ConfirmModeChange(self, mode):
        print "ConfirmModeChange (%s)" % (mode)
        authorize = raw_input("Authorize mode change (yes/no): ")
        if (authorize == "yes"):
            return
        raise Rejected("Mode change by user")

    @dbus.service.method("org.bluez.Agent",
                    in_signature="", out_signature="")
    def Cancel(self):
        print "Cancel"
