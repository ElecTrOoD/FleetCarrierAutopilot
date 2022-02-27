import csv
import glob
import os
import sys
from time import sleep

from pyautogui import write, locateOnScreen
from pydirectinput import press, moveTo


class FCAutopilot:
    route = None
    tritium_position = None
    count = 0
    total_fuel = 0

    def __init__(self, tritium_position):
        self.tritium_position = tritium_position

    def load_route(self):
        """
        method loads the route from the csv file and serializes the required data
        """
        data = []
        try:
            files = glob.glob('*.csv')
            latest_file = max(files, key=os.path.getctime)

            with open(latest_file) as file:
                dics = csv.DictReader(file)

                for item in dics:
                    data.append({'system': item['System Name'], 'fuel': int(item['Fuel Used'])})

            self.route = data[1:]
        except Exception:
            print(f'Error, check route file')
            sleep(5)
            sys.exit(1)

    def open_inventory_transfer_menu(self):
        """
        macro method that opens inventory transfer menu
        """
        self.press_button('4', interval=2)
        self.press_button('e', presses=4)
        self.press_button('d')
        self.press_button('w')
        self.press_button('d')
        self.press_button('space')

    def select_tritium_n_refuel(self, fuel_used):
        """
        macro method taking tritium into the ship's cargo.
        """
        self.press_button('w', presses=self.tritium_position)
        self.press_button('a', presses=fuel_used - 2, interval=0)
        self.press_button('s', presses=self.tritium_position)

    def close_inventory_transfer_menu(self):
        """
        macro method that closes inventory transfer menu
        """
        self.press_button('d')
        self.press_button('space')
        self.press_button('backspace')
        self.press_button('q', presses=4)
        self.press_button('backspace')

    def open_carrier_services_menu(self):
        """
        macro method that opens carrier services menu
        """
        self.press_button('w', presses=3)
        self.press_button('s')
        self.press_button('space', interval=3)
        self.press_button('w', presses=3)
        self.press_button('a', presses=3)

    def refill_tritium_depot(self):
        """
        macro method that refills the tritium depot.
        """
        self.press_button('s', presses=2)
        self.press_button('space', presses=2, interval=1)
        self.press_button('w')
        self.press_button('space')
        self.press_button('backspace')
        self.press_button('s')
        self.press_button('space')
        self.press_button('backspace')

    def open_carrier_managment_menu(self):
        """
        macro method that opens carrier managment menu
        """
        self.press_button('s', presses=2)
        self.press_button('d', presses=2)
        self.press_button('space', interval=4)

    def open_galmap(self):
        """
        macro method that opens galactic map
        """
        self.press_button('s')
        self.press_button('space')
        self.press_button('space', interval=8)

    def initiate_jump(self, system_name):
        """
        macro method that initiates the jump
        """
        moveTo(900, 130)
        self.press_button('space', interval=1)
        write(system_name, interval=0.025)
        sleep(2)
        self.press_button('enter', interval=3)
        moveTo(1550, 400)
        self.press_button('space', interval=3)

    @staticmethod
    def confirm_jump_initiation():
        """
        method that looks for a green jump confirmation sign on the screen
        """
        locate = locateOnScreen('images\\jump_initiation.png', confidence=0.9)
        return locate

    @staticmethod
    def wait_jump_completion():
        """
        method that looks for the gray carrier services menu button on the screen, indicating the completion of the jump
        """
        while not locateOnScreen('images\\jump_completion_en.png', confidence=0.9) and not locateOnScreen(
                'images\\jump_completion_ru.png', confidence=0.9):
            pass
        sleep(60 * 3)

    @staticmethod
    def press_button(button, presses=1, interval=0.3):
        """
        Wrapper over the press() function that changes the standard interval
        """
        press(button, presses, interval)

    def refuel(self, fuel_used):
        """
        method that gathers together submethods for refueling
        """
        self.open_inventory_transfer_menu()
        self.select_tritium_n_refuel(fuel_used)
        self.close_inventory_transfer_menu()
        self.open_carrier_services_menu()
        self.refill_tritium_depot()

    def make_jump(self, system_name):
        """
        method that gathers together submethods for jump
        """
        self.open_carrier_services_menu()
        self.open_carrier_managment_menu()

        while True:
            self.open_galmap()
            self.initiate_jump(system_name)
            if self.confirm_jump_initiation():
                break
            sleep(30)

        sleep(3)
        self.press_button('backspace', presses=2)

    def run(self):
        """
        method starts all autopilot processes
        """
        self.load_route()
        for waypoint in self.route:
            self.count += 1
            self.total_fuel += waypoint['fuel']
            print(f'[INFO] Jump #{self.count} to {waypoint["system"]} | '
                  f'Fuel needed: {waypoint["fuel"]} | '
                  f'Total fuel: {self.total_fuel}')
            self.make_jump(waypoint['system'])
            self.wait_jump_completion()
            self.refuel(waypoint['fuel'])


if __name__ == '__main__':
    tritium_pos = int(input('Write tritium position from bottom of list: '))
    for i in range(10, 0, -1):
        print(f'\rStarting in {i}s', end='')
        sleep(1)
    print('\n\n')
    ap = FCAutopilot(tritium_pos)
    ap.run()
