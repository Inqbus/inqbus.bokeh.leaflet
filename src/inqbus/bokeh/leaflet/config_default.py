
# ===================
# Anchoring of files
# ===================

import os
MODULE_PATH = os.path.dirname(__file__)

# ===================
# Development mode
# ===================

# Base dir for locating coffe, css, js files to reference in __implemetation__ stanzas
BOKEHJS_DIR = os.path.join(MODULE_PATH, "bokehjs")
COFFEE_DIR = os.path.join(BOKEHJS_DIR, "coffee")

# ===================
# Bokeh server parameter
# ===================

BOKEH_HOST_INTERN_IP = '127.0.0.1'
BOKEH_HOST_INTERN_PORT = '5006'
# Replace by extern bokeh address
BOKEH_HOST_EXTERN = '127.0.0.1:5006'

USE_HTTPS = False

if USE_HTTPS:
    HTTP_PREFIX = 'https://'
else:
    HTTP_PREFIX = 'http://'

BOKEH_URL = HTTP_PREFIX + BOKEH_HOST_EXTERN

# =================
# Leaflet
# =================
# available Zoomlevels
ZOOM_LEVELS = range(19)
ZOOM_LEVEL_MIN = min(ZOOM_LEVELS)
ZOOM_LEVEL_MAX = max(ZOOM_LEVELS)

# important LF-Fields which are used to pass options to leaflet
LF_COLOR_FIELD = 'markerColor'
LF_MARKER_ICON_FIELD = 'icon'
LF_ICON_SIZE_FIELD = 'iconSize'
LF_ICON_OFFSET_FIELD = 'iconAnchor'
LF_SHADOW_SIZE_FIELD = 'shadowSize'
LF_SHADOW_OFFSET_FIELD = 'shadowAnchor'
LF_ICON_ID = 'id'

# default sizes and anchors of marker and shadows. Used for scaling markers
DEFAULT_MARKER_SIZE = [30, 50]
DEFAULT_MARKER_ANCHOR = [15, 50]
DEFAULT_SHADOW_SIZE = [54, 51]
DEFAULT_SHADOW_ANCHOR = [45, 39]

