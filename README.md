# Power_charging_simulation_for_Arknight_Endfield
模拟明日方舟：终末地中的发电耗电过程，以验证极限发电方案是否会中途停电

发电方案默认为多个热能池稳定供电，单个热能池间歇发电。该方案在一些情况下无法实现极限压缩发电功率，但会有最稳定的预期。

`power_consumpsion`为总耗电功率，`power_generation`为最高发电功率，`power_per_battery`为单热能池发电功率（高容谷地电池为1100，低容武陵电池为1600）

只需设置上述3个参数，运行程序即可得到一段二进制数表示的传送带设置方案。配合蓝图码使用，将二进制数为1的位对应的中间一行的汇流器改为物流桥即可。

蓝图码：
EF01o5u88AEeU6aIieO

![实时电量](power_curve.jpg)
