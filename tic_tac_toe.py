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
        celll = lambda cell: '/img/blank.png' if cell is None else '/img/o.png' if cell == 'O' else '/img/x.png' if cell == 'X' else cell
        
        ttype = lambda cell: 'X' if cell == 'X' else 'O' if cell == 'O' else 'Empty' if cell is None else cell

    board_str = f"""| Tic | Tac | Toe |
|--|--|--|
| [![{ttype(board[0])}]({celll(board[0])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%200) | 
[![{ttype(board[1])}]({celll(board[1])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%201) | 
[![{ttype(board[2])}]({celll(board[2])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%202) |
| [![{ttype(board[3])}]({celll(board[3])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%203) | 
[![{ttype(board[4])}]({celll(board[4])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%204) | 
[![{ttype(board[5])}]({celll(board[5])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%205) |
| [![{ttype(board[6])}]({celll(board[6])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%206) | 
[![{ttype(board[7])}]({celll(board[7])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%207) | 
[![{ttype(board[8])}]({celll(board[8])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%208) |
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
