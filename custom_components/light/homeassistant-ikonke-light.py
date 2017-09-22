import os

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT,
    ATTR_RGB_COLOR, ATTR_WHITE_VALUE, ATTR_XY_COLOR, SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP, SUPPORT_EFFECT, SUPPORT_RGB_COLOR, SUPPORT_WHITE_VALUE,
    Light)

platformVersion = "0.0.1"

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    print("[IkonkeLightPlatform][INFO]********************************************************************")
    print("[IkonkeLightPlatform][INFO]                IkonkeLightPlatform v%s By YinHang"%(platformVersion))
    print("[IkonkeLightPlatform][INFO]  GitHub: https://github.com/YinHangCode/homeassistant_ikonke_light ")
    print("[IkonkeLightPlatform][INFO]                                                QQ Group: 107927710 ")
    print("[IkonkeLightPlatform][INFO]********************************************************************")
    print("[IkonkeLightPlatform][INFO]start success...")
    
    addDeviceArr = []
    
    ikonkeIO = config.get("ikonkeIO")
    deviceCfgs = config.get("deviceCfgs")
    for deviceCfg in deviceCfgs:
            type = deviceCfg.get("type")
            if type == "klight":
                addDeviceArr.append(\
                    KLight("klight_" + deviceCfg.get("mac").replace('-',''), ikonkeIO, deviceCfg.get("type"), deviceCfg.get("ip"), deviceCfg.get("mac"), deviceCfg.get("password")))
            else:
                print("[IkonkeLightPlatform][ERROR]error type" + type)
    
    add_devices_callback(addDeviceArr)

class KLight(Light):
    ikonkeIO = ''
    type = ''
    ip = ''
    mac = ''
    passwd = ''
    
    def __init__(self, name, ikonkeIO, type, ip, mac, passwd):
        self._name = name or DEVICE_DEFAULT_NAME
        self._state = False
        self._available = False
        self._rgb = (255, 255, 255)
        self._brightness = 180
        
        self.ikonkeIO = ikonkeIO
        self.type = type
        self.ip = ip
        self.mac = mac
        self.passwd = passwd
        
        self.update()
    
    @property
    def name(self):
        return self._name
    
    @property
    def available(self) -> bool:
        return self._available
    
    @property
    def is_on(self):
        return self._state
    
    @property
    def should_poll(self):
        return True
    
    @property
    def rgb_color(self):
        return self._rgb
    
    @property
    def brightness(self):
        return self._brightness
    
    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS | SUPPORT_RGB_COLOR
    
    def update(self):
        command = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' getRelay'
        result = os.popen(command).read().strip('\n')
        if result == 'open':
            self._state = True
            self._available = True
        elif result == 'close':
            self._state = False
            self._available = True
        else:
            self._available = False
        
        command = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' getBrightness'
        result = os.popen(command).read().strip('\n')
        if result == 'fail':
            self._available = False
        else:
            self._brightness = int(255 * int(result) / 100)
            self._available = True
        
        command = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' getRGB'
        result = os.popen(command).read().strip('\n')
        if result == 'fail':
            self._available = False
        else:
            self._rgb = result.split(',')
            self._available = True
    
    def turn_on(self, **kwargs):
        if self._state == False:
            command = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' setRelay open'
            # print(command)
            result = os.popen(command).read().strip('\n')
            if result == 'success':
                self._state = True
            else:
                pass
        
        if ATTR_RGB_COLOR in kwargs:
            command2 = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' setRGB ' + ','.join(str(i) for i in kwargs[ATTR_RGB_COLOR])
            # print(command2)
            result = os.popen(command2).read().strip('\n')
            if result == 'success':
                self._rgb = kwargs[ATTR_RGB_COLOR]
            else:
                pass
        
        if ATTR_BRIGHTNESS in kwargs:
            command3 = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' setBrightness ' + str(int(100 * kwargs[ATTR_BRIGHTNESS] / 255))
            # print(command3)
            result = os.popen(command3).read().strip('\n')
            if result == 'success':
                self._brightness = kwargs[ATTR_BRIGHTNESS]
            else:
                pass
        
        self.schedule_update_ha_state()
    
    def turn_off(self, **kwargs):
        command = 'sh ' + self.ikonkeIO + ' -C ' + self.type + ' ' + self.ip + ' ' + self.mac + ' ' + self.passwd + ' setRelay close'
        result = os.popen(command).read().strip('\n')
        if result == 'success':
            self._state = False
            self.schedule_update_ha_state()
        else:
            pass


