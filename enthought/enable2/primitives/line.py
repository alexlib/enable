""" A line segment component. """

from numpy import array, resize

# Enthought library imports.
from enthought.kiva import FILL_STROKE, STROKE
from enthought.traits.api import Any, Event, Float, List, Trait, Tuple

# Local imports.
from enthought.enable2.api import border_size_trait, Component
from enthought.enable2.traits.rgba_color_trait import RGBAColor


class Line(Component):
    """A line segment component"""

    # Event fired when the points are no longer updating.
    # PZW: there seems to be a missing defn here; investigate.

    # An event to indicate that the point list has changed
    updated = Event

    # The color of the line.
    line_color = RGBAColor("black")

    # The dash pattern for the line.
    line_dash = Any

    # The width of the line.
    line_width = Trait(1.0, border_size_trait)

    # The points that make up this polygon.
    points = List  # List of Tuples

    # The color of each vertex.
    vertex_color = RGBAColor("black")

    # The size of each vertex.
    vertex_size = Float(3.0)

    #--------------------------------------------------------------------------
    # 'Line' interface
    #--------------------------------------------------------------------------

    def reset(self):
        "Reset the polygon to the initial state"

        self.points = []
        self.event_state = 'normal'
        self.updated = self
        return

    #--------------------------------------------------------------------------
    # 'Component' interface
    #--------------------------------------------------------------------------

    def _draw(self, gc):
        "Draw this line in the specified graphics context"
        gc.save_state()
        try:
            # Set the drawing parameters.
            gc.set_stroke_color(self.line_color_)
            gc.set_line_dash(self.line_dash)
            gc.set_line_width(self.line_width)

            # Draw the path as lines.
            gc.begin_path()
            offset_points = [(x, y) for x, y in self.points ]
            offset_points = resize(array(offset_points), (len(self.points),2))
            gc.lines(offset_points)
            gc.draw_path(STROKE)

            # Draw the vertices.
            self._draw_points(gc)
        finally:
            gc.restore_state()
        return

    #--------------------------------------------------------------------------
    # Private interface
    #--------------------------------------------------------------------------

    def _draw_points(self, gc):
        "Draw the points of the line"

        # Shortcut out if we would draw transparently.
        if self.vertex_color_[3] != 0:
            gc.save_state()
            try:
                gc.set_fill_color(self.vertex_color_)
                gc.set_line_dash(None)

                offset_points = [(x, y) for x, y in self.points ]
                offset_points = resize(array(offset_points), (len(self.points),2))
                offset = self.vertex_size / 2.0
                if hasattr(gc, 'draw_path_at_points'):
                    path = gc.get_empty_path()
                    path.rect( -offset, -offset,
                               self.vertex_size, self.vertex_size)
                    gc.draw_path_at_points(offset_points, path, FILL_STROKE)
                else:
                    for x, y in offset_points:
                        gc.begin_path()
                        gc.rect(x-offset, y-offset,
                                self.vertex_size, self.vertex_size)
                        gc.fill_path()
            finally:
                gc.restore_state()
        return

# EOF
