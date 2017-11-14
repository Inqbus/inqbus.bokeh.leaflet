import json


import os
import re
from bokeh.core.properties import Instance
from bokeh.models import InputWidget, Text

try:
    from inqbus.bokeh.leaflet import config as bcfg
except:
    from inqbus.bokeh.leaflet import config_default as bcfg
from inqbus.bokeh.leaflet.log import logger


PYTHON_RPC_PATTERN = re.compile("(?P<func>[a-zA-Z_.]*)\((?P<params>.*)\)")


class RPCWidget(InputWidget):
    """
    Base View providing a api to deal with Leaflet Map and remote procedure calls
    """

    __implementation__ = os.path.join(bcfg.COFFEE_DIR, 'widgets/rpc.coffee')

    # helper objects for rpc
    python_calls = Instance(Text)
    js_calls = Instance(Text)


    def __init__(self, *args, **kwargs):
        super(RPCWidget, self).__init__(*args, **kwargs)

        self.python_calls = Text(text='')

        self.js_calls = Text(text='')

        self.python_calls.on_change('text', self.python_call)

        self._registered_functions = {}

    def register_function(self, id, function):
        self._registered_functions[id] = function

    def python_call(self, attrname, old, new):
        text = self.python_calls.text

        match = PYTHON_RPC_PATTERN.match(text)
        if text == '':
            return
        if match:
            func = match.group('func')
            params = match.group('params')


            if func in self._registered_functions:

                self._registered_functions[func](json.loads(params))
            else:
                logger.error("RPC python call %s not registered" % text)
        else:
            logger.error("RPC python call %s not correct" % text)
        self.python_calls.text = ''

    def send_js_calls(self, calls=''):
        logger.info('Send JS call: ' + calls)
        self.js_calls.text = calls
        # reset js_calls.text to make sure on next change it is recognized again
        self.js_calls.text = ''


