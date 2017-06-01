import time
from tmp102 import TMP102

# Initialize TMP Object
tmp = TMP102('C', 0x48, 1)

# Actually, lets make the temperatures Farenheit
tmp.setUnits('F')

while True:
    print "Current temp: {:.1f}degF".format(tmp.readTemperature())
    time.sleep(1)
