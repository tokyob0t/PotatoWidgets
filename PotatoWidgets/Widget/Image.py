from ..Imports import *
from ..Variable import Listener, Poll, Variable
from .Common import BasicProps


class Image(Gtk.Image, BasicProps):
    def __init__(
        self,
        path: Union[str, Variable, Listener, Poll, GdkPixbuf.Pixbuf, Gtk.IconInfo] = "",
        size: Union[list, int] = 20,
        hexpand=False,
        vexpand=False,
        halign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        valign: Literal["fill", "start", "center", "end", "baseline"] = "fill",
        visible=True,
        classname="",
        attributes: Callable = lambda self: self,
        css="",
    ) -> None:
        Gtk.Image.__init__(self)
        BasicProps.__init__(
            self,
            css=css,
            halign=halign,
            valign=valign,
            hexpand=hexpand,
            vexpand=vexpand,
            active=True,
            visible=visible,
            classname=classname,
            size=0,
        )

        self.__size = [0, 0]
        self.__path = ""

        self.set_size(size)
        if isinstance(path, (str, GdkPixbuf.Pixbuf, Gtk.IconInfo)):
            self.set_image(path)

        for key, value in locals().items():
            if key not in [
                "self",
                "halign",
                "valign",
                "hexpand",
                "vexpand",
                "visible",
                "active",
                "visible",
                "classname",
            ] and isinstance(value, (Listener, Poll, Variable)):
                callback = {
                    "path": self.set_image,
                    "size": self.set_size,
                }.get(key)

                if not callback:
                    continue

                self.bind(value, callback)
        attributes(self) if attributes else None

    def set_size(
        self,
        size: Union[int, List[int]],
        *,
        resize_method: GdkPixbuf.InterpType = GdkPixbuf.InterpType.BILINEAR,
    ) -> None:

        self.__size = [size, size] if isinstance(size, (int)) else size
        if self.__path:
            self.set_image(self.__path, resize_method=resize_method)

    def set_image(
        self,
        path: Union[GdkPixbuf.Pixbuf, str, Gtk.IconInfo],
        *,
        resize_method: GdkPixbuf.InterpType = GdkPixbuf.InterpType.BILINEAR,
    ) -> None:
        if not path:
            return

        if isinstance(path, (str)):
            self.__path = path
            self.set_image(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    filename=self.__path,
                    width=self.__size[0],
                    height=self.__size[1],
                    preserve_aspect_ratio=True,
                ),
                resize_method=resize_method,
            )

        elif isinstance(path, (Gtk.IconInfo)):

            def wrapper(_: Gtk.IconInfo, task: Gio.Task):
                self.set_image(path.load_icon_finish(task))

            return path.load_icon_async(callback=wrapper)

        elif isinstance(path, (GdkPixbuf.Pixbuf)):
            self.set_pixel_size(sum(self.__size) // 2)
            _w, _h = self.__preserve_aspect_ratio(path, *self.__size)
            path = path.scale_simple(_w, _h, resize_method)

            self.set_from_pixbuf(path)
            self.__path = path

            self.show()

    def __preserve_aspect_ratio(
        self, pixbuf: GdkPixbuf.Pixbuf, new_width: int, new_height: int
    ) -> Tuple[int, int]:
        original_width, original_height = pixbuf.get_width(), pixbuf.get_height()

        width_ratio = new_width / original_width
        height_ratio = new_height / original_height

        scale_factor = min(width_ratio, height_ratio)

        new_width_scaled = int(original_width * scale_factor)
        new_height_scaled = int(original_height * scale_factor)

        return new_width_scaled, new_height_scaled
