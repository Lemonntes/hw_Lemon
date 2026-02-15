import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose = False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT, initial = 0)
    
    def deinit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        if number < 0:
            number = 0
        elif number > 255:
            number = 255
        
        for i in range(8):
            GPIO.output(self.gpio_bits[i], (number >> i) & 1)
        
        if self.verbose:
            actual_voltage = number / 255 * self.dynamic_range
            print(f"Установлено число: {number}, напряжение: {actual_voltage:.3f} В")
    
    def set_voltage(self, voltage):
        if voltage < 0:
            number = 0
        elif voltage > self.dynamic_range:
            number = 255
        else:
            number = int(voltage / self.dynamic_range * 255)
        
        self.set_number(number)

if __name__ == "__main__":
    dac_pins = [10, 9, 11, 5, 6, 13, 19, 26]
    
    try:
        dac = R2R_DAC(dac_pins, 3.3, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в Вольтах: "))
                dac.set_voltage(voltage)
            except ValueError:
                print("Вы ввели не число. Попробуйте ещё раз\n")
    finally:
        dac.deinit()