import utime
from machine import Pin, I2C

import notecard
import adafruit_bme680

ledPin = 25

productUID = "com.your_company.your_name:pi_pico"

led = Pin(ledPin, Pin.OUT)
i2c = I2C(0)

card = notecard.OpenI2C(i2c, 0, 0, debug=True)
print("Connected to Notecard...")

bmeSensor = adafruit_bme680.BME680_I2C(i2c)
print("Connected to BME680...")

req = {"req": "hub.set"}
req["product"] = productUID
req["mode"] = "periodic"
req["inbound"] = 120
req["outbound"] = 60
rsp = card.Transaction(req)

while True:
    # Turn on the LED to take a reading
    led.value(1)

    temp = bmeSensor.temperature
    humidity = bmeSensor.humidity
    print("\nTemperature: %0.1f C" % temp)
    print("Humidity: %0.1f %%" % humidity)

    req = {"req": "note.add"}
    req["file"] = "sensors.qo"
    req["sync"] = True
    req["body"] = { "temp": temp, "humidity": humidity}
    req = card.Transaction(req)

    # Turn off the LED
    led.value(0)
    utime.sleep(3600)