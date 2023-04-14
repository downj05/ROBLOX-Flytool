from roblox.player import Player
import command
import logging
from colorama import init, Fore, Style

def parseAxis(val,argument):
	if '~' in argument:
		if len(argument) == 1: # Only supplied ~
			return val
		# Otherwise add argument to current val
		return val + float(argument.replace('~', ''))
	else:
		return float(argument)

def printVector3(v, r=3):
	print(round(v.x, r), round(v.y, r), round(v.z, r))
	return


# Initialize colorama
init()

# Define command functions
def cmd_tp(x,y,z):
	p = Player().HumanoidRootPart
	p.position.x = parseAxis(p.position.x, x) # X value
	p.position.y = parseAxis(p.position.y, y) # Y value
	p.position.z = parseAxis(p.position.z, z) # Z value
	return

def cmd_pos():
	p = Player().HumanoidRootPart
	printVector3(p.position)
	return

def cmd_info(address):
	address = int(address, 16)
	print(f"Attempting Player() object from {hex(address)}")
	temp_p = Player(rootPartBaseAddress=address).HumanoidRootPart
	printVector3(temp_p.position)
	return

# Create command system and add commands
cmd_system = command.CommandSystem()
cmd_system.add_command('tp', cmd_tp, help_msg="Teleport to the provided coordinates, use ~x ~y ~z for relative coordinates", num_args=3)
cmd_system.add_command('pos', cmd_pos, help_msg="Get your current position",)
cmd_system.add_command('info', cmd_info, help_msg="Get info about a provided base address (experimental)", num_args=1)
cmd_system.add_command('help', cmd_system.help)

# Define colors for input and output
INPUT_COLOR = Fore.GREEN
OUTPUT_COLOR = Fore.BLUE

# Run the command prompt
while True:
    # Get user input
    input_str = input(INPUT_COLOR + '> ' + Style.RESET_ALL)

    # Execute the command
    try:
        cmd_system.execute_command(input_str)
    except Exception as e:
        print(OUTPUT_COLOR + str(e) + Style.RESET_ALL)