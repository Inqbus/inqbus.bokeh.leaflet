import os

from bokeh.core.properties import Instance
from bokeh.models import InputWidget, Text

try:
    from inqbus.bokeh.leaflet import config as cfg
except ImportError:
    from inqbus.bokeh.leaflet import config_default as cfg


class LeafletWidget(InputWidget):
    """
    Base View providing a api to deal with Leaflet Map and remote procedure calls
    """
    __javascript__ = [cfg.BOKEH_URL + '/bokeh/static/js/leaflet.js',
                      cfg.BOKEH_URL + '/bokeh/static/js/jquery-3.2.1.min.js',
                      cfg.BOKEH_URL + "/bokeh/static/js/leaflet-beautify-marker-icon.js",
                      cfg.BOKEH_URL + "/bokeh/static/leaflet.awesome-markers/leaflet.awesome-markers.js",
                      cfg.BOKEH_URL + "/bokeh/static/vectormarkers/leaflet-vector-markers.min.js",]
    __css__ = [cfg.BOKEH_URL + '/bokeh/static/css/leaflet.css',
               cfg.BOKEH_URL + '/bokeh/static/font-awesome-4.7.0/css/font-awesome.min.css',
               'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
               cfg.BOKEH_URL + '/bokeh/static/css/leaflet-beautify-marker-icon.css',
               cfg.BOKEH_URL + '/bokeh/static/css/ionicons.min.css',
               cfg.BOKEH_URL + '/bokeh/static/leaflet.awesome-markers/leaflet.awesome-markers.css',
               cfg.BOKEH_URL + '/bokeh/static/vectormarkers/leaflet-vector-markers.css',
               ]


    if cfg.DEV_MODE:
        __implementation__ = os.path.join(cfg.COFFEE_DIR,'widgets/leaflet_widget.coffee')

    def __init__(self, parent_layout=None, *args, **kwargs):
        super(LeafletWidget, self).__init__(*args, **kwargs)
        self._zoom = 3
        self._parent_layout = parent_layout
        if parent_layout:
            self.parent_layout_id = Text(text=parent_layout._id)
        else:
            self.parent_layout_id = Text(text='')

        self.bokeh_ref = Text(text=cfg.BOKEH_URL)
        if self._parent_layout and hasattr(self._parent_layout, 'rpc'):
            self._parent_layout.rpc.register_function('Map.zoomed', self.map_zoomed)


    def map_zoomed(self, zoom):
        """
        Dummy method to react on zoom-events in map. Should be overwritten by child class
        :param zoom:
        :return:
        """
        pass
    
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



