
######
import RPi.GPIO as GPIO
import gpiod
import time
from datetime import datetime
from gpiozero import OutputDevice
from time import sleep
LINE_OFFSET = 18
chip0 = gpiod.Chip("0", gpiod.Chip.OPEN_BY_NUMBER)

gpio0_b0 = chip0.get_line(LINE_OFFSET)
gpio0_b0.request(consumer="gpio", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])

print(gpio0_b0.consumer())
# Temperature thresholds and timing
TEMP_ON = 48  # Fan on at 48°C
TEMP_OFF = TEMP_ON - 6  # Fan off at 42°C
MIN_RUN_TIME = 120  # minimum run seconds

def get_cpu_temp():
    """Read CPU temperature from Raspberry Pi thermal sensor."""
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = float(f.read()) / 1000  # Convert to Celsius
    return temp

def main():
    fan_running = False
    fan_start_time = 0

    try:
        while True:
          
            temp = get_cpu_temp()
            current_time = time.time()

            if temp > TEMP_ON and not fan_running:
                gpio0_b0.set_value(1)
                print("value1 - on")
                current_datetime = datetime.now()
                print(f"Current Date and Time: {current_datetime}")
                fan_running = True
                fan_start_time = current_time
                print(f"Fan ON: CPU temp = {temp:.1f}°C")
                current_datetime = datetime.now()
                print(f"Current Date and Time: {current_datetime}")
            elif fan_running:
                # Keep fan on for at least MIN_RUN_TIME or if temp is above TEMP_OFF
                if temp <= TEMP_OFF and (current_time - fan_start_time) >= MIN_RUN_TIME:
                    gpio0_b0.set_value(0)
                    print("value0 - off")
                    fan_running = False
                    current_datetime = datetime.now()
                    print(f"Current Date and Time: {current_datetime}")
                    print(f"Fan OFF: CPU temp = {temp:.1f}°C")
                    
                else:
                    print(f"Fan running: CPU temp = {temp:.1f}°C")

            time.sleep(10)  # Check every 10 seconds

    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()  # Reset GPIO settings

if __name__ == "__main__":
    main()