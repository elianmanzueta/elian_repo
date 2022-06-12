'''
    File name: Network Configuration GUI.py
    Author: Elian Manzueta
    Date created: 06/05/2022
    Date last modified: 06/11/2022
    Python Version: 3.10.2
'''

import tkinter as tk
import sys
import re
from netmiko import ConnectHandler

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

# Populates options menu depending on available interfaces.
# Uses a regular expression to detect FastEthernet and GigabitEthernet interfaces
show_interfaces = net_connect.send_command("show ip int br")
options = list(re.findall('Fast|Gigabit\w+/\w', show_interfaces)) # Grab interfaces

def get_interface(*args):
    """Get the interface"""
    return interface_selection.get()

def get_port_mode(*args):
    """Get the port mode"""
    return port_selection.get()

def get_ip(*args):
    """#Get the IP"""
    print(f"Selected IP: {ent_ip.get()}")
    return ent_ip.get()

def get_subnet(*args):
    """Get the subnet"""
    print(f"Selected subnet: {ent_subnet.get()}")
    return ent_subnet.get()

def get_vlan(*args):
    """Grabs the VLAN"""
    print(f"Selected VLAN {ent_vlan.get()}")
    return ent_vlan.get()

def switch_config(*args):
    """Switches between L2 or L3 switch configuration"""
    if (radio_var.get()) == 0:
        frm_l3_entries.grid_forget()
        port_menu.grid(row=0, column=1)
        frm_l2_entries.grid(row=1, column=0)
    else:
        frm_l2_entries.grid_forget()
        port_menu.grid_forget()
        frm_l3_entries.grid(row=1, column=0)

def assign_values(*args):
    """Checks if L2 or L3 switch configuration is selected."""
    if radio_var.get() == 0:
        net_connect.enable()
        if get_port_mode() == 'access':
            output = net_connect.send_config_set([f'interface {get_interface()}',
                                                  'switchport',
                                                  f'switchport mode {get_port_mode()}',
                                                  f'switchport access vlan {get_vlan()}',
                                                  'exit'])
            print(output)
        elif get_port_mode() == 'trunk':
            output = net_connect.send_config_set([f'interface {get_interface()}',
                                                  'switchport',
                                                  'switchport trunk encapsulation dot1q',
                                                  f'switchport mode {get_port_mode()}',
                                                  'switchport trunk allowed vlan none',
                                                  f'switchport trunk allowed vlan add {get_vlan()}',
                                                  'exit'])
            print(output)
    else:
        net_connect.enable()
        output = net_connect.send_config_set([f'interface {get_interface()}',
                                              'no switchport',
                                              f'ip address {get_ip()} {get_subnet()}'])
        print(output)
    print(("Complete").center(20, '='))
    output = net_connect.send_command(f'show run | sec interface {get_interface()}') # Show changes
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
interface_menu = tk.OptionMenu(frm_int, interface_selection, *options, command=get_interface) # Interface options menu
interface_menu.grid(row=0, column=0)

# Trunk Menu
port_selection = tk.StringVar(window)
port_selection.set("Port mode")
port_menu = tk.OptionMenu(frm_int, port_selection, *port_modes, command=get_port_mode) # Port mode
port_menu.grid(row=0, column=1)

# L3 Frame
frm_l3_entries = tk.Frame(master=window)

# IP and Subnet Labels and Entries
lbl_ip = tk.Label(master=frm_l3_entries, text="IP Address:") # IP
ent_ip = tk.Entry(master=frm_l3_entries, width=25)
ent_ip.bind("<Return>", get_ip) # Grab IP value on enter
lbl_subnet = tk.Label(master=frm_l3_entries, text="Subnet Mask:") # Subnet
ent_subnet = tk.Entry(master=frm_l3_entries, width=25)
ent_subnet.bind('<Return>', get_subnet) # Grab subnet value on enter

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
ent_vlan.bind('<Return>', get_vlan) # Grab VLAN value on enter

# VLAN Grid
lbl_vlan.grid(row=1, column=0, sticky='w') # VLAN Label
ent_vlan.grid(row=1, column=1) # VLAN Entry

# Buttons
frm_button = tk.Frame(master=window)
frm_button.grid(row=5, column=0)

btn_compile = tk.Button(master=frm_button, text="Assign", command=assign_values) # Assignment button

# Radio Buttons
radio_var = tk.IntVar(window)
radio_var.set(0) # The program defaults to Layer 2 configuration
radio_l2 = tk.Radiobutton(master=frm_button, text="Layer 2", variable=radio_var, value=0, command=switch_config)
radio_l3 = tk.Radiobutton(master=frm_button, text="Layer 3", variable=radio_var, value=1, command=switch_config)

# Button Grid
btn_compile.grid(row=5, column=0, sticky='ew', columnspan=2)
radio_l2.grid(row=6, column=0)
radio_l3.grid(row=6, column=1)

# Text Box
txt_progress = tk.Text()
txt_progress.grid()


def redirector(input_str):
    """Outputs terminal output to the text box"""
    txt_progress.insert(tk.INSERT, input_str)

sys.stdout.write = redirector

# Run
window.mainloop()
