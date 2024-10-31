from py_modules.services.asus_service import AsusService
from py_modules.models.throttle_thermal_policy import ThrottleThermalPolicy
from py_modules.utils.on_widget_active_strict import on_widget_active_strict
from py_modules.utils.di import inject

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, GLib

@inject
class ProfileController:
    asus_service:AsusService
    menu_items = [] 
    last_active = None

    @property
    def active_item(self) -> ThrottleThermalPolicy:
        return self.asus_service.get_throttle_thermal_policy()

    @on_widget_active_strict
    def on_activation(self, widget: Gtk.MenuItem):
        policy = ThrottleThermalPolicy[widget.get_label().upper()]
        self.asus_service.set_throttle_thermal_policy(policy)

    def attach(self, menu: Gtk.Menu) -> None:
        title = Gtk.MenuItem.new_with_label("Performance profile")
        title.set_sensitive(False)
        menu.append(title)

        group = []
        for item in [policy for policy in ThrottleThermalPolicy]:
            menu_item = Gtk.RadioMenuItem.new_with_label(
                group=group,
                label=item.name.capitalize(),
            )
            menu_item.set_active(item == self.active_item)

            menu_item.connect("activate", self.on_activation)
            group = menu_item.get_group()
            menu.append(menu_item)
            self.menu_items.append(menu_item)

        menu.append(Gtk.SeparatorMenuItem())


    def update_menu_items(self) -> bool:
        active_item = self.active_item
        for menu_item in self.menu_items:
            active = menu_item.get_label() == active_item.name.capitalize()
            if(active):
                if(self.last_active is None or self.last_active != menu_item):
                    self.last_active = menu_item
                    menu_item.set_active(active)
        return True
