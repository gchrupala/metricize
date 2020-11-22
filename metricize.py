#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from itertools import izip, chain, repeat
import os.path
import modifyzip

def main():
    '''Apply unit conversion to all html files found in a zip (i.e. epub) file'''
    inp = sys.argv[1]
    out = sys.argv[2]
    convert = lambda x: replaceUnits(x, logger=sys.stderr)
    modifyzip.modifyZip(inp, out, \
            lambda f: os.path.splitext(f)[1] == ".html", convert)

def replaceUnits(text, logger=None):
    '''Convert quantities in legacy units to SI units in a text string'''
    def replace(match):
        try:
            x = float(match.group(1).replace(",", ""))
        except ValueError:
            return match.group(0)
        sep  = match.group(2)
        unit = match.group(3)
        unit_si, (a, b) = units[unit]
        output = "%s%s%s" % (prettify(a * x + b), sep, unit_si)
        if logger:
            logger.write("%s --> %s\n" % (match.group(0), output))
        return output
    number_unit = re.compile(
        "([0-9,\.]+)(-|\s+)(" 
        + "|".join(sorted(units.keys(), key=lambda x: len(x), reverse=True)) 
        + ")")
    return re.sub(number_unit, replace, text)

def prettify(n):
    '''Readably format input string using simple heuristics'''
    string = "%f" % n
    whole, decimal = string.split(".")
    whole_pretty = "".join(reversed(",".join(["".join(x) for x in grouper(3, reversed(whole), "") ] )))
    if whole_pretty == "0":
        # Use complete decimal
        return whole_pretty + "." + decimal
    elif int(whole) > 10:
        # Skip the decimal
        return whole_pretty
    elif float("0." + decimal)      == 0:
        # Skip the decimal
        return whole_pretty
    else:
        # Round to 2 decimal places
        return whole_pretty + "." + ("%.1f" % float("0." + decimal))[2:]

def grouper(n, iterable, padvalue=None):
    "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
    return izip(*[chain(iterable, repeat(padvalue, n-1))]*n)


#          slope, intercept
in_cm   = (2.54,    0)
ft_m    = (0.3048,  0)
yd_m    = (0.9144,  0)
mi_km   = (1.60934, 0)
oz_g    = (28.3495, 0)
lb_kg   = (0.453592,0)
gal_L   = (3.78541, 0)
ac_ha   = (0.404686,0)
sqmi_sqkm = (2.58999, 0)
F_C     = (0.5556,   -17.7778)

units = {
   # distance
          "inch":   ("cm", in_cm)
        , "inches": ("cm", in_cm)
        , "foot":   ("m", ft_m)
        , "feet":   ("m", ft_m)
        , "yard":   ("m", yd_m)
        , "yards":   ("m", yd_m)
        , "mile":   ("km", mi_km)
        , "miles":  ("km", mi_km)
        # weight
        , "ounce":  ("g", oz_g)
        , "ounces": ("g", oz_g)
        , "pound":  ("kg", lb_kg)
        , "pounds":  ("kg", lb_kg)
        # volume
        , "gallon": ("L", gal_L)
        , "gallons": ("L", gal_L)
        # area
        , "acre": ("ha", ac_ha)
        , "acres": ("ha", ac_ha)
        , "square mile": ("square km", sqmi_sqkm)
        , "square miles": ("square km", sqmi_sqkm)
        # temperature
        , "degree Fahrenheit": ("°C", F_C)
        , "degrees Fahrenheit": ("°C", F_C)
        , "degrees": ("°C", F_C)
        , "degree":  ("°C", F_C)
        , "°F": ("°C", F_C)
        }

if __name__ == '__main__':
    main()
