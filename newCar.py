import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
car_initial_speed = 2
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 100
TRACK_MARGIN = WIDTH * 0.15  # 15% margin from both sides
CAR_AREA_WIDTH = WIDTH * 0.7  # 70% of the track width

# Spacing constants
MIN_VERTICAL_SPACING = CAR_HEIGHT + 50  # Minimum vertical spacing between cars
MIN_HORIZONTAL_SPACING = CAR_WIDTH + 30  # Minimum horizontal spacing between cars

# Load images
track_img = pygame.image.load('Images/Track.png')
track_img = pygame.transform.scale(track_img, (WIDTH, HEIGHT))

player_car_img = pygame.image.load('Images/Red Car.png')
blue_car_img = pygame.image.load('Images/Blue Car.png')
yellow_car_img = pygame.image.load('Images/Yellow Car.png')
green_car_img = pygame.image.load('Images/Green Car.png')

player_car_img = pygame.transform.scale(player_car_img, (CAR_WIDTH, CAR_HEIGHT))
blue_car_img = pygame.transform.scale(blue_car_img, (CAR_WIDTH, CAR_HEIGHT))
yellow_car_img = pygame.transform.scale(yellow_car_img, (CAR_WIDTH, CAR_HEIGHT))
green_car_img = pygame.transform.scale(green_car_img, (CAR_WIDTH, CAR_HEIGHT))

# Load background music
pygame.mixer.music.load('Music/DRIVE(chosic.com).mp3')  # Replace with your file path
pygame.mixer.music.play(-1)  # Loop the music infinitely
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)

# Car class
class Car:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.speed = car_initial_speed
        # Default speed for opponent cars
        self.image = image

    def move(self, is_opponent=False):
        if is_opponent:
            self.y += self.speed  # Opponent cars move downward
        else:
            self.y -= self.speed  # Player car moves upward

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# Function to check collision
def check_collision(car1, car2):
    car1_rect = pygame.Rect(car1.x, car1.y, CAR_WIDTH, CAR_HEIGHT)
    car2_rect = pygame.Rect(car2.x, car2.y, CAR_WIDTH, CAR_HEIGHT)
    return car1_rect.colliderect(car2_rect)

# Function to show game over screen
def game_over_screen(score, high_score):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    screen.fill((0, 0, 0))
    
    text_game_over = font.render("Game Over", True, (255, 0, 0))
    text_score = font.render(f"Score: {int(score)} meters", True, (255, 255, 255))
    text_high_score = font.render(f"High Score: {int(high_score)} meters", True, (255, 255, 0))
    play_again_text = small_font.render("Press Enter to Play Again", True, (255, 255, 255))

    screen.blit(text_game_over, (WIDTH // 2 - text_game_over.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(text_score, (WIDTH // 2 - text_score.get_width() // 2, HEIGHT // 2 - 20))
    screen.blit(text_high_score, (WIDTH // 2 - text_high_score.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(play_again_text, (WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2 + 160))

    pygame.display.flip()

# Function to generate opponent cars with no overlap
def generate_opponent_cars(num_cars):
    cars = []
    while len(cars) < num_cars:
        new_x = random.randint(int(TRACK_MARGIN), int(WIDTH - TRACK_MARGIN - CAR_WIDTH))
        new_y = random.randint(-600, -100)

        # Check overlap with existing cars
        overlap = False
        for car in cars:
            if abs(new_x - car.x) < MIN_HORIZONTAL_SPACING and abs(new_y - car.y) < MIN_VERTICAL_SPACING:
                overlap = True
                break
        
        if not overlap:
            new_car = Car(new_x, new_y, random.choice([blue_car_img, yellow_car_img, green_car_img]))
            cars.append(new_car)
    return cars

# Function to respawn opponent car without overlap
def respawn_opponent_car(car, cars):
    while True:
        new_x = random.randint(int(TRACK_MARGIN), int(WIDTH - TRACK_MARGIN - CAR_WIDTH))
        new_y = random.randint(-600, -100)
        overlap = False

        # Check for overlap with other cars
        for other_car in cars:
            if other_car != car and abs(new_x - other_car.x) < MIN_HORIZONTAL_SPACING and abs(new_y - other_car.y) < MIN_VERTICAL_SPACING:
                overlap = True
                break

        if not overlap:
            car.x = new_x
            car.y = new_y
            break

# Persistent high score
high_score = 0

# Load the background image for the score
score_bg_img = pygame.image.load('Images/scoreBoard.png')
score_bg_img = pygame.transform.scale(score_bg_img, (150, 230))  # Keep the size as 150x230

# Function to display real-time score with a background
def show_score(screen, score, font):
    score_bg_x, score_bg_y = 30, -80  # Adjusted closer to the top
    score_text = font.render(f"{int(score)} Meter", True, (255, 255, 255))
    
    # Blit the background image
    screen.blit(score_bg_img, (score_bg_x, score_bg_y))
    
    # Blit the score text on top of the background, centered
    text_x = score_bg_x + (score_bg_img.get_width() - score_text.get_width()) // 2
    text_y = score_bg_y + (score_bg_img.get_height() - score_text.get_height()) // 2
    screen.blit(score_text, (text_x, text_y))


# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Car Racing Game")
clock = pygame.time.Clock()

# Game logic
def run_game():
    global high_score

    player_car = Car(WIDTH // 2, HEIGHT - 120, player_car_img)
    opponent_cars = generate_opponent_cars(6)  # Ensure no overlap when creating opponent cars

    track_offset = 0
    track_cycles = 0
    max_cycles = 100
    distance = 0  # Distance traveled in meters
    font = pygame.font.Font(None, 36)

    running = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if not running and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return run_game()  # Restart the game

        if running:
            # Handle player input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player_car.y > 0:  # Ensure the car doesn't go off the top
                player_car.speed = 5  # Move forward
            elif keys[pygame.K_DOWN] and player_car.y < HEIGHT - CAR_HEIGHT:  # Ensure the car doesn't go off the bottom
                player_car.speed = -5  # Move backward
            else:
                player_car.speed = 0  # Stop vertical movement

            if keys[pygame.K_LEFT] and player_car.x > TRACK_MARGIN:
                player_car.x -= 5
            if keys[pygame.K_RIGHT] and player_car.x < WIDTH - TRACK_MARGIN - CAR_WIDTH:
                player_car.x += 5

            # Update track offset for scrolling
            track_offset += 5
            if track_offset >= HEIGHT:
                track_offset = 0
                track_cycles += 1
            
            # Initial game speed
            game_speed = car_initial_speed


            # Update distance
            distance += 0.1  # Increment distance (1 cycle = 10 meters)
            
            # Increase speed every 100 meters
            print("Car speed : ", game_speed)
            if int(distance) % 100 == 0 and distance > 0:
                game_speed += 5  # Increase player car base speed
                print("I am into the condition")
            
            print("Car speed : ", game_speed)

            # End game after given cycles
            if track_cycles >= max_cycles:
                running = False

            # Update positions
            player_car.move()
            for opponent in opponent_cars:
                opponent.move(is_opponent=True)
                if opponent.y > HEIGHT:
                    respawn_opponent_car(opponent, opponent_cars)  # Respawn car without overlap

            # Collision detection
            for opponent in opponent_cars:
                if check_collision(player_car, opponent):
                    running = False
                    break

            # Drawing
            screen.blit(track_img, (0, track_offset - HEIGHT))  # Top part of the track
            screen.blit(track_img, (0, track_offset))  # Bottom part of the track

            for opponent in opponent_cars:
                opponent.draw(screen)
            player_car.draw(screen)
            
            # Display real-time score
            show_score(screen, distance, font)

            pygame.display.flip()
            clock.tick(FPS)
        else:
            if distance > high_score:
                high_score = distance  # Update high score only if the new score is greater
            game_over_screen(distance, high_score)

run_game()
