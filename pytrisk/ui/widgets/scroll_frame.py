# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2026 Jerome Quelin
# This file is part of pytrisk.

import platform
import tkinter as tk
from tkinter import ttk
from tkinter import ALL, BOTH, LEFT, NW, RIGHT, VERTICAL, Y

class ScrolledFrame(tk.Frame):
    """A scrollable frame that can be treated like any other frame.  The inner
    frame can be accessed through the 'inner' attribute.  To create widgets in
    the inner frame, use the 'inner' attribute as the parent.

    For example:
        scroll_frame = ScrolledFrame(parent)
        inner = scroll_frame.inner
        label = tk.Label(inner, text="This is a scrollable frame")
        label.pack()
    """

    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        # Create a canvas and place a frame on it, then use the canvas to
        # scroll the frame when needed.
        # The frame will hold the child widgets, and the canvas will provide a
        # scrollable view of it.
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.inner  = tk.Frame(self.canvas)
        self.vsb    = tk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=Y)
        self.canvas_window = self.canvas.create_window(
            (4,4), window=self.inner, anchor=NW)

        # Bind events to make sure the scrollable region is always large enough
        # to encompass the inner frame
        self.inner.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Bind mouse wheel events to scroll the canvas when the cursor is over
        # the inner frame.
        self.inner.bind('<Enter>', self._on_enter)
        self.inner.bind('<Leave>', self._on_leave)

        # Perform an initial stretch on render, otherwise the scroll region has
        # a tiny border until the first resize.
        self._on_frame_configure(None)


    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        # When the inner frame changes size, alter the scroll region
        # respectively.
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
        self.canvas.configure(width=self.inner.winfo_reqwidth())


    def _on_canvas_configure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        # Whenever the size of the canvas changes, alter the window region
        # respectively.
        self.canvas.itemconfig(self.canvas_window, width = canvas_width)


    def _on_mouse_wheel(self, event):
        """Scroll the canvas when the mouse wheel is moved.  This is a bit
        tricky because the event is different on different platforms, so we
        have to handle it differently depending on the platform."""
        # cross platform scroll wheel event
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(int(-1* (event.delta/120)), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(int(-1 * event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll( -1, "units" )
            elif event.num == 5:
                self.canvas.yview_scroll( 1, "units" )


    def _on_enter(self, event):
        """Bind mouse wheel events to scroll the canvas when the cursor is over
        the inner frame."""
        # Bind wheel events when the cursor enters the control.
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self._on_mouse_wheel)
            self.canvas.bind_all("<Button-5>", self._on_mouse_wheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)


    def _on_leave(self, event):
        """Unbind mouse wheel events to stop scrolling the canvas when the
        cursor leaves the inner frame."""
        # Unbind wheel events when the cursor leaves the control.
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")
