import tkinter as tk
from tkinter import font

def draw_bracket(teams):
    window = tk.Tk()
    window.title("Sơ đồ thi đấu")

    # Adjust canvas width to accommodate longer team names
    canvas_width = 1000
    canvas_height = 600
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg='white')
    canvas.pack()

    num_teams = len(teams)
    rounds = 1
    while 2 ** rounds < num_teams:
        rounds += 1

    bracket_height = canvas_height // num_teams
    x_spacing = 200  # Increase spacing between rounds
    y_offset = bracket_height // 2

    positions = []

    team_color = "blue"
    decider_color = "green"
    champion_color = "red"

    # Create a font object to measure text width
    text_font = font.Font(family="Helvetica", size=12, weight="bold")

    for i in range(num_teams):
        y = i * bracket_height + y_offset
        positions.append((200, y))
        text = teams[i]
        text_width = text_font.measure(text)
        # Adjust text position to avoid overlap with the line
        if "(decider)" in teams[i]:
            canvas.create_text(190 - text_width, y, text=text, anchor=tk.W, fill=decider_color, font=text_font)
        else:
            canvas.create_text(190 - text_width, y, text=text, anchor=tk.W, fill=team_color, font=text_font)

    round_positions = positions
    line_color = "black"

    for r in range(1, rounds + 1):
        next_round_positions = []
        for i in range(0, len(round_positions), 2):
            if i + 1 < len(round_positions):
                x1, y1 = round_positions[i]
                x2, y2 = round_positions[i + 1]
                x_mid = x1 + x_spacing
                y_mid = (y1 + y2) // 2

                # Draw lines
                canvas.create_line(x1, y1, x_mid, y1, fill=line_color, width=2)
                canvas.create_line(x1, y2, x_mid, y2, fill=line_color, width=2)
                canvas.create_line(x_mid, y1, x_mid, y2, fill=line_color, width=2)

                next_round_positions.append((x_mid, y_mid))

        round_positions = next_round_positions
        line_color = "green" if r % 2 == 0 else "blue"

    if round_positions:
        x_final, y_final = round_positions[0]
        # Position the championship text to avoid overlap
        canvas.create_text(x_final + 40, y_final, text="Vô địch", anchor=tk.W, fill=champion_color, font=text_font)

    window.mainloop()

def get_teams_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            teams = [line.strip() for line in file if line.strip()]

        num_teams = len(teams)

        if num_teams % 2 != 0:
            print(f"Số đội lẻ, thêm đội 'Bye' vào để đủ {num_teams + 1} đội.")
            teams.append("Bye")

        return teams

    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra lại đường dẫn.")
        return []

# Example usage
file_path = "tour.txt"  # Replace with your file path
teams = get_teams_from_file(file_path)
if teams:
    draw_bracket(teams)
