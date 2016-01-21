=== Definitions ===
Device 			-	A target entity that Dispatch interacts with. This is usally this is usually a computer
					or appliance with an IP Address.
		
Device Profile 	-	A set of state parameters that can be set or get on a device. Device Profiles typically
					follow the Recommended Profile Heirarchy.


=== Recommended Profile Heirarchy ===
-> Profile (always the highest level parent)
	-> Type of Device (e.g. Server, Router, Firewall, Embedded, Cloud Service)
		-> Manufacturer -> (e.g. Apple, Microsoft, Cisco, Huawei)
			-> 


=== Requirements ===
# Retrieve current state values from a device.
# Set state values on a device.
# Define supported state values per device profile
# Alter the inheritance of profiles during runtime





=== Example Usage ===

Dispatch can be used from the command-line or from within Python.


Command-line Example:
```shell
$ dispatch server01 get cpu.load_averages
0.03 0.12 0.11
$ 
$ dispatch server01 get interfaces:name=eth0.ip_address
192.168.16.122
$ 
$ dispatch server01 get interfaces:ip_address="192.168.16.122".name
eth0
```


=== Guidelines ===
* One device profile per file.
*






includes = [""