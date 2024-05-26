from ... import Widget
from ..._Logger import Logger
from ...Env import DIR_CACHE_TRAY
from ...Imports import *
from ...Methods import lookup_icon
from ..Service import BaseGObjectClass, Service

org_kde_StatusNotifier_xml = """
<?xml version="1.0" encoding="UTF-8"?>
<node>
   <interface name="org.kde.StatusNotifierWatcher">
      <annotation name="org.gtk.GDBus.C.Name" value="Watcher" />
      <method name="RegisterStatusNotifierItem">
         <annotation name="org.gtk.GDBus.C.Name" value="RegisterItem" />
         <arg name="Service" type="s" direction="in" />
      </method>
      <method name="RegisterStatusNotifierHost">
         <annotation name="org.gtk.GDBus.C.Name" value="RegisterHost" />
         <arg name="Service" type="s" direction="in" />
     </method>
      <property name="RegisteredStatusNotifierItems" type="as" access="read">
         <annotation name="org.gtk.GDBus.C.Name" value="RegisteredItems" />
         <annotation name="org.qtproject.QtDBus.QtTypeName.Out0" value="QStringList" />
      </property>
      <property name="IsStatusNotifierHostRegistered" type="b" access="read">
         <annotation name="org.gtk.GDBus.C.Name" value="IsHostRegistered" />
      </property>
      <property name="ProtocolVersion" type="i" access="read" />
      <signal name="StatusNotifierItemRegistered">
         <annotation name="org.gtk.GDBus.C.Name" value="ItemRegistered" />
         <arg name="Service" type="s" direction="out" />
      </signal>
      <signal name="StatusNotifierItemUnregistered">
         <annotation name="org.gtk.GDBus.C.Name" value="ItemUnregistered" />
         <arg name="Service" type="s" direction="out" />
      </signal>
      <signal name="StatusNotifierHostRegistered">
         <annotation name="org.gtk.GDBus.C.Name" value="HostRegistered" />
      </signal>
      <signal name="StatusNotifierHostUnregistered">
         <annotation name="org.gtk.GDBus.C.Name" value="HostUnregistered" />
      </signal>
   </interface>

   <interface name="org.kde.StatusNotifierItem">
      <property name="Category" type="s" access="read" />
      <property name="Id" type="s" access="read" />
      <property name="Title" type="s" access="read" />
      <property name="Status" type="s" access="read" />
      <property name="WindowId" type="i" access="read" />
      <property name="IconThemePath" type="s" access="read" />
      <property name="ItemIsMenu" type="b" access="read" />
      <property name="Menu" type="o" access="read" />
      <property name="IconName" type="s" access="read" />
      <property name="IconPixmap" type="a(iiay)" access="read">
         <annotation name="OrgQtprojectQtDBusQtTypeName" value="KDbusImageVector" />
      </property>
      <property name="AttentionIconName" type="s" access="read" />
      <property name="AttentionIconPixmap" type="a(iiay)" access="read">
         <annotation name="OrgQtprojectQtDBusQtTypeName" value="KDbusImageVector" />
      </property>
      <property name="ToolTip" type="(sa(iiay)ss)" access="read">
         <annotation name="OrgQtprojectQtDBusQtTypeName" value="KDbusToolTipStruct" />
      </property>
      <method name="ContextMenu">
         <arg name="X" type="i" direction="in" />
         <arg name="Y" type="i" direction="in" />
      </method>
      <method name="Activate">
         <arg name="X" type="i" direction="in" />
         <arg name="Y" type="i" direction="in" />
      </method>
      <method name="SecondaryActivate">
         <arg name="X" type="i" direction="in" />
         <arg name="Y" type="i" direction="in" />
      </method>
      <method name="Scroll">
         <arg name="Delta" type="i" direction="in" />
         <arg name="Orientation" type="s" direction="in" />
      </method>
      <signal name="NewTitle" />
      <signal name="NewIcon" />
      <signal name="NewAttentionIcon" />
      <signal name="NewOverlayIcon" />
      <signal name="NewToolTip" />
      <signal name="NewStatus">
         <arg name="Status" type="s" />
      </signal>
   </interface>
</node>
"""


NodeInfo = Gio.DBusNodeInfo.new_for_xml(org_kde_StatusNotifier_xml)


class _TrayItemMenu(Widget.Menu):
    def __init__(
        self,
        Connection: Gio.DBusConnection,
        Sender: str,
        Path: str,
        MenuPath: str,
        MenuData: tuple,
    ):
        super().__init__()
        self._connection: Gio.DBusConnection = Connection
        self._children: List[Gtk.MenuItem] = []
        self._sender: str = Sender
        self._path: str = Path
        self._menu_path: str = MenuPath
        self._menu_data: tuple = MenuData

        self.MakeItself()

    def MakeItself(self):
        self._menu_data = self._connection.call_sync(
            self._sender,
            self._menu_path,
            "com.canonical.dbusmenu",
            "GetLayout",
            GLib.Variant("(iias)", (0, -1, [])),
            GLib.VariantType("(u(ia{sv}av))"),
            Gio.DBusCallFlags.NONE,
            -1,
        ).unpack()

        for children in self.get_children():
            children.destroy()

        for i in self._menu_data:
            if isinstance(i, tuple) and i[1]["children-display"] == "submenu":
                self.MakeMenu(i[2], self)

    def MakeMenu(self, item: list, menu: Widget.Menu):
        # ChildrenItems: Widget.MenuItem = []
        ID: int
        DICT: dict
        CHILDRENS: list

        for i in item:
            ID, DICT, CHILDRENS = i

            if DICT.get("type"):
                match DICT["type"]:
                    case "separator":
                        temp = Gtk.SeparatorMenuItem.new()
                        temp.set_visible(True)

                        menu.append(temp)
                    case _:
                        print(DICT["type"])

            elif DICT.get("label") and DICT.get("visible") != False:
                Icon = None
                NewSubmenu = None

                if DICT.get("icon-data"):
                    Icon = Widget.Image(
                        self.__decode_icon(
                            DICT["icon-data"],
                            self._menu_path.replace("/", "_") + str(ID),
                        )
                    )

                if DICT.get("children-display") == "submenu":
                    NewSubmenu = Widget.Menu()
                    self.MakeMenu(CHILDRENS, NewSubmenu)

                menu.append(
                    # doing this bc im lazy to create another function
                    (
                        lambda id: Widget.MenuItem(
                            Widget.Box(
                                spacing=10,
                                children=[
                                    Icon,
                                    Widget.Label(
                                        DICT["label"], hexpand=True, halign="start"
                                    ),
                                ],
                            ),
                            onactivate=lambda: self.CallEvent(id),
                            active=DICT.get("enabled", True),
                            submenu=NewSubmenu,
                        )
                    )(ID)
                )

            # print(ID, DICT, CHILDRENS)

    def CallEvent(self, id: int) -> None:
        self._connection.call_sync(
            self._sender,
            self._menu_path,
            "com.canonical.dbusmenu",
            "Event",
            GLib.Variant(
                "(isvu)",
                (
                    id,
                    "clicked",
                    GLib.Variant("s", ""),
                    GLib.get_real_time() * 10**-7,
                ),
            ),
            GLib.VariantType("()"),
            Gio.DBusCallFlags.NONE,
            -1,
        )
        return self.MakeItself()

    def __decode_icon(self, Data: List[int], Id) -> str:
        FilePath: str = f"{DIR_CACHE_TRAY}/{Id}.png"
        from PIL import Image

        with Image.open(io.BytesIO(bytes(Data))) as Content:
            Content.save(FilePath)
        return FilePath


