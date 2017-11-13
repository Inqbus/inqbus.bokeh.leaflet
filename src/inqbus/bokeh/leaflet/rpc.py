import json

import os

from bokeh.core.properties import Instance
from bokeh.models import InputWidget, Text

import re

from bokeh.util.compiler import JavaScript

try:
    from eprofile.bokeh import config as bcfg
except:
    from eprofile.bokeh import config_default as bcfg
try:
    import eprofile.configs.config as cfg
except:
    import eprofile.configs.config_default as cfg
from eprofile.bokeh.log import logger

from eprofile.bokeh.log import logger

PYTHON_RPC_PATTERN = re.compile("(?P<func>[a-zA-Z_.]*)\((?P<params>.*)\)")


class RPCWidget(InputWidget):
    """
    Base View providing a api to deal with Leaflet Map and remote procedure calls
    """

    if bcfg.DEV_MODE:
        __implementation__ = os.path.join(bcfg.COFFEE_DIR, 'widgets/rpc.coffee')

    # helper objects for rpc
    python_calls = Instance(Text)
    js_calls = Instance(Text)
#    bokeh_ref = Instance(Text)
#    parent_layout_id = Instance(Text)


    def __init__(self, parent_layout=None, *args, **kwargs):
        super(RPCWidget, self).__init__(*args, **kwargs)
        self._parent_layout = parent_layout
#        if parent_layout:
#            self.parent_layout_id = Text(text=parent_layout._id)
#        else:
#            self.parent_layout_id = Text(text='')

        self.python_calls = Text(text='')

        self.js_calls = Text(text='')

#        self.bokeh_ref = Text(text=bcfg.BOKEH_URL)

        self.python_calls.on_change('text', self.python_call)

        self._registered_functions = {}

    def register_function(self, id, function):
        self._registered_functions[id] = function

    def python_call(self, attrname, old, new):
        text = self.python_calls.text

        match = PYTHON_RPC_PATTERN.match(text)
        if match:
            func = match.group('func')
            params = match.group('params')


            if func in self._registered_functions:

                self._registered_functions[func](json.loads(params))
            else:
                logger.error("RPC python call %s not registered" % text)
        else:
            logger.error("RPC python call %s not correct" % text)
#        self.python_calls.text = ''

    def send_js_calls(self, calls=''):
        logger.info('Send JS call: ' + calls)
        self.js_calls.text = calls
        # reset js_calls.text to make sure on next change it is recognized again
        self.js_calls.text = ''


