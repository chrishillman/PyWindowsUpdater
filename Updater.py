import subprocess, sys
from _winreg import *

lines=[]
try:
	with open("Updater.ini", "r") as f:
		for line in f:
			lines.append(line)
except:
	print("Updater.ini not found!")
	print("Create the file with the following format:")
	print("Program Name, Program Version, Installation command")
	sys.exit()

aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
subkeys = QueryInfoKey(aKey)[0]
programs=[]
for i in range(subkeys):
    keyname = EnumKey(aKey, i)
    asubkey = OpenKey(aKey, keyname)
    try:
        val = QueryValueEx(asubkey, "DisplayName")
        if len(set(val[0].upper().split(" ")) & set(["MICROSOFT", "AUTO", "HELPER", "GUEST", "MAINTENANCE", "TOOLBAR"])) == 0:
        	programName=val[0]
	        try:
		        val = QueryValueEx(asubkey, "DisplayVersion")
		        programVersionName=val[0]
		        programs.append(str(programName).translate(None, "()") + " " + str(programVersionName))
	        except:
		    	programs.append(str(programName).translate(None, "()"))
	    		pass
    except:
    	pass
for line in lines:
	UpdateVersion = line.split(",")[1]
	UpdateName = line.split(",")[0]
	UpdateCommand = line.split(",")[2]
	for program in programs:
		if UpdateName.upper() in program.upper():
			print(" Program: " + program)
			if program.split(" ")[-1].split(".")[-1].isdigit():
				ProgramVersion = program.split(" ")[-1]
				UpdateProgramFlag = False
				for i in range(len(ProgramVersion.split("."))):
					if int(ProgramVersion.split(".")[i]) < int(UpdateVersion.split(".")[i]):
						UpdateProgramFlag = True
				if UpdateProgramFlag:
					try:
						UpdateResults = subprocess.Popen(UpdateCommand, stdout=subprocess.PIPE, shell=True)
						print(UpdateResults)
					except:
						print("Command Failed: " + str(sys.exc_info()[0]))
						raise OSError(" fail ")
