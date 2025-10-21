import pygame, sys, random, time, math

pygame.init()

# Screen settings
width, height = 1000, 700
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
font_small = pygame.font.Font(None, 24)
font_medium = pygame.font.Font(None, 32)
font_large = pygame.font.Font(None, 48)

# Game state
class GameState:
    def __init__(self):
        # Core values
        self.value = 0
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
            "noob": {"multiplier": 1, "rebirth_req": 0, "ascension_req": 0},
            "noober": {"multiplier": 2, "rebirth_req": 20000, "ascension_req": 0},
            "noob_beginner": {"multiplier": 4, "rebirth_req": 2000000, "ascension_req": 0},
            "noober_beginner": {"multiplier": 7, "rebirth_req": 800000000, "ascension_req": 1},
            "noob_good": {"multiplier": 12, "rebirth_req": 5000000000000, "ascension_req": 1},
            "noober_good": {"multiplier": 18, "rebirth_req": 1000000000000000000, "ascension_req": 2},
            "noob_pro": {"multiplier": 25, "rebirth_req": 1000000000000000000000, "ascension_req": 2},
            "noober_pro": {"multiplier": 33, "rebirth_req": 1000000000000000000000000, "ascension_req": 3}
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
    pygame.draw.line(screen, WHITE, (200, 0), (200, height), 3)  # Left line
    pygame.draw.line(screen, WHITE, (800, 0), (800, height), 3)  # Right line
    # Horizontal divider
    pygame.draw.line(screen, WHITE, (0, 60), (width, 60), 3)  # Top line

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
    button_labels = ["Strength", "Endurance", "Agility", "Speed", "Meditation", "Rebirth", "Ascension"]
    button_width = 180
    button_height = 40
    start_x = 10
    start_y = 80
    
    for i, label in enumerate(button_labels):
        x = start_x
        y = start_y + i * (button_height + 10)
        
        # Highlight current page
        color = LIGHT_BLUE if game_state.current_page.lower() == label.lower() else GRAY
        text_color = WHITE if game_state.current_page.lower() == label.lower() else BLACK
        
        is_hovered = draw_button(x, y, button_width, button_height, label, color, text_color)
        
        if is_hovered and pygame.mouse.get_pressed()[0]:
            game_state.current_page = label.lower()

def draw_main_content():
    if game_state.current_page in ["strength", "endurance", "agility", "speed", "meditation"]:
        draw_stat_page(game_state.current_page)
    elif game_state.current_page == "rebirth":
        draw_rebirth_page()
    elif game_state.current_page == "ascension":
        draw_ascension_page()

def draw_stat_page(stat_name):
    # Title
    title_text = stat_name.title()
    title_surface = font_large.render(title_text, True, WHITE)
    screen.blit(title_surface, (220, 80))
    
    # Current value
    stat_value = getattr(game_state, stat_name)
    value_text = f"Current {stat_name}: {abbreviate_number(stat_value)}"
    value_surface = font_medium.render(value_text, True, WHITE)
    screen.blit(value_surface, (220, 130))
    
    # Progress bar
    bar_data = game_state.progress_bars[stat_name]
    bar_x, bar_y = 220, 180
    bar_width, bar_height = 560, 40
    
    draw_progress_bar(bar_x, bar_y, bar_width, bar_height, bar_data["current"], bar_data["max"])
    
    # Progress text
    progress_text = f"Level {bar_data['level']}: {abbreviate_number(bar_data['current'])} / {abbreviate_number(bar_data['max'])}"
    progress_surface = font_medium.render(progress_text, True, WHITE)
    screen.blit(progress_surface, (220, 240))
    
    # Click to train button
    train_button_hovered = draw_button(220, 300, 200, 50, f"Train {stat_name}", GREEN, WHITE)
    
    if train_button_hovered and pygame.mouse.get_pressed()[0]:
        # Add progress to the bar
        bar_data["current"] += 100 * game_state.multiplier
        
        # Check for level up
        if bar_data["current"] >= bar_data["max"]:
            bar_data["level"] += 1
            bar_data["current"] = 0
            bar_data["max"] = int(bar_data["max"] * 1.5)  # Increase max for next level
            setattr(game_state, stat_name, getattr(game_state, stat_name) + 1)
    
    # Auto-train toggle
    auto_text = "Auto-train: OFF"
    auto_surface = font_medium.render(auto_text, True, WHITE)
    screen.blit(auto_surface, (220, 380))

def draw_rebirth_page():
    # Title
    title_surface = font_large.render("Rebirth", True, WHITE)
    screen.blit(title_surface, (220, 80))
    
    # Current rebirth count
    rebirth_text = f"Rebirths: {game_state.rebirth_count}"
    rebirth_surface = font_medium.render(rebirth_text, True, WHITE)
    screen.blit(rebirth_surface, (220, 130))
    
    # Rebirth requirements
    current_class_data = game_state.classes[game_state.current_class]
    req_text = f"Next Rebirth requires: {abbreviate_number(current_class_data['rebirth_req'])} value"
    req_surface = font_medium.render(req_text, True, WHITE)
    screen.blit(req_surface, (220, 180))
    
    # Current value
    value_text = f"Current value: {abbreviate_number(game_state.value)}"
    value_surface = font_medium.render(value_text, True, WHITE)
    screen.blit(value_surface, (220, 220))
    
    # Rebirth button
    can_rebirth = game_state.value >= current_class_data['rebirth_req']
    button_color = GREEN if can_rebirth else DARK_GRAY
    rebirth_button_hovered = draw_button(220, 280, 200, 50, "Rebirth", button_color, WHITE)
    
    if rebirth_button_hovered and pygame.mouse.get_pressed()[0] and can_rebirth:
        # Perform rebirth
        game_state.rebirth_count += 1
        game_state.value = 0
        game_state.multiplier = current_class_data['multiplier']
        
        # Reset stats but keep some progress
        for stat in game_state.progress_bars:
            game_state.progress_bars[stat]["current"] = 0
            game_state.progress_bars[stat]["level"] = 1
            game_state.progress_bars[stat]["max"] = 1000
        
        # Update class if possible
        for class_name, class_data in game_state.classes.items():
            if game_state.rebirth_count >= class_data['rebirth_req'] and game_state.ascension_count >= class_data['ascension_req']:
                game_state.current_class = class_name

