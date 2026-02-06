import matplotlib.pyplot as plt
import math

default_power = 12  # 使用的分流器数量
charge_cycle = 40 # 一个电池可以让热能池工作40秒
power_maximum = 100000
power_consumpsion = 5475  
power_generation = 5700
power_per_battery = 1100
power_increase = power_generation - power_consumpsion  # 发电时每秒增加的电量
power_decrease = power_consumpsion - (power_generation - power_per_battery) # 不发电时每秒减少的电量

conveyor_power_minimum = (charge_cycle * power_per_battery) / (pow(2, default_power + 1))  # 分流器最末端的发电功率
binary_numbers = bin(math.ceil(power_decrease / conveyor_power_minimum) + 1)[2:]  # 所需发电功率除以分流器最末端功率得到的倍数向上取整后，转化为二进制数
binary_conveyor = binary_numbers.zfill(default_power)
print(f"二分传送带设置：{binary_conveyor}")

    
power_current = 0
battery_conveyed = 3
time = 0  # 离散循环时间
count = 0 # 停电次数

class Conveyor:
    """传送带，按一定时间周期送电池"""
    def __init__(self, period):
        self.period = period #传送周期
    
    def set_period(self, period):
        self.period = period
        
    def run(self):
        global battery_conveyed
        
        if self.period == -1: return
            
        if time % self.period == 0:
            battery_conveyed = battery_conveyed + 1        

class Generator:
    """发电机"""
    def __init__(self):
        self.cycle = charge_cycle
        self.charge_timer = 0
        self.charge_enable = True
        
    def run(self):
        global power_current, battery_conveyed, count
        
        if self.charge_enable: # 在发电
            power_current = power_current + power_increase
            if power_current > power_maximum:
                power_current = power_maximum
            self.charge_timer = self.charge_timer + 1
            if self.charge_timer >= self.cycle:
                self.charge_enable = False
                self.charge_timer = 0    
        elif battery_conveyed > 0: # 不在发电但有电池
            power_current = power_current - power_decrease
            if power_current <= 0:
                power_current = 0
            self.charge_enable = True
            battery_conveyed = battery_conveyed - 1
        else: #不在发电且没有电池
            power_last = power_current
            power_current = power_current - power_decrease
            if power_current <= 0:
                power_current = 0
            if power_last > 0 and power_current == 0:    
                count = count + 1

if __name__ == '__main__':
    # 初始化传送带
    conveyors = [Conveyor(-1) for i in range(default_power)] 
    for i, binary_number in enumerate(binary_conveyor):
        if binary_number == "1":
            conveyors[i].set_period(pow(2, i + 2))
        elif binary_number != "0":
            print("二分传送带格式错误")
            break
            
    # 初始化发电机
    generator = Generator()
    
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write("开始\n")
    
    time_line = range(0, 16385, 1)
    power_current_line = []   
    for time in time_line:
        for conveyor in conveyors:
            conveyor.run()
        generator.run()
        
        power_current_line.append(power_current)    
        with open("output.txt", "a", encoding="utf-8") as file:
            file.write(f"当前时间：{time}\t当前电量：{power_current}\t充电状态：{generator.charge_enable}\t停电次数：{count}\n")
    
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'KaiTi', 'FangSong'] 
    plt.plot(time_line, power_current_line)
    plt.title('实时电量曲线')
    plt.xlabel('时间')
    plt.ylabel('实时电量')      
    plt.show()  