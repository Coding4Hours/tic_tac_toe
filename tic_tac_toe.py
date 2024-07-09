import re
import urllib.parse
import json

def update_board(board, move, player):
    if board[move] == 'X' or board[move] == 'O':
        return False
    board[move] = player
    return True

def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:
        return 'Tie'
    return None

def update_readme(board, status):
    with open('README.md', 'r') as file:
        content = file.read()
        
    board = ['&nbsp;' if tile == ' ' else tile for tile in board]

    board_str = f"""| {board[0]} | {board[1]} | {board[2]} |
|---|---|---|
| {board[3]} | {board[4]} | {board[5]} |
| {board[6]} | {board[7]} | {board[8]} |"""

    possible_moves = [i+1 for i, v in enumerate(board) if v == ' ']
    moves_str = "Possible moves:\n\n"
    for move in possible_moves:
        issue_title = f"move {move}"
        encoded_title = urllib.parse.quote(issue_title)
        moves_str += f"- [Move {move}](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title={encoded_title})\n"

    new_content = re.sub(r'## Current Board\n\n.*?\n\n', f'## Current Board\n\n{board_str}\n\n', content, flags=re.DOTALL)
    new_content = re.sub(r'## Game Status\n\n.*', f'## Game Status\n\n{status}', new_content)

    with open('README.md', 'w') as file:
        file.write(new_content)

def main(move):
    with open('README.md', 'r') as file:
        content = file.read()

    current_player = 'X' if content.endswith("It's X's turn to play.") else 'O'
    
    with open('stuff.json', 'r') as file:
        data = json.load(file) 
    board = data['board']
        
    print(board)
    
    if update_board(board, move, current_player):
        winner = check_winner(board)
        if winner:
            status = f'{winner} wins!' if winner != 'Tie' else "It's a tie!"
        else:
            next_player = 'O' if current_player == 'X' else 'X'
            status = f"It's {next_player}'s turn to play."
        
        update_readme(board, status)
        return True
    else:
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        move = int(sys.argv[1]) - 1
        main(move)
