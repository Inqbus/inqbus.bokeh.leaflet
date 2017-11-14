# bokeh serve src/inqbus/bokeh/leaflet src/inqbus/bokeh/leaflet/examples/leaflet_example.py
# go to http://localhost:5006/leaflet_example

from bokeh.io import curdoc

from inqbus.bokeh.leaflet.leaflet import LeafletWidget
try:
    # here you can add a custom config, but it must be located in inqbus.bokeh.leaflet because it is used by Widgets, too
    from inqbus.bokeh.leaflet import config as cfg
except ImportError:
    from inqbus.bokeh.leaflet import config_default as cfg

# CREATE WIDGET
widget = LeafletWidget(width=1024, height=768)

# SET MARKERS
# for marker_size we use widget calculate_size to fit shadows and offset
size_options = widget.calculate_marker_scale(1.0)

# we set blue markers without icon
# in option you can put everything passed to the leaflet-marker
options = {
    # color can be every rgb color
    cfg.LF_COLOR_FIELD: 'blue',
    cfg.LF_MARKER_ICON_FIELD: '',
}
# we add marker size to options
options.update(size_options)
# list of lists is required by ColumnDataSource used in widget
marker_data = [
    [{'longitude':-0.118092, 'latitude':51.509865, 'options':options, 'tooltip': 'Marker Tooltip 1', 'popup': 'Marker PopUp 1', 'id': 'marker1'}],
    [{'longitude':13.404954, 'latitude':52.520008, 'options':options, 'tooltip': 'Marker Tooltip 2', 'popup': 'Marker PopUp 2', 'id': 'marker2'}],
]
# add the marker
widget.set_marker(marker_data)

# SET ICONS
url = cfg.BOKEH_URL + '/leaflet/static/example_images/example.png'
size = 50
options = {
    cfg.LF_ICON_SIZE_FIELD: [size, size],
    cfg.LF_ICON_OFFSET_FIELD: [size/2, size/2], # long, lat are placed in the center of the image.
}
# list of lists is required by ColumnDataSource used in widget
icon_data = [
    [{'icon': url, 'longitude':5.234565, 'latitude':50.509865, 'options':options, 'tooltip': 'Icon Tooltip 1', 'popup': 'Icon PopUp 1', 'id': 'icon1'}],
    [{'icon': url, 'longitude':12.404954, 'latitude':49.520008, 'options':options, 'tooltip': 'Icon Tooltip 2', 'popup': 'Icon PopUp 2', 'id': 'icon2'}],
]
widget.set_icons(icon_data)

# SET LEGEND
widget.set_legend('<div>LEGEND</br>Put your legend here</div>')

# ZOOMING
# react on zoom events
def zoom_handler(widget, zoom):
    print(zoom)

widget.set_map_zoomed_handler(zoom_handler)

doc = curdoc()
doc.add_root(widget.get_layout())



