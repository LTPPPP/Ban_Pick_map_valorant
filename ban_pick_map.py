import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
from PIL import Image, ImageTk


class ValorantMapPicker:
    def __init__(self, master):
        TEAM_A = "PRX"
        TEAM_B = "EG"
        self.master = master
        self.master.title("Valorant Map Picker")
        self.master.attributes('-fullscreen', True)

        self.maps = ["Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset"]
        self.banned_maps = {f"{TEAM_A}": [], f"{TEAM_B}": []}
        self.picked_maps = {f"{TEAM_A}": [], f"{TEAM_B}": []}
        self.current_team = f"{TEAM_A}"

        self.map_images = {
            "Ascent": "map/Ascent.png",
            "Bind": "map/Bind.png",
            "Haven": "map/Haven.png",
            "Icebox": "map/IceBox.png",
            "Lotus": "map/Lotus.png",
            "Sunset": "map/Sunset.png"
        }

        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()

        self.exit_button = tk.Button(self.master, text="Exit Fullscreen", command=self.toggle_fullscreen)
        self.exit_button.pack(side=tk.BOTTOM, pady=10)

        self.font_size = tk.IntVar(value=24)
        self.font_label = tk.Label(self.master, text="Font Size")
        self.update_font_size()

    def create_widgets(self):
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

        self.ban_button = tk.Button(self.main_frame, text="Ban", command=lambda: self.set_action("ban"))
        self.ban_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

        self.pick_button = tk.Button(self.main_frame, text="Pick", command=lambda: self.set_action("pick"))
        self.pick_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

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
        for btn in [self.ban_button, self.pick_button]:
            btn.config(font=("TkDefaultFont", font_size))
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

    def set_action(self, action):
        self.current_action = action
        self.result_label.config(text=f"{self.current_team} - {action.capitalize()} a map")

    def map_action(self, map_name):
        if hasattr(self, 'current_action'):
            if self.current_action == "ban":
                if len(self.banned_maps[self.current_team]) < 2 and len(self.banned_maps[self.other_team()]) < 2:
                    self.banned_maps[self.current_team].append(map_name)
                    self.result_label.config(text=f"{self.current_team} banned {map_name}")
                    self.update_button(map_name, "red")
                    self.switch_team()
                else:
                    self.result_label.config(text=f"{self.current_team} cannot ban more maps")

            elif self.current_action == "pick":
                if len(self.picked_maps[self.current_team]) < 2 and len(self.picked_maps[self.other_team()]) < 2:
                    self.picked_maps[self.current_team].append(map_name)
                    self.result_label.config(text=f"{self.current_team} picked {map_name}")
                    self.update_button(map_name, "green")
                    self.switch_team()
                else:
                    self.result_label.config(text=f"{self.current_team} cannot pick more maps")

            if self.check_end_condition():
                self.show_final_result()
        else:
            self.result_label.config(text="Please select Ban or Pick first")

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

    def switch_team(self):
        self.current_team = f"{TEAM_B}" if self.current_team == f"{TEAM_A}" else f"{TEAM_A}"

    def check_end_condition(self):
        total_actions = sum(len(maps) for maps in self.banned_maps.values()) + sum(
            len(maps) for maps in self.picked_maps.values())
        return total_actions == 6  # 3 bans and 3 picks per team

    def show_final_result(self):
        result = "Banned maps:\n"
        for team, maps in self.banned_maps.items():
            for map_name in maps:
                result += f"{map_name} (by {team})\n"
        result += "\nPicked maps:\n"
        for team, maps in self.picked_maps.items():
            for map_name in maps:
                result += f"{map_name} (by {team})\n"

        # Save result to a file
        filename = self.generate_filename()
        with open(filename, 'w') as file:
            file.write(result)

        messagebox.showinfo("Final Result", f"Results saved to {filename}")

    def generate_filename(self):
        # Create a filename based on bans and picks
        bans_A = "_".join(self.banned_maps[f"{TEAM_A}"])
        picks_A = "_".join(self.picked_maps[f"{TEAM_A}"])
        bans_B = "_".join(self.banned_maps[f"{TEAM_B}"])
        picks_B = "_".join(self.picked_maps[f"{TEAM_B}"])
        return f"map_picked/{TEAM_A}_VS_{TEAM_B}_BAN_PICK_map.txt"

    def other_team(self):
        return f"{TEAM_B}" if self.current_team == f"{TEAM_A}" else f"{TEAM_A}"


root = tk.Tk()
TEAM_A ="PRX"
TEAM_B ="EG"
app = ValorantMapPicker(root)
root.mainloop()
