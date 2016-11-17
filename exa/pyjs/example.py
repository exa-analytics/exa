from ipywidgets import register, DOMWidget
from traitlets import Unicode


@register("hello.Hello")
class HelloWorld(DOMWidget):
    """Example widget."""
    _view_name = Unicode("HelloView").tag(sync=True)
    _model_name = Unicode("HelloModel").tag(sync=True)
    _view_module = Unicode("jupyter-exa").tag(sync=True)
    _model_module = Unicode("Jupyter-exa").tag(sync=True)

    value = Unicode("Hello World!").tag(sync=True)
    
