==============================================================================
inqbus.bokeh.leaflet
==============================================================================

Leaflet Integration for Bokeh Server

Features
--------

- Leaflet Map with VectorMarkers, Icons and Legend
- Communication over RemoteProcedureCall (RPCWidget)


Examples
--------

You may find an example in src/inqbus/bokeh/leaflet/examples/leaflet_example.py


Installation
------------

Create a virtualenv with python3::

    mkvirtualenv --python=/usr/bin/python3 bokeh_leaflet
    cdvirtualenv

Than install nodejs. It is possible to install a prebuild nodejs using pip::

    pip install nodeenv
    nodeenv -p

Than clone the repo and install package::

    git clone https://github.com/Inqbus/inqbus.bokeh.leaflet.git
    cd inqbus.bokeh.leaflet
    python setup.py develop

Run example::

    # serve src/inqbus/bokeh/leaflet to get statics
    # serve src/inqbus/bokeh/leaflet/examples/leaflet_example.py to see example
    bokeh serve src/inqbus/bokeh/leaflet src/inqbus/bokeh/leaflet/examples/leaflet_example.py
    # go to http://localhost:5006/leaflet_example

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@example.com
