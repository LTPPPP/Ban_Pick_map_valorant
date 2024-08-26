import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
import sys


class ValorantMapPicker:
    def __init__(self, master):
        self.master = master
        self.master.title("Valorant Map Picker")
        self.master.attributes('-fullscreen', True)

        self.TEAM_A = tk.StringVar()
        self.TEAM_B = tk.StringVar()

        self.maps = ["Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset", "Abyss"]
        self.banned_maps = {}
        self.picked_maps = {}
        self.current_team = None
        self.current_action = None
        self.turn = 0

        self.map_images = {
            "Ascent": "map/Ascent.png",
            "Bind": "map/Bind.png",
            "Haven": "map/Haven.png",
            "Icebox": "map/IceBox.png",
            "Lotus": "map/Lotus.png",
            "Sunset": "map/Sunset.png",
            "Abyss": "map/Abyss.png",
        }

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_team_entry()

        self.exit_button = tk.Button(self.master, text="Exit Fullscreen", command=self.toggle_fullscreen)
        self.exit_button.pack(side=tk.BOTTOM, pady=10)

        self.font_size = tk.IntVar(value=24)
        self.font_label = tk.Label(self.master, text="Font Size")
        self.font_label.pack(side=tk.BOTTOM)

    def setup_team_entry(self):
        team_frame = tk.Frame(self.main_frame)
        team_frame.pack(pady=20)

        tk.Label(team_frame, text="TEAM A:").grid(row=0, column=0, padx=5)
        tk.Entry(team_frame, textvariable=self.TEAM_A).grid(row=0, column=1, padx=5)

        tk.Label(team_frame, text="TEAM B:").grid(row=0, column=2, padx=5)
        tk.Entry(team_frame, textvariable=self.TEAM_B).grid(row=0, column=3, padx=5)

        tk.Button(team_frame, text="Start", command=self.start_game).grid(row=0, column=4, padx=5)

    def start_game(self):
        if not self.TEAM_A.get() or not self.TEAM_B.get():
            messagebox.showerror("Error", "Please enter names for both teams.")
            return

        self.banned_maps = {self.TEAM_A.get(): [], self.TEAM_B.get(): []}
        self.picked_maps = {self.TEAM_A.get(): [], self.TEAM_B.get(): []}
        self.current_team = self.TEAM_A.get()
        self.turn = 0

        self.create_widgets()
        self.update_font_size()
        self.next_turn()

    def create_widgets(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        self.map_buttons = []
        for i, map_name in enumerate(self.maps):
            frame = tk.Frame(self.main_frame)
            frame.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="nsew")
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(0, weight=1)

            btn = tk.Button(frame, text=map_name, compound=tk.CENTER,
                            command=lambda x=map_name: self.map_action(x))
            btn.grid(sticky="nsew")
            self.map_buttons.append(btn)

        self.result_label = tk.Label(self.main_frame, text="")
        self.result_label.grid(row=4, column=0, columnspan=3, pady=10, sticky="nsew")

        for i in range(3):
            self.main_frame.columnconfigure(i, weight=1)
        for i in range(5):
            self.main_frame.rowconfigure(i, weight=1)

    def update_font_size(self, *args):
        font_size = self.font_size.get()
        button_size = font_size * 6
        for btn in self.map_buttons:
            btn.config(font=("TkDefaultFont", font_size))
            map_name = btn['text'].split('\n')[0]
            image = Image.open(self.map_images[map_name])
            image = image.resize((button_size, button_size), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            btn.config(image=photo, text=map_name, compound=tk.TOP)
            btn.image = photo
        self.result_label.config(font=("TkDefaultFont", font_size))
        self.exit_button.config(font=("TkDefaultFont", font_size // 2))
        self.font_label.config(font=("TkDefaultFont", font_size // 2))

    def toggle_fullscreen(self):
        is_fullscreen = self.master.attributes('-fullscreen')
        self.master.attributes('-fullscreen', not is_fullscreen)
        if is_fullscreen:
            self.exit_button.config(text="Enter Fullscreen")
        else:
            self.exit_button.config(text="Exit Fullscreen")

    def next_turn(self):
        turn_order = [
            (self.TEAM_A.get(), "ban"),
            (self.TEAM_B.get(), "ban"),
            (self.TEAM_A.get(), "pick"),
            (self.TEAM_B.get(), "pick"),
            (self.TEAM_A.get(), "ban"),
            (self.TEAM_B.get(), "pick")
        ]

        if self.turn < len(turn_order):
            self.current_team, self.current_action = turn_order[self.turn]
            self.result_label.config(text=f"{self.current_team} - {self.current_action.capitalize()} a map")
            self.turn += 1
        else:
            self.show_final_result()

    def map_action(self, map_name):
        if self.current_action == "ban":
            self.banned_maps[self.current_team].append(map_name)
            self.result_label.config(text=f"{self.current_team} banned {map_name}")
            self.update_button(map_name, "red")
        elif self.current_action == "pick":
            self.picked_maps[self.current_team].append(map_name)
            self.result_label.config(text=f"{self.current_team} picked {map_name}")
            self.update_button(map_name, "green")

        self.next_turn()

    def update_button(self, map_name, color):
        for btn in self.map_buttons:
            if btn['text'].split('\n')[0] == map_name:
                btn.config(bg=color, state="disabled", fg="white")
                bold_font = tkfont.Font(font=btn['font'])
                bold_font.configure(weight="bold")
                btn.config(font=bold_font)
                if color == "green":
                    btn.config(text=f"{map_name}\n({self.current_team})")
                btn.config(compound=tk.TOP)

    def show_final_result(self):
        result = "Banned maps:\n"
        for team, maps in self.banned_maps.items():
            for map_name in maps:
                result += f"{map_name} (by {team})\n"
        result += "\nPicked maps:\n"
        for team, maps in self.picked_maps.items():
            for map_name in maps:
                result += f"{map_name} (by {team})\n"

        filename = self.generate_filename()
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(result)

        messagebox.showinfo("Final Result", f"Results saved to {filename}")
        self.master.quit()
        sys.exit()

    def generate_filename(self):
        bans_A = "_".join(self.banned_maps[self.TEAM_A.get()])
        picks_A = "_".join(self.picked_maps[self.TEAM_A.get()])
        bans_B = "_".join(self.banned_maps[self.TEAM_B.get()])
        picks_B = "_".join(self.picked_maps[self.TEAM_B.get()])
        return f"map_picked/{self.TEAM_A.get()}_VS_{self.TEAM_B.get()}_BAN_PICK_map.txt"


root = tk.Tk()
app = ValorantMapPicker(root)
root.mainloop()