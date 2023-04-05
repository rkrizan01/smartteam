#! /bin/bash
echo "Bluetooth connection opened. Kill With './end_bluetooth_connection.sh or with Ctrl+C'" &
sudo rfcomm connect hci0 00:14:03:05:59:51
