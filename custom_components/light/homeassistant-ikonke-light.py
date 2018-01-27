import os

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT,
    ATTR_RGB_COLOR, ATTR_WHITE_VALUE, ATTR_XY_COLOR, SUPPORT_BRIGHTNESS,
    SUPPORT_COLOR_TEMP, SUPPORT_EFFECT, SUPPORT_RGB_COLOR, SUPPORT_WHITE_VALUE,
    Light)

platformVersion = "0.0.2"

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    print(\
        "[IkonkeLightPlatform][INFO]*******************************************************************\r\n"\
        "[IkonkeLightPlatform][INFO]               IkonkeLightPlatform v%s By YinHang \r\n"\
        "[IkonkeLightPlatform][INFO] GitHub: https://github.com/YinHangCode/homeassistant-ikonke-light \r\n"\
        "[IkonkeLightPlatform][INFO]                                               QQ Group: 107927710 \r\n"\
        "[IkonkeLightPlatform][INFO]*******************************************************************\r\n"\
        "[IkonkeLightPlatform][INFO]start success...\r\n"\
    %(platformVersion))
    
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
        command = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" getRelay'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd)
        result = os.popen(command).read().strip('\n')
        if result == 'open':
            self._state = True
            self._available = True
        elif result == 'close':
            self._state = False
            self._available = True
        else:
            self._available = False
        
        command2 = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" getBrightness'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd)
        result = os.popen(command2).read().strip('\n')
        if result == 'fail':
            self._available = False
        else:
            self._brightness = int(255 * int(result) / 100)
            self._available = True
        
        command3 = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" getRGB'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd)
        result = os.popen(command3).read().strip('\n')
        if result == 'fail':
            self._available = False
        else:
            self._rgb = result.split(',')
            self._available = True
    
    def turn_on(self, **kwargs):
        if self._state == False:
            command = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" setRelay open'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd)
            # print(command)
            result = os.popen(command).read().strip('\n')
            if result == 'success':
                self._state = True
            else:
                pass
        
        if ATTR_RGB_COLOR in kwargs:
            command2 = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" setRGB "{rgb}"'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd, rgb=','.join(str(i) for i in kwargs[ATTR_RGB_COLOR]))
            # print(command2)
            result = os.popen(command2).read().strip('\n')
            if result == 'success':
                self._rgb = kwargs[ATTR_RGB_COLOR]
            else:
                pass
        
        if ATTR_BRIGHTNESS in kwargs:
            command3 = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" setBrightness "{brightness}"'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd, brightness=str(int(100 * kwargs[ATTR_BRIGHTNESS] / 255)))
            # print(command3)
            result = os.popen(command3).read().strip('\n')
            if result == 'success':
                self._brightness = kwargs[ATTR_BRIGHTNESS]
            else:
                pass
        
        self.schedule_update_ha_state()
    
    def turn_off(self, **kwargs):
        command = 'sh "{ikonkeio}" -C "{type}" "{ip}" "{mac}" "{password}" setRelay close'.format(ikonkeio=self.ikonkeIO, type=self.type, ip=self.ip, mac=self.mac, password=self.passwd)
        result = os.popen(command).read().strip('\n')
        if result == 'success':
            self._state = False
            self.schedule_update_ha_state()
        else:
            pass