def draw_ascension_page():
    # Title
    title_surface = font_large.render("Ascension", True, WHITE)
    screen.blit(title_surface, (220, 80))
    
    # Current ascension count
    ascension_text = f"Ascensions: {game_state.ascension_count}"
    ascension_surface = font_medium.render(ascension_text, True, WHITE)
    screen.blit(ascension_surface, (220, 130))
    
    # Ascension requirements
    current_class_data = game_state.classes[game_state.current_class]
    req_text = f"Next Ascension requires: {abbreviate_number(current_class_data['ascension_req'])} ascensions"
    req_surface = font_medium.render(req_text, True, WHITE)
    screen.blit(req_surface, (220, 180))
    
    # Ascension button
    can_ascend = game_state.rebirth_count >= 10  # Need 10 rebirths to ascend
    button_color = PURPLE if can_ascend else DARK_GRAY
    ascension_button_hovered = draw_button(220, 250, 200, 50, "Ascend", button_color, WHITE)
    
    if ascension_button_hovered and pygame.mouse.get_pressed()[0] and can_ascend:
        # Perform ascension
        game_state.ascension_count += 1
        game_state.rebirth_count = 0
        game_state.value = 0
        game_state.multiplier *= 2  # Double multiplier on ascension
        
        # Reset all progress
        for stat in game_state.progress_bars:
            game_state.progress_bars[stat]["current"] = 0
            game_state.progress_bars[stat]["level"] = 1
            game_state.progress_bars[stat]["max"] = 1000

def draw_right_panel():
    # Class info
    class_text = f"Class: {game_state.current_class.replace('_', ' ').title()}"
    class_surface = font_medium.render(class_text, True, WHITE)
    screen.blit(class_surface, (820, 80))
    
    # Multiplier
    mult_text = f"Multiplier: {game_state.multiplier}x"
    mult_surface = font_medium.render(mult_text, True, WHITE)
    screen.blit(mult_surface, (820, 120))
    
    # Value per second
    vps_text = f"Value/sec: {abbreviate_number(game_state.value_per_second)}"
    vps_surface = font_medium.render(vps_text, True, WHITE)
    screen.blit(vps_surface, (820, 160))
    
    # Stats summary
    stats_text = "Stats:"
    stats_surface = font_medium.render(stats_text, True, WHITE)
    screen.blit(stats_surface, (820, 220))
    
    y_offset = 250
    for stat in ["strength", "endurance", "agility", "speed", "meditation"]:
        stat_value = getattr(game_state, stat)
        stat_text = f"{stat.title()}: {abbreviate_number(stat_value)}"
        stat_surface = font_small.render(stat_text, True, WHITE)
        screen.blit(stat_surface, (820, y_offset))
        y_offset += 25

def draw_clickable_progress_bar():
    # Main progress bar at the top
    bar_x, bar_y = 220, 10
    bar_width, bar_height = 560, 40
    
    # Calculate progress
    progress = min(game_state.value / 1000000, 1.0)  # Fill bar at 1M value
    
    # Draw background
    pygame.draw.rect(screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
    
    # Draw fill
    fill_width = int(progress * bar_width)
    pygame.draw.rect(screen, LIGHT_BLUE, (bar_x, bar_y, fill_width, bar_height))
    
    # Draw border
    pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 3)
    
    # Draw progress text
    progress_text = f"Progress: {abbreviate_number(game_state.value)} / 1M"
    progress_surface = font_medium.render(progress_text, True, WHITE)
    screen.blit(progress_surface, (bar_x, bar_y + 50))
    
    # Check for clicks on the bar
    mouse_pos = pygame.mouse.get_pos()
    if (bar_x <= mouse_pos[0] <= bar_x + bar_width and 
        bar_y <= mouse_pos[1] <= bar_y + bar_height and 
        pygame.mouse.get_pressed()[0]):
        # Add value when clicked
        game_state.value += 1000 * game_state.multiplier

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    current_time = time.time()
    dt = current_time - game_state.last_time
    game_state.last_time = current_time
    
    # Auto-increment value
    game_state.value += game_state.value_per_second * game_state.multiplier * dt
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Handle navigation button clicks
                button_labels = ["Strength", "Endurance", "Agility", "Speed", "Meditation", "Rebirth", "Ascension"]
                button_width = 180
                button_height = 40
                start_x = 10
                start_y = 80
                
                for i, label in enumerate(button_labels):
                    x = start_x
                    y = start_y + i * (button_height + 10)
                    
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