# We will subclass in JavaScript from the same class that was subclassed
# from in Python
import {InputWidget, InputWidgetView} from "models/widgets/input_widget"
# The "core/properties" module has all the property types
import * as p from "core/properties"

export class RPCView extends InputWidgetView

  initialize: (options) ->
    super(options)
    @model._view = @
    @_rpc_calls = {}
    @initialize_handler()

  initialize_handler: () ->
    # Handler for RPC on Python site
    @model.js_calls.change.connect( RPCView::js_call, @)

  register_rpc_call: ( name, target, method ) ->
    @_rpc_calls[name] = {'target': target, 'method': method }

  # send RPC from JS to Python
  send_python_calls: (new_calls) ->
    @model.python_calls.text = new_calls
    @model.python_calls.change.emit()
    return

  # eval js RPC from Python
  js_call: (context) ->
    if @model.js_calls.text.field == '' or @model.js_calls.text == ''
        return
    else
        call = @model.js_calls.text.field
        if call of @_rpc_calls
            @_rpc_calls[call].method.apply(@_rpc_calls[call].target)
        return


export class RPCWidget extends InputWidget

  # This is usually boilerplate. In some cases there may not be a view.
  default_view: RPCView

  # The ``type`` class attribute should generally match exactly the name
  # of the corresponding Python class.
  type: "RPCWidget"

  # The @define block adds corresponding "properties" to the JS model. These
  # should basically line up 1-1 with the Python model class. Most property
  # types have counterparts, e.g. ``bokeh.core.properties.String`` will be
  # ``p.String`` in the JS implementatin. Where the JS type system is not yet
  # as rich, you can use ``p.Any`` as a "wildcard" property type.
  @define {
    python_calls: [p.Any]
    js_calls: [p.Any]

  }