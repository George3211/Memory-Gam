import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Memory Game")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Square dimensions
square_size = 100
margin = 10

# Function to resize images
def load_and_resize_images(image_names, new_size):
    resized_images = {}
    for name in image_names:
        try:
            image = pygame.image.load(f"images/{name}")
            resized_images[name] = pygame.transform.scale(image, new_size)
        except pygame.error as e:
            print(f"Error loading or resizing image {name}: {e}")
    return resized_images

# Load and resize images
image_names = [
    "aluminum.png", "beryllium.png", "boron.png", "carbon.png",
    "fluorine.png", "helium.png", "hydrogen.png", "lithium.png",
    "magnesium.png", "neon.png", "nitrogen.png", "oxygen.png"
]
images = load_and_resize_images(image_names, (square_size, square_size))

# Generate positions for squares
def generate_positions(rows, cols, square_size, margin):
    positions = []
    for row in range(rows):
        for col in range(cols):
            x = col * (square_size + margin) + margin
            y = row * (square_size + margin) + margin
            positions.append((x, y))
    return positions

# Main game logic
def main():
    rows, cols = 4, 6
    positions = generate_positions(rows, cols, square_size, margin)
    
    # Shuffle and pair images
    all_images = list(images.keys()) * 2
    random.shuffle(all_images)
    
    card_mapping = {i: all_images[i] for i in range(len(positions))}
    flipped = [False] * len(positions)
    matched = [False] * len(positions)
    
    first_card = None
    second_card = None
    check_time = 0
    running = True

    while running:
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds

        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and check_time == 0:
                if first_card is None or second_card is None:
                    mouse_x, mouse_y = event.pos
                    for i, pos in enumerate(positions):
                        x, y = pos
                        if (
                            x < mouse_x < x + square_size
                            and y < mouse_y < y + square_size
                            and not flipped[i]
                            and not matched[i]
                        ):
                            flipped[i] = True
                            if first_card is None:
                                first_card = i
                            elif second_card is None:
                                second_card = i

        # Check for match logic
        if first_card is not None and second_card is not None and check_time == 0:
            if card_mapping[first_card] == card_mapping[second_card]:
                matched[first_card] = True
                matched[second_card] = True
                first_card = None
                second_card = None
            else:
                check_time = current_time + 1000  # Set a 1-second delay

        # If the delay is active, flip back the cards after the time has passed
        if check_time > 0 and current_time >= check_time:
            flipped[first_card] = False
            flipped[second_card] = False
            first_card = None
            second_card = None
            check_time = 0

        # Draw the cards
        for i, pos in enumerate(positions):
            x, y = pos
            if matched[i] or flipped[i]:
                image_name = card_mapping[i]
                screen.blit(images[image_name], (x, y))
            else:
                pygame.draw.rect(screen, GRAY, (x, y, square_size, square_size))

        # Check for win condition
        if all(matched):
            print("You Win!")
            running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
