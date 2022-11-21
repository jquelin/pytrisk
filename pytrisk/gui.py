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

from pytrisk.locale import _
from pytrisk.logging import log
from pytrisk import config

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import GLib
from gi.repository import Gtk
import types
from PIL import Image

class Canvas(Gtk.ScrolledWindow):
    def __init__(self, path):
        super().__init__()

        evbox = Gtk.EventBox()
        self.image = Gtk.Image()
        evbox.add(self.image)
        self.add(evbox)

        self.loader = GdkPixbuf.PixbufLoader()
        with  open(path, 'rb') as f:
            imgdata = f.read()
        self.loader.write(imgdata)
        self.loader.close()

        self.original = self.loader.get_pixbuf()
        self.image.set_from_pixbuf(self.original)

        self.origw  = self.original.get_width()
        self.origh = self.original.get_height()

        self.curw = 1
        self.curh = 1

        self.connect('size-allocate', self.on_resize)



    def on_resize(self, widget, rect):
        neww = rect.width
        newh = rect.height
        if self.curw != neww or self.curh != newh:
            log.info(f'newsize {neww}x{newh}')
            self.curw = neww
            self.curh = newh
            self.pixbuf = self.original.scale_simple(
                neww, newh,
                GdkPixbuf.InterpType.BILINEAR
            )
            self.image.set_from_pixbuf(self.pixbuf)



class MainWindow(Gtk.Window):
    def __init__(self, controller):
        super().__init__(title="pytrisk")

        self.controller = controller
        self.widgets = types.SimpleNamespace()
        self.widgets.vbox = Gtk.VBox()

        self.widgets.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(self.widgets.accelgroup)

        self._build_menubar()




        button = Gtk.Button(label="Click Here")
        button.connect("clicked", self._on_button_clicked)
        button.add_accelerator("activate", 
                            self.widgets.accelgroup,
                            Gdk.keyval_from_name("o"),
                            Gdk.ModifierType.CONTROL_MASK,
                            Gtk.AccelFlags.VISIBLE)
        self.widgets.vbox.pack_start(button, expand=False, fill=True, padding=5)
#        grid.attach(button, 0, 1, 1, 1)
#        label = Gtk.Label(label="Hello World", angle=25,
#                halign=Gtk.Align.END)
#        vbox.add(label)
#        self.vbox = vbox

#        area = Gtk.DrawingArea()
#        area.connect("draw", self.expose)
#        area.show()
#        self.widgets.vbox.add(area)

#        submenu_file = Gtk.MenuButton(label='File')
#        menuitem_open = Gtk.MenuItem(label="Open")
#        submenu_file.append(menuitem_open)
#        menuitem_open.connect('activate', self.on_menu_open)
#
#        menu_open.add_accelerator("activate", 
#                            accelgroup,
#                            Gdk.keyval_from_name("o"),
#                            Gdk.ModifierType.CONTROL_MASK,
#                            Gtk.AccelFlags.VISIBLE)
#        menu_quit.add_accelerator("activate", 
#                            accelgroup,
#                            Gdk.keyval_from_name("q"),
#                            Gdk.ModifierType.CONTROL_MASK,
#                            Gtk.AccelFlags.VISIBLE)


#        im = Image.open(self.controller.map.background)
#        data = im.tobytes()
#        w, h = im.size
#        data = GLib.Bytes.new(data)
#        self.pixbuf = GdkPixbuf.Pixbuf.new_from_bytes(data, GdkPixbuf.Colorspace.RGB,
#            False, 8, w, h, w * 3)
#        self.image = im
#
#        wimg = Gtk.Image().new_from_pixbuf(self.pixbuf)
#        self.widgets.vbox.pack_start(wimg, expand=True, fill=True, padding=0)
#        self.temp_height = 0
#        self.temp_width = 0
#        wimg.connect('size-allocate', self.on_resize)
#        wimg.connect('configure-event', self.on_resize)

#        self.widgets.image = wimg
        self.canvas = Canvas(self.controller.map.background)
        self.widgets.vbox.pack_start(self.canvas, expand=True, fill=True, padding=0)
        self.canvas.connect('button-press-event', self._on_canvas_clicked)


        self.add(self.widgets.vbox)
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(400, 250)
#        self.maximize()
        self.show_all()


    #
    def run(self):
        Gtk.main()

    # -- gui construction

    def _add_menuitem(self, submenu, label, callback, hotkey):
        if label == '--':
            menuitem = Gtk.SeparatorMenuItem()
        else:
            menuitem = Gtk.MenuItem(label=label)
            menuitem.connect('activate', callback)
            menuitem.add_accelerator('activate', self.widgets.accelgroup,
                    Gdk.keyval_from_name(hotkey),
                    Gdk.ModifierType.CONTROL_MASK,
                    Gtk.AccelFlags.VISIBLE)
        submenu.append(menuitem)
        return menuitem

    def _add_submenu(self, menubar, label):
        menuitem = Gtk.MenuItem(label=label)
        menubar.append(menuitem)
        submenu = Gtk.Menu()
        menuitem.set_submenu(submenu)
        return submenu

    def _build_menubar(self):
        menubar = Gtk.MenuBar()
#        menubar.set_hexpand(True)
        self.widgets.vbox.pack_start(menubar, expand=False, fill=True, padding=0)
        self.widgets.menubar = menubar
        self.widgets.menu = {}

        menus = [
            [_('Game'), [
                [_('New game')],
                [_('Close')],
                ['--'],
                [_('Quit')],
            ]],
            [_('View'), [
            ]]
        ]

        menu_game = self._add_submenu(menubar, _('Game'))
        menuitems = (
            ('new',   _('New game'), self._on_new_game, 'n'),
            ('close', _('Close'),    self._on_close,    'w'),
            (None,    '--',          None,              None),
            ('quit',  _('Quit'),     self._on_quit,     'q'),
        )
        for name, label, callback, hotkey in menuitems:
            menuitem = self._add_menuitem(menu_game, label, callback, hotkey)
            if name is not None:
                self.widgets.menu[f'game_{name}'] = menuitem

        self.widgets.menu['game_close'].set_sensitive(False)


    # -- handlers

    def _on_close(self, widget):
        print('close')

    def _on_new_game(self, widget):
#        config.set('foo.bar', 234)
        print(config.get('foo.bar', 123))

    def _on_quit(self, widget):
        Gtk.main_quit()

    def _on_button_clicked(self, widget):
        print(config.get('foo.bar', 123))

    def _on_canvas_clicked(self, widget, ev):
        print(f'canvas clicked {ev.x}x{ev.y}')

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
