'''
    File name: Network Configuration GUI.py
    Author: Elian Manzueta
    Date created: 06/05/2022
    Date last modified: 06/08/2022
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
    selection = interface_selection.get() 
    print(f"Selected interface {selection}")
    return selection 

# Get the port mode
def getPortMode(*args):
    selection = port_selection.get() 
    print(f"Selected port {selection}")
    return selection

# Get interface description 
def getDescription(*args):
    print(f"Description: \n {ent_desc.get()}")
    return ent_desc.get() 

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
    vlan = (ent_vlan.get())
    print(f"Selected VLAN {vlan}")
    return vlan

# Executes VLAN Assignment command 
def assignValues(*args):
    # For L2 interfaces. I'll add a separate L3 interface option at a later time
    net_connect.enable() # Enable mode
    if getPortMode == 'access':
        output = net_connect.send_config_set([f'interface {getInterface()} ', 
                                              f'switchport mode {getPortMode()} ', 
                                              f'switchport access vlan {getVLAN()} ', 
                                              'exit'])
    else:
               output = net_connect.send_config_set([f'interface {getInterface()} ', 
                                                     f'switchport trunk encapsulation dot1q', 
                                                     f'switchport mode {getPortMode()} ', 
                                                     f'switchport trunk allowed vlan add {getVLAN()} ', 
                                                     'exit'])
    print(output)
    print(("Complete").center(20, '='))
    output = net_connect.send_command(f'show run | sec interface {interface_selection.get()}') # Show changes
    print(output)
        
# Tkinter root
window = tk.Tk()
window.title("Network Configuration")

# Interface Selection Frame
frm_int = tk.Frame()
frm_int.grid(column=0, row=0) 

# Interface Menu
interface_selection = tk.StringVar(window) 
interface_selection.set("Interface") 
interface_menu = tk.OptionMenu(frm_int, interface_selection, *options, command=getInterface) # Interface options menu
interface_menu.grid(row=0, column=0) 

# Trunk Menu
port_selection = tk.StringVar(window)
port_selection.set("Port Mode")
port_menu = tk.OptionMenu(frm_int, port_selection, *port_modes, command=getPortMode) # Port mode
port_menu.grid(row=0, column=1)

# VLAN and IP Address Entry Frame
frm_entries = tk.Frame(borderwidth=10)
frm_entries.grid(row=1, column=0)

# IP and Subnet Labels and Entries
lbl_ip = tk.Label(master=frm_entries, text="IP Address:") # IP
ent_ip = tk.Entry(master=frm_entries, width=25)
ent_ip.bind("<Return>", getIP) # Grab IP value on enter
lbl_subnet = tk.Label(master=frm_entries, text="Subnet Mask:") # Subnet
ent_subnet = tk.Entry(master=frm_entries, width=25)
ent_subnet.bind('<Return>', getSubnet) # Grab subnet value on enter

# VLAN Labels and Entries
lbl_vlan = tk.Label(master=frm_entries, text="VLANs:") 
ent_vlan = tk.Entry(master=frm_entries, width=25) # Grab VLAN
ent_vlan.bind('<Return>', getVLAN) # Grab VLAN value on enter

# Interface Description
lbl_desc = tk.Label(master=frm_entries, text="Description:")
ent_desc = tk.Entry(master=frm_entries, width=25)

# IP and Subnet Grid
lbl_ip.grid(row=1, column=0, sticky='w') # IP Label
ent_ip.grid(row=1, column=1) # IP Entry
lbl_subnet.grid(row=2, column=0) # Subnet Label
ent_subnet.grid(row=2, column=1) # Subnet Entry

# VLAN Grid
lbl_vlan.grid(row=3, column=0, sticky='w') # VLAN Label
ent_vlan.grid(row=3, column=1) # VLAN Entry

# Interface Description Grid
lbl_desc.grid(row=4, column=0, sticky='w')
ent_desc.grid(row=4, column=1)

# Buttons
frm_button = tk.Frame(master=window)
frm_button.grid()
btn_compile = tk.Button(master=frm_button, text="Assign", command=assignValues) 

# Button Grid 
btn_compile.grid(row=5, column=0)

# Text Box
txt_progress = tk.Text()
txt_progress.grid() 

# Outputs terminal output to the text box
def redirector(inputStr):
    txt_progress.insert(tk.INSERT, inputStr)

print(("Welcome!").center(80, '='))
sys.stdout.write = redirector 

# Run
window.mainloop() 


