'''
    File name: Network Configuration GUI.py
    Author: Elian Manzueta
    Date created: 06/05/2022
    Date last modified: 06/11/2022
    Python Version: 3.10.2
'''

import tkinter as tk
from netmiko import ConnectHandler
import sys
import re

# Device settings
cisco = {
    'device_type':'cisco_ios',
    'host':'10.10.20.172',
    'username':'elian',
    'password':'cisco',
    'secret':'cisco'
}

port_modes = [
    'trunk',
    'access'
]

# Connect to device
net_connect = ConnectHandler(**cisco)

# Populates options menu depending on available interfaces. Uses a regular expression to detect FastEthernet and GigabitEthernet interfaces
show_interfaces = net_connect.send_command("show ip int br")
options = list(re.findall('Fast|Gigabit\w+/\w', show_interfaces)) # Grab interfaces

# Get the interface
def getInterface(*args):
    return interface_selection.get() 

# Get the port mode
def getPortMode(*args):
    return port_selection.get() 

# Get the IP
def getIP(*args):
    print(f"Selected IP: {ent_ip.get()}")
    return ent_ip.get()

# Get the subnet
def getSubnet(*args):
    print(f"Selected subnet: {ent_subnet.get()}")
    return ent_subnet.get() 

# Grabs the VLAN
def getVLAN(*args):
    print(f"Selected VLAN {ent_vlan.get()}")
    return ent_vlan.get() 

# Switches between L2 or L3 switch configuration
def switchConfig(*args): 
    # 0 = L2, 1 = # L3
    if (radio_var.get()) == 0:
        frm_l3_entries.grid_forget()
        port_menu.grid(row=0, column=1)
        frm_l2_entries.grid(row=1, column=0)
    else:
        frm_l2_entries.grid_forget() 
        port_menu.grid_forget() 
        frm_l3_entries.grid(row=1, column=0) 


def assignValues(*args):
    # Checks if L2 or L3 switch configuration is selected.
    if radio_var.get() == 0:
        net_connect.enable() # Enable mode
        if (getPortMode() == 'access'):
            output = net_connect.send_config_set([f'interface {getInterface()}',
                                                  f'switchport', 
                                                  f'switchport mode {getPortMode()} ', 
                                                  f'switchport access vlan {getVLAN()} ', 
                                                  'exit'])
            print(output) 
        elif (getPortMode() == 'trunk'):
            output = net_connect.send_config_set([f'interface {getInterface()} ', 
                                                  f'switchport',
                                                  f'switchport trunk encapsulation dot1q', 
                                                  f'switchport mode {getPortMode()} ', 
                                                  f'switchport trunk allowed vlan none', 
                                                  f'switchport trunk allowed vlan add {getVLAN()} ', 
                                                  'exit'])
            print(output)
    else:
        net_connect.enable() 
        output = net_connect.send_config_set([f'interface {getInterface()}', 
                                              f'no switchport', 
                                              f'ip address {getIP()} {getSubnet()}'])
        print(output) 
    print(("\nComplete").center(20, '='))
    output = net_connect.send_command(f'show run | sec interface {getInterface()}') # Show changes
    print(output)

# Tkinter root
window = tk.Tk()
window.title("Switch Configuration Tool")
window.resizable(False, False)


# Interface Selection Frame
frm_int = tk.Frame(master=window)
frm_int.grid(column=0, row=0) 

# Interface Menu
interface_selection = tk.StringVar(window)
interface_selection.set("Interface") 
interface_menu = tk.OptionMenu(frm_int, interface_selection, *options, command=getInterface) # Interface options menu
interface_menu.grid(row=0, column=0) 

# Trunk Menu
port_selection = tk.StringVar(window)
port_selection.set("Port mode")
port_menu = tk.OptionMenu(frm_int, port_selection, *port_modes, command=getPortMode) # Port mode
port_menu.grid(row=0, column=1)

# L3 Frame
frm_l3_entries = tk.Frame(master=window)

# IP and Subnet Labels and Entries
lbl_ip = tk.Label(master=frm_l3_entries, text="IP Address:") # IP
ent_ip = tk.Entry(master=frm_l3_entries, width=25)
ent_ip.bind("<Return>", getIP) # Grab IP value on enter
lbl_subnet = tk.Label(master=frm_l3_entries, text="Subnet Mask:") # Subnet
ent_subnet = tk.Entry(master=frm_l3_entries, width=25)
ent_subnet.bind('<Return>', getSubnet) # Grab subnet value on enter

#IP and Subnet Grid
lbl_ip.grid(row=1, column=0, sticky='w') # IP Label
ent_ip.grid(row=1, column=1) # IP Entry
lbl_subnet.grid(row=2, column=0) # Subnet Label
ent_subnet.grid(row=2, column=1) # Subnet Entry

# L2 Frame 
frm_l2_entries = tk.Frame(master=window)
frm_l2_entries.grid(row=1, column=0) 
# VLAN Labels and Entries, column=0
lbl_vlan = tk.Label(master=frm_l2_entries, text="VLANs:") 
ent_vlan = tk.Entry(master=frm_l2_entries, width=25) # Grab VLAN
ent_vlan.bind('<Return>', getVLAN) # Grab VLAN value on enter

# VLAN Grid
lbl_vlan.grid(row=1, column=0, sticky='w') # VLAN Label
ent_vlan.grid(row=1, column=1) # VLAN Entry

# Buttons
frm_button = tk.Frame(master=window)
frm_button.grid(row=5, column=0)

btn_compile = tk.Button(master=frm_button, text="Assign", command=assignValues) # Assignment button

# Radio Buttons
radio_var = tk.IntVar(window) 
radio_var.set(0) # The program defaults to Layer 2 configuration
radio_l2 = tk.Radiobutton(master=frm_button, text="Layer 2", variable=radio_var, value=0, command=switchConfig)
radio_l3 = tk.Radiobutton(master=frm_button, text="Layer 3", variable=radio_var, value=1, command=switchConfig)  

# Button Grid 
btn_compile.grid(row=5, column=0, sticky='ew', columnspan=2)
radio_l2.grid(row=6, column=0)
radio_l3.grid(row=6, column=1) 

# Text Box
txt_progress = tk.Text()
txt_progress.grid() 

# Outputs terminal output to the text box
def redirector(inputStr):
    txt_progress.insert(tk.INSERT, inputStr)

sys.stdout.write = redirector 

# Run
window.mainloop() 