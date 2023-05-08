import os
import re
import sys

class NotSudo(Exception):
    pass

if os.getuid() != 0:
    # If not root, try to elevate privileges
    print("Not root, trying to elevate privileges")
    os.execvp("sudo", ["sudo", "python3"] + sys.argv)
    raise NotSudo("Not root and couldn't elevate privileges")

PATH_TO_BOOT_CONFIG = """/boot/efi/loader/entries/Pop_OS-current.conf"""

with open(PATH_TO_BOOT_CONFIG, "r") as f:
    config_original = f.readlines()

# Make a copy of the original config
config = config_original.copy()

# Find the line with the "options" key
for i, line in enumerate(config):
    if re.match(r"options", line):
        # Remove the "quiet" and "splash" options
        config[i] = re.sub(r"quiet splash ", "", line)
        # Change the systemd.show_status=False to True
        config[i] = re.sub(r"systemd.show_status=False", "systemd.show_status=True", config[i])

# Write to new file in this directory
with open("new_boot_config.conf", "w") as f:
    f.writelines(config)

# Print the diff
print(
    f"Original config:\n{'_'*30}\n{''.join(config_original)}{'_'*30}\n\nNew config:\n{'_'*30}\n{''.join(config)}{'_'*30}")

# Check if the new config is the same as the original
if config == config_original:
    print("Config already loud. They are the same. Exiting")
    exit()

# Ask the user if they want to replace the original config
if input("Do you want to replace the original config? (y/n): ").lower() == "y":
    with open(PATH_TO_BOOT_CONFIG, "w") as f:
        f.writelines(config)
    print("Config replaced")
else:
    print("Config not replaced")
