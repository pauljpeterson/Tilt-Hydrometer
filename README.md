# Tilt-Hydrometer

*Last updated: 2020 May 19*

## Connecting the Tilt Hydrometer to Avimesa's IoT platform

This project allows you to remotely monitor your brew using a Tilt Hydrometer, a Raspberry Pi and Avimesa's IoT cloud platform and application, giving you real-time charts and the ability to set SMS and email alerts if the temperature or gravity readings hit a specified number. Using this Python script, we will read the data from the Tilt device and pipe it into Avimesa Gadget, which in turn sends the data to the Avimesa Cloud and ultimately displayed in the Avimesa.Live web application.

### Things you will need

1. [Tilt Hydrometer][1]
2. [Raspberry Pi][2] with Bluetooth and WiFi
3. [Avimesa.Live][3] account - (Free account includes 10,000 readings per month)
4. [Avimesa Gadget][4] - Free download
5. Some knowledge of the command line and either using the Terminal directly on the Raspberry Pi or accessing the Pi remotely via SSH is helpful. 

### Step 1

If accessing your Raspberry Pi remotely from another machine, open a terminal window and SSH into your Pi: usually something like `ssh pi@192.168.0.101`, or open a terminal window in the Pi itself if directly connected to it. 

More info on SSH on a Raspberry Pi [here][8].

Follow `Step 1` and `Step 2` [on this page][5]

Make sure you're getting a data reading from your Tilt by making sure the Tilt is activated then running `sudo python3 -u -m aioblescan -T` per the instructions. You should see some output something like this:

`{"mac": "f7:a2:58:95:f0:96", "uuid": "a495bb30c5b14b44b5121370f02d74de", "rssi": -72, "minor": 1035, "major": 74, "tx_power": 29}`

### Step 2

If you haven't already signed up for a free Avimesa.Live account, do so [here][3].

### Step 3

Install Avimesa Gadget. [Instructions here][6]. Avimesa Gadget turns a Raspberry Pi, or machine running Debian Linux, into an IoT device that can send messages to the Avimesa Cloud.

### Step 4

Create a folder for your project on the Pi and copy the `avimesa-tilt.py` file to the folder. A quick way of doing that is to type `mkdir foldername` replacing *foldername* with the name of your choice, then `cd foldername` to change into that folder. Now, download the `avimesa-tilt.py` file to your project folder. Run the following command to download the file:

```
curl -O https://raw.githubusercontent.com/pauljpeterson/Tilt-Hydrometer/master/avimesa-tilt.py
```
Retrieve one of your Avimesa Device ID's and its respective Auth Code. You should have this info in your welcome email.

Edit the `avimesa-tilt.py` file by running command: `nano avimesa-tilt.py`

Look for the following lines and replace the Device ID and Auth code with your own:

```
nano avimesa-tilt.py
```

Save the file by hitting `Ctrl+o` (the letter 'o', not zero) then hit `Enter` to accept and `Ctrl+X` to exit.

### Step 5

Sign in to [Avimesa.Live][7]

Click on the device that matches the Device ID that you added to the `avimesa-tilt.py` file.

Click the `+` icon to add a new sensor.

This will be for the temperature, so name it `Tilt Temperature` or whatever you want. Next select `Temperature Fahrenheit` from the drop-down.

The next two fields are optional, but give the Chart Title a name like `Temperature`

For the Analog channel no. select `0` and a Minimum and Maximum reading of `0` and `100` respectively. These values aren't applicable to this sensor so these can be arbitrary numbers. It doesn't matter.

Click the `Add Sensor` button.

Now add another sensor, following the same steps above. This time call it `Gravity` or something to your liking.

For Analog channel no. select `1` with a Minimum and Maximum reading of `0` and `100` respectively. Again, these values can be anything as they don't apply here.

Click the `Add Sensor` button.

### Step 6 - Getting your data to flow

By now, hopefully everything is set up correctly. Now, activate your Tilt Hydrometer and from the command line type the following command:

```
python3 avimesa-tilt.py
```
Now check your dashboard in Avimesa.Live. You should now be able to see your data on the charts and set alerts for SMS and emails.


[1]: https://tilthydrometer.com/
[2]: https://raspberrypi.org/
[3]: https://avimesa.com/create-account/
[4]: https://www.avimesa.com/avimesa-gadget/
[5]: https://tilthydrometer.com/blogs/news/install-tilt-pi-on-raspbian-buster-compatible-with-all-rpi-models-including-rpi-4
[6]: https://www.avimesa.com/docs/user-guides/avimesa-gadget-virtual-device-client/
[7]: https://avimesa.live/login/
[8]: https://www.raspberrypi.org/documentation/remote-access/ssh/
