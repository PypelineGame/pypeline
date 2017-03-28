import pygame
def healthPoints(x, y, point):
    if point < 0:
        point = 0
    healthTotal = 100
    healthWidth = 10
    color = (point/100) * healthTotal
    colorAround = pygame.Rect(x, y, healthTotal, healthWidth)
    colorIn = pygame.Rect(x, y, color, healthWidth)
    pygame.draw.rect(p1, RED, colorIn)
    pygame.draw.rect(p1, WHITE, colorAround, 2)
    pygame.draw.rect(p2, RED, colorIn)
    pygame.draw.rect(p2, WHITE, colorAround, 2)
    
    
timeSeconds = 240 
pygame.time.set_timer(USEREVENT+1, 1000) 

#everything below this line should be in your main loop
for event in pygame.event.get():
    if event.type == USEREVENT+1:
        time -= 1

if timeSeconds == 0:
    print "GAME OVER"
    

 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
 
pygame.init()
 
# Set the height and width of the screen
size = [700, 500]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Game Over Example")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Starting position of the rectangle
rect_x = 50
rect_y = 50
 
# Speed and direction of rectangle
rect_change_x = 5
rect_change_y = 5
 
# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
 
# Use this boolean variable to trigger if the game is over.
game_over = False
 
# -------- Main Program Loop -----------
while not done:
 
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        # We will use a mouse-click to signify when the game is
        # over. Replace this, and set game_over to true in your
        # own game when you know the game is over. (Like lives==0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game_over = True
 
    # --- Game Logic
 
    # Only move and process game logic if the game isn't over.
    if not game_over:
        # Move the rectangle starting point
        rect_x += rect_change_x
        rect_y += rect_change_y
 
        # Bounce the ball if needed
        if rect_y > 450 or rect_y < 0:
            rect_change_y = rect_change_y * -1
        if rect_x > 650 or rect_x < 0:
            rect_change_x = rect_change_x * -1
 
    # --- Draw the frame
 
    # Set the screen background
    screen.fill(BLACK)
 
    # Draw the rectangle
    pygame.draw.rect(screen, GREEN, [rect_x, rect_y, 50, 50])
 
    if game_over:
        # If game over is true, draw game over
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])
 
    else:
        # If game isn't over, draw this stuff.
        text = font.render("Click to end game", True, WHITE)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])
 
    # Limit frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()
