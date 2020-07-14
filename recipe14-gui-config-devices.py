from tkinter import *
from jnpr.junos import Device
from jnpr.junos.exception import *
from pprint import pformat

USER = "lab"
PASSWD = "lab@123"
DEVICE_IP = "172.16.100.1"


def output(st):
    text.insert(END, chars=st)
    text.see(END)


def read_and_display(message, function):
    output(message)
    try:
        with Device(host=entry_dev.get(), user=entry_user.get(), password=entry_pw.get()) as dev:
            res = function(dev)
    except ConnectRefusedError:
        print("\n Error: Connection refused! \n")
    except ConnectTimeoutError:
        output("\n Connect timeout error! \n")
    except ConnectUnknownHostError:
        output("\n Error: Connection attempt to unknown host. \n")
    except ConnectAuthError:
        output("\n Connection authentication error! \n")
    except ConnectError:
        output("\n Connection error!")
    else:
        output(res)


def print_facts():
    read_and_display("\n Device facts: \n", lambda dev: pformat(dev.facts))


def show_bgp():
    read_and_display("\n BGP summary information:",
                     lambda dev: dev.rpc.get_bgp_summary_information({"format": "text"}).text)


def show_intf():
    read_and_display("\n Interface information:",
                     lambda dev: dev.rpc.get_interface_information({"format": "text"}, terse=True).text)


def main():
    global entry_dev, entry_user, entry_pw, text
    root = Tk()

    Frame(root, height=10).grid(row=0)

    Label(root, text="Device address:").grid(row=1, column=0)
    entry_dev = Entry(root)
    entry_dev.grid(row=1, column=1)
    entry_dev.insert(END, DEVICE_IP)

    Label(root, text="login:").grid(row=2, column=0)
    entry_user = Entry(root)
    entry_user.grid(row=2, column=1)
    entry_user.insert(END, USER)

    Label(root, text="Password:").grid(row=3, column=0)
    entry_pw = Entry(root, show="*")
    entry_pw.grid(row=3, column=1)
    entry_pw.insert(END, PASSWD)

    Frame(root, height=10).grid(row=4)
    Button(root, text="Read facts!", command=print_facts).grid(row=5, column=0)
    Button(root, text="Show interfaces!", command=show_intf).grid(row=5, column=1)
    Button(root, text="Show BGP!", command=show_bgp).grid(row=5, column=2)
    Frame(root, height=10).grid(row=6)

    frame = Frame(root, width=800, height=700)
    frame.grid(row=7, column=0, columnspan=4)
    frame.grid_propagate(False)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    text = Text(frame, borderwidth=3)
    text.config(font=("courier", 11), wrap='none')
    text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    scrollbarY = Scrollbar(frame, command=text.yview)
    scrollbarY.grid(row=0, column=1, sticky='nsew')
    text['yscrollcommand'] = scrollbarY.set
    scrollbarX = Scrollbar(frame, orient=HORIZONTAL, command=text.xview)
    scrollbarX.grid(row=1, column=0, sticky='nsew')
    text['xscrollcommand'] = scrollbarX.set

    root.mainloop()


if __name__ == "__main__":
    main()





