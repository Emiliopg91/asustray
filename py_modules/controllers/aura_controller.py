from py_modules.services.asus_service import AsusService
from py_modules.models.aura_level import AuraLevel
from py_modules.models.aura_mode import AuraMode
from py_modules.utils.on_widget_active_strict import on_widget_active_strict
from py_modules.utils.di import inject

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk

@inject
class AuraController():
    asus_service: AsusService
    menu_items_mode = [] 
    menu_items_level = [] 
    last_active_mode = None
    
    @property
    def active_mode(self):
        return self.asus_service.get_aura_mode()

    @on_widget_active_strict
    def on_mode_activation(self, widget: Gtk.MenuItem):
        mode = AuraMode[widget.get_label().replace(" ", "_").upper()]
        self.asus_service.set_aura_mode(mode)
    
    @property
    def active_level(self):
        return self.asus_service.get_aura_level()

    @on_widget_active_strict
    def on_level_activation(self, widget: Gtk.MenuItem):
        level = AuraLevel[widget.get_label().upper()]
        self.asus_service.set_aura_level(level)

    def attach(self, menu: Gtk.Menu) -> None:
        title = Gtk.MenuItem.new_with_label("AuraSync")
        title.set_sensitive(False)
        menu.append(title)

        group = []
        submenu = Gtk.Menu()
        for mode in AuraMode:
            entry = Gtk.RadioMenuItem.new_with_label(group, label=mode.name.capitalize().replace("_", " "))
            entry.set_active(mode == self.active_mode)
            entry.connect("activate", self.on_mode_activation)
            self.menu_items_mode.append(entry)
            submenu.append(entry)
            group = entry.get_group()

        item = Gtk.MenuItem()
        item.set_label("Mode")
        item.set_submenu(submenu)
        menu.append(item)

        group = []
        submenu = Gtk.Menu()
        for level in AuraLevel:
            entry = Gtk.RadioMenuItem.new_with_label(group, label=level.name.capitalize())
            entry.set_active(level == self.active_level)
            entry.connect("activate", self.on_level_activation)
            self.menu_items_level.append(entry)
            submenu.append(entry)
            group = entry.get_group()

        item2 = Gtk.MenuItem()
        item2.set_label("Brightness")
        item2.set_submenu(submenu)
        menu.append(item2)


        menu.append(Gtk.SeparatorMenuItem())

    
    