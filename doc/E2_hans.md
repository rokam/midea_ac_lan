# 电热水器
## 特性
- 支持温度设定

## 生成实体
### 默认生成实体
实体ID | 类型 | 描述
--- | --- | ---
water_heater.{DEVICEID}_water_heater | water_heater | 热水器实体

### 额外生成实体

EntityID | 类型 | 名称 | 描述
--- | --- | --- | --- 
binary_sensor.{DEVICEID}_heating | binary_sensor | Heating | 加热
binary_sensor.{DEVICEID}_heat_insulating | binary_sensor | Heat Insulating | 保温
binary_sensor.{DEVICEID}_protection | binary_sensor | Protection | 安全防护
sensor.{DEVICEID}_heating_power | sensor | Heating Power | 加热功率
sensor.{DEVICEID}_current_temperature | sensor | Current Temperature | 当前温度
switch.{DEVICEID}_auto_cut_out | switch | Auto Cut-out | 出水断电
switch.{DEVICEID}_power | switch | Power | 电源开关
switch.{DEVICEID}_variable_heating | switch | Variable Heating | 变频加热
switch.{DEVICEID}_whole_tank_heating | switch | Whole Tank Heating | 全胆速热


## 服务
生成以下扩展服务

### midea_ac_lan.set_attribute

[![Service](https://my.home-assistant.io/badges/developer_call_service.svg)](https://my.home-assistant.io/redirect/developer_call_service/?service=midea_ac_lan.set_attribute)

设置热水器属性, 服务数据:

名称 | 描述
--- | ---
device_id | 设备的编号(Device ID)
attribute | "auto_cut_out"<br />"power"<br />"variable_heating"<br/>"whole_tank_heating"
value | true 或 false

示例
```
service: midea_ac_lan.set_attribute
data:
  device_id: XXXXXXXXXXXX
  attribute: variable_heating
  value: true
```