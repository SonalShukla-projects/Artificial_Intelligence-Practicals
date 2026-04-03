# Sonal Shukla CS23176

def alpha_beta_pruning(game_values):
   
    # Alpha stores the best value for MAX player
    alpha_value = -1000
   
    # Beta stores the best value for MIN player
    beta_value = 1000

    # MAX player checks all possible game values
    for current_value in game_values:
       
        # Update alpha if a better value is found
        if current_value > alpha_value:
            alpha_value = current_value
       
        # Pruning condition:
        # If alpha is greater than or equal to beta,
        # further checking is not needed
        if alpha_value >= beta_value:
            break

    # Return the best value for MAX player
    return alpha_value


# Game leaf node values (possible scores)
game_values = [3, 5, 6, 9, 1, 2]

# Find the best move using Alpha–Beta Pruning
best_move_value = alpha_beta_pruning(game_values)

# Display the result
print("Best move value:", best_move_value)