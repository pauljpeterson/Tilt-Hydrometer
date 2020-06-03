# This app pipes in data from the Tilt Hydrometer into Avimesa's IoT platform via Avimesa Gadget on a Raspberry Pi.
# Written by Collin Hinson and Paul Peterson of Avimesa Corp.

import subprocess
import re

from time import sleep

sub_str_1 = '"major":' # Temperature
sub_str_2 = '"minor":' # Gravity

# Same as running from a CLI
# IMPORTANT: You'll need to change the creds for your device
gadget_args = [
    'avmsagadget',
    '-i',
    '00000000000000000000000000000000', #Avimesa Device ID
    '11111111111111111111111111111111' #Avimesa Device Auth Code
]

# This is where we wrap Gadget (using the subprocess module)
# After this call, Gadget is running
gadget = subprocess.Popen(args=gadget_args,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)

# Command to run the aioblescan app and get data
# Probably a better way to do this later on
test_args = ['sudo', 'python3', '-u', '-m', 'aioblescan', '-T']

aioblescan = subprocess.Popen(args=test_args,
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

gadget.stdin.flush()

# Now let's read the BLE data from the Tilt and find the major (temperature) and minor (Gravity) values

while True:
    try:
        my_str = aioblescan.stdout.readline().decode()
        my_str = my_str.replace(' ', '')
        idx_1 = my_str.find(sub_str_1)
        idx_2 = my_str.find(sub_str_2)
        read_1 = my_str[idx_1 + len(sub_str_1) : my_str.find(',', idx_1)]
        read_2 = my_str[idx_2 + len(sub_str_2) : my_str.find(',', idx_2)]
        
        # Make sure only alph/num chars are present
        read_2_cleaned = re.sub('[\W_]+', '', read_2)
        
        # Inject the tilt temperature and gravity data into the dialtone data
        temperature_data = '{{"ch_idx":0,"ch_data":[{{"data_idx":0,"units":1,"val":{0}}}]}}\n'.format(read_1)
        gravity_data  = '{{"ch_idx":1,"ch_data":[{{"data_idx":0,"units":1,"val":{0}}}]}}\n'.format(int(read_2_cleaned)/1000)

        # Encode the string (turn it into binary)
        temperature_data = temperature_data.encode()
        gravity_data = gravity_data.encode()

        # Write the data into Gadget
        gadget.stdin.write(temperature_data)
        gadget.stdin.write(gravity_data)
        gadget.stdin.flush()

        # Run Gadget
        gadget.stdin.write(b'run\n')
        gadget.stdin.flush()


        # Set the delay in seconds. Set this low for testing purposes.
        # Each loop counts as 2 messages in Avimesa as we're using 2 channels.
        sleep(1)

    except KeyboardInterrupt:
        print('Closing Gadget...')

        # Close Gadget (trick)
        gadget.stdin.close()

        break
