import tkinter as tk
from tkinter import messagebox
import random
import time

def read_teams_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        teams = [line.strip() for line in file if line.strip()]
    return teams

def write_pairs_to_file(pairs_file_path, tour_file_path, pairs):
    with open(pairs_file_path, 'w', encoding='utf-8') as pairs_file:
        for pair in pairs:
            pairs_file.write(f"{pair[0]} (decider) vs {pair[1]}\n" if pair[2] == 0 else f"{pair[0]} vs {pair[1]} (decider)\n")

    with open(tour_file_path, 'w', encoding='utf-8') as tour_file:
        for pair in pairs:
            if pair[2] == 0:
                tour_file.write(f"{pair[0]} (decider)\n")
                tour_file.write(f"{pair[1]}\n")
            else:
                tour_file.write(f"{pair[0]}\n")
                tour_file.write(f"{pair[1]} (decider)\n")

def generate_pairs(teams):
    if len(teams) % 2 != 0:
        raise ValueError("Số lượng đội phải là số chẵn")
    random.shuffle(teams)
    pairs = [(teams[i], teams[i + 1], random.randint(0, 1)) for i in range(0, len(teams), 2)]
    return pairs

def start_randomization():
    try:
        teams = read_teams_from_file('team/team.txt')
        if len(teams) % 2 != 0:
            raise ValueError("Số lượng đội phải là số chẵn")
        canvas.delete("all")
        animate_teams(teams)
        pairs = generate_pairs(teams)
        write_pairs_to_file('pairs.txt', 'tour.txt', pairs)
        display_pairs(pairs)
        messagebox.showinfo("Thành công", "Các cặp đấu đã được tạo thành công và lưu vào file pairs.txt và tour.txt")
    except ValueError as e:
        messagebox.showerror("Lỗi", str(e))

def animate_teams(teams):
    canvas.delete("all")
    team_labels = []
    for i, team in enumerate(teams):
        label = canvas.create_text(random.randint(50, 350), random.randint(50, 350), text=team, font=("Arial", 14))
        team_labels.append(label)

    for _ in range(50):  # Số lần di chuyển
        for label in team_labels:
            x, y = canvas.coords(label)
            canvas.move(label, random.randint(-10, 10), random.randint(-10, 10))
        canvas.update()
        time.sleep(0.05)  # Thời gian giữa các bước di chuyển

def display_pairs(pairs):
    text_widget.delete(1.0, tk.END)
    for pair in pairs:
        text_widget.insert(tk.END, f"{pair[0]} (decider) vs {pair[1]}\n" if pair[2] == 0 else f"{pair[0]} vs {pair[1]} (decider)\n")

def create_gui():
    global canvas, text_widget

    root = tk.Tk()
    root.title("Random Cặp Thi Đấu")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Nhấn nút để bắt đầu random cặp thi đấu")
    label.pack(pady=10)

    button = tk.Button(frame, text="Bắt đầu", command=start_randomization)
    button.pack(pady=10)

    canvas = tk.Canvas(frame, width=400, height=400, bg="white")
    canvas.pack(pady=10)

    text_widget = tk.Text(frame, height=10, width=50)
    text_widget.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
