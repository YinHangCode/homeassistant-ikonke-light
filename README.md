# homeassistant-ikonke-light

HomeAssistant的控客插座插件。   
   
**注: 如果有bug请提交到 [issues](https://github.com/YinHangCode/homeassistant-ikonke-light/issues) 或 [QQ群: 107927710](//shang.qq.com/wpa/qunwpa?idkey=8b9566598f40dd68412065ada24184ef72c6bddaa11525ca26c4e1536a8f2a3d)。**   

![](https://raw.githubusercontent.com/YinHangCode/homeassistant-ikonke-light/master/images/KLight.jpg)

## 支持的设备
1.K Light   

## 安装说明
1.安装HomeAssistant。   
2.安装[ikonkeIO](https://github.com/YinHangCode/ikonkeIO)。   
3.将homeassistant-ikonke-light.py文件放到~/.homeassistant/custom_components/light/下。

## 配置说明
配置"ikonkeIO"为ikonkeIO目录下sh文件的绝度路径。   
设备的"type"、"ip"、"mac"、"password"可以通过ikonkeIO获取，具体参考[ikonkeIO](https://github.com/YinHangCode/ikonkeIO)项目。   
示例如下：   
```
light:
  - platform: homeassistant-ikonke-light
    ikonkeIO: '/home/pi/ikonkeIO/ikonkeIO.sh'
    deviceCfgs:
      - type: 'klight'
        ip: '192.168.88.20'
        mac: '18-fe-56-d7-5d-ea'
        password: 'A?lz?=]G'
      - type: 'klight'
        ip: '192.168.88.21'
        mac: '18-fe-56-d8-5a-e6'
        password: '[58DzqaX'
      - type: 'klight'
        ip: '192.168.88.22'
        mac: '18-fe-78-d1-0f-3e'
        password: 'aDU[7.AQ'
```
## 版本更新记录
### 0.0.2
1.修复密码的首字母是"/"的情况下报错的bug.   
### 0.0.1
1.支持控制K Light设备.   
