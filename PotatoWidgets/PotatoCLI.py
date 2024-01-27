from .__Import import *


def list_windows():
    command = [
        "gdbus",
        "call",
        "--session",
        "--dest=com.T0kyoB0y.PotatoWidgets",
        "--object-path=/com/T0kyoB0y/PotatoWidgets",
        "--method=com.T0kyoB0y.PotatoWidgets.ListWindows",
    ]

    out = subprocess.getoutput(" ".join(command))
    out = json.loads(out.replace("('", "").replace("',)", ""))
    for i in out:
        if i["opened"]:
            print("*", end=" ")
        print(i["name"])


def toggle_window(window_name):
    command = [
        "gdbus",
        "call",
        "--session",
        "--dest=com.T0kyoB0y.PotatoWidgets",
        "--object-path=/com/T0kyoB0y/PotatoWidgets",
        "--method=com.T0kyoB0y.PotatoWidgets.WindowAction",
        "toggle",
        window_name,
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser(description="PotatoWidgets CLI")
    parser.add_argument(
        "--windows", action="store_true", help="List all exported windows"
    )
    parser.add_argument("--toggle", help="Toggle window with the given name")

    args = parser.parse_args()

    if args.windows:
        list_windows()
    elif args.toggle:
        toggle_window(args.toggle)
    else:
        print("Usage: potatocli --help")


if __name__ == "__main__":
    main()
