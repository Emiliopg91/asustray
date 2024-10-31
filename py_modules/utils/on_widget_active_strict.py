import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk  # noqa: E402

def on_widget_active_strict(callback) -> None:
    """Decorator to inject a check for widget activation, calls the function only
    when the widget is active"""

    def inner(self, widget: Gtk.MenuItem):
        # Return if the widget is not actually active
        if not widget.get_active():
            return
        callback(self, widget)

    return inner