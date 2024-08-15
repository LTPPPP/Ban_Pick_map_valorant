import tkinter as tk

def draw_bracket(teams):
    window = tk.Tk()
    window.title("Sơ đồ thi đấu")

    canvas = tk.Canvas(window, width=800, height=600, bg='white')
    canvas.pack()

    num_teams = len(teams)
    rounds = 1
    while 2 ** rounds < num_teams:
        rounds += 1

    bracket_height = 600 // num_teams
    x_spacing = 150
    y_offset = bracket_height // 2

    positions = []

    team_color = "blue"
    champion_color = "red"

    for i in range(num_teams):
        y = i * bracket_height + y_offset
        # NAME _ POS
        positions.append((60, y))
        canvas.create_text(20, y, text=teams[i], anchor=tk.W, fill=team_color, font=("Helvetica", 12, "bold"))

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

                canvas.create_line(x1, y1, x_mid, y1, fill=line_color, width=2)
                canvas.create_line(x1, y2, x_mid, y2, fill=line_color, width=2)
                canvas.create_line(x_mid, y1, x_mid, y2, fill=line_color, width=2)

                next_round_positions.append((x_mid, y_mid))

        round_positions = next_round_positions
        line_color = "green" if r % 2 == 0 else "blue"

    if round_positions:
        x_final, y_final = round_positions[0]
        canvas.create_text(x_final + 20, y_final, text="Vô địch", anchor=tk.W, fill=champion_color, font=("Helvetica", 14, "bold"))

    window.mainloop()

def get_teams_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            teams = [line.strip() for line in file if line.strip()]

        num_teams = len(teams)

        # If the number of teams is odd, add a placeholder team
        if num_teams % 2 != 0:
            print(f"Số đội lẻ, thêm đội 'Bye' vào để đủ {num_teams + 1} đội.")
            teams.append("Bye")

        return teams

    except FileNotFoundError:
        print("File không tồn tại. Vui lòng kiểm tra lại đường dẫn.")
        return []

# Example usage
file_path = "team/team.txt"  # Replace with your file path
teams = get_teams_from_file(file_path)
if teams:
    draw_bracket(teams)
