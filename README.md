# How to run

1. Clone repository
2. Install python 3 from [python.org](https://www.python.org/)
3. Install requirements packages

 ```
 pip install -r requirements.txt
 ```

3. Create route with [Fleet Carrier Router](https://spansh.co.uk/fleet-carrier). Do not use "Determine Tritium
   Requirements" option. Specify the correct "Used Capacity", "Tritium in tank" and "Tritium in market" manually
4. Download the csv file and put it in the folder with the script
5. Run using shell

 ```
 python fc_autopilot.py
 ```

6. Enter the tritium position from the bottom of the fleet carrier's inventory list
7. Go to sleep

Tritium is refueled a little less than actually required, to level out the error in calculating the required tritium by
the route planner.

Use a ship with a 150+ tons of cargo, but leave it empty. The first tab must be selected on the internal panel (opens by
pressing the "4" button)

Only works with FullHD(1920x1080) resolution. For correct operation, the interface language must be Russian or English,
and also have a max brightness, standart UI navigation keybindings. Performance with custom HUD has not been tested

The script is a simple macro, but I'm not sure if FDEV welcomes this. So use at your own risk.
