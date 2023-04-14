from roblox.player import Player
import math
import keyboard
from time import sleep as wait
import curses


tps = 120

flight_speed = 2

toggle_key = 'b'

reset_key = 'r'

forward_key = 'w'
left_key = 'a'
right_key = 'd'
back_key = 's'

up_key = 'space'
down_key = 'shift'

exit_key = ';'

def moveDirection(yaw, rotation_offset,flight_speed,positive=True):
    if positive == True:
        x = -1
    else:
        x = 1
    deltaXvel = float(x*(flight_speed*math.sin((yaw + rotation_offset) * math.pi /180)))
    deltaZvel = float(x*(flight_speed*math.cos((yaw + rotation_offset)* math.pi /180)))
    return deltaXvel, deltaZvel

def main():
    screen = curses.initscr()
    curses.start_color()
    curses.curs_set(0) # Hide blinking cursor

    # Top window colours
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    # Info window colours
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Highlighted color
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)

    # Key color
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)

    res_y, res_x = screen.getmaxyx()
    
    # Message window
    top_window = curses.newwin(6, res_x)
    top_window.bkgd(' ', curses.color_pair(1))
    top_window.addstr(1,1, f"Welcome to W32 Roblox Flyhack V3! Controls ⮧")
    top_window.addstr(2,1, f"Toggle Flight -> {toggle_key.upper()}     Reset Address: {reset_key.upper()} (Press when you die or exit a chair)")
    top_window.addstr(3,1, f"Movement -> {forward_key.upper()} {back_key.upper()} {left_key.upper()} {right_key.upper()} (WASD layout)")
    top_window.addstr(4,1, f"{up_key.upper()} to ascend, {down_key.upper()} to descend, {exit_key.upper()} to exit program.")
    top_window.border(0,0,0,0,0,0,0,0)
    top_window.refresh()

    # Info window
    info_window = curses.newwin(8, res_x//2, 6, 0)
    info_window.bkgd(' ', curses.color_pair(2))
    info_window.border(0,0,0,0,0,0,0,0)
    
    running = False

    # Create player object
    p = Player()
    while True:
        res_y, res_x = screen.getmaxyx()
        # Draw info to screen
        info_window.addstr(1,1, p.HumanoidRootPart.position.pretty_print())
        if running:
            info_window.addstr(1,42, "FLYING", curses.color_pair(3))
            info_window.addstr("    ")
        else:
            info_window.addstr(1,42, "INACTIVE")

        info_window.addstr(5,1, "Keys:")
        info_window.addstr(5,10, "w", curses.color_pair(4))
        info_window.addstr(6,9, "asd", curses.color_pair(4))

        if keyboard.is_pressed(exit_key): # Exit program
            curses.endwin()
            break

        if keyboard.is_pressed(toggle_key): # Toggle key input
            wait(0.2)  # Debounce
            running = not running

            if running is True: # Flight activation
                p.HumanoidRootPart.gravity.value = 0.0

            if running is False: # Flight deactivation
                p.HumanoidRootPart.gravity.value = 196.2

        if keyboard.is_pressed(reset_key): # Recalculate base address
            wait(0.2)  # Debounce
            # Recreate player object
            p = Player()

        if running:
            yaw, pitch, roll = p.HumanoidRootPart.cframe.angles
            # Vertical movement
            if keyboard.is_pressed(up_key):
                p.HumanoidRootPart.position.y += flight_speed        
            elif keyboard.is_pressed(down_key):
                p.HumanoidRootPart.position.y += -flight_speed/2
            if keyboard.is_pressed(forward_key): # If going forwards
                x,z = moveDirection(yaw, 0, flight_speed)
                info_window.addstr(5,10, "w", curses.color_pair(3))
                p.HumanoidRootPart.position.x += x
                p.HumanoidRootPart.position.z += z
            elif keyboard.is_pressed(back_key):
                info_window.addstr(6,10, "s", curses.color_pair(3))
                x,z = moveDirection(yaw, 0, flight_speed)
                p.HumanoidRootPart.position.x -= x
                p.HumanoidRootPart.position.z -= z
            if keyboard.is_pressed(left_key):
                x,z = moveDirection(yaw, 90, flight_speed)
                info_window.addstr(6,9, "a", curses.color_pair(3))
                p.HumanoidRootPart.position.x += x
                p.HumanoidRootPart.position.z += z
            elif keyboard.is_pressed(right_key):
                x,z = moveDirection(yaw, -90, flight_speed)
                info_window.addstr(6,11, "d", curses.color_pair(3))
                p.HumanoidRootPart.position.x += x
                p.HumanoidRootPart.position.z += z
            # Cancel all velocity
            p.HumanoidRootPart.velocity.x = 0.001
            p.HumanoidRootPart.velocity.y = 0.001
            p.HumanoidRootPart.velocity.z = 0.001  
        wait(1/120)
        info_window.refresh()


if __name__ == '__main__':
    main()