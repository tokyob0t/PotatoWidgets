from .__Import import *


class _LoopClass:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Daemon de ejemplo con opciones."
        )
        self.parser.add_argument(
            "--print", dest="print_message", help="Mensaje a imprimir"
        )
        self.parser.add_argument(
            "subcommand", choices=["start", "stop"], help="Comando a ejecutar"
        )
        self.args = self.parser.parse_args()

    def __start(self):
        print("La aplicación está en ejecución...")
        Gtk.main()

    def __stop(self):
        Gtk.main_quit()

    def run(self):
        if hasattr(self.args, "print_message") and self.args.print_message:
            print("Mensaje personalizado:", self.args.print_message)

        if self.args.subcommand == "start":
            self.__run_daemon()
        elif self.args.subcommand == "stop":
            self.__stop()
        else:
            print("Comando no reconocido.")

    def __run_daemon(self):
        daemon = daemonize.Daemonize(
            app="PotatoLoop", pid="/tmp/PotatoLoop.pid", action=self.__start
        )
        daemon.start()


# PotatoLoop = _LoopClass()
def PotatoLoop():
    try:
        Gtk.main()
    except KeyboardInterrupt:
        exit(0)
