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
from pathlib import Path


class MainWindow(Gtk.Window):
    def __init__(self, controller):
        super().__init__(title="pytrisk")

        self.controller = controller
        self.widgets = types.SimpleNamespace()
        self._btns   = types.SimpleNamespace()
        self._vbox = Gtk.VBox()

        self.widgets.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(self.widgets.accelgroup)

        self._build_menubar()
        self._build_toolbar()

        self._build_stack()
        self._build_statusbar()



        button = Gtk.Button(label="Click Here")
        button.connect("clicked", self._on_button_clicked)
        self._vbox.pack_start(button, expand=False, fill=True, padding=5)

#        self.widgets.image = wimg
        self.canvas = Gtk.DrawingArea()
        self.canvas.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.canvas.connect('draw', self._on_canvas_draw)
        self.canvas.connect('size-allocate', self._on_canvas_resize)
        self.canvas.connect('motion-notify-event', self._on_canvas_mouse_motion)
        self._vbox.pack_start(self.canvas, expand=True, fill=True, padding=0)
        self.canvas.connect('button-press-event', self._on_canvas_clicked)

        self.orig_background = GdkPixbuf.Pixbuf.new_from_file(
            self.controller.map.background.as_posix())
        self.cur_width  = 1
        self.cur_height = 1


        self.add(self._vbox)
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
        self._vbox.pack_start(menubar, expand=False, fill=True, padding=0)
        self.widgets.menubar = menubar
        self.widgets.menu = {}


        menu_game = self._add_submenu(menubar, _('Game'))
        menuitems = (
            ('close', _('Close'),    self._on_menu_close,    'w'),
            (None,    '--',          None,                   None),
            ('quit',  _('Quit'),     self._on_menu_quit,     'q'),
        )
        for name, label, callback, hotkey in menuitems:
            menuitem = self._add_menuitem(menu_game, label, callback, hotkey)
            if name is not None:
                self.widgets.menu[f'game_{name}'] = menuitem

        self.widgets.menu['game_close'].set_sensitive(False)

    def _build_stack(self):
        pass

    def _build_statusbar(self):
        statusbar = Gtk.Statusbar()
        self._vbox.pack_start(statusbar, expand=False, fill=True, padding=0)
        self._statusbar = statusbar

    def _build_toolbar(self):
        toolbar = Gtk.Toolbar()

        icon_quit = Gtk.Image.new_from_file(self._get_icon_by_name('exit'))
        btn_quit  = Gtk.ToolButton.new(icon_quit, _('Quit'))
        btn_quit.connect('clicked', self._on_menu_quit)
        toolbar.insert(btn_quit, -1)
        btn_quit.add_accelerator('activate', self.widgets.accelgroup,
                    Gdk.keyval_from_name('q'),
                    Gdk.ModifierType.CONTROL_MASK,
                    Gtk.AccelFlags.VISIBLE)

        icon_close = Gtk.Image.new_from_file(self._get_icon_by_name('close'))
        btn_close  = Gtk.ToolButton.new(icon_close, _('Close'))
        toolbar.insert(btn_close, -1)
        btn_close.add_accelerator('activate', self.widgets.accelgroup,
                    Gdk.keyval_from_name('q'),
                    Gdk.ModifierType.CONTROL_MASK,
                    Gtk.AccelFlags.VISIBLE)
        btn_close.set_sensitive(False)
        self._btns.tb_close = btn_close

        toolbar.insert(Gtk.SeparatorToolItem(), -1)
        self._vbox.pack_start(toolbar, fill=True, expand=False, padding=0)

        lab = Gtk.Label(label=_('Game state:'))
        item = Gtk.ToolItem()
        item.add(lab)
        toolbar.insert(item, -1)
        item.set_sensitive(False)

        lab = Gtk.Label(label=_('place armies'))
        item = Gtk.ToolItem()
        item.add(lab)
        toolbar.insert(item, -1)
        item.set_sensitive(False)

        icon_redo = Gtk.Image.new_from_file(self._get_icon_by_name('redo'))
        btn_redo  = Gtk.ToolButton.new(icon_redo, _('undo'))
        btn_redo.set_tooltip_text(_('undo all'))
        toolbar.insert(btn_redo, -1)
        btn_redo.set_sensitive(False)
#        self._btns.tb_close = btn_close

        icon_next = Gtk.Image.new_from_file(self._get_icon_by_name('next'))
        btn_attack  = Gtk.ToolButton.new(icon_next, _('attack'))
        btn_attack.set_tooltip_text(_('ready for attack'))
        toolbar.insert(btn_attack, -1)
        btn_attack.set_sensitive(False)
#        self._btns.tb_close = btn_close

        lab = Gtk.Label(label=_('attack'))
        item = Gtk.ToolItem()
        item.add(lab)
        toolbar.insert(item, -1)
        item.set_sensitive(False)

        icon_next = Gtk.Image.new_from_file(self._get_icon_by_name('next'))
        btn_move  = Gtk.ToolButton.new(icon_next, _('consolidate'))
        btn_move.set_tooltip_text(_('attack done'))
        toolbar.insert(btn_move, -1)
        btn_move.set_sensitive(False)
#        self._btns.tb_close = btn_close

        lab = Gtk.Label(label=_('move armies'))
        item = Gtk.ToolItem()
        item.add(lab)
        toolbar.insert(item, -1)
        item.set_sensitive(False)

        icon_stop = Gtk.Image.new_from_file(self._get_icon_by_name('stop'))
        btn_stop  = Gtk.ToolButton.new(icon_stop, _('end turn'))
        btn_stop.set_tooltip_text(_('end turn'))
        toolbar.insert(btn_stop, -1)
        btn_stop.set_sensitive(False)




        self._toolbar = toolbar


    # --

    def _get_icon_by_name(self, name):
        return Path(Path(__file__).parent, 'gui', 'icons', f'{name}.png').as_posix()

    # -- handlers

    def _on_new_game(self, widget):
#        config.set('foo.bar', 234)
        print(config.get('foo.bar', 123))

    def _on_button_clicked(self, widget):
        print(config.get('foo.bar', 123))
        self._statusbar.push(0, 'clicked')
        ib = Gtk.InfoBar()
        ib.add(Gtk.Label(label='foo'))
#        ib.set_show_close_button(True)
        ib.show()
        self._vbox.add(ib)

    def _on_canvas_clicked(self, widget, ev):
        print(f'canvas clicked {ev.x}x{ev.y}')

    def _on_canvas_draw(self, widget, context):
        print(f'canvas redraw')
        Gdk.cairo_set_source_pixbuf(context, self.background, 0, 0)
        context.paint()

    def _on_canvas_mouse_motion(self, widget, ev):
        x, y = int(ev.x), int(ev.y)
#        pixel = self.greyscale.getpixel((x,y))
#        print(f'{x}.{y} {pixel}')
        print(f'canvas motion {x}.{y}')

    def _on_canvas_resize(self, widget, rect):
        neww = rect.width
        newh = rect.height
        if self.cur_width != neww or self.cur_height != newh:
            log.debug(f'canvas resize: from {self.cur_width}x{self.cur_height} to {neww}x{newh}')
            self.cur_width  = neww
            self.cur_height = newh
            self.background = self.orig_background.scale_simple(
                neww, newh,
                GdkPixbuf.InterpType.BILINEAR
            )

    def _on_menu_close(self, widget):
        log.info('close')

    def _on_menu_quit(self, widget):
        log.info('quit')
        self.destroy()


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
