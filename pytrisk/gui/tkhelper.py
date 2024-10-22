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

import tkinter

class Action:
    """Action abstraction for Tk

    Menu entries are often also available in toolbars or other widgets.
    And sometimes, we want to enable or disable a given action, and this
    means having to update everywhere this action is allowed.

    This class helps managing actions in a Tk GUI: just create a new
    object, associate some widgets and bindings with widget_add() and
    then de/activate the whole action at once with enable() or
    disable().
    """

    # -- constructor
    def __init__(self, window, callback):
        """Parameters

        window:
            The window holding the widgets being part of the action
            object. It is needed to create the shortcut bindings.
            Required, no default.

        callback:
            the callback associated to the action. It is needed to
            create the shortcut bindings. Required, no default.
        """


        self.widgets    = set()
        self.bindings   = set()
        self.is_enabled = True
        self.window     = window
        self.callback   = callback
        self.menu       = None
        self.menu_item  = None


    # -- adding dependent items

    def add_menu(self, menu, menu_item):
        """Add a menu item to the object.

        Parameters

        menu:
            The menu containing the menu item.
        menu_item:
            The label of the menu item.
        """
        self.menu = menu
        self.menu_item = menu_item
        state = tkinter.NORMAL if self.is_enabled else tkinter.DISABLED
        self.menu.entryconfig(self.menu_item, state=state)

    def add_widget(self, widget):
        """Add a widget to the object.

        Parameters

        widget:
            The new widget to add to the object.
        """
        self.widgets.add(widget)
        state = tkinter.NORMAL if self.is_enabled else tkinter.DISABLED
        widget.configure(state=state)

    def add_binding(self, binding):
        """Add a binding to the object.

        Parameters

        binding:
            The new binding to add to the object.
        """
        self.bindings.add(binding)
        callback = self.callback if self.is_enabled else None
        self.window.bind(binding, callback)


    # -- enabling / disabling

    def enable(self):
        """Enable the action object

        Activate all associated widgets and shortcuts.
        """
        self.is_enabled = True
        for widget in self.widgets:
            widget.configure(state=tkinter.NORMAL)
        for binding in self.bindings:
            self.window.bind(binding, self.callback)
        if self.menu is not None:
            self.menu.entryconfig(self.menu_item, state=tkinter.NORMAL)

    def disable(self):
        """Disable the action object

        De-activate all associated widgets and shortcuts.
        """
        self.is_enabled = False
        for widget in self.widgets:
            widget.configure(state=tkinter.DISABLED)
        for binding in self.bindings:
            self.window.bind(binding, None)
        if self.menu is not None:
            self.menu.entryconfig(self.menu_item, state=tkinter.DISABLED)


