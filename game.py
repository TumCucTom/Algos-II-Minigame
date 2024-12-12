import pygame
import random

FRONT = 0
BACK = 1
LEFT = 2
RIGHT = 4

WALKING_1 = 0
STILL = 1
WALKING_2 = 2

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH, SCREEN_HEIGHT = 526, 595
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Resource Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
EARTHY_GREEN = (102, 153, 102)
EARTHY_BROWN = (139, 69, 19)
LIGHT_GREY = (211, 211, 211)

# Fonts
FONT = pygame.font.Font("8bit.ttf", 36)
BIG_FONT = pygame.font.Font('8bit.ttf', 60)

# Button class with rounded corners and dynamic content
class Button:
    def __init__(self, x, y, width, height, color, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.action = action
        self.radius = 20
        self.display_content = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=self.radius)
        
        # Calculate the total width of the content (text and images combined)
        total_width = 0
        if self.display_content:
            for item in self.display_content:
                if isinstance(item, str):
                    text_obj = FONT.render(item, True, self.text_color)
                    total_width += text_obj.get_width() + 5
                elif isinstance(item, pygame.Surface):
                    total_width += item.get_width() + 5

            # Calculate starting X position to center the content
            x_offset = self.rect.centerx - total_width // 2

            # Draw the content centered
            for item in self.display_content:
                if isinstance(item, str):
                    text_obj = FONT.render(item, True, self.text_color)
                    surface.blit(text_obj, (x_offset, self.rect.centery - text_obj.get_height() // 2))
                    x_offset += text_obj.get_width() + 5
                elif isinstance(item, pygame.Surface):
                    surface.blit(item, (x_offset, self.rect.centery - item.get_height() // 2))
                    x_offset += item.get_width() + 5

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def setup_sprite():
    spriteImages = [[0 for x in range(3)] for y in range(5)]

    #front
    spriteImages[FRONT][WALKING_1] = ('images/sprite/walking_front_1.png')
    spriteImages[FRONT][STILL] = ('images/sprite/still_front.png')
    spriteImages[FRONT][WALKING_2] = ('images/sprite/walking_front_2.png')

    #back
    spriteImages[BACK][WALKING_1] = ('images/sprite/walking_back_1.png')
    spriteImages[BACK][STILL] = ('images/sprite/still_back.png')
    spriteImages[BACK][WALKING_2] = ('images/sprite/walking_back_2.png')

    #left
    spriteImages[LEFT][WALKING_1] = ('images/sprite/walking_left_1.png')
    spriteImages[LEFT][STILL] = ('images/sprite/still_left.png')
    spriteImages[LEFT][WALKING_2] = ('images/sprite/walking_left_2.png')

    #right
    spriteImages[RIGHT][WALKING_1] = ('images/sprite/walking_right_1.png')
    spriteImages[RIGHT][STILL] = ('images/sprite/still_right.png')
    spriteImages[RIGHT][WALKING_2] = ('images/sprite/walking_right_2.png')

    return spriteImages

# Helper functions
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def trade_resources(resources, trade_from, trade_to, trade_amount, trade_to_amount):
    resources[trade_from] -= trade_amount
    resources[trade_to] += trade_to_amount
    return resources

def load_resource_image(resource):
    resource_images = {
        "wood": "images/wood.png",
        "bread": "images/bread.png",
        "stone": "images/stone.png",
        "gold": "images/gold.png",
        "sheep": "images/sheep.png"
    }
    image = pygame.image.load(resource_images[resource])
    return pygame.transform.scale(image, (30, 30))
    
def put_sprite_at(spriteImages, direction,state, pos):
     # Load and scale the resource image
    image_path = spriteImages[direction][state]
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (30, 30))

    # Blit the sprite
    screen.blit(image,pos)


def update_buttons(collect_button, trade_button, resource_to_collect, trade_to, trade_from, trade_to_amount, trade_amount):
    collect_button.display_content = ["+", load_resource_image(resource_to_collect)]
    trade_button.display_content = (
        ["+"] + [load_resource_image(trade_to)] * trade_to_amount +
        ["-"] + [load_resource_image(trade_from)] * trade_amount
    )

def display_game_over(resources):
    # Calculate final score as the sum of all resources
    final_score = sum(value ** 2 for value in resources.values())

    # Draw an earthy-colored box in the center of the screen
    box_width, box_height = 400, 200
    box_rect = pygame.Rect(
        (SCREEN_WIDTH - box_width) // 2,
        (SCREEN_HEIGHT - box_height) // 2,
        box_width,
        box_height
    )
    pygame.draw.rect(screen, EARTHY_BROWN, box_rect, border_radius=20)

    # Display final score
    draw_text(screen, "Game Over", BIG_FONT, WHITE, SCREEN_WIDTH // 2, box_rect.top + 60)
    draw_text(screen, f"Final Score: {final_score}", FONT, WHITE, SCREEN_WIDTH // 2, box_rect.top + 120)
    pygame.display.flip()

def draw_resource_box(x, y, resource, amount):
    # Define resource images
    resource_images = {
        "wood": "images/wood.png",
        "bread": "images/bread.png",
        "stone": "images/stone.png",
        "gold": "images/gold.png",
        "sheep": "images/sheep.png",
        "stall": "images/stall.png"
    }
    
    # Load and scale the resource image
    image_path = resource_images[resource]
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (30, 30))

    # Dimensions for the transparent box
    box_width = 70
    box_height = 50

    # Create the box with a thin black border
    box_rect = pygame.Rect(x, y, box_width, box_height)
    pygame.draw.rect(screen, LIGHT_GREY + (128,), box_rect, border_radius=10)  # Semi-transparent light grey
    pygame.draw.rect(screen, BLACK, box_rect, 2, border_radius=10)  # Black border

    # Blit the resource image in the box
    screen.blit(image, (x + 5, y + (box_height - image.get_height()) // 2))

    # Render the resource amount and center it
    amount_text = FONT.render(str(amount), True, BLACK)
    amount_text_rect = amount_text.get_rect(center=(x + box_width - 20, y + box_height // 2))
    screen.blit(amount_text, amount_text_rect)


def main():

    def animate_sprite_at(spriteImages, direction,state, pos1):
        # Load and scale the resource image
        image_path = spriteImages[direction][state]
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (30, 30))

        screen.fill(WHITE)
        screen.blit(bg_image, (0, 0))
        pygame.draw.rect(screen, LIGHT_GREY, (0, 0, SCREEN_WIDTH, 75))

        # Render resource boxes
        draw_resource_box(15, 15, "stall", min(round_num, 10))
        draw_resource_box(100, 15, "wood", resources["wood"])
        draw_resource_box(185, 15, "bread", resources["bread"])
        draw_resource_box(270, 15, "stone", resources["stone"])
        draw_resource_box(355, 15, "gold", resources["gold"])
        draw_resource_box(440, 15, "sheep", resources["sheep"])


        for pos in stall_character_positions:
            screen.blit(stall_image, pos[0])

        # Blit the sprite
        screen.blit(image,pos1)

        collect_button.draw(screen)
        trade_button.draw(screen)

        pygame.display.flip()
        pygame.time.wait(100)

    def move_sprite(spriteImages, stall_index):
        if stall_index == 1:
            animation1(spriteImages)
        elif stall_index == 2:
            animation2(spriteImages)
        elif stall_index == 3:
            animation3(spriteImages)
        elif stall_index == 4:
            animation4(spriteImages)
        elif stall_index == 5:
            animation5(spriteImages)
        elif stall_index == 6:
            animation6(spriteImages)
        elif stall_index == 7:
            animation7(spriteImages)
        elif stall_index == 8:
            animation8(spriteImages)
        elif stall_index == 9:
            animation9(spriteImages)

    def animation1(spriteImages):
        animate_sprite_at(spriteImages, RIGHT, STILL, (70,145))

        count = 0
        for step in range (75,95,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,145))
            count += 1

        animate_sprite_at(spriteImages, RIGHT, STILL, (100,145))
        animate_sprite_at(spriteImages, FRONT, STILL, (100,145))

        count = 0
        for step in range (150,280,5):
            animate_sprite_at(spriteImages, FRONT, count%3, (100,step))
            count += 1

        animate_sprite_at(spriteImages, FRONT, STILL, (100,280))
        animate_sprite_at(spriteImages, LEFT, STILL, (100,280))

        count = 0
        for step in range (5,65,5):
            animate_sprite_at(spriteImages, LEFT, count%3, (100-step,280))
            count +=1
        
        animate_sprite_at(spriteImages, LEFT, STILL, (35,280))


    def animation2(spriteImages):
        animate_sprite_at(spriteImages, FRONT, STILL, (35,280))

        count = 0
        for step in range (285,385,5):
            animate_sprite_at(spriteImages, FRONT, count%3, (35,step))
            count += 1
        
        animate_sprite_at(spriteImages, FRONT, STILL, (35,385))
        animate_sprite_at(spriteImages, RIGHT, STILL, (35,385))

        count = 0
        for step in range (40,75,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,385))
            count += 1

        animate_sprite_at(spriteImages, RIGHT, STILL, (75,385))
    
    def animation3(spriteImages):
        animate_sprite_at(spriteImages, BACK, STILL, (75,385))

        count = 0
        for step in range (5,65,5):
            animate_sprite_at(spriteImages, BACK, count%3, (75,385-step))
            count += 1
        
        animate_sprite_at(spriteImages, BACK, STILL, (75,320))
        animate_sprite_at(spriteImages, RIGHT, STILL, (75,320))

        count = 0
        for step in range (80,155,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,320))
            count += 1

        animate_sprite_at(spriteImages, RIGHT, STILL, (155,320))
        animate_sprite_at(spriteImages, BACK, STILL, (155,320))

    def animation4(spriteImages):
        animate_sprite_at(spriteImages, FRONT, STILL, (155,320))

        count = 0
        for step in range (325,355,5):
            animate_sprite_at(spriteImages, FRONT, count%3, (155,step))
            count += 1
        
        animate_sprite_at(spriteImages, FRONT, STILL, (155,360))
        animate_sprite_at(spriteImages, RIGHT, STILL, (155,360))

        count = 0
        for step in range (155,245,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,360))
            count += 1

        animate_sprite_at(spriteImages, RIGHT, STILL, (250,360))
        animate_sprite_at(spriteImages, BACK, STILL, (250,360))

        count = 0
        for step in range (5,50,5):
            animate_sprite_at(spriteImages, BACK, count%3, (250,360-step))
            count += 1

        animate_sprite_at(spriteImages, BACK, STILL, (250,310))
        animate_sprite_at(spriteImages, RIGHT, STILL, (250,310))

        count = 0
        for step in range (255,305,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,310))
            count += 1

        animate_sprite_at(spriteImages, RIGHT, STILL, (305,310))

    def animation5(spriteImages):
        animate_sprite_at(spriteImages, RIGHT, STILL, (305,310))

        count = 0
        for step in range (310,415,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,310))
            count += 1
        
        animate_sprite_at(spriteImages, RIGHT, STILL, (415,310))
        animate_sprite_at(spriteImages, BACK, STILL, (415,310))

        count = 0
        for step in range (5,130,5):
            animate_sprite_at(spriteImages, BACK, count%3, (415,310-step))
            count += 1

        animate_sprite_at(spriteImages, BACK, STILL, (415,180))
        animate_sprite_at(spriteImages, RIGHT, STILL, (415,180))

        count = 0
        for step in range (420,430,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,180))
            count += 1

        animate_sprite_at(spriteImages, RIGHT, STILL, (430,180))

    def animation6(spriteImages):
        animate_sprite_at(spriteImages, FRONT, STILL, (430,180))

        count = 0
        for step in range (185,410,5):
            animate_sprite_at(spriteImages, FRONT, count%3, (430, step))
            count += 1
        
        animate_sprite_at(spriteImages, FRONT, STILL, (430,410))
        animate_sprite_at(spriteImages, LEFT, STILL, (430,410))

        animate_sprite_at(spriteImages, LEFT, 0, (425,410))

    def animation7(spriteImages):
        animate_sprite_at(spriteImages, BACK, STILL, (425,410))

        count = 0
        for step in range (5,100,5):
            animate_sprite_at(spriteImages, BACK, count%3, (425,410-step))
            count += 1
        
        animate_sprite_at(spriteImages, BACK, STILL, (425,310))
        animate_sprite_at(spriteImages, LEFT, STILL, (425,310))

        count = 0
        for step in range (5,120,5):
            animate_sprite_at(spriteImages, LEFT, count%3, (425-step,310))
            count += 1

        animate_sprite_at(spriteImages, LEFT, STILL, (305,310))

    def animation8(spriteImages):
        animate_sprite_at(spriteImages, LEFT, STILL, (305,310))

        count = 0
        for step in range (5,55,5):
            animate_sprite_at(spriteImages, LEFT, count%3, (305-step,310))
            count += 1

        animate_sprite_at(spriteImages, LEFT, STILL, (250,310))
        animate_sprite_at(spriteImages, FRONT, STILL, (250,310))

        count = 0
        for step in range (315,360,5):
            animate_sprite_at(spriteImages, FRONT, count%3, (250,step))
            count += 1

        animate_sprite_at(spriteImages, FRONT, STILL, (250,360))
        animate_sprite_at(spriteImages, LEFT, STILL, (250,360))

        count = 0
        for step in range (5,95,5):
            animate_sprite_at(spriteImages, LEFT, count%3, (250-step,360))
            count += 1

        animate_sprite_at(spriteImages, LEFT, STILL, (155,360))
        animate_sprite_at(spriteImages, BACK, STILL, (155,360))

        count = 0
        for step in range (5,30,5):
            animate_sprite_at(spriteImages, BACK, count%3, (155,360-step))
            count += 1

        animate_sprite_at(spriteImages, BACK, STILL, (155,330))
        animate_sprite_at(spriteImages, LEFT, STILL, (155,330))

        count = 0
        for step in range (5,120,5):
            animate_sprite_at(spriteImages, LEFT, count%3, (155-step,330))
            count += 1

        animate_sprite_at(spriteImages, LEFT, STILL, (35,330))
        animate_sprite_at(spriteImages, BACK, STILL, (35,330))

        count = 0
        for step in range (5,50,5):
            animate_sprite_at(spriteImages, BACK, count%3, (35,330-step))
            count += 1

        animate_sprite_at(spriteImages, BACK, STILL, (35,280))

    def animation9(spriteImages):
        animate_sprite_at(spriteImages, RIGHT, STILL, (35,280))

        count = 0
        for step in range (40,100,5):
            animate_sprite_at(spriteImages, RIGHT, count%3, (step,280))
            count +=1

        animate_sprite_at(spriteImages, RIGHT, STILL, (100,280))
        animate_sprite_at(spriteImages, BACK, STILL, (100,280))

        count = 0
        for step in range (5,135,5):
            animate_sprite_at(spriteImages, BACK, count%3, (100,280-step))
            count += 1

        animate_sprite_at(spriteImages, BACK, STILL, (100,145))
        animate_sprite_at(spriteImages, LEFT, STILL, (100,145))

        count = 0
        for step in range (5,30,5):
            animate_sprite_at(spriteImages, LEFT, count%3, (100-step,145))
            count += 1

        animate_sprite_at(spriteImages, LEFT, STILL, (70,145))

    spriteImages = setup_sprite()

    resources = {
        "bread": 2,
        "wood": 2,
        "stone": 0,
        "gold": 0,
        "sheep": 0
    }

    round_num = 1
    game_over = False
    selected_action = None

    stall_character_positions = [
        ((45, 85),(70,145),BACK), 
        ((-20, 250),(35,280),LEFT),
        ((80, 360),(75,385),RIGHT), 
        ((130, 260),(155,320),BACK),
        ((278, 255),(305,310),BACK), 
        ((405,120),(430,180),BACK),
        ((365, 382),(425,410),LEFT),
        ((278, 255),(305,310),BACK), 
        ((-20, 250),(35,280),LEFT),
        ((45, 85),(70,145),BACK)
    ]

    collect_button = Button(135, SCREEN_HEIGHT - 135, 150, 50, EARTHY_BROWN, WHITE, "collect")
    trade_button = Button(50, SCREEN_HEIGHT - 75, 300, 50, EARTHY_BROWN, WHITE, "trade")

    stall_image = pygame.image.load("images/stall.png")
    stall_image = pygame.transform.scale(stall_image, (80, 80))

    bg_image = pygame.image.load("images/bg.jpg")
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    stall_index = 0


    resource_to_collect = random.choice(list(resources.keys()))
    trade_from = random.choice([res for res in resources if resources[res] > 0])
    trade_to = random.choice([res for res in resources if res != trade_from])
    trade_amount = random.randint(1, min(3, resources[trade_from]))
    trade_to_amount = random.randint(2, 4)

    update_buttons(collect_button, trade_button, resource_to_collect, trade_to, trade_from, trade_to_amount, trade_amount)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if collect_button.is_clicked(event.pos):
                    selected_action = "collect"
                elif trade_button.is_clicked(event.pos):
                    selected_action = "trade"

        if selected_action:
            if selected_action == "collect":
                if resources[resource_to_collect] < 10:
                    resources[resource_to_collect] += 1

                    resource_to_collect = random.choice(list(resources.keys()))
                    trade_from = random.choice([res for res in resources if resources[res] > 0])
                    trade_to = random.choice([res for res in resources if res != trade_from])
                    trade_amount = random.randint(1, min(3, resources[trade_from]))
                    trade_to_amount = random.randint(2, 4)

                    while resources[resource_to_collect] == 10 and resources[trade_to] + trade_to_amount > 10:
                        resource_to_collect = random.choice(list(resources.keys()))
                        trade_from = random.choice([res for res in resources if resources[res] > 0])
                        trade_to = random.choice([res for res in resources if res != trade_from])
                        trade_amount = random.randint(1, min(3, resources[trade_from]))
                        trade_to_amount = random.randint(2, 4)

                    round_num += 1
                    stall_index = (stall_index + 1) % len(stall_character_positions)
                    update_buttons(collect_button, trade_button, resource_to_collect, trade_to, trade_from, trade_to_amount, trade_amount)
                    selected_action = None

                    move_sprite(spriteImages,stall_index)

            elif selected_action == "trade":
                if resources[trade_from] >= trade_amount:
                    if resources[trade_to] + trade_to_amount <= 10:
                        resources = trade_resources(resources, trade_from, trade_to, trade_amount, trade_to_amount)

                        resource_to_collect = random.choice(list(resources.keys()))
                        trade_from = random.choice([res for res in resources if resources[res] > 0])
                        trade_to = random.choice([res for res in resources if res != trade_from])
                        trade_amount = random.randint(1, min(3, resources[trade_from]))
                        trade_to_amount = random.randint(2, 4)

                        while resources[resource_to_collect] == 10 and resources[trade_to] + trade_to_amount > 10:
                            resource_to_collect = random.choice(list(resources.keys()))
                            trade_from = random.choice([res for res in resources if resources[res] > 0])
                            trade_to = random.choice([res for res in resources if res != trade_from])
                            trade_amount = random.randint(1, min(3, resources[trade_from]))
                            trade_to_amount = random.randint(2, 4)

                        round_num += 1
                        stall_index = (stall_index + 1) % len(stall_character_positions)
                        update_buttons(collect_button, trade_button, resource_to_collect, trade_to, trade_from, trade_to_amount, trade_amount)
                        selected_action = None

                        move_sprite(spriteImages,stall_index)

        if round_num > 10:
            display_game_over(resources)
            break

        screen.fill(WHITE)
        screen.blit(bg_image, (0, 0))
        pygame.draw.rect(screen, LIGHT_GREY, (0, 0, SCREEN_WIDTH, 75))

        # Render resource boxes
        draw_resource_box(15, 15, "stall", min(round_num, 10))
        draw_resource_box(100, 15, "wood", resources["wood"])
        draw_resource_box(185, 15, "bread", resources["bread"])
        draw_resource_box(270, 15, "stone", resources["stone"])
        draw_resource_box(355, 15, "gold", resources["gold"])
        draw_resource_box(440, 15, "sheep", resources["sheep"])


        for pos in stall_character_positions:
            screen.blit(stall_image, pos[0])

        state = stall_character_positions[stall_index]
        put_sprite_at(spriteImages,state[2],STILL, state[1])

        collect_button.draw(screen)
        trade_button.draw(screen)

        pygame.display.flip()
        pygame.time.wait(300)

    pygame.time.wait(10000)
    pygame.quit()

if __name__ == "__main__":
    main()
