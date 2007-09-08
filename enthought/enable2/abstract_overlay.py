""" Abstract base class for overlays.

This class is primarily used so that tools can easily distinguish between 
items underneath them.
"""

from enthought.traits.api import Instance

from component import Component


class AbstractOverlay(Component):
    """ The base class for overlays and underlays of the area.
    
    The only default additional feature of an overlay is that it implements
    an overlay() drawing method that overlays this component on top of
    another, without the components necessarily having an object 
    containment-ownership relationship.
    """

    # The component that this object overlays. This can be None. By default, if 
    # this object is called to draw(), it tries to render onto this component.
    component = Instance(Component)
    
    # The default layer that this component draws into.
    draw_layer = "overlay"

    # The background color (overrides PlotComponent). 
    # Typically, an overlay does not render a background.
    bgcolor = "transparent"

    def __init__(self, component=None, *args, **kw):
        if component is not None:
            self.component = component
        super(AbstractOverlay, self).__init__(*args, **kw)

    def overlay(self, other_component, gc, view_bounds=None, mode="normal"):
        """ Draws this component overlaid on another component.
        """
        pass

    def _draw(self, gc, view_bounds=None, mode="normal"):
        """ Draws the component, paying attention to **draw_order**.
        
        Overrides Component.
        """
        if self.component is not None:
            self.overlay(self.component, gc, view_bounds, mode)
        return

    def _request_redraw(self):
        """ Overrides Enable2 Component.
        """
        if self.component is not None:
            self.component.request_redraw()
        super(AbstractOverlay, self)._request_redraw()
        return

# EOF