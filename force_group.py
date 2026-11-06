import sublime
import sublime_plugin

SETTINGS_FILE = "ForceGroup.sublime-settings"


def get_settings():
    return sublime.load_settings(SETTINGS_FILE)


def target_group_index(window):
    """Resolve the configured (1-based) group number to a valid 0-based index."""
    configured = get_settings().get("group", 1)
    try:
        configured = int(configured)
    except (TypeError, ValueError):
        configured = 1
    # Clamp: if the layout has fewer groups than configured, use the last one.
    return max(0, min(configured - 1, window.num_groups() - 1))


class ForceGroupListener(sublime_plugin.EventListener):
    def __init__(self):
        self._moving = False
        # Views that were already placed once (only used with allow_manual_move)
        self._placed = set()

    def on_activated(self, view):
        settings = get_settings()
        if self._moving or not settings.get("enabled", True):
            return
        if settings.get("allow_manual_move", True) and view.id() in self._placed:
            return
        sublime.set_timeout(lambda: self.move_to_target_group(view), 10)

    def on_close(self, view):
        self._placed.discard(view.id())

    def move_to_target_group(self, view):
        if self._moving or not view.is_valid():
            return

        window = view.window()
        if window is None or window.num_groups() < 2:
            return

        # Skip untitled buffers, widgets (find panel, etc.) and transient previews
        file_name = view.file_name()
        if file_name is None or view.settings().get("is_widget"):
            return

        # Leave settings files alone so "Edit Settings" can keep its side-by-side layout
        if file_name.endswith(".sublime-settings"):
            return

        self._placed.add(view.id())

        target = target_group_index(window)
        group, _ = window.get_view_index(view)
        if group < 0 or group == target:
            return

        self._moving = True
        try:
            index = len(window.views_in_group(target))
            window.set_view_index(view, target, index)
        except Exception:
            self._moving = False
            raise

        sublime.set_timeout(
            lambda: self.focus_in_target_group(window, view, target), 0
        )

    def focus_in_target_group(self, window, view, target):
        try:
            if view.is_valid() and view.window() is not None:
                window.focus_view(view)
                window.focus_group(target)
        finally:
            sublime.set_timeout(self.release, 50)

    def release(self):
        self._moving = False


class ForceGroupToggleCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        settings = get_settings()
        enabled = not settings.get("enabled", True)
        settings.set("enabled", enabled)
        sublime.save_settings(SETTINGS_FILE)
        sublime.status_message("Force Group: %s" % ("on" if enabled else "off"))
