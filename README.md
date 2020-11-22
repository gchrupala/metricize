# metricize

Metricize detects uses of many types of legacy units in an ebook 
and converts them to the SI (metric) equivalents.

Example: In order to convert an book-us.epub to book-si.epub run the following

    > ./metricize.py book-us.epub book-si.epub
    
## Details 
Conversion will be applied to all HTML files found in the epub archive.
Currently detected units are:

* inch
* foot
* yard
* mile
* ounce
* pound
* gallon
* acre
* square mile
* degree Fahrenheit

Heuristics are used to avoid using too much precision in the output quantities, 
but this is currently very simplistic.

