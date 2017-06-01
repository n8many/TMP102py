# TMP102py

Python Library for reading temperature data from the TMP102 breakout board from Sparkfun.
https://www.sparkfun.com/products/13314

Written for the Raspberry Pi, but should work on other Linux based computers so long as they have an i2c bus you can connect to.

## Installation

1. Enable I2C on your computer
2. Install the smbus library (via pip)
3. Add this library to your project. You can either...
   * Clone this repo to your project via:

       ```git clone https://github.com/n8many/TMP102py.git```

   * Or download "tmp102.py" to have the code in your project base directory.


## Usage

If you cloned the repo to your project, add the TMP102 object via:

```from TMP102py.tmp102 import TMP102```

If you added the file directly to your project, then use:

```from tmp102 import TMP102```

Initializing a sensor can be as easy as:

```tmp = TMP102()```

Or optionally, you can specify the output units (default 'C' for Celcius), sensor address (default 0x48), and i2c bus (default 1)

```tmp = TMP102(units='C', address=0x48, busnum=1)```

If you would like to change the output units after initialzing an object, you can use the setUnits function.

```tmp.setUnits('F') #Possible inputs are C(elcius), F(arenheit), K(elvin), and R(ankine)```

If you would like to get a temperature reading, then use:

```tmp.readTemperature()```

## History

5/25/17 - Creation

## Credits

Most of this code is being translated from the original Sparkfun library here: https://github.com/sparkfun/SparkFun_TMP102_Arduino_Library

## License

This is under the MIT License
