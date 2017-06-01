import smbus

TEMPERATURE_REG = 0x00
CONFIG_REG = 0x01
T_LOW_REG = 0x02
T_HIGH_REG = 0x03

ADDRESSES = [0x48, 0x49, 0x4A, 0x4B]

tempConvert = {
    'C': lambda x: x,
    'K': lambda x: x+273.15,
    'F': lambda x: x*9/5+32,
    'R': lambda x: (x+273.15)*9/5
}

tempConvertInv = {
    'C': lambda x: x,
    'K': lambda x: x-273.15,
    'F': lambda x: (x-32)*5/9,
    'R': lambda x: (x*5/9)-273.15
}
class TMP102(object):
    def __init__(self, units=None, address=0x48, busnum=1):
        units = units or 'C'
        if (address not in ADDRESSES):
            raise ValueError("Invalid Address: {0:#x}".format(address))
        self.address = address
        self.busnum = busnum

        self.setUnits(units)
        self.bus = smbus.SMBus(self.busnum)
        self.readTemperature()

    def bytesToTemp(self, data):
        # Adjustment for extended mode
        ext = self.extractConfig(1, 4, 1)
        #ext = data[1] & 0x01
        res = int((data[0] << (4+ext)) + (data[1] >> (4-ext)))

        if (data[0] | 0x7F is 0xFF):
            # Perform 2's complement operation (x = x-2^bits)
            res = res - 4096*(2**ext)
        # Outputs temperature in degC
        return res*0.0625

    def tempToBytes(self, temp):
        # Temp MUST be converted prior to input
        data = [0 , 0]
        res = int(temp/0.0625)
        ext = self.extractConfig(1, 4, 1)
        if (res < 0):
            res = res + 4096 * (2**ext)
        data[0] = (res >> (4 + ext)) & 0xFF
        data[1] = ((res & (2**(4 + ext)-1)) << (4 - ext)) | ext
        return data

    def extractConfig(self, num, location=0, length=0):

        data = self.bus.read_i2c_block_data(self.address, CONFIG_REG, 2)
        if (num == 3):
            #Full register dump
            return data
        else:
            mask = 2**length - 1
            return (data[num] >> location) & mask

    def injectConfig(self, setting, num, location, length):
        mask = (2**length - 1) << location
        setting = (setting << location) & mask
        data = self.bus.read_i2c_block_data(self.address, CONFIG_REG, 2)
        data[num] &= ~mask
        data[num] |= setting
        self.bus.write_i2c_block_data(self.address, CONFIG_REG, data)

    def readTemperature(self, units=None):
        data = self.bus.read_i2c_block_data(self.address, TEMPERATURE_REG, 2)
        tempC = self.bytesToTemp(data)
        units = units or self.units

        try:
            tempOut = tempConvert[units](tempC)
        except:
            raise ValueError('Invalid Units "' + self.units + '"')
        return tempOut

    def getUnits(self):
        return self.units

    def setUnits(self, units):
        if (units.upper() in 'RCKF' and len(units) == 1):
            self.units = units.upper()
        else:
            raise ValueError("Invalid Unit, must use C(elcius), K(elvin),"
                    "F(ahrenheit), or R(ankine)")



    def setConversionRate(self, rate):
        # 0 : 0.25 Hz
        # 1 : 1 Hz
        # 2 : 4 Hz (default)
        # 3 : 8 Hz
        self.injectConfig(rate, 1, 6, 2)

    def setExtendedMode(self, mode):
        # 0 : 12-bit ( -55C to 128C)
        # 1 : 13-bit ( -55C to 150C)

        self.injectConfig(mode, 1, 4, 1)

    def sleep(self):
        self.injectConfig(True, 0, 0, 1)

    def wakeup(self):
        self.injectConfig(False, 0, 0, 1)

    def setAlertPolarity(self, polarity):
        # 0 : Active Low
        # 1 : Active High
        self.injectConfig(polarity, 0, 2, 1)

    def alert(self):
        return extractConfig(1, 5, 1)

    def setFault(self, faultSetting):
        # 0 : 1 fault
        # 1 : 2 faults
        # 2 : 4 faults
        # 3 : 6 faults
        self.injectConfig(faultSetting, 0, 3, 2)

    def setAlertMode(self, mode):
        # 0 : Comparator Mode (Active within temp range)
        # 1 : Thermostat Mode (Active if over T_High, reset on read)
        self.injectConfig(mode, 0, 1, 1)

    def setBoundTemp(self, upper, temperature, units=None):
        units = units or self.units
        ext = self.extractConfig(1, 4, 1)
        try:
            temperature = tempConvertInv[units](temperature)
        except:
            raise ValueError('Invalid Units "' + self.units + '"')
        if (ext is 1 and temperature > 150):
            temperature = 150
        elif (temperature < -55):
            temperature = -55
        data = self.tempToBytes(temperature)

        if (upper):
            reg = T_HIGH_REG
        else:
            reg = T_LOW_REG

        self.bus.write_i2c_block_data(self.address, reg, data)

    def getBoundTemp(self, upper, units=None):
        units = units or self.units
        if (upper):
            reg = T_HIGH_REG
        else:
            reg = T_LOW_REG
        data = self.bus.read_i2c_block_data(self.address, reg, 2)
        tempC = self.bytesToTemp(data)

        try:
            tempOut = tempConvert[units](tempC)
        except:
            raise ValueError('Invalid Units "' + self.units + '"')
        return tempOut
