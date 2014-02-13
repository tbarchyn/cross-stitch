#!/bin/bash

# Pass README output file name as argument

HEADER="cross-stitch
============

A Python application to turn your images into patterns for cross stitching.

https://github.com/anders-dc/cross-stitch

Requirements
------------
Python 2 or 3, Numpy, Scipy, and Matplotlib.

To install these dependencies in Debian and its derivatives, run:

  $ sudo apt-get install python python-numpy python-scipy python-matplotlib

License
-------
GNU Public License version 3 or newer. See LICENSE.txt for details.

Author
------
Anders Damsgaard (andersd@riseup.net)

Todo
----
Add color processing functions to enhance colors and limit the number of colors.
Show product names of needed yarn colors.

Usage
-----
"

echo "Generating $1"
echo "$HEADER" > $1
echo "  `./cross-stitch.py -h`" >> $1

EXAMPLE="
Example
-------

  $ ./cross-stitch.py -i fiskeren.jpg -o fisker-pattern.py -w 50

.. image:: fiskeren.jpg
   :scale: 50 %
   :alt: Original image
   :align: center

.. image:: fisker-pattern.png
   :scale: 60 %
   :alt: Cross stitching pattern
   :align: center

"

echo "$EXAMPLE" >> $1
