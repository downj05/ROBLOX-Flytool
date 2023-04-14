import tkinter as tk
from gui import GUI
import threading, keyboard, math, command, keybinds
from roblox.player import Player
from time import sleep as wait

backend_tps = 120

# Create an instance of the GUI
root = tk.Tk()
gui = GUI(root)

def moveDirection(yaw, rotation_offset,flight_speed,positive=True):
    if positive == True:
        x = -1
    else:
        x = 1        # Create a frame for X, Y, and Z coordinates
        coord_frame = ttk.LabelFrame(frame, text="Coordinates", borderwidth=2, relief="solid", padding=0)
        coord_frame.grid(row=0, column=0, padx=(5,0), pady=5, sticky='w')
    deltaXvel = float(x*(flight_speed*math.sin((yaw + rotation_offset) * math.pi /180)))
    deltaZvel = float(x*(flight_speed*math.cos((yaw + rotation_offset)* math.pi /180)))
    return deltaXvel, deltaZvel


def backend():
    # Create player object
    p = Player()

    gravity_old = p.HumanoidRootPart.gravity.value
    while True:
        # Update the X, Y, and Z coordinates
        pos = p.HumanoidRootPart.position
        gui.updateXYZ(pos.x, pos.y, pos.z)


        # Toggle checkbox if key pressed
        if keyboard.is_pressed(keybinds.toggle_key):
            gui.toggle_value.set(not gui.toggle_value.get())
            wait(0.2) # Debounce

        # Recalculate base address if key pressed
        if keyboard.is_pressed(keybinds.toggle_key): 
            wait(0.2)  # Debounce
            # Recreate player object
            p = Player()

        # Calculate flight speed based on slider value
        flight_speed = gui.speed_value.get() * 8

        if gui.toggle_value.get():
            yaw, pitch, roll = p.HumanoidRootPart.cframe.angles
            # Vertical movement
            if keyboard.is_pressed(keybinds.up_key):
                p.HumanoidRootPart.position.y += flight_speed        
            elif keyboard.is_pressed(keybinds.down_key):
                p.HumanoidRootPart.position.y += -flight_speed/2
            if keyboard.is_pressed(keybinds.forward_key): # If going forwards
                x,z = moveDirection(yaw, 0, flight_speed)
                p.HumanoidRootPart.position.x += x
                p.HumanoidRootPart.position.z += z
            elif keyboard.is_pressed(keybinds.back_key):
                x,z = moveDirection(yaw, 0, flight_speed)
                p.HumanoidRootPart.position.x -= x
                p.HumanoidRootPart.position.z -= z
            if keyboard.is_pressed(keybinds.left_key):
                x,z = moveDirection(yaw, 90, flight_speed)
                p.HumanoidRootPart.position.x += x
                p.HumanoidRootPart.position.z += z
            elif keyboard.is_pressed(keybinds.right_key):
                x,z = moveDirection(yaw, -90, flight_speed)
                p.HumanoidRootPart.position.x += x
                p.HumanoidRootPart.position.z += z
            # Cancel all velocity
            p.HumanoidRootPart.velocity.x = 0.001
            p.HumanoidRootPart.velocity.y = 0.001
            p.HumanoidRootPart.velocity.z = 0.001  

            # Set gravity to zero if not already set
            if p.HumanoidRootPart.gravity.value != 0.0:
                p.HumanoidRootPart.gravity.value = 0.0
        else:
            # set gravity to normal if not set
            if p.HumanoidRootPart.gravity.value != gravity_old:
                p.HumanoidRootPart.gravity.value = gravity_old
        wait(1/backend_tps)

if __name__ == '__main__':
    backend_thread = threading.Thread(target=backend)
    backend_thread.start()
    root.mainloop()

print("hi")