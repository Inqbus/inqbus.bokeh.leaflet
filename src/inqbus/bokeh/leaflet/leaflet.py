import os
from bokeh.core.properties import Instance
from bokeh.layouts import row
from bokeh.models import InputWidget, ColumnDataSource

from inqbus.bokeh.leaflet.rpc import RPCWidget

try:
    from inqbus.bokeh.leaflet import config as cfg
except ImportError:
    from inqbus.bokeh.leaflet import config_default as cfg


class LeafletWidget(InputWidget):
    """
    Base View providing a api to deal with Leaflet Map and remote procedure calls
    """
    __javascript__ = [cfg.BOKEH_URL + '/leaflet/static/js/leaflet.js',
                      cfg.BOKEH_URL + '/leaflet/static/js/jquery-3.2.1.min.js',
                      cfg.BOKEH_URL + "/leaflet/static/js/leaflet-beautify-marker-icon.js",
                      cfg.BOKEH_URL + "/leaflet/static/leaflet.awesome-markers/leaflet.awesome-markers.js",
                      cfg.BOKEH_URL + "/leaflet/static/vectormarkers/leaflet-vector-markers.min.js",]
    __css__ = [cfg.BOKEH_URL + '/leaflet/static/css/leaflet.css',
               cfg.BOKEH_URL + '/leaflet/static/font-awesome-4.7.0/css/font-awesome.min.css',
               'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
               cfg.BOKEH_URL + '/leaflet/static/css/leaflet-beautify-marker-icon.css',
               cfg.BOKEH_URL + '/leaflet/static/css/ionicons.min.css',
               cfg.BOKEH_URL + '/leaflet/static/leaflet.awesome-markers/leaflet.awesome-markers.css',
               cfg.BOKEH_URL + '/leaflet/static/vectormarkers/leaflet-vector-markers.css',
               ]


    __implementation__ = os.path.join(cfg.COFFEE_DIR,'widgets/leaflet_widget.coffee')

    rpc = Instance(RPCWidget)
    marker_source = Instance(ColumnDataSource)
    icon_source = Instance(ColumnDataSource)
    legend_source = Instance(ColumnDataSource)

    def __init__(self, *args, **kwargs):
        super(LeafletWidget, self).__init__(*args, **kwargs)
        self._zoom = 3
        self.rpc = RPCWidget(name='RPC')

        self.marker_source = ColumnDataSource(data={'rows': []})
        self.icon_source = ColumnDataSource(data={'rows': []})
        self.legend_source = ColumnDataSource(data={'legend': []})
        self.rpc.register_function('Map.zoomed', self.map_zoomed)

        self._map_zoomend_handler = None

    def set_map_zoomed_handler(self, handler):
        self._map_zoomend_handler = handler


    def map_zoomed(self, zoom):
        """
        :param zoom:
        :return:
        """
        if self._map_zoomend_handler:
            self._map_zoomend_handler(zoom)
    
    def calculate_marker_scale(self, size_scale):
        size = [int(a*size_scale) for a in cfg.DEFAULT_MARKER_SIZE]
        anchor = [int(a*size_scale) for a in cfg.DEFAULT_MARKER_ANCHOR]
        shadow_size = [int(a*size_scale) for a in cfg.DEFAULT_SHADOW_SIZE]
        shadow_anchor = [int(a*size_scale) for a in cfg.DEFAULT_SHADOW_ANCHOR]

        settings = {
            cfg.LF_ICON_SIZE_FIELD: size,
            cfg.LF_ICON_OFFSET_FIELD: anchor,
            cfg.LF_SHADOW_SIZE_FIELD: shadow_size,
            cfg.LF_SHADOW_OFFSET_FIELD: shadow_anchor,
        }

        return settings

    def set_marker(self, data):
        self.marker_source.data = {'rows': data}
        self.rpc.send_js_calls('map.set_all_marker')

    def set_icons(self, data):
        self.icon_source.data = {'rows': data}
        self.rpc.send_js_calls('map.set_all_icons')

    def set_legend(self, html):
        self.legend_source.data = {'legend': [html]}
        self.rpc.send_js_calls('map.update_legend')

    def get_layout(self):
        return row(self.rpc, self)


