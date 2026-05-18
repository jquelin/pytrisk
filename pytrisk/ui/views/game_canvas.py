# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk

from pytrisk.config    import config
from pytrisk.locale    import _
from pytrisk.logger    import log
import pytrisk.settings as settings


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
        log.info('Creating canvas')

        # Subscribe to events & store the controller for later use.
        event_bus.subscribe(self)
        self.controller = controller
        self.event_bus  = event_bus

        # Variables
        self._resize_job = None
        self._topleft    = Point(0, 0)  # top left corner of background
        self._zoom       = Point(1, 1)

        # Store the map files
        self._load_map_images()

        # GUI creation
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
        bg, overlay = self.controller.get_map_image_files()
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
        self._resize_job = self.after(settings.gui.wait_redraw,
            lambda: self._canvas_configure_real(event.width, event.height),
        )

    def _canvas_configure_real(self, width, height):
        # Get canvas size
        log.info(f'Canvas configure event: {width}x{height}')
        self._resize_job = None

        # Compute zoom
        self._zoom = Point(width / self._size.x, height / self._size.y)
        if config.get('gui.aspect.keep_ratio'):
            log.debug('Keeping aspect ratio')
            minzoom = min(self._zoom.x, self._zoom.y)
            self._zoom = Point(minzoom, minzoom)
        log.debug(f'Zoom: {self._zoom}')

        # Resize background image
        neww = int(self._size.x * self._zoom.x)
        newh = int(self._size.y * self._zoom.y)
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
        # center background
        self._topleft = Point(
            (width - neww) // 2,
            (height - newh) // 2
        )
        topleft = self._topleft
        canvas.create_image(topleft.x, topleft.y, image=self._background, anchor=tk.NW, tag='background')
        canvas.lower('background', tk.ALL)


    def _canvas_motion(self, event):
        x = event.x
        y = event.y
        log.debug(f'Canvas motion event: ({x}, {y})')


    # -- Public methods: event bus handlers

    def on_aspect_ratio_changed(self):
        self._canvas_configure_real(self.winfo_width(), self.winfo_height())
