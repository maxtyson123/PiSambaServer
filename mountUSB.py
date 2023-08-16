import os

command_output = ""

print("Detecting Usbs & their mount points")
usbs = []
mounts = []


#GET THE USBS:
command_output = os.popen('lsblk -d -o NAME,TRAN,MOUNTPOINT | grep usb').read().split("\n")
for line in command_output:
	
	# Split the commnads
	line_data = line.split(" ")

	# Remove all the elemts that are empty
	line_data = [value for value in line_data if value != ""]

	if(len(line_data) < 1):
		continue

	usbs.append(line_data[0])	

#GET THE MOUNT POINTS:
command_output = os.popen('lsblk -rno name,mountpoint').read().split("\n")
for line_index in range(len(command_output)):
	
	# Split the commnads
	line_data = command_output[line_index].split(" ")

	if(len(line_data) < 2):
		continue

	for usb in usbs:
		if(usb in line_data[0] and line_data[1] != ""):
			mounts.append([line_data[0], line_data[1]])
for mountedUSB in mounts:
	print(f"Usb: {mountedUSB[0]}. Mounted at: {mountedUSB[1]}")



print("Unmounting all usbs")
def unMountUSBS(mountedUSBs):
	for mountedUSB in mountedUSBs:
		if "/External/" not in mountedUSB[1]:
			print(f"Usb: {mountedUSB[0]} is not mounted onto server, Skipping")
			continue

		os.system(f"sudo umount {mountedUSB[1]}")
		print(f"Unmounted: {mountedUSB[0]}")
unMountUSBS(mounts)

print("Removing previous drive mount points")
def cleanFolders():
	os.system("sudo rm -rf /External/*/")
	cleanFolders()

print("Mounting USB(s) to server")
for usb_index in range(len(mounts)):
	os.system(f"sudo mkdir /External/0{usb_index}")
	os.system(f"sudo mount /dev/{mounts[usb_index][0]} /External/0{usb_index}")
	print(f"Mounted /dev/{mounts[usb_index][0]} to /External/0{usb_index}")

input("Press a button to unmount the USBs once finished")
unMountUSBS(mounts)
cleanFolders()
