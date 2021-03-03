# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


def gen_image():
    import numpy as np

    img = np.zeros((256, 256, 4), dtype=np.uint8)
    img[50:150, 50:150, (0, 3)] = 255
    img[5:200, 5:50, (1, 3)] = 255
    img[85:195, 85:195, (2, 3)] = 255
    img[205:250, 205:250, :] = 255
    return img


def gen_large_path(obj):
    import math

    obj.arc(125, 125, 100, 0.0, 2 * math.pi)
    for x in range(0, 250, 25):
        obj.move_to(x, 10)
        obj.line_to(x, 250)
    for y in range(0, 250, 25):
        obj.move_to(10, y)
        obj.line_to(250, y)

    return obj


def gen_small_path(obj):
    for x in range(5, 25, 5):
        obj.move_to(x, 5)
        obj.line_to(x, 20)
    for y in range(5, 25, 5):
        obj.move_to(5, y)
        obj.line_to(20, y)

    return obj


def gen_points(count=100):
    import numpy as np

    points = (np.random.random(size=count) * 250.0)
    return points.reshape(count // 2, 2)


def gen_moderate_complexity_path(obj):
    import math

    obj.arc(150, 100, 50, math.pi, 1.5*math.pi)
    obj.move_to(150, 50)
    obj.line_to(250, 75)
    obj.line_to(150, 100)
    obj.curve_to(115, 75, 135, 125, 100, 100)

    return obj


class draw_path:
    def __init__(self, gc, module):
        self.gc = gc

    def __call__(self):
        with self.gc:
            gen_large_path(self.gc)
            self.gc.set_stroke_color((0.33, 0.66, 0.99, 1.0))
            self.gc.stroke_path()


class draw_rect:
    def __init__(self, gc, module):
        self.points = gen_points()
        self.gc = gc

    def __call__(self):
        with self.gc:
            self.gc.set_fill_color((0.33, 0.66, 0.99, 1.0))
            for pt in self.points:
                self.gc.rect(pt[0], pt[1], 20.0, 20.0)
            self.gc.fill_path()


class draw_marker_at_points:
    def __init__(self, gc, module):
        self.points = gen_points(1000)
        self.gc = gc

    def __call__(self):
        from kiva import constants

        self.gc.draw_marker_at_points(
            self.points, 5.0, constants.PLUS_MARKER
        )


class draw_path_at_points:
    def __init__(self, gc, module):
        self.points = gen_points()
        self.path = gen_small_path(getattr(module, 'CompiledPath')())
        self.gc = gc

    def __call__(self):
        from kiva.api import STROKE

        with self.gc:
            self.gc.set_stroke_color((0.99, 0.66, 0.33, 0.75))
            self.gc.set_line_width(1.5)
            self.gc.draw_path_at_points(
                self.points, self.path, STROKE
            )


class draw_image:
    def __init__(self, gc, module):
        self.img = gen_image()
        self.gc = gc

    def __call__(self):
        self.gc.draw_image(self.img, (0, 0, 256, 256))


class show_text:
    def __init__(self, gc, module):
        from kiva.api import Font

        self.text = [
            'The quick brown',
            'fox jumped over',
            'the lazy dog',
            '狐假虎威',
        ]
        self.font = Font('Times New Roman', size=36)
        self.gc = gc

    def __call__(self):
        with self.gc:
            self.gc.set_fill_color((0.5, 0.5, 0.0, 1.0))
            self.gc.set_font(self.font)
            y = 256 - self.font.size * 1.4
            for line in self.text:
                self.gc.set_text_position(4, y)
                self.gc.show_text(line)
                y -= self.font.size * 1.4


class draw_path_linear_gradient:
    def __init__(self, gc, module):
        import numpy as np
        # colors are 5 doubles: offset, red, green, blue, alpha
        starting_color = np.array([0.0, 1.0, 1.0, 1.0, 1.0])
        ending_color = np.array([1.0, 0.0, 0.0, 0.0, 1.0])
        self.grad_args = (
            100,
            100,
            250,
            75,
            np.array([starting_color, ending_color]),
            'pad',
        )
        self.gc = gc

    def __call__(self):
        with self.gc:
            gen_moderate_complexity_path(self.gc)
            self.gc.linear_gradient(*self.grad_args)
            self.gc.fill_path()


class show_text_radial_gradient:
    def __init__(self, gc, module):
        import numpy as np
        from kiva.api import Font

        starting_color = np.array([0.0, 1.0, 1.0, 1.0, 1.0])
        ending_color = np.array([1.0, 0.0, 0.0, 0.0, 1.0])
        self.grad_args = (
            128,
            128,
            150,
            128,
            128,
            np.array([starting_color, ending_color]),
            'pad',
        )
        self.text = [
            'The quick brown',
            'fox jumped over',
            'the lazy dog',
            '狐假虎威',
        ]
        self.font = Font('Times New Roman', size=36)
        self.gc = gc

    def __call__(self):
        from kiva import constants

        with self.gc:
            self.gc.radial_gradient(*self.grad_args)
            self.gc.set_text_drawing_mode(constants.TEXT_FILL_STROKE)
            self.gc.set_font(self.font)
            y = 256 - self.font.size * 1.4
            for line in self.text:
                self.gc.set_text_position(4, y)
                self.gc.show_text(line)
                y -= self.font.size * 1.4