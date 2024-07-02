import os
from time import sleep


CSV_data = [
    ["Connector_name", "Connector_number","GPIO"],
    ["j15", 5, 27],
    ["j15", 6, 26],
    ["j15", 7, 21],
    ["j15", 9, 20],
    ["j15", 10, 10],
    ["j15", 11, 18],
    ["j15", 15, 130],
    ["j15", 16, 134],
    ["j15", 17, 131],
    ["j15", 18, 135],
    ["j15", 20, 136],
    ["j15", 23, 129],
    ["j15", 25, 137],
    ["j15", 26, 132],
    ["j16", 7, 116],
    ["j16", 8, 115],
    ["j16", 9, 114],
    ["j16", 10, 113],
    ["j16", 11, 65],
    ["j16", 14, 64],
    ["j16", 15, 68],
    ["j16", 17, 106],
    ["j16", 19, 117],
    ["j16", 20, 118],
    ["j16", 21, 119],
    ["j16", 22, 120],
    ["j16", 23, 121],
    ["j16", 24, 122],
    ["j16", 25, 123],
    ["j16", 26, 124],
    ["j16", 27, 66],
    ["j16", 28, 67],

]


class GPIOController:
    def __init__(self, gpio):
        """Initialize the GPIO pin by exporting it and setting the direction."""
        try:
            self.gpio = gpio
            os.system(f'echo {gpio} > /sys/class/gpio/export')
            os.system(f'echo out > /sys/class/gpio/gpio{gpio}/direction')
        except Exception as e:
            print(f"error in initialising {self.gpio}")

    def set_value(self, value):
        """Set the GPIO value to 1 (ON) or 0 (OFF)."""
        try:
            os.system(f'echo {value} > /sys/class/gpio/gpio{self.gpio}/value')
            print(f"{self.gpio} is {value}")
        except Exception as e:
            print(f"error in setting value for {self.gpio}")
    def cleanup(self):
        """Unexport the GPIO pin."""
        os.system(f'echo {self.gpio} > /sys/class/gpio/unexport')

def auto_test():
    numbers = [
        27, 26, 21, 20, 10, 18, 130, 134, 131, 135, 136, 129, 137,
        132, 116, 115, 114, 113, 65, 64, 68, 106, 117, 118, 119, 120,
        121, 122, 123, 124, 66, 67
    ]

    controllers = [GPIOController(number) for number in numbers]
    print(controllers)
    while True:
        try:
            for controller in controllers:
                controller.set_value(1)
                sleep(1)

            for controller in controllers:
                controller.set_value(0)
                sleep(1)
        except KeyboardInterrupt:
            break
        except Exception:
            print("Error start auto test")
def get_gpio(connector_name, pin_number):
    try:
        for row in CSV_data:
            if row[0] == connector_name and row[1] == int(pin_number):
                return row[2]
    except Exception as e:
        print("could get gpio")

def manual_test():
    print("Connector name is the connector you are trying to access (j15 or j16)\nPin number is corresponding pin number you are trying to control (eg. 11)\nValue is the intended behaviour (eg. ON or OFF)")
    while True:
        try:
            connector = input("Enter connector name:")
            pin_number = input("Enter Pin number:")
            value = input("Enter value:")
            gpio = get_gpio(connector.lower(),pin_number)
            if value.upper() == "ON":
                GPIOController(gpio).set_value(1)
            elif value.upper() == "OFF":
                GPIOController(gpio).set_value(0)
            else:
                print("invalid entry\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error{e}")


def main():
    print("\n\nPress A for doing Auto test\nPress M for doing Manual test\n ")
    try:
        while True:
            test_mode = input("Enter Your Choice:")
            if test_mode.upper() == "A":
                auto_test()

            elif test_mode.upper() == "M":
                manual_test()
        
            else:
                print("Invalid entry! try again\n")
    except Exception as e:
        print(f"Error in Excecution:{e}")


if __name__ == "__main__":
    main()





