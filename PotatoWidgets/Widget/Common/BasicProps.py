from ...Imports import *
from ...Variable import Listener, Poll, Variable


class BasicProps(Gtk.Widget):
    def __init__(
        self,
        halign: str,
        valign: str,
        hexpand: bool,
        vexpand: bool,
        active: bool,
        classname: str,
        # tooltip,
        css: str,
        visible: bool = True,
        size: Union[int, list] = 0,
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
        self.set_size(size)
        self.rand_classname = ""

        if css:
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
        if size:
            if isinstance(size, int):
                self.set_size_request(size, size)
            elif isinstance(size, list):
                if len(size) == 2:
                    self.set_size_request(size[0], size[1])
                elif len(size) == 1:
                    self.set_size_request(size[0], size[0])

    def set_halign(self, param):
        super().set_halign(self.__clasif_align(str(param)))

    def set_valign(self, param):
        super().set_valign(self.__clasif_align(str(param)))

    def set_active(self, param):
        if param != None and param:
            super().set_sensitive(param)

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

    def _add_randclassname(self):
        if not self.rand_classname:
            context = self.get_style_context()

            self.rand_classname = (
                self.get_name().replace("+", "_") + "_" + str(randint(1111, 9999))
            )
            context.add_class(self.rand_classname)

    def set_css(self, css_rules):
        self._add_randclassname()

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
            variable.bind(callback)

    def __clasif_args(self, variable, callback):
        arg_num = callback.__code__.co_argcount
        arg_tuple = callback.__code__.co_varnames[:arg_num]

        if arg_num == 2:
            variable.connect(
                "valuechanged",
                lambda out: GLib.idle_add(
                    lambda: callback(self=self, out=out.get_value())
                ),
            )

        elif arg_num == 1:
            if "out" in arg_tuple:
                variable.connect(
                    "valuechanged",
                    lambda out: GLib.idle_add(lambda: callback(out=out.get_value())),
                )
            elif "self" in arg_tuple:
                variable.connect(
                    "valuechanged",
                    lambda _: GLib.idle_add(lambda: callback(self=self)),
                )
            else:
                variable.connect(
                    "valuechanged",
                    lambda out: GLib.idle_add(lambda: callback(out.get_value())),
                )
        else:
            variable.connect(
                "valuechanged",
                lambda _: GLib.idle_add(callback),
            )
