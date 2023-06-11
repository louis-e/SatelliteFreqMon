# Automated Satellite SDR Groundstation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

The goal of this project is to provide a comprehensive open source solution for accurately monitoring satellite passes[^1] using configurable [TLE (Two-Line Elements)](https://en.wikipedia.org/wiki/Two-line_element_set)[^2] and precise frequency recording using the software-defined radio application GQRX[^3].


## Hardware Setup

<img src="git-assets/hardware-setup.png?raw=true" width="70%">

### Hardware List
- RTL-SDR RTL2832U Dongle
- Wideband LNA
- V Dipole Antenna (tuned for NOAA frequencies)
- Raspberry Pi


## TLE File Configuration
Place the TLE files in the `sats/` directory.

### Syntax
```
SATELLITE NAME
TLE-LINE-1
TLE-LINE-2
FREQUENCY
BANDWIDTH (Frequency range)
```

### Example
```
NOAA19
1 33591U 09005A   23156.14173894  .00000208  00000-0  13708-3 0  9991
2 33591  99.1001 201.8759 0012774 277.1213  82.8506 14.12764011738249
137100
42000
```

Also make sure to adapt the GROUNDSTATION_LOCATION variable to set the groundstation location. This is necessary to accurately calculate the satellite passes.

## Example Output

```
pi@sdrpi:~/sat-tracker $ python tracker.py
===== Passes calculated for: ['METEOR M2', 'NOAA19', 'NOAA15', 'ISS (ZARYA)', 'JAS 2 (FO-29)', 'NOAA18'] =====
=== Configuring GQRX...
M WFM 45000 RPRT 0
L SQL -150 RPRT 0
=== ISS (ZARYA) overpass (2023-06-07 17:52:22 - 2023-06-07 18:02:57 for 0:10:34.696568) on 145800KHz.
F 145800000 RPRT 0
M WFM 40000 RPRT 0
AOS RPRT 0
```

<img src="git-assets/gqrx-noaa.png?raw=true" width="50%">

## Maintainership and License

If you have any suggestions for improvements or would like to contribute to the project, feel free to submit a pull request.
This project is licensed under the MIT License[^4]. See the [LICENSE](LICENSE) file for details.

Copyright (c) 2023 louis-e

[^1]: https://github.com/satellogic/orbit-predictor

[^2]: "A two-line element set (TLE) is a data format encoding a list of orbital elements of an Earth-orbiting object for a given point in time, the epoch." https://en.wikipedia.org/wiki/Two-line_element_set

[^3]: "Gqrx is an open source software defined radio receiver (SDR) powered by the GNU Radio and the Qt graphical toolkit." https://gqrx.dk/

[^4]:
    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
    
    The above copyright notice, the author ("louis-e") and this permission notice shall be included in all copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.