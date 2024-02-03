from ...__Import import *
from ...Variable import Listener, Poll, Variable


class BasicProps(Gtk.Widget):
    def __init__(
        self,
        halign,
        valign,
        hexpand,
        vexpand,
        active,
        visible,
        classname,
        # tooltip,
        css,
        size=0 or [0],
    ):
        Gtk.Widget.__init__(self)
        self._default_classnames = self.get_style_context().list_classes()
        self.set_hexpand(True if hexpand else False)
        self.set_vexpand(True if vexpand else False)
        self.set_halign(halign)
        self.set_valign(valign)
        self.set_visible(visible)
        self.set_active(active)
        self.set_classname(classname)
        self.__clasif_size(size)
        self.rand_classname = (
            self.get_name().replace("+", "_") + "_" + str(randint(1111, 9999))
            if css
            else ""
        )

        self.set_classname(self.rand_classname) if self.rand_classname else None
        self.set_css(css)

        for key, value in locals().items():
            callback = {
                "halign": self.set_halign,
                "valign": self.set_valign,
                "hexpand": self.set_hexpand,
                "vexpand": self.set_vexpand,
                "active": self.set_sensitive,
                "visible": self.set_visible,
                "size": self.set_size,
                "classname": self.set_classname,
            }.get(key)

            self.bind(value, callback) if callback else None

    def set_size(self, size):
        self.__clasif_size(size)

    def set_halign(self, param):
        super().set_halign(self.__clasif_align(str(param)))

    def set_valign(self, param):
        super().set_valign(self.__clasif_align(str(param)))

    def set_active(self, param):
        if param != None and param:
            super().set_sensitive(param)

    def __clasif_size(self, size):
        if isinstance(size, int):
            self.set_size_request(size, size)
        elif isinstance(size, list):
            if len(size) == 2:
                self.set_size_request(size[0], size[1])
            elif len(size) == 1:
                self.set_size_request(size[0], size[0])

    def __clasif_align(self, param):
        dict = {
            "fill": Gtk.Align.FILL,
            "start": Gtk.Align.START,
            "end": Gtk.Align.END,
            "center": Gtk.Align.CENTER,
            "baseline": Gtk.Align.BASELINE,
        }
        return dict.get(param.lower(), Gtk.Align.FILL)

    def set_classname(self, classname):
        if isinstance(classname, (str)):
            context = self.get_style_context()
            [
                context.remove_class(i)
                for i in context.list_classes()
                if i not in self._default_classnames
            ]

            for j in classname.split(" "):
                if j != " ":
                    context.add_class(j)

        elif isinstance(classname, (list)):
            for i in classname:
                if isinstance(i, (Listener, Variable, Poll)):
                    pass

    def set_css(self, css_rules):
        if css_rules and self.rand_classname:
            context = self.get_style_context()

            try:
                css_style = f".{self.rand_classname} {{{css_rules}}}"

                provider = Gtk.CssProvider()
                provider.load_from_data(css_style.encode())

                context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

            except Exception as e:
                print(e)

    def bind(self, variable, callback):
        if isinstance(variable, (Listener, Variable, Poll)):
            variable.connect(
                "valuechanged",
                lambda out: GLib.idle_add(lambda: callback(out.get_value())),
            )
