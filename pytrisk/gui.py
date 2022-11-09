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

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gdk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="pytrisk")
#        vbox = Gtk.VBox()

        grid = Gtk.Grid()
        accelgroup = Gtk.AccelGroup()
        self.add_accel_group(accelgroup)
        self.add(grid)

        menubar = Gtk.MenuBar()
        menubar.set_hexpand(True)
        grid.attach(menubar, 0, 0, 1, 1)

#        menu1 = Gtk.Menu()
#        file = Gtk.MenuItem("_File")
#        file.set_submenu(menu1)
#        item1 = Gtk.MenuItem("New")
#        item2 = Gtk.MenuItem("Open")
#        menu1.append(item1)
#        menu1.append(item2)
#        menubar.append(file)
#
        menu_file = self.add_submenu(menubar, 'File')
        menu_open = self.add_menuitem(menu_file, 'Open')
        menu_open.connect('activate', self.on_menu_open)
        menu_open.set_sensitive(False)

        menu_quit = self.add_menuitem(menu_file, 'Quit')
        menu_quit.connect('activate', self.on_menu_quit)

        menu_edit = self.add_submenu(menubar, 'Edit')
#
#        menubar = Gtk.MenuBar()
#        menubar.show()
#        menubar.set_hexpand(True)
#        vbox.add(menubar)


        button = Gtk.Button(label="Click Here")
        button.connect("clicked", self.on_button_clicked)
        button.add_accelerator("activate", 
                            accelgroup,
                            Gdk.keyval_from_name("o"),
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.VISIBLE)
        grid.attach(button, 0, 1, 1, 1)
#        label = Gtk.Label(label="Hello World", angle=25,
#                halign=Gtk.Align.END)
#        vbox.add(label)
#        self.add(vbox)
#        self.vbox = vbox


#        submenu_file = Gtk.MenuButton(label='File')
#        menuitem_open = Gtk.MenuItem(label="Open")
#        submenu_file.append(menuitem_open)
#        menuitem_open.connect('activate', self.on_menu_open)
#
        menu_open.add_accelerator("activate", 
                            accelgroup,
                            Gdk.keyval_from_name("o"),
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.VISIBLE)
        menu_quit.add_accelerator("activate", 
                            accelgroup,
                            Gdk.keyval_from_name("q"),
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.VISIBLE)



    def add_submenu(self, menubar, label):
        menuitem = Gtk.MenuItem(label=label)
        menubar.append(menuitem)
        submenu = Gtk.Menu()
        menuitem.set_submenu(submenu)
        return submenu

    def add_menuitem(self, submenu, label):
        menuitem = Gtk.MenuItem(label=label)
        submenu.append(menuitem)
        return menuitem

    def on_menu_open(self, widget):
        print("add file open dialog")

    def on_menu_quit(self, widget):
        Gtk.main_quit()

    def on_button_clicked(self, widget):
        print('click')
#        ib = Gtk.InfoBar()
#        l = Gtk.Label(label='ready?')
#        ib.add(l)
#        b = Gtk.Button(label='ok')
#        b.show()
#        ib.add(b)
#        ib.show()
#        l.show()
#        self.vbox.add(ib)
#        l2 = Gtk.AccelLabel(label='go')
#        l2.set_accel('Ctrl+G')
#        l2.show()
#        self.vbox.add(l2)
#        self.vbox.add(l)
#        self.vbox.redraw()

def run():
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
