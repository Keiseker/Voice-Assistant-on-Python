import tkinter as tk
import customtkinter as CTk


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("300x500")
        self.title("Password generator")
        self.resizable(False, False)

        # ? ОБЩИЙ
        self.tree = CTk.CTkFrame(
            master=self, fg_color="#092a36")
        self.tree.grid(row=0,  column=0, padx=(
            0, 0), pady=(0, 0), sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        # ? upbar_frame
        self.upbar_frame = CTk.CTkFrame(
            master=self.tree, fg_color="#011a27")
        self.upbar_frame.grid(row=1,  column=0, padx=(
            0, 0), pady=(0, 0), sticky="nsew")

        self.name = CTk.CTkLabel(
            master=self.upbar_frame, text="Джарвис", text_color="#99ee44", font=("Roboto", 18))
        self.name.grid(row=0, column=0, padx=(10, 0))

        self.btn_help = CTk.CTkButton(master=self.upbar_frame, fg_color="#99ee44", corner_radius=20, text="", text_color="#ffffff",  hover_color="#7f29ff",  width=40, height=40,
                                      )
        self.btn_help.grid(row=0, column=1, padx=(170, 5), pady=(5, 5),)

        # ? textbox_frame
        self.textbox_frame = CTk.CTkFrame(
            master=self.tree, fg_color="#092a36")
        self.textbox_frame.grid(row=1, column=0, padx=(
            0, 0), pady=(50, 0), sticky="nsew")

        # ? chat_frame
        self.chat_frame = CTk.CTkFrame(
            master=self.tree, fg_color="#011a27")
        self.chat_frame.grid(row=1, column=0, padx=(
            0, 0), pady=(450, 0), sticky="nsew")

        self.entry_message = CTk.CTkEntry(
            master=self.chat_frame, width=240, height=40, fg_color="#011a27", text_color="#ffffff", font=("Roboto", 14))
        self.entry_message.grid(row=0, column=0, padx=(5, 10), pady=(5, 5))

        self.btn_micro = CTk.CTkButton(master=self.chat_frame, fg_color="#99ee44", corner_radius=20, hover_color="#7f29ff", text="", width=40, height=40,
                                       )
        self.btn_micro.grid(row=0, column=1, padx=(0, 5),)


if __name__ == "__main__":
    app = App()
    app.mainloop()
