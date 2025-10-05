import tkinter as tk # Thư viện tkinter trong Python dùng để tạo giao diện đồ họa
from tkinter import messagebox # Thư viện để hiển thị hộp thoại thông báo
import math # Thư viện toán học trong Python

# Khởi tạo bàn cờ và nút
board = [" " for _ in range(9)] # Khởi tạo bàn cờ 3x3
buttons = []

player_first = True  # Biến xác định ai đi trước

# Kiểm tra thắng
def check_winner(board, player):
    win_states = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
# Các trường hợp để xác định được bước đi thắng
    ]
    for state in win_states:
        if all(board[i] == player for i in state):
            return True
    return False

def is_full(board):
    return " " not in board

def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    elif check_winner(board, "X"):
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score

def best_move():
    best_score = -math.inf
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

def player_move(i):
    if board[i] == " ":
        board[i] = "X"
        buttons[i].config(text="X", state="disabled")
        if check_winner(board, "X"):
            messagebox.showinfo("Kết quả", "Bạn thắng! (không thể xảy ra nếu máy chơi đúng)")
            root.quit()
        elif is_full(board):
            messagebox.showinfo("Kết quả", "Hòa!")
            root.quit()
        else:
            ai_turn()

def ai_turn():
    move = best_move()
    if move is not None:
        board[move] = "O"
        buttons[move].config(text="O", state="disabled")
        if check_winner(board, "O"):
            messagebox.showinfo("Kết quả", "Máy thắng!")
            root.quit()
        elif is_full(board):
            messagebox.showinfo("Kết quả", "Hòa!")
            root.quit()

# Hàm bắt đầu game sau khi chọn ai đi trước
def start_game(first_player):
    global player_first, root, buttons
    player_first = first_player
    selection_window.destroy()  # Đóng cửa sổ lựa chọn
# Tạo giao diện bàn cờ
    root = tk.Tk()
    root.title("Caro 3x3 (Welcome to Caro Game)")

    buttons = []
    for i in range(9):
        btn = tk.Button(root, text=" ", font=("Times New Roman", 24), width=5, height=2,
                        command=lambda i=i: player_move(i))
        btn.grid(row=i//3, column=i%3)
        buttons.append(btn)

    # Nếu máy đi trước, đi ngay
    if not player_first:
        ai_turn()

    root.mainloop()

#  Cửa sổ lựa chọn ai đi trước 
selection_window = tk.Tk()
selection_window.title("Chọn người đi trước")
tk.Label(selection_window, text="Ai đi trước?", font=("Times New Roman", 14)).pack(pady=10)
tk.Button(selection_window, text="Người đi trước", font=("Times New Roman", 12),
          command=lambda: start_game(True)).pack(pady=5)
tk.Button(selection_window, text="Máy đi trước", font=("Times New Roman", 12),
          command=lambda: start_game(False)).pack(pady=5)

selection_window.mainloop()