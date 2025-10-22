import pygame, sys, random, time, math

pygame.init()

# Screen settings
width, height = 600, 470
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Incremental Training Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)
LIGHT_BLUE = (100, 150, 255)
DARK_BLUE = (50, 100, 200)
GREEN = (100, 255, 100)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
PURPLE = (200, 100, 255)

# Fonts
font_small = pygame.font.Font(None, 18)
font_medium = pygame.font.Font(None, 24)
font_large = pygame.font.Font(None, 32)

# Game state
class GameState:
    def __init__(self):
        # Core values
        self.value = 0  # Current value (spendable)
        self.total_value = 0  # Total value earned (for rebirth cost)
        self.value_per_second = 1000
        self.multiplier = 1.0
        
        # Stats
        self.strength = 0
        self.endurance = 0
        self.agility = 0
        self.speed = 0
        self.meditation = 0
        
        # Progression
        self.current_page = "strength"  # strength, endurance, agility, speed, meditation, rebirth, ascension
        self.rebirth_count = 0
        self.ascension_count = 0
        
        # Auto-training
        self.auto_training = False
        self.auto_training_stat = None
        
        # Progress bars
        self.progress_bars = {
            "strength": {"current": 0, "max": 1000, "level": 1},
            "endurance": {"current": 0, "max": 1000, "level": 1},
            "agility": {"current": 0, "max": 1000, "level": 1},
            "speed": {"current": 0, "max": 1000, "level": 1},
            "meditation": {"current": 0, "max": 1000, "level": 1}
        }
        
        # Classes
        self.current_class = "noob"
        self.classes = {
            "noob": {"multiplier": 1, "rebirth_req": 100000, "ascension_req": 0, "ascension_unlock": 0},
            "noober": {"multiplier": 2, "rebirth_req": 500000, "ascension_req": 0, "ascension_unlock": 0},
            "noob_beginner": {"multiplier": 4, "rebirth_req": 2000000, "ascension_req": 0, "ascension_unlock": 0},
            "noober_beginner": {"multiplier": 7, "rebirth_req": 10000000, "ascension_req": 5, "ascension_unlock": 1},
            "noob_good": {"multiplier": 12, "rebirth_req": 50000000, "ascension_req": 10, "ascension_unlock": 1},
            "noober_good": {"multiplier": 18, "rebirth_req": 200000000, "ascension_req": 20, "ascension_unlock": 2},
            "noob_pro": {"multiplier": 25, "rebirth_req": 1000000000, "ascension_req": 50, "ascension_unlock": 2},
            "noober_pro": {"multiplier": 33, "rebirth_req": 5000000000, "ascension_req": 100, "ascension_unlock": 3}
        }
        
        # Time tracking
        self.last_time = time.time()
        self.start_time = time.time()

game_state = GameState()

def abbreviate_number(num):
    if num < 1000:
        return str(int(num))
    
    suffixes = ["", "K", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No", "Dc", "UDc", "DDc", "TDc", "QaDc", "QiDc", "SxDc", "SpDc", "OcDc", "NoDc", "Vi", "UVi", "DVi", "TVi", "QaVi", "QiVi", "SxVi", "SpVi", "OcVi", "NoVi", "Tr", "UTr", "DTr", "TTr", "QaTr", "QiTr", "SxTr", "SpTr", "OcTr", "NoTr", "Qa", "UQa", "DQa", "TQa", "QQa", "QiQa", "SxQa", "SpQa", "OcQa", "NoQa", "Qi", "UQi", "DQi", "TQi", "QQi", "QiQi", "SxQi", "SpQi", "OcQi", "NoQi", "Sx", "USx", "DSx", "TSx", "QSx", "QiSx", "SxSx", "SpSx", "OcSx", "NoSx", "Sp", "USp", "DSp", "TSp", "QSp", "QiSp", "SxSp", "SpSp", "OcSp", "NoSp", "Oc", "UOc", "DOc", "TOc", "QOc", "QiOc", "SxOc", "SpOc", "OcOc", "NoOc", "No", "UNo", "DNo", "TNo", "QNo", "QiNo", "SxNo", "SpNo", "OcNo", "NoNo", "Ce"]
    
    magnitude = 0
    while num >= 1000 and magnitude < len(suffixes) - 1:
        num /= 1000
        magnitude += 1
    
    return f"{num:.2f}{suffixes[magnitude]}".rstrip("0").rstrip(".")

def create_lines():
    # Vertical dividers
    pygame.draw.line(screen, WHITE, (120, 0), (120, height), 2)  # Left line
    pygame.draw.line(screen, WHITE, (480, 0), (480, height), 2)  # Right line
    # Horizontal divider
    pygame.draw.line(screen, WHITE, (0, 40), (width, 40), 2)  # Top line

def draw_progress_bar(x, y, width, height, current, max_val, color=GREEN):
    # Background
    pygame.draw.rect(screen, DARK_GRAY, (x, y, width, height))
    # Fill
    if max_val > 0:
        fill_width = int((current / max_val) * width)
        pygame.draw.rect(screen, color, (x, y, fill_width, height))
    # Border
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)

def draw_button(x, y, width, height, text, color=GRAY, text_color=BLACK, hover_color=DARK_GRAY):
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = (x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height)
    
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=8)
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2, border_radius=8)
    
    text_surface = font_medium.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surface, text_rect)
    
    return is_hovered

def draw_navigation_buttons():
    button_labels = ["Str", "End", "Agi", "Spd", "Med", "Reb", "Asc"]
    full_labels = ["Strength", "Endurance", "Agility", "Speed", "Meditation", "Rebirth", "Ascension"]
    button_width = 100
    button_height = 30
    start_x = 10
    start_y = 50
    
    for i, (label, full_label) in enumerate(zip(button_labels, full_labels)):
        x = start_x
        y = start_y + i * (button_height + 5)
        
        # Highlight current page
        color = LIGHT_BLUE if game_state.current_page.lower() == full_label.lower() else GRAY
        text_color = WHITE if game_state.current_page.lower() == full_label.lower() else BLACK
        
        is_hovered = draw_button(x, y, button_width, button_height, label, color, text_color)
        
        if is_hovered and pygame.mouse.get_pressed()[0]:
            game_state.current_page = full_label.lower()

def draw_main_content():
    if game_state.current_page in ["strength", "endurance", "agility", "speed", "meditation"]:
        draw_stat_page(game_state.current_page)
    elif game_state.current_page == "rebirth":
        draw_rebirth_page()
    elif game_state.current_page == "ascension":
        draw_ascension_page()
    
    # Turn off auto-training when switching pages
    if game_state.current_page not in ["strength", "endurance", "agility", "speed", "meditation"]:
        game_state.auto_training = False
        game_state.auto_training_stat = None

def draw_stat_page(stat_name):
    # Title
    title_text = stat_name.title()
    title_surface = font_large.render(title_text, True, WHITE)
    screen.blit(title_surface, (130, 80))
    
    # Current value
    stat_value = getattr(game_state, stat_name)
    value_text = f"{stat_name}: {abbreviate_number(stat_value)}"
    value_surface = font_medium.render(value_text, True, WHITE)
    screen.blit(value_surface, (130, 110))
    
    # Progress bar
    bar_data = game_state.progress_bars[stat_name]
    bar_x, bar_y = 130, 140
    bar_width, bar_height = 340, 25
    
    draw_progress_bar(bar_x, bar_y, bar_width, bar_height, bar_data["current"], bar_data["max"])
    
    # Progress text
    progress_text = f"Lv{bar_data['level']}: {abbreviate_number(bar_data['current'])}/{abbreviate_number(bar_data['max'])}"
    progress_surface = font_small.render(progress_text, True, WHITE)
    screen.blit(progress_surface, (130, 175))
    
    # Click to train button
    train_button_hovered = draw_button(130, 200, 120, 35, f"Train", GREEN, WHITE)
    
    if train_button_hovered and pygame.mouse.get_pressed()[0]:
        # Add progress to the bar
        bar_data["current"] += 100 * game_state.multiplier
        
        # Check for level up
        if bar_data["current"] >= bar_data["max"]:
            bar_data["level"] += 1
            bar_data["current"] = 0
            bar_data["max"] = int(bar_data["max"] * 1.5)  # Increase max for next level
            setattr(game_state, stat_name, getattr(game_state, stat_name) + 1)
            # Add to total value when leveling up
            game_state.total_value += 1000 * game_state.multiplier
    
    # Auto-train toggle
    auto_text = "Auto: ON" if game_state.auto_training and game_state.auto_training_stat == stat_name else "Auto: OFF"
    auto_color = GREEN if game_state.auto_training and game_state.auto_training_stat == stat_name else WHITE
    auto_surface = font_small.render(auto_text, True, auto_color)
    screen.blit(auto_surface, (130, 250))
    
    # Auto-train button
    auto_button_hovered = draw_button(130, 280, 120, 35, "Toggle Auto", YELLOW, BLACK)
    
    if auto_button_hovered and pygame.mouse.get_pressed()[0]:
        if game_state.auto_training and game_state.auto_training_stat == stat_name:
            # Turn off auto-training
            game_state.auto_training = False
            game_state.auto_training_stat = None
        else:
            # Turn on auto-training for this stat
            game_state.auto_training = True
            game_state.auto_training_stat = stat_name

def draw_rebirth_page():
    # Title
    title_surface = font_large.render("Rebirth", True, WHITE)
    screen.blit(title_surface, (130, 80))
    
    # Current rebirth count
    rebirth_text = f"Rebirths: {game_state.rebirth_count}"
    rebirth_surface = font_medium.render(rebirth_text, True, WHITE)
    screen.blit(rebirth_surface, (130, 110))
    
    # Rebirth requirements
    current_class_data = game_state.classes[game_state.current_class]
    req_text = f"Cost: {abbreviate_number(current_class_data['rebirth_req'])} total value"
    req_surface = font_small.render(req_text, True, WHITE)
    screen.blit(req_surface, (130, 140))
    
    # Current total value
    value_text = f"Have: {abbreviate_number(game_state.total_value)}"
    value_surface = font_small.render(value_text, True, WHITE)
    screen.blit(value_surface, (130, 160))
    
    # Rebirth button
    can_rebirth = game_state.total_value >= current_class_data['rebirth_req']
    button_color = GREEN if can_rebirth else DARK_GRAY
    rebirth_button_hovered = draw_button(130, 190, 120, 35, "Rebirth", button_color, WHITE)
    
    if rebirth_button_hovered and pygame.mouse.get_pressed()[0] and can_rebirth:
        # Perform rebirth
        game_state.rebirth_count += 1
        game_state.value = 0
        game_state.total_value = 0  # Reset total value
        game_state.multiplier = current_class_data['multiplier']
        
        # Reset stats but keep some progress
        for stat in game_state.progress_bars:
            game_state.progress_bars[stat]["current"] = 0
            game_state.progress_bars[stat]["level"] = 1
            game_state.progress_bars[stat]["max"] = 1000
        
        # Update class if possible
        for class_name, class_data in game_state.classes.items():
            if game_state.rebirth_count >= class_data['rebirth_req'] and game_state.ascension_count >= class_data['ascension_unlock']:
                game_state.current_class = class_name

def draw_ascension_page():
    # Title
    title_surface = font_large.render("Ascension", True, WHITE)
    screen.blit(title_surface, (130, 80))
    
    # Current ascension count
    ascension_text = f"Ascensions: {game_state.ascension_count}"
    ascension_surface = font_medium.render(ascension_text, True, WHITE)
    screen.blit(ascension_surface, (130, 110))
    
    # Ascension requirements
    current_class_data = game_state.classes[game_state.current_class]
    req_text = f"Cost: {current_class_data['ascension_req']} rebirths"
    req_surface = font_small.render(req_text, True, WHITE)
    screen.blit(req_surface, (130, 140))
    
    # Current rebirths
    rebirth_text = f"Have: {game_state.rebirth_count}"
    rebirth_surface = font_small.render(rebirth_text, True, WHITE)
    screen.blit(rebirth_surface, (130, 160))
    
    # Class requirement
    class_req_text = f"Class needed: {current_class_data['ascension_unlock']} ascensions"
    class_req_surface = font_small.render(class_req_text, True, WHITE)
    screen.blit(class_req_surface, (130, 180))
    
    # Ascension button
    can_ascend = (game_state.rebirth_count >= current_class_data['ascension_req'] and 
                  game_state.ascension_count >= current_class_data['ascension_unlock'])
    button_color = PURPLE if can_ascend else DARK_GRAY
    ascension_button_hovered = draw_button(130, 210, 120, 35, "Ascend", button_color, WHITE)
    
    if ascension_button_hovered and pygame.mouse.get_pressed()[0] and can_ascend:
        # Perform ascension
        game_state.ascension_count += 1
        game_state.rebirth_count -= current_class_data['ascension_req']  # Spend rebirths
        game_state.value = 0
        game_state.total_value = 0
        game_state.multiplier *= 2  # Double multiplier on ascension
        
        # Reset all progress
        for stat in game_state.progress_bars:
            game_state.progress_bars[stat]["current"] = 0
            game_state.progress_bars[stat]["level"] = 1
            game_state.progress_bars[stat]["max"] = 1000

def draw_right_panel():
    # Class info
    class_text = f"Class: {game_state.current_class.replace('_', ' ').title()}"
    class_surface = font_small.render(class_text, True, WHITE)
    screen.blit(class_surface, (490, 80))
    
    # Multiplier
    mult_text = f"Mult: {game_state.multiplier}x"
    mult_surface = font_small.render(mult_text, True, WHITE)
    screen.blit(mult_surface, (490, 100))
    
    # Value per second
    vps_text = f"VPS: {abbreviate_number(game_state.value_per_second)}"
    vps_surface = font_small.render(vps_text, True, WHITE)
    screen.blit(vps_surface, (490, 120))
    
    # Current value
    current_text = f"Value: {abbreviate_number(game_state.value)}"
    current_surface = font_small.render(current_text, True, WHITE)
    screen.blit(current_surface, (490, 140))
    
    # Stats summary
    stats_text = "Stats:"
    stats_surface = font_small.render(stats_text, True, WHITE)
    screen.blit(stats_surface, (490, 170))
    
    y_offset = 190
    for stat in ["strength", "endurance", "agility", "speed", "meditation"]:
        stat_value = getattr(game_state, stat)
        stat_text = f"{stat[:3].title()}: {abbreviate_number(stat_value)}"
        stat_surface = font_small.render(stat_text, True, WHITE)
        screen.blit(stat_surface, (490, y_offset))
        y_offset += 18

def draw_clickable_progress_bar():
    # Main progress bar at the top (moved down from line)
    bar_x, bar_y = 130, 15
    bar_width, bar_height = 340, 25
    
    # Calculate progress for ascension (rebirths needed)
    current_class_data = game_state.classes[game_state.current_class]
    rebirth_progress = min(game_state.rebirth_count / max(current_class_data['ascension_req'], 1), 1.0)
    
    # Draw background
    pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
    
    # Draw fill
    fill_width = int(rebirth_progress * bar_width)
    pygame.draw.rect(screen, PURPLE, (bar_x, bar_y, fill_width, bar_height))
    
    # Draw border
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
    
    # Draw progress text
    progress_text = f"Rebirths: {game_state.rebirth_count} / {current_class_data['ascension_req']}"
    progress_surface = font_small.render(progress_text, True, WHITE)
    screen.blit(progress_surface, (bar_x, bar_y + 30))
    
    # Draw total value text below
    total_text = f"Total Value: {abbreviate_number(game_state.total_value)}"
    total_surface = font_small.render(total_text, True, WHITE)
    screen.blit(total_surface, (bar_x, bar_y + 50))
    
    # Check for clicks on the bar
    mouse_pos = pygame.mouse.get_pos()
    if (bar_x <= mouse_pos[0] <= bar_x + bar_width and 
        bar_y <= mouse_pos[1] <= bar_y + bar_height and 
        pygame.mouse.get_pressed()[0]):
        # Add value when clicked
        game_state.value += 1000 * game_state.multiplier
        game_state.total_value += 1000 * game_state.multiplier

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    current_time = time.time()
    dt = current_time - game_state.last_time
    game_state.last_time = current_time
    
    # Auto-increment value
    game_state.value += game_state.value_per_second * game_state.multiplier * dt
    game_state.total_value += game_state.value_per_second * game_state.multiplier * dt
    
    # Auto-training logic
    if game_state.auto_training and game_state.auto_training_stat:
        stat_name = game_state.auto_training_stat
        bar_data = game_state.progress_bars[stat_name]
        
        # Add progress to the bar
        bar_data["current"] += 50 * game_state.multiplier * dt  # Slower than manual training
        
        # Check for level up
        if bar_data["current"] >= bar_data["max"]:
            bar_data["level"] += 1
            bar_data["current"] = 0
            bar_data["max"] = int(bar_data["max"] * 1.5)  # Increase max for next level
            setattr(game_state, stat_name, getattr(game_state, stat_name) + 1)
            # Add to total value when leveling up
            game_state.total_value += 1000 * game_state.multiplier
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Handle navigation button clicks
                button_labels = ["Strength", "Endurance", "Agility", "Speed", "Meditation", "Rebirth", "Ascension"]
                button_width = 100
                button_height = 30
                start_x = 10
                start_y = 50
                
                for i, label in enumerate(button_labels):
                    x = start_x
                    y = start_y + i * (button_height + 5)
                    
                    if x <= event.pos[0] <= x + button_width and y <= event.pos[1] <= y + button_height:
                        game_state.current_page = label.lower()
                        break
    
    # Draw everything
    screen.fill((30, 30, 30))
    create_lines()
    
    # Draw clickable progress bar
    draw_clickable_progress_bar()
    
    # Draw navigation buttons
    draw_navigation_buttons()
    
    # Draw main content
    draw_main_content()
    
    # Draw right panel
    draw_right_panel()
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()