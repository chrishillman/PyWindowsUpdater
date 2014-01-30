from sys import exit, exc_info
from subprocess import Popen, PIPE
from _winreg import ConnectRegistry, QueryValueEx, QueryInfoKey, EnumKey, OpenKey, HKEY_LOCAL_MACHINE

lines=[]
try:
        with open("Updater.ini", "r") as f:
                for line in f:
                        lines.append(line)
except:
        print("Updater.ini not found!")
        print("Create the file with the following format:")
        print("Program Name, Program Version, Installation command")
        print("A Program Version of 999 will always run the Installation Command")
        exit()

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
        UpdateName = line.split(",")[0]
        UpdateVersion = line.split(",")[1].strip()
        alwaysinstallFlag = False
        if UpdateVersion == "999":
            alwaysinstallFlag = True
        UpdateCommand = line.split(",")[2]
        for program in programs:
            if (UpdateName.upper() in program.upper()) or (alwaysinstallFlag):
                if program.split(" ")[-1].split(".")[-1].isdigit():
                    ProgramVersion = program.split(" ")[-1]
                    UpdateProgramFlag = False
                    if len(ProgramVersion.split(".")) < len(UpdateVersion.split(".")):
                        VersionRange = len(ProgramVersion.split("."))
                    else:
                        VersionRange = len(UpdateVersion.split("."))
                    for i in range(VersionRange):
                        if (int(ProgramVersion.split(".")[i]) < int(UpdateVersion.split(".")[i])) or alwaysinstallFlag:
                                UpdateProgramFlag = True
                    if UpdateProgramFlag:
                        alwaysinstallFlag = False
                        try:
                                print("Preparing to update " + UpdateName + " running command: " + UpdateCommand)
                                UpdateResults = Popen(UpdateCommand, stdout=PIPE, shell=True)
                                stdoutdata, stderrdata = UpdateResults.communicate()
                                print("Command " + UpdateCommand + " gave return code: " + str(UpdateResults.returncode))
                        except:
                                print("Command Failed: " + str(exc_info()[0]))
                                raise