class TrayItem(BaseGObjectClass):
    __gsignals__ = Service.signals(
        {
            "removed": [[str]],
        }
    )
    __gproperties__ = Service.properties(
        {
            "icon": [str],
            "title": [str],
        }
    )

    def __init__(self, Sender: str, Path: str) -> None:
        super().__init__()
        #
        self._connection: Gio.DBusConnection
        self._proxy: Gio.DBusProxy
        self._sender: str = Sender
        self._path: str = Path
        self._menu: _TrayItemMenu
        #
        self._id = ""
        self._icon = ""
        self._title = ""
        self._status = ""

        #
        self.__register__()

    # Accesible Functions

    @property
    def id(self) -> str:
        return self._id

    @property
    def icon(self) -> str:
        return self._icon

    @property
    def title(self) -> str:
        return self._title

    #
    # DbusMethods
    #
    def Activate(
        self, X: int = 0, Y: int = 0, *, event: Union[Gdk.EventButton, None] = None
    ) -> None:
        if event:
            X, Y = round(event.x_root), round(event.y_root)

        self._proxy.call_sync(
            "Activate",
            GLib.Variant("(ii)", (X, Y)),
            Gio.DBusCallFlags.NONE,
            -1,
        )

    def SecondaryActivate(
        self, X: int = 0, Y: int = 0, *, event: Union[Gdk.EventButton, None] = None
    ) -> None:

        if event:
            X, Y = round(event.x_root), round(event.y_root)

        self._proxy.call_sync(
            "SecondaryActivate",
            GLib.Variant("(ii)", (X, Y)),
            Gio.DBusCallFlags.NONE,
            -1,
        )

    def ContextMenu(
        self,
        event: Union[Gdk.EventButton, None] = None,
    ) -> None:
        if event:
            self._menu.popup_at_pointer(event)

    def __register__(self) -> None:
        return Gio.DBusProxy.new_for_bus(
            Gio.BusType.SESSION,
            Gio.DBusProxyFlags.NONE,
            NodeInfo.interfaces[1],
            self._sender,
            self._path,
            "org.kde.StatusNotifierItem",
            callback=self.__on_success__,
        )

    def __on_success__(self, Proxy: Gio.DBusProxy, Task: Gio.Task) -> None:
        def wrapper(_: Gio.DBusProxy, Task: Gio.Task):
            MenuData = self._connection.call_finish(Task).unpack()
            self._menu = _TrayItemMenu(
                self._connection, self._sender, self._path, MenuPath, MenuData
            )

        Proxy = Proxy.new_for_bus_finish(Task)
        Connection = Proxy.get_connection()
        self._proxy = Proxy
        self._connection = Connection
        self._proxy.connect("g-signal", self.__on_gsignal__)
        self._proxy.connect("notify::g-name-owner", self.__on_gname_owner__)

        MenuPath = self.__get_cached_property("Menu")
        self._connection.call(
            self._sender,
            MenuPath,
            "com.canonical.dbusmenu",
            "GetLayout",
            GLib.Variant("(iias)", (0, -1, [])),
            GLib.VariantType("(u(ia{sv}av))"),
            Gio.DBusCallFlags.NONE,
            -1,
            None,
            wrapper,
        )
        self.__on_gsignal__(self._proxy, self._sender, "NewIcon", ())

    def __on_gsignal__(
        self,
        Proxy: Gio.DBusProxy,
        Sender: str,
        Signal: Union[
            Literal["NewTitle"],
            Literal["NewIcon"],
            Literal["NewAttentionIcon"],
            Literal["NewStatus"],
            Literal["NewToolTip"],
            Literal["NewOverlayIcon"],
            Literal["NewStatus"],
        ],
        Arguments: Tuple[Any, ...],
    ) -> None:
        match Signal:
            case "NewIcon":
                IconPixmap = self.__get_cached_property("IconPixmap")
                IconName = self.__get_cached_property("IconName")
                if IconName:
                    self._icon = lookup_icon(IconName)
                elif IconPixmap:
                    self._icon = self.__decode_icon(IconPixmap)
                else:
                    return
                self.emit("icon")

            case "NewTitle":
                pass
            case "NewStatus":
                pass
            case "NewToolTip":
                pass
            case "NewOverlayIcon":
                pass
            case "NewAttentionIcon":
                pass
            case _:
                print(Signal, Arguments)

    def __on_gname_owner__(self, Proxy: Gio.DBusProxy, _: GObject.ParamSpec) -> None:
        if not Proxy.get_name_owner():
            self.emit("removed", self._path)

    def __get_cached_property(self, property_name: str) -> Any:
        value = self._proxy.get_cached_property(property_name)
        return None if not value else value.unpack()

    def __decode_icon(self, data: List[Tuple[int, int, List[int]]]):

        FilePath = f"{DIR_CACHE_TRAY}/{self._sender}.png"

        Data: Tuple[int, int, List[int]] = data[0]
        Alpha = Data[2][0::4]
        Red = Data[2][1::4]
        Green = Data[2][2::4]
        Blue = Data[2][3::4]

        NewData = []

        for i in range(len(Alpha)):
            NewData.append(Red[i])
            NewData.append(Green[i])
            NewData.append(Blue[i])
            NewData.append(Alpha[i])

        GdkPixbuf.Pixbuf.new_from_bytes(
            data=GLib.Bytes(NewData),
            colorspace=GdkPixbuf.Colorspace.RGB,
            has_alpha=True,
            bits_per_sample=8,
            width=Data[0],
            height=Data[1],
            rowstride=(4 * Data[0]),
        ).savev(FilePath, "png")

        return FilePath


#
# StatusNotifierWatcher
#


