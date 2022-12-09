import customtkinter, os

class run():
    def start():
        import main
        main.start()

    def udev():
        import linuxudev
        linuxudev()

    def requirements():
        os.system("pip install requests")


os.system('cls' if os.name == 'nt' else 'clear')

root = customtkinter.CTk()
customtkinter.set_appearance_mode("system")
root.geometry("400x350")
root.title("ADB installer")

frame = customtkinter.CTkFrame(root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(frame, text="ADB Installer", font=("Segoe UI", 30, "bold"))
label.pack(pady=12, padx=10)

buttonInstall = customtkinter.CTkButton(frame, text="Start! (CMD)", command=run.start)
buttonInstall.pack(pady=12, padx=10)

buttonUdev = customtkinter.CTkButton(frame, text="Install Linux UDev!", command=run.udev)
buttonUdev.pack(pady=12, padx=10)

requiremensButton = customtkinter.CTkButton(frame, text="Install requirements!", command=run.requirements)
requiremensButton.pack(pady=12, padx=10)

bottomlabel = customtkinter.CTkLabel(frame, text="Thanks dumpydev for Unix script.\n GUI and Windows by matejmajny", font=("Segoe UI", 13))
bottomlabel.pack(pady=27, padx=10)

root.mainloop()

