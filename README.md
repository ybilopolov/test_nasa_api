Quick test framework draft for testing some (very few) parts of 
[NASA's open API](https://api.nasa.gov/index.html#getting-started).

Written and tested for Python 3.6.

### Installation

    $ pip install -r requirements.txt

This is tested on Linux with vanilla Python 3.6 + pip. 
On platforms where building scipy/numpy may be an issue (e.g. Windows)
using any of the available scientific Python distributions 
(like [conda](https://conda.io/miniconda.html)) is recommended 
(which is actually a good idea in any case).

Then for conda, for example, installation will look like

    $ conda install scipy
    $ pip install -r requirements.txt

### Usage

    $ pytest tests -sv