class _Tray(Service):
    """
    WIP; PLEASE DONT USE
    """

    __gsignals__ = Service.signals(
        {
            "added": [[str]],
            "removed": [[str]],
        }
    )
    __gproperties__ = Service.properties(
        {
            "items": [object],
        }
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._items: Dict[str, TrayItem] = {}
        self._connection: Gio.DBusConnection
        self.__register__()

    def GetItem(self, path: str):
        return self._items.get(path)

    # Data Return
    def ProtocolVersion(self) -> GLib.Variant:
        return GLib.Variant("i", 0)

    def IsStatusNotifierHostRegistered(self) -> GLib.Variant:
        return GLib.Variant("b", True)

    def RegisteredStatusNotifierItems(self) -> GLib.Variant:
        return GLib.Variant("as", self._items.keys())

    def RegisterStatusNotifierItem(self, Sender: str, BusName: str) -> GLib.Variant:
        NewTrayItem = TrayItem(Sender, BusName)
        NewTrayItem.connect("removed", self.UnRegisterStatusNotifierItem)
        self.emit("added", BusName)
        self.emit("items")
        self._items[BusName] = NewTrayItem

        self._connection.emit_signal(
            "org.kde.StatusNotifierWatcher",
            "/org/kde/StatusNotifierWatcher",
            "org.kde.StatusNotifierWatcher",
            "StatusNotifierItemRegistered",
            GLib.Variant("(s)", (Sender + BusName,)),
        )
        return GLib.Variant("()", ())

    def UnRegisterStatusNotifierItem(self, Item: TrayItem, BusPath: str) -> None:
        del self._items[BusPath]
        self.emit("removed", BusPath)
        self.emit("items")

        self._connection.emit_signal(
            "org.kde.StatusNotifierWatcher",
            "/org/kde/StatusNotifierWatcher",
            "org.kde.StatusNotifierWatcher",
            "StatusNotifierItemUnregistered",
            GLib.Variant("(s)", (BusPath,)),
        )

    def __register__(self):
        return Gio.bus_own_name(
            Gio.BusType.SESSION,
            "org.kde.StatusNotifierWatcher",
            Gio.BusNameOwnerFlags.NONE,
            self.__on_success__,
            None,
            self.__on_failed__,
        )

    def __on_success__(
        self,
        Connection: Gio.DBusConnection,
        BusName: Literal["org.kde.StatusNotifierWatcher"],
    ):

        self._connection = Connection

        Connection.register_object(
            "/StatusNotifierWatcher",
            NodeInfo.interfaces[0],
            self.__on_call__,
        )

    def __on_failed__(
        self,
        Connection: Gio.DBusConnection,
        BusName: Literal["org.kde.StatusNotifierWatcher"],
    ):
        Logger.ERROR("Cant register the Tray Service ;(")

    def __on_call__(
        self,
        Connection: Gio.DBusConnection,
        Sender: str,
        Path: Literal["/org/kde/StatusNotifierWatcher"],
        BusName: Literal["org.kde.StatusNotifierWatcher"],
        Method: str,
        Parameters: tuple,
        MethodInvocation: Gio.DBusMethodInvocation,
    ):
        try:
            match Method:
                case "Get":
                    match Parameters[1]:
                        case "IsStatusNotifierHostRegistered":
                            Properties = self.IsStatusNotifierHostRegistered()
                        case "ProtocolVersion":
                            Properties = self.ProtocolVersion()
                        case "RegisteredStatusNotifierItems":
                            Properties = self.RegisteredStatusNotifierItems()
                        case _:
                            Properties = None

                    if Properties:
                        MethodInvocation.return_value(
                            GLib.Variant("(v)", (Properties,))
                        )
                case "GetAll":
                    MethodInvocation.return_value(
                        GLib.Variant(
                            "(a{sv})",
                            (
                                {
                                    "ProtocolVersion": self.ProtocolVersion(),
                                    "IsStatusNotifierHostRegistered": self.IsStatusNotifierHostRegistered(),
                                    "RegisteredStatusNotifierItems": self.RegisteredStatusNotifierItems(),
                                },
                            ),
                        )
                    )

                # New Item added
                case "RegisterStatusNotifierItem":
                    if Parameters and Parameters[0].startswith("/"):
                        ItemPath = Parameters[0]
                    else:
                        ItemPath = "/StatusNotifierItem"

                    MethodInvocation.return_value(
                        self.RegisterStatusNotifierItem(Sender, ItemPath)
                    )
                case _:
                    print(Method, Parameters)
                    print("Cllback no llamado")

        except Exception as r:
            print("ERRORRRRR: ", r)
        finally:
            return Connection.flush()


TrayService = _Tray()
