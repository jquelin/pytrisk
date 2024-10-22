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

from pytrisk import config  # should go first

from pytrisk.locale import _
from pytrisk.logging import log
from pytrisk import maps
from pytrisk.gui.tkhelper import Action

from pathlib import Path
import PIL.Image
import PIL.ImageTk
from tkinter import *
from tkinter import ttk
from tkinter import font
from tktooltip import ToolTip
import types




class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.icons = {}

        self.title('pytrisk')
        self._build_actions()
        self._build_menubar()
        self._build_toolbar()


#        self.maps = sorted(maps.all_maps(), key=lambda x: x.title)
        return

        self.widgets = types.SimpleNamespace()
        self._btns   = types.SimpleNamespace()
        self._vbox = Gtk.VBox()

        self.widgets.accelgroup = Gtk.AccelGroup()
        self.add_accel_group(self.widgets.accelgroup)

        self._build_menubar()

        self._build_stack()
#        self._build_statusbar()



#        button = Gtk.Button(label="Click Here")
#        button.connect("clicked", self._on_button_clicked)
#        self._vbox.pack_start(button, expand=False, fill=True, padding=5)



        self.add(self._vbox)
        self.connect("destroy", Gtk.main_quit)
        self.set_size_request(400, 250)
#        self.maximize()
        self.show_all()



    # -- gui construction

    def _build_actions(self):
        self.actions = types.SimpleNamespace()

        action = Action(self, lambda ev: self.do_quit())
        action.add_binding('<Control-q>')
        self.actions.quit = action

        action = Action(self, lambda ev: self.do_close())
        action.add_binding('<Control-w>')
        action.disable()
        self.actions.close = action


    def _build_menubar(self):
        menubar = Menu(self)
        self.config(menu=menubar)

        # Menu: game
        mnu_game = Menu(menubar, tearoff=False)
        label = _('Close')
        mnu_game.add_command(
                label=label, accelerator='Ctrl+W',
                underline=0,
                command=self.do_close)
        self.actions.close.add_menu(mnu_game, label)
        mnu_game.add_separator()
        mnu_game.add_command(
                label=_('Quit'), accelerator='Ctrl+Q',
                underline=0,
                command=self.do_quit)
        menubar.add_cascade(label=_('Game'), underline=0, menu=mnu_game)


    def _build_toolbar(self):
        toolbar = Frame(self)
        self.toolbar = toolbar
        toolbar.pack(side=TOP)

        icon = self._get_icon_by_name('exit')
        but = Button(toolbar, image=icon, command=self.do_quit)
        but.pack(side=LEFT)
        tooltip = ToolTip(but, msg=_('Quit'))
        self.actions.quit.add_widget(but)

        icon = self._get_icon_by_name('close')
        but = Button(toolbar, image=icon, command=self.do_close)
        but.pack(side=LEFT)
        tooltip = ToolTip(but, msg=_('Close'))
        self.actions.close.add_widget(but)

        sep = ttk.Separator(toolbar, orient=VERTICAL)
        sep.pack(side=LEFT, fill='y', padx=4, pady=4)


    # -- gui callbacks

    def do_close(self):
        pass

    def do_quit(self):
        self.destroy()

    # -- old gtk


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

    def _xxxbuild_menubar(self):
        menubar = Gtk.MenuBar()
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
        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        self._vbox.pack_start(stack, expand=True, fill=True, padding=0)
        self._stack = stack
        self._build_stack_pane_new_game()
        self._build_stack_pane_game_running()

    def _build_stack_pane_game_running(self):
        self.canvas = Gtk.DrawingArea()
        self.canvas.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.canvas.connect('draw', self._on_canvas_draw)
        self.canvas.connect('size-allocate', self._on_canvas_resize)
        self.canvas.connect('motion-notify-event', self._on_canvas_mouse_motion)
        self.canvas.connect('button-press-event', self._on_canvas_clicked)

        self.orig_background = GdkPixbuf.Pixbuf.new_from_file(
            self.maps[0].background)
        self.cur_width  = 1
        self.cur_height = 1
        self._stack.add_titled(self.canvas, 'current_game', _("Current game"))

    def _build_stack_pane_new_game(self):
        vbox = Gtk.VBox()

        label = Gtk.Label()
        label.set_markup("<big>A fancy label</big>")
        vbox.pack_start(label, expand=False, fill=True, padding=5)

        flowbox = Gtk.FlowBox(homogeneous=True)
        vbox.pack_start(flowbox, expand=True, fill=True, padding=5)
        for m in self.maps:
            f = Gtk.Frame()
            evb = Gtk.EventBox()
            f.add(evb)
            evb.connect('button-press-event', self._on_new_game_map_selected, m)
            vb = Gtk.VBox()
            evb.add(vb)

            pixbuf = GdkPixbuf.Pixbuf.new_from_file(m.background)
            neww = pixbuf.get_width() / 8
            newh = pixbuf.get_height() / 8
            log.debug(f'resizing to {neww}x{newh}')
            pixbuf = pixbuf.scale_simple(neww, newh, GdkPixbuf.InterpType.BILINEAR)

            img = Gtk.Image.new_from_pixbuf(pixbuf)
            vb.pack_start(img, expand=False, fill=False, padding=5)

            l = Gtk.Label(label=m.title)
            vb.pack_start(l, expand=False, fill=False, padding=5)

            flowbox.insert(f, -1)


        button = Gtk.Button(label=_("Start game"))
        button.connect('clicked', self._on_btn_new_game_clicked)
        vbox.pack_start(button, expand=False, fill=True, padding=0)

        self._stack.add_titled(vbox, 'start_screen', _("New game"))

    def _build_statusbar(self):
        statusbar = Gtk.Statusbar()
        self._vbox.pack_start(statusbar, expand=False, fill=True, padding=0)
        self._statusbar = statusbar

    def _xxxbuild_toolbar(self):
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
        # check if icon is already loaded
        if name in self.icons:
            return self.icons[name]

        # icon not loaded, first compute path
        path = Path(Path(__file__).parent, 'icons', f'{name}.png').as_posix()
        log.debug(f'loading icon {path}')

        # load image and convert to RGBA if needed
        img = PIL.Image.open(path)
        if img.mode != 'RGBA':
            img = img.convert(mode="RGBA")

        # create the icon ready to be used by tk, store it and return it
        icon = PIL.ImageTk.PhotoImage(img)
        self.icons[name] = icon
        return icon


    # -- handlers

    def _on_new_game(self, widget):
#        config.set('foo.bar', 234)
        print(config.get('foo.bar', 123))

    def _on_btn_new_game_clicked(self, widget):
        print(config.get('foo.bar', 123))
#        self._statusbar.push(0, 'clicked')
#        ib = Gtk.InfoBar()
#        ib.add(Gtk.Label(label='foo'))
#        ib.set_show_close_button(True)
#        ib.show()
#        self._vbox.add(ib)
        self._stack.set_visible_child_name('current_game')

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

    def _on_new_game_map_selected(self, widget, ev, curmap):
        self.selected_map = curmap
        self.orig_background = GdkPixbuf.Pixbuf.new_from_file(
            curmap.background)
        self.cur_width  = 1
        self.cur_height = 1

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
