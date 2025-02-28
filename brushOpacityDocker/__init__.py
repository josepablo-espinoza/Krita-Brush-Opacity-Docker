from .brushOpacityDocker import BrushOpacityDocker
from krita import DockWidgetFactory,  DockWidgetFactoryBase# type: ignore

__ver__ = "1.0.0"

DOCKER_NAME = 'Brush Opacity Docker '
DOCKER_ID = 'pykrita_opacityDocker'

# Register the Docker with Krita
instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID, DockWidgetFactoryBase.DockRight, BrushOpacityDocker)

instance.addDockWidgetFactory(dock_widget_factory)