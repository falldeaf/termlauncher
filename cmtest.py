import os

#py plugin-apps.py --search fir
command = "py plugin_apps.py --search fir"
output = os.popen(command).read()
print(output)