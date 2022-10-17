import os
import subprocess
from sys import argv
import json

slashes = "////////////////////////////////////////////////" \
          "///////////////////////////////////////////////////////////////\n"

map_for_json = {"Menu item": "", "Commands": "", "Output": []}
commands = ["sudo -S ufw status verbose", "do-release-upgrade -c", "lscpu", "free", "df -h /dev/sda5"]
packages = []
for param in argv:
    if param == argv[0]:
        continue
    package_command = "apt-cache policy " + param
    packages.append(package_command)
print(packages[0])


def print_info(c, jf):
    if jf:
        map_for_json["Menu item"] = input_key
        map_for_json["Commands"] = commands[c]
        proc = subprocess.Popen([commands[c]], stdout=subprocess.PIPE, shell=True)
        (out, err) = proc.communicate()
        out_str = out.decode("utf-8")
        map_for_json["Output"] = out_str.split('\n')
        map_for_json["Output"] = map_for_json["Output"][0:len(map_for_json["Output"]) - 1]
        for item in map_for_json["Output"]:
            if item == "":
                map_for_json["Output"].remove("")
        json_string = json.dumps(map_for_json, indent=4)
        print(json_string)
    else:
        print(slashes)
        os.system(commands[c])
        print("\n" + slashes)


def check_packages(jf):
    if jf:
        map_for_json["Menu item"] = input_key
        map_for_json["Commands"] = "apt-cache policy <package>"
        out_str = ""
        for pac in packages:
            proc = subprocess.Popen(pac, stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            out_str += out.decode("utf-8") + slashes
        map_for_json["Output"] = out_str.split('\n')
        map_for_json["Output"] = map_for_json["Output"][0:len(map_for_json["Output"]) - 1]
        json_string = json.dumps(map_for_json, indent=4)
        print(json_string)
    else:
        for par in packages:
            print(slashes)
            os.system(par)
            print("\n" + slashes)


print("\t\tMenu:\n"
      "\t1. Show all OS info.\n"
      "\t2. Show only FW info.\n"
      "\t3. Show only available release upgrade.\n"
      "\t4. Show only processor/cores info.\n"
      "\t5. Show only RAM info.\n"
      "\t6. Show only disk space info.\n"
      "\t7. Show packages status.\n"
      "Input menu item: ")

input_key = input()
print("\t\tPrint in json:\n"
      "\t1. Yes\n"
      "\t2. No\n"
      "Input 1 or 2: ")
json_format = input()
if json_format == "1":
    json_format = True
else:
    json_format = False

if input_key == "1":
    for i in range(5):
        print_info(i, json_format)
elif input_key == "2":
    print_info(0, json_format)
elif input_key == "3":
    print_info(1, json_format)
elif input_key == "4":
    print_info(2, json_format)
elif input_key == "5":
    print_info(3, json_format)
elif input_key == "6":
    print_info(4, json_format)
elif input_key == "7":
    check_packages(json_format)
else:
    print("There is no such menu item...")
