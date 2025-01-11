import random
from django.shortcuts import render
from django.http import JsonResponse

# Directions for snake movement
DIRECTIONS = {
    'UP': (0, -20),
    'DOWN': (0, 20),
    'LEFT': (-20, 0),
    'RIGHT': (20, 0)
}

# Game page view
def game_page(request):
    return render(request, 'pro/index.html')

# Start game view
def start_game(request):
    """Initialize the game state."""
    snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake positions
    direction = 'RIGHT'
    apple = generate_apple(snake)
    game_state = {
        'snake': snake,
        'apple': apple,
        'direction': direction,
        'score': 0,
        'level': 1,  # Start at level 1
        'eaten_apples': 0,  # Track the number of apples eaten
        'blocks': []  # No blocks in level 1
    }
    return JsonResponse(game_state)

# Move snake view (updates snake and game state)
def move_snake(request):
    """Update the snake's position and handle collisions."""
    # Get data from the request
    snake = [tuple(map(int, seg.split(','))) for seg in request.GET.get('snake', '').split(';')]
    direction = request.GET.get('direction', 'RIGHT')
    apple = tuple(map(int, request.GET.get('apple', '').split(',')))
    score = int(request.GET.get('score', 0))
    level = int(request.GET.get('level', 1))
    eaten_apples = int(request.GET.get('eaten_apples', 0))
    blocks = request.GET.get('blocks', '').split(';') if level == 2 else []

    head = snake[0]
    dx, dy = DIRECTIONS[direction]
    new_head = (head[0] + dx, head[1] + dy)

    # Check for collision with walls
    if new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 400:
        return JsonResponse({'gameOver': True, 'level': level})

    # Check for collision with the snake itself
    if new_head in snake:
        return JsonResponse({'gameOver': True, 'level': level})

    # Check for collision with puzzle blocks in Level 2
    if level == 2 and new_head in blocks:
        return JsonResponse({'gameOver': True, 'level': level})

    # Check for collision with the apple
    if new_head == apple:
        snake.append(snake[-1])  # Grow snake
        apple = generate_apple(snake)  # Generate new apple
        score += 10  # Increase score
        eaten_apples += 1  # Increase apples eaten

        # If the player eats 7 apples, promote to level 2
        if eaten_apples >= 7 and level == 1:
            level = 2
            blocks = generate_blocks(snake)  # Generate blocks for Level 2
    else:
        snake = [new_head] + snake[:-1]  # Move snake forward

    # Return updated game state
    return JsonResponse({
        'snake': snake,
        'apple': apple,
        'direction': direction,
        'score': score,
        'level': level,
        'eaten_apples': eaten_apples,
        'blocks': blocks,  # Return puzzle blocks in level 2
        'gameOver': False
    })

# Function to generate a random apple
def generate_apple(snake):
    """Generate a new apple at a random position."""
    while True:
        apple = (random.randint(0, 29) * 20, random.randint(0, 19) * 20)
        if apple not in snake:
            break
    return apple

# Function to generate puzzle blocks in Level 2
def generate_blocks(snake):
    """Generate obstacles (blocks) for Level 2."""
    blocks = []
    while len(blocks) < 5:  # Let's add 5 blocks in Level 2
        block = (random.randint(0, 29) * 20, random.randint(0, 19) * 20)
        if block not in snake and block not in blocks:
            blocks.append(block)
    return blocks

































# from django.shortcuts import render
# from django.http import JsonResponse
# import random

# def game_page(request):
    
#     return render(request, 'pro/index.html')

# DIRECTIONS = {
#     'UP': (0, -20),
#     'DOWN': (0, 20),
#     'LEFT': (-20, 0),
#     'RIGHT': (20, 0)
# }

# def start_game(request):
#     """Initialize the game state."""
#     snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake positions
#     direction = 'RIGHT'
#     apple = generate_apple(snake)
#     game_state = {'snake': snake, 'apple': apple, 'direction': direction, 'score': 0}
#     return JsonResponse(game_state)

# def move_snake(request):
#     """Update the snake's position and handle collisions."""
#     snake = [tuple(map(int, seg.split(','))) for seg in request.GET.get('snake', '').split(';')]
#     direction = request.GET.get('direction', 'RIGHT')
#     apple = tuple(map(int, request.GET.get('apple', '').split(',')))
#     score = int(request.GET.get('score', 0))

#     head = snake[0]
#     dx, dy = DIRECTIONS[direction]
#     new_head = (head[0] + dx, head[1] + dy)

#     # Check for collision with the walls
#     if new_head[0] < 0 or new_head[0] >= 600 or new_head[1] < 0 or new_head[1] >= 400:
#         return JsonResponse({'gameOver': True})

#     # Check for collision with the snake itself
#     if new_head in snake:
#         return JsonResponse({'gameOver': True})

#     # Check for collision with the apple
#     if new_head == apple:
#         snake.append(snake[-1])  # Grow snake
#         apple = generate_apple(snake)
#         score += 10
#     else:
#         snake = [new_head] + snake[:-1]

#     return JsonResponse({'snake': snake, 'apple': apple, 'direction': direction, 'score': score, 'gameOver': False})

# def generate_apple(snake):
#     """Generate a new apple at a random position."""
#     while True:
#         apple = (random.randint(0, 29) * 20, random.randint(0, 19) * 20)  # Adjusted for grid size
#         if apple not in snake:
#             break
#     return apple
