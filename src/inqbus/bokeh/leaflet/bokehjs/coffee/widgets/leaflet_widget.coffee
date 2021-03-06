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
    # view ca be reached by other objects
    @model._view = @
    # create a div for the leaflet map
    @_map_div = div({id: 'map'})
    @_map_div.style.width= @model.width.toString() + 'px'
    @_map_div.style.height= @model.height.toString() + 'px'
    @el.appendChild( @_map_div )
    @init_map()
    @initialize_handler()

    return @

  init_map: () ->
    # create the map object
    LeafletWidgetView::_map = L.map(@_map_div, {center:[49.51, 3.17], zoom:5});

    # OpenStreetMap tileLayer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(@_map);
    @_has_map = 1

    # create panes and layers for icons and marker
    @_map.createPane('icon_pane')
    @_map.getPane('icon_pane').style.zIndex = 610
    @_marker_layer = @add_new_layer()
    @_icon_layer = @add_new_layer('icon_pane')

    # set legend
    @legend = L.control({position: 'bottomleft'});
    @legend.onAdd = (map) ->
      div = L.DomUtil.create('div', 'info legend')
      return div

    @legend.addTo(@_map)

    # set initial data
    @update_legend()
    @set_all_icons()
    @set_all_marker()

  render: () ->
    @_map.invalidateSize()

  initialize_handler: () ->
    @_rpc = @model.document._all_models_by_name.get_one('RPC')._view
    # Handler for Python Site listening on map
    @_map.on('zoomend', jQuery.proxy(() -> @_rpc.send_python_calls('Map.zoomed(' + @_map._zoom.toString() + ')')), this)
    # initialize map data on Python Site
    @_rpc.send_python_calls('Map.zoomed(' + @_map._zoom + ')')
    # register possible js callbacks
    @_rpc.register_rpc_call( 'map.set_all_marker', @, LeafletWidgetView::set_all_marker )
    @_rpc.register_rpc_call( 'map.set_all_icons', @, LeafletWidgetView::set_all_icons)
    @_rpc.register_rpc_call( 'map.update_legend', @, LeafletWidgetView::update_legend)
    return

  add_new_layer: (pane = 'markerPane') ->
    layer = L.layerGroup()
    layer.pane = pane
    @_map.addLayer(layer)
    return layer

  empty_layer: (layer) ->
    layer.clearLayers()
    return

  set_marker: (latitude, longitude, parent, options={}) ->
    # use options for kwargs which are not supported by coffee script

    # check if kwargs are set or set default value
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

    # create marker
    # we use VectorMarkers because they are easy to scale and available in each rgb-color
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
    # use options for kwargs which are not supported by coffee script
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
    if id != null
        icon.options['id'] = id
    icon.addTo(parent)
    return icon

  set_all_marker: () ->
        # remove all markers for the case some of them are deleted
        @empty_layer(@_marker_layer)

        # get the source
        source = @model.marker_source.data
        markers = source.rows
        number_points = markers.length
        l = 0
        # set each marker in source
        while l < number_points
            # data is a list of lists holding dictionaries. So we grep the dict first
            data = markers[l][0]

            # we read the data from dict and add the marker to the map
            lon = data.longitude
            lat = data.latitude
            lf_options = data.options
            tooltip = data.tooltip
            popup = data.popup
            id = data.id
            @set_marker(lat, lon, @_marker_layer, {lf_options:lf_options, tooltip:tooltip, popup:popup, id:id})
            l++
        return

    set_all_icons: () ->
        # remove all icons for the case some of them are deleted
        @empty_layer(@_icon_layer)
        source = @model.icon_source.data
        icons = source.rows
        number_points = icons.length
        l = 0
        while l < number_points
            # icons data is a list of lists holding dictionaries. So we grep the dict first
            data = icons[l][0]

            # we read the data from dict and add the icon to the map
            lon = data.longitude
            lat = data.latitude
            icon = data.icon
            lf_options = data.options
            tooltip = data.tooltip
            popup = data.popup
            id = data.id
            @set_icon(lat, lon, icon, @_icon_layer, {lf_options:lf_options, tooltip:tooltip, popup:popup, id:id})
            l++
        return

    update_legend: () ->
        # grep the legend div
        div = @legend._container
        # get the html from legend_source
        source = @model.legend_source.data.legend[0]
        # update legend_html
        div.innerHTML = source


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
    rpc: [p.Any]
    marker_source: [p.Any]
    icon_source: [p.Any]
    legend_source: [p.Any]
  }
