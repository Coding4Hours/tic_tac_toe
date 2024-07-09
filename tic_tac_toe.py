import re

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
        
    cell_image = lambda cell: '/img/blank.png' if cell == ' ' else '/img/o.png' if cell == 'O' else '/img/x.png'
    cell_type = lambda cell: 'X' if cell == 'X' else 'O' if cell == 'O' else 'Empty' if cell == ' ' else cell

    board_str = f"""| Tic | Tac | Toe |
|--|--|--|
| [![{cell_type(board[0])}]({cell_image(board[0])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%201) | 
[![{cell_type(board[1])}]({cell_image(board[1])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%202) | 
[![{cell_type(board[2])}]({cell_image(board[2])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%203) |
| [![{cell_type(board[3])}]({cell_image(board[3])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%204) | 
[![{cell_type(board[4])}]({cell_image(board[4])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%205) | 
[![{cell_type(board[5])}]({cell_image(board[5])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%206) |
| [![{cell_type(board[6])}]({cell_image(board[6])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%207) | 
[![{cell_type(board[7])}]({cell_image(board[7])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%208) | 
[![{cell_type(board[8])}]({cell_image(board[8])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%209) |
"""

    new_content = re.sub(r'## Current Board\n\n.*?\n\n', f'## Current Board\n\n{board_str}\n\n', content, flags=re.DOTALL)
    new_content = re.sub(r'## Game Status\n\n.*', f'## Game Status\n\n{status}', new_content)

    with open('README.md', 'w') as file:
        file.write(new_content)

def main(move):
    with open('README.md', 'r') as file:
        content = file.read()

    board = re.findall(r'\| (.) \| (.) \| (.) \|', content)
    board = [item for sublist in board for item in sublist]
    board = [' ' if cell == 'Empty' else cell for cell in board]

    current_player = 'X' if content.endswith("It's X's turn to play.") else 'O'

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
