#!/bin/bash

# Start Bluetooth service if it's not running
echo "Starting Bluetooth service..."
sudo systemctl start bluetooth

# Wait a few seconds to allow Bluetooth to initialize (increase sleep time if necessary)
echo "Sleeping for 10 seconds to allow Bluetooth to initialize..."
sleep 10

# Start bluetoothctl in a more controlled manner
echo "Running bluetoothctl commands to set up Bluetooth connection..."
bluetoothctl << EOF
power on
agent on
default-agent
trust 90:89:5F:C5:63:CC      # Trust the device
connect 90:89:5F:C5:63:CC    # Connect to the device
exit
EOF

# Monitor the connection status and reconnect if necessary
echo "Starting Bluetooth connection monitoring loop..."
while true; do
  # Check if the device is still connected
  if ! bluetoothctl info 90:89:5F:C5:63:CC | grep -q "Connected: yes"; then
    echo "Device disconnected, reconnecting..."
    bluetoothctl << EOF
    connect 90:89:5F:C5:63:CC
    exit
EOF
  fi
  sleep 5  # Wait for 5 seconds before checking again
done &  # Run the monitoring loop in the background

# After the loop starts, we can run the Python script.
echo "Bluetooth device is connected and monitoring loop is running. Running Python script now..."

# Run the Python script
/usr/bin/python3.9 /home/ibrahim/final.py

# If Python script execution reaches here, confirm its availability.
echo "Python script has finished executing."
