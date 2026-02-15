
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

dac_bits = [10, 9, 11, 5, 6, 13, 19, 26]  

dynamic_range = 3.3  

GPIO.setup(dac_bits, GPIO.OUT)

def voltage_to_number(voltage):
    
    if voltage < 0:
        print(f"Напряжение не может быть отрицательным (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем 0.0 В")
        return 0
    
    if voltage > dynamic_range:
        print(f"Напряжение выходит за динамический диапазон ЦАП (0.00 - {dynamic_range:.2f} В)")
        print("Устанавливаем максимальное напряжение")
        return 255
    
    number = int(voltage / dynamic_range * 255)
    return number

def number_to_dac(number):
    
    if number < 0:
        number = 0
    elif number > 255:
        number = 255
    
    
    for i, bit_pin in enumerate(dac_bits):
        bit_value = (number >> i) & 1
        GPIO.output(bit_pin, bit_value)
    
    actual_voltage = number / 255 * dynamic_range
    print(f"Установлено число: {number:3d} (0x{number:02X})")
    print(f"Выходное напряжение: {actual_voltage:.3f} В")
    print(f"Двоичный код: {number:08b} (MSB -> LSB)")
    print("-" * 40)

def print_help():
    """Выводит подсказку по использованию"""
    print("\n" + "="*50)
    print("УПРАВЛЕНИЕ 8-БИТНЫМ ЦАП")
    print("="*50)
    print(f"Динамический диапазон: 0.00 - {dynamic_range:.2f} В")
    print("Для выхода нажмите Ctrl+C")
    print("-"*50)

def main():
    """Основная функция скрипта"""
    print_help()
    
    try:
        while True:
            try:
                
                user_input = input("\nВведите напряжение в Вольтах: ")
                voltage = float(user_input)
                number = voltage_to_number(voltage)
                number_to_dac(number)
                
            except ValueError:
                print("Ошибка: Вы ввели не число. Попробуйте ещё раз")
                print("Примеры корректного ввода: 1.5, 2.0, 0.75")
                
    except KeyboardInterrupt:
        print("\n\nПрограмма остановлена пользователем")
        
    finally:
        print("\nЗавершение работы...")
        GPIO.output(dac_bits, 0)
        GPIO.cleanup()
        
        print("Выход ЦАП установлен в 0 В")
        print("Настройки GPIO сброшены")
