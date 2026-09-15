PIN_COUNT = 10
DEBUG_MINIMAX = False


def show_row(pins):
	"""Print the row and the position numbers used for moves."""
	positions = " ".join(str(number) for number in range(1, len(pins) + 1))
	row = " ".join("|" if pin else "." for pin in pins)
	print(f"Positions: {positions}")
	print(f"Pins:      {row}")


def pins_are_available(pins):
	"""Return True when at least one pin remains."""
	return any(pins)


def valid_move(pins, start, amount):
	"""Check whether a move removes one pin or two adjacent pins."""
	first_index = start - 1

	if amount not in (1, 2):
		return False
	if first_index < 0 or first_index + amount > len(pins):
		return False

	return all(pins[index] for index in range(first_index, first_index + amount))


def legal_moves(pins):
	"""Return every legal move as a (starting position, amount) tuple."""
	moves = []

	for start in range(1, len(pins) + 1):
		for amount in (1, 2):
			if valid_move(pins, start, amount):
				moves.append((start, amount))

	return moves


def remove_pins(pins, start, amount):
	"""Remove the selected pins after the move has been validated."""
	first_index = start - 1
	for index in range(first_index, first_index + amount):
		pins[index] = False


def new_game_state(pins, move):
	"""Return a new state with the move applied, leaving the old state unchanged."""
	start, amount = move
	new_pins = pins.copy()
	remove_pins(new_pins, start, amount)
	return new_pins


def game_over(pins):
	"""Return True when no pins remain and no move is possible."""
	return not pins_are_available(pins)


def minimax(pins, computer_turn, states_checked, cache=None, unique_states=None):
	"""Return the computer's score, optionally reusing cached states."""
	states_checked[0] += 1
	state_key = (tuple(pins), computer_turn)
	if unique_states is not None:
		unique_states.add(state_key)

	if cache is not None and state_key in cache:
		return cache[state_key]

	# Base case: the previous player removed the last available pin.
	if game_over(pins):
		score = -1 if computer_turn else 1
		if cache is not None:
			cache[state_key] = score
		return score

	move_scores = []

	# Recursion: evaluate every possible move and the state it creates.
	for move in legal_moves(pins):
		new_state = new_game_state(pins, move)
		score = minimax(
			new_state, not computer_turn, states_checked, cache, unique_states
		)
		move_scores.append(score)

	# The computer maximizes its score; the human is assumed to minimize it.
	if computer_turn:
		score = max(move_scores)
	else:
		score = min(move_scores)

	if cache is not None:
		cache[state_key] = score
	return score


def best_computer_move(pins, debug=False, use_cache=True, stats=None):
	"""Return the move with the best possible score for the computer."""
	states_checked = [0]
	unique_states = set()
	cache = {} if use_cache else None
	best_move = None
	best_score = -2

	# Evaluate each computer move by recursively looking ahead at the game.
	for move in legal_moves(pins):
		new_state = new_game_state(pins, move)
		score = minimax(
			new_state, False, states_checked, cache, unique_states
		)
		if score > best_score:
			best_score = score
			best_move = move

	if stats is not None:
		stats["calls"] = states_checked[0]
		stats["unique_states"] = len(unique_states)

	if debug:
		print(f"Minimax calls: {states_checked[0]}")
		print(f"Unique states: {len(unique_states)}")

	return best_move


def print_minimax_tree(pins=None, computer_turn=True, indent=""):
	"""Print a small game tree with each state's minimax value."""
	if pins is None:
		pins = [True, True, True]

	states_checked = [0]
	value = minimax(pins, computer_turn, states_checked)
	state_text = " ".join("|" if pin else "." for pin in pins)
	player = "computer" if computer_turn else "human"

	print(f"{indent}State {state_text} | {player} to move | value = {value}")

	if game_over(pins):
		print(f"{indent}  Terminal state")
		return

	for move in legal_moves(pins):
		child_state = new_game_state(pins, move)
		print(f"{indent}  Move {move}:")
		print_minimax_tree(child_state, not computer_turn, indent + "    ")


def get_move(pins, player):
	"""Read and validate one move from a player."""
	while True:
		try:
			start = int(input(f"{player}, choose the first pin: "))
			amount = int(input("Remove 1 or 2 pins? "))
		except ValueError:
			print("Please enter whole numbers.")
			continue

		if valid_move(pins, start, amount):
			return start, amount

		print("That is not a valid move. Choose available adjacent pins.")


def play_game(debug=False):
	"""Run one game with a human player against the computer."""
	pins = [True] * PIN_COUNT
	computer_turn = False

	print("Welcome to Kayles!")
	print("Choose a starting position and remove one pin or two adjacent pins.")
	print("You play first against the computer.")

	while not game_over(pins):
		print()
		show_row(pins)

		if computer_turn:
			move = best_computer_move(pins, debug)
			start, amount = move
			print(f"Computer removes {amount} pin(s) starting at position {start}.")
		else:
			move = get_move(pins, "You")
			start, amount = move

		remove_pins(pins, start, amount)

		if game_over(pins):
			winner = "Computer" if computer_turn else "You"
			print(f"\n{winner} removed the last pin and wins!")
			break

		computer_turn = not computer_turn


def print_move_examples():
	"""Print legal moves for a few useful example states."""
	examples = {
		"one group of 3": [True, True, True],
		"one group of 5": [True, True, True, True, True],
		"two separate groups": [True, True, False, True, True, True],
	}

	print("\nExample legal moves:")
	for name, pins in examples.items():
		print(f"{name}: {legal_moves(pins)}")


if __name__ == "__main__":
	print_move_examples()
	print("\nSmall minimax game tree (3 pins):")
	print_minimax_tree()
	play_game(DEBUG_MINIMAX)
