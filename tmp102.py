import smbus

TEMPERTAURE_REG = 0x00
CONFIG_REG = 0x01
T_LOW_REG = 0x02
T_HIGH_REG = 0x03

ADDRESSES = [0x48, 0x49, 0x4A, 0x4B]

class TMP102(object):
    def __init__(self, units=None, address=0x48, busnum=1):
        units = units or 'C'
        if (address not in ADDRESSES):
            raise ValueError("Invalid Address: {0:#x}".format(address))
        self.address = address
        self.busnum = busnum

        self.setUnits(units)
        self.bus = smbus.SMBus(self.busnum)
        self.getTemperature()

    def getUnits(self):
        return self.units

    def setUnits(self, units):
        if (units.upper() in 'RCKF' and len(units) == 1):
            self.units = units.upper()
        else:
            raise ValueError("Invalid Unit, must use C(elcius), K(elvin),"
                    "F(ahrenheit), or R(ankine)")

    def getTemperature(self):
        data = self.bus.read_i2c_block_data(self.address, TEMPERTAURE_REG, 2)

        #Adjustment for extended mode
        ext = data[1] & 0x01
        res = int((data[0] << (4+ext)) + (data[1] >> (4-ext)))

        if (data[0] | 0x7F is 0xFF):
            res = res - 4096*(2**ext)

        tempC = res*0.0625
        tempConvert = {
            'C': lambda x: x,
            'K': lambda x: x+273.15,
            'F': lambda x: x*9/5+32,
            'R': lambda x: (x+273.15)*9/5
        }
        try:
            tempOut = tempConvert[self.units](tempC)
        except:
            raise ValueError('Invalid Units "' + self.units + '"')
        return tempOut

    def setConversionRate(self, rate):
        pass

    def setExtendedMode(self, mode):
        pass

    def sleep(self):
        pass

    def wakeup(self):
        pass

    def setAlertPolarity(self, polarity):
        pass

    def alert(self):
        pass

    def setLowTemp(self, temperature):
        pass

    def setHighTemp(self, temperature):
        pass

    def readLowTemp(self):
        pass

    def readHighTemp(self):
        pass

    def setFault(self, faultSetting):
        pass

    def setAlertMode(self, mode):
        pass
