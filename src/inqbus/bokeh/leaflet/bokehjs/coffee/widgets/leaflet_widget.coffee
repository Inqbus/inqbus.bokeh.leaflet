import {throttle} from "core/util/callback"

# The "core/properties" module has all the property types
import * as p from "core/properties"

# HTML construction and manipulongitudeion functions
import {empty, label, input, div} from "core/dom"

# We will subclass in JavaScript from the same class that was subclassed
# from in Python
import {InputWidget, InputWidgetView} from "models/widgets/input_widget"

export class LeafletWidgetView extends InputWidgetView

  initialize: (options) ->
    super(options)
    @model._view = @

    @_map_div = div({id: 'map'})
    @_map_div.style.width= @model.width.toString() + 'px'
    @_map_div.style.height= @model.height.toString() + 'px'
    @el.appendChild( @_map_div )
    @init_map()
    @initialize_handler()

    return @

  init_map: () ->
    LeafletWidgetView::_map = L.map(@_map_div, {center:[49.51, 3.17], zoom:5});

    # OpenStreetMap tileLayer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(@_map);
    @_has_map = 1

    @_map.createPane('icon_pane')
    @_map.getPane('icon_pane').style.zIndex = 610

    @_marker_layer = @add_new_layer()
    @_icon_layer = @add_new_layer('icon_pane')


  render: () ->
    @_map.invalidateSize()


  initialize_handler: () ->
    @_rpc = @model.document._all_models_by_name.get_one('RPC_Control')._view

    # Handler for Python Site listening on map
    @_map.on('zoomend', jQuery.proxy(() -> @_rpc.send_python_calls('Map.zoomed(' + @_map._zoom.toString() + ')')), this)
    # initialize map data on Python Site
    @_rpc.send_python_calls('Map.zoomed(' + @_map._zoom + ')')
    return

  add_new_layer: (pane = 'markerPane') ->
    layer = L.layerGroup()
    layer.pane = pane
    @_map.addLayer(layer)
    return layer

  add_layer: (layer) ->
    @_map.addLayer(layer)

  remove_layer: (layer) ->
    @_map.removeLayer(layer)

  empty_layer: (layer) ->
    layer.clearLayers()
    return

  set_marker: (latitude, longitude, parent, options={}) ->
    #use options for kwargs which are not supported by coffee script
    if 'tooltip' of options
        tooltip = options['tooltip']
    else
        tooltip = null
    if 'lf_options' of options
        lf_options = options['lf_options']
    else
        lf_options = {}
    if 'popup' of options
        popup = options['popup']
    else
        popup = null
    if 'id' of options
        id = options['id']
    else
        id = null

    marker = L.marker([
          latitude
          longitude
        ], icon: L.VectorMarkers.icon(
          lf_options
          ))
    if tooltip != null
        marker.bindTooltip(tooltip)
    if popup != null
        marker.bindPopup(popup)
    if id != null
        marker.options['id'] = id
    marker.addTo(parent)
    return marker


  set_icon: (latitude, longitude, icon_path, parent, options={}) ->
    if 'tooltip' of options
        tooltip = options['tooltip']
    else
        tooltip = null
    if 'lf_options' of options
        lf_options = options['lf_options']
    else
        lf_options = {}
    if 'popup' of options
        popup = options['popup']
    else
        popup = null

    lf_options['iconUrl'] = icon_path

    icon = L.marker([
        latitude,
        longitude,
    ], {icon: L.icon(lf_options), pane: 'icon_pane'
    })
    if tooltip != null
        icon.bindTooltip(tooltip)
    if popup != null
        icon.bindPopup(popup)
    icon.addTo(parent)
    return icon



export class LeafletWidget extends InputWidget

  # This is usually boilerplongitudee. In some cases there may not be a view.
  default_view: LeafletWidgetView

  # The ``type`` class attribute should generally match exactly the name
  # of the corresponding Python class.
  type: "LeafletWidget"

  # The @define block adds corresponding "properties" to the JS model. These
  # should basically line up 1-1 with the Python model class. Most property
  # types have counterparts, e.g. ``bokeh.core.properties.String`` will be
  # ``p.String`` in the JS implementatin. Where the JS type system is not yet
  # as rich, you can use ``p.Any`` as a "wildcard" property type.
  @define {
  }
