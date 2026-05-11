#
# This file is part of pytrisk.
#
# pytrisk is free software: you can redistribute it and/or modify it
# under the # terms of the GNU General Public License as published by
# the Free Software # Foundation, either version 3 of the License, or
# (at your option) any later # version.
#
# pytrisk is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with pytrisk. If not, see <https://www.gnu.org/licenses/>.
#

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk

from pytrisk.locale    import _
from pytrisk.logger    import log


@dataclass
class MapImage:
    path  : Path
    image : Image.Image

@dataclass
class Point:
    x : int
    y : int


class GameCanvasView(tk.LabelFrame):
    def __init__(self, parent, controller, event_bus):
        super().__init__(parent, text=' ' + _('Map') + ' ')

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # Variables
        self._resize_job = None

        # Store the map files
        self._load_map_images()

        # GUI creation
        log.info('Creating canvas')
        self._create_canvas()


    # -- Private methods

    def _create_canvas(self):
        """Create canvas"""
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=2, pady=2)
        self._canvas = canvas

        # removing canvas bindings
        for button in [4, 5, 6, 7]:
            canvas.unbind(f'<Button-{button}>')
            canvas.unbind(f'<Shift-Button-{button}>')
        for key in ['Down', 'End', 'Home', 'Left', 'Next', 'Prior', 'Right', 'Up']:
            canvas.unbind(f'<Key-{key}>')
            canvas.unbind(f'<Control-Key-{key}>')

        # Adding canvas bindings
        canvas.bind('<Configure>', self._canvas_configure)
        canvas.bind('<Motion>',    self._canvas_motion)

    def _load_map_images(self):
        """Load map images (background and overlay) to be reused later
        on."""
        # Load map images
        log.info('Loading map images')
        bg, overlay = self.controller.sub.game.get_map_image_files()
        log.debug(f'Background: {bg}')
        log.debug(f'overlay: {overlay}')
        self._bg = MapImage(bg, Image.open(bg))
        self._overlay = MapImage(overlay, Image.open(overlay))

        # Store the image size for easier zoom in / out
        self._size = Point(self._bg.image.width, self._bg.image.height)
        log.debug(f'Image size: {self._size}')



    # -- GUI event handlers

    def _canvas_configure(self, event):
        """Event handler for canvas configure event - ie, when size changes.

        This also gets called when the canvas is first created."""
        # Cancel previous resize job
        if self._resize_job:
            self.after_cancel(self._resize_job)
        # Do not resize too often
        self._resize_job = self.after( 50,
            lambda: self._do_resize(event.width, event.height),
        )

    def _do_resize(self, width, height):
        # Get canvas size
        log.info(f'Canvas configure event: {width}x{height}')

        # Compute zoom
        self._zoom = min(width / self._size.x, height / self._size.y)
        log.debug(f'Zoom: {self._zoom}')

        # Resize background image
        neww = int(self._size.x * self._zoom)
        newh = int(self._size.y * self._zoom)
        resized = self._bg.image.resize(
            (neww, newh),
            Image.Resampling.LANCZOS,
        )
        self._background = ImageTk.PhotoImage(resized)

        # No need to resize overlay because:
        #   - It takes time
        #   - It is unneeded since it is not displayed
        #   - Greyscale is quite close from country to country and resizing
        #     will blur this to the point that it's no longer usable.
        # Therefore, just storing a zoom factor and using it will be enough
        # for greyscale.

        # Draw background on canvas
        canvas = self._canvas
        canvas.delete('background')
        canvas.create_image(0, 0, image=self._background, anchor=tk.NW, tag='background')
        canvas.lower('background', tk.ALL)


    def _canvas_motion(self, event):
        x = event.x
        y = event.y
        log.info(f'Canvas motion event: ({x}, {y})')


