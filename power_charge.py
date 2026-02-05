import matplotlib.pyplot as plt

power_maximum = 100000
power_consumpsion = 5565  
power_generation = 5700
power_per_battery = 1100
power_increase = power_generation - power_consumpsion
power_decrease = power_consumpsion - (power_generation - power_per_battery)

power_current = 0
battery_conveyed = 3
time = 0  # 离散循环时间
count = 0 # 停电次数

class Conveyor:
    """传送带，按一定时间周期送电池"""
    def __init__(self, period):
        self.period = period #传送周期
        
    def run(self):
        global battery_conveyed
        
        if time % self.period == 0:
            battery_conveyed = battery_conveyed + 1        

class Generator:
    """发电机"""
    def __init__(self):
        self.cycle = 40
        self.charge_timer = 0
        self.charge_enable = True
        
    def run(self):
        global power_current, battery_conveyed, count
        
        if self.charge_enable: 
            power_current = power_current + power_increase
            if power_current > power_maximum:
                power_current = power_maximum
            self.charge_timer = self.charge_timer + 1
            if self.charge_timer >= self.cycle:
                self.charge_enable = False
                self.charge_timer = 0    
        elif battery_conveyed > 0:
            power_current = power_current - power_decrease
            if power_current <= 0:
                power_current = 0
            self.charge_enable = True
            battery_conveyed = battery_conveyed - 1
        else:
            power_last = power_current
            power_current = power_current - power_decrease
            if power_current <= 0:
                power_current = 0
            if power_last > 0 and power_current == 0:    
                count = count + 1

if __name__ == '__main__':
    conveyor_1 = Conveyor(64)
    conveyor_2 = Conveyor(256)
    conveyor_3 = Conveyor(512)
    conveyor_4 = Conveyor(2048)
    generator = Generator()
    
    power_current = power_maximum
    
    with open("output.txt", "w", encoding="utf-8") as file:
        file.write("开始\n")
    
    time_line = range(0, 16385, 1)
    power_current_line = []   
    for time in time_line:
        conveyor_1.run()
        conveyor_2.run()
        conveyor_3.run()
        conveyor_4.run()
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