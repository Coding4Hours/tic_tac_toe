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

    updated_board = ['&nbsp;' if tile == ' ' else tile for tile in board]

    #test
    cell_image = lambda cell: '/img/blank.png' if cell == ' ' else '/img/o.png' if cell == 'O' else '/img/x.png'
    cell_type = lambda cell: 'X' if cell == 'X' else 'O' if cell == 'O' else 'Empty' if cell == ' ' else cell

    board_str = f"""| Tic | Tac | Toe |
|--|--|--|
| [![{cell_type(updated_board[0])}]({cell_image(updated_board[0])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%201) | 
[![{cell_type(updated_board[1])}]({cell_image(updated_board[1])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%202) | 
[![{cell_type(updated_board[2])}]({cell_image(updated_board[2])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%203) |
| [![{cell_type(updated_board[3])}]({cell_image(updated_board[3])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%204) | 
[![{cell_type(updated_board[4])}]({cell_image(updated_board[4])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%205) | 
[![{cell_type(updated_board[5])}]({cell_image(updated_board[5])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%206) |
| [![{cell_type(updated_board[6])}]({cell_image(updated_board[6])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%207) | 
[![{cell_type(updated_board[7])}]({cell_image(updated_board[7])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%208) | 
[![{cell_type(updated_board[8])}]({cell_image(updated_board[8])})](https://github.com/Coding4Hours/tic_tac_toe/issues/new?title=move%209) |
"""

   # board_str = f"""| {updated_board[0]} | {updated_board[1]} | {updated_board[2]} |
#|---|---|---|
#| {updated_board[3]} | {updated_board[4]} | {updated_board[5]} |
#| {updated_board[6]} | {updated_board[7]} | {updated_board[8]} |"""

    with open('stuff.json', 'r') as file:
        data = json.load(file)
    data['board'] = updated_board  # Update board in data dictionary

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

    # If you need to persist the updated board in "stuff.json"
    with open('stuff.json', 'w') as file:
        json.dump(data, file)
    
def main(move):
    with open('README.md', 'r') as file:
        content = file.read()
            
    
    with open('stuff.json', 'r') as file:
        data = json.load(file) 
    board = data['board']
    
    current_player = data['turn']

    print(board)
    
    if update_board(board, move, current_player):
        winner = check_winner(board)
        if winner:
            status = f'{winner} wins!' if winner != 'Tie' else "It's a tie!"
        else:
            next_player = 'O' if current_player == 'X' else 'X'
            status = f"It's {next_player}'s turn to play."
        with open('stuff.json') as file:
            a = json.load(file)
            a['turn'] = 'O' if current_player == 'X' else 'X'
            file.write(json.dumps(a))
        update_readme(board, status)
        return True
    else:
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        move = int(sys.argv[1]) - 1
        main(move)
