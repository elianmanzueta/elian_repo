# Cisco Switch Configuration Tool
Elian Manzueta
June 5, 2022

I created a Cisco switch configuration tool in Python using the modules Tkiner and Netmiko. This script supports both L2 and L3 switch configuration, allowing the user to specify their desired VLANs, port modes, and IP addresses. This script works with Layer 3 Cisco switches running Cisco IOS. For my testing environment, I used edge-sw01 in the Cisco Modeling Labs sandbox.

## GUI

![](images/Layer%202%20Blank.png)

## Configuring a Layer 2 Access or Trunk Port

![](images/Access%20Port.png)
![](images/Trunk%20Port.png)

## Configuring a Layer 3 Port

![](images/Layer%203%20Port.png)

After configuration, the script will output the Cisco IOS CLI commands and a show run for verification.
### Sources

https://realpython.com/python-gui-tkinter/

https://pyneng.readthedocs.io/en/latest/
