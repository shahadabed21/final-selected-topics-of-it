import serial
import time
from azure.iot.device import IoTHubDeviceClient, Message

# Azure IoT Central device connection string
CONNECTION_STRING = "HostName=iotc-83deaab4-5266-485c-b08e-1a04cf870cde.azure-devices.net;DeviceId=project-device;SharedAccessKey=o+BfTPyDUoMCxhPwFFycEuOMyRb+tRlpOTQR5qnM6zI="

# Connect to Arduino Serial (Ensure COM port is correct)
arduino = serial.Serial('COM5', 9600)
time.sleep(2)

# Create Azure IoT client
client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

# Define air quality status and gas level
def interpret_air_quality(aqi):
    aqi = int(aqi)
    if aqi <= 50:
        return "Good", "Low"
    elif aqi <= 100:
        return "Moderate", "Medium"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups", "Elevated"
    elif aqi <= 200:
        return "Unhealthy", "High"
    elif aqi <= 300:
        return "Very Unhealthy", "Very High"
    else:
        return "Hazardous", "Extremely High"

while True:
    try:
        # Read AQI data from Arduino
        data = arduino.readline().decode().strip()

        # Skip if data is not a valid number
        if not data.isdigit():
            continue

        aqi = int(data)
        status, gas_level = interpret_air_quality(aqi)

        print(f"AQI: {aqi}, Status: {status}, Gas Level: {gas_level}")

        # Format message as JSON and send to Azure
        message = Message(f'{{"AQI": {aqi}, "Status": "{status}", "GasLevel": "{gas_level}"}}')
        client.send_message(message)
        print("Message sent to Azure IoT Central")

        time.sleep(5)
    except Exception as e:
        print("Error:", e)
