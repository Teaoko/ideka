# Incremental Training Game

A complete incremental/idle game built with Python and Pygame featuring stat progression, rebirth, and ascension systems. Optimized for 600x470 screen size.

## Features

### Core Gameplay
- **Clickable Progress Bar**: Click the purple progress bar at the top to gain value (shows rebirth progress for ascension)
- **Auto-Progression**: Value automatically increases over time
- **Stat Training**: Train 5 different attributes (Strength, Endurance, Agility, Speed, Meditation)
- **Level System**: Each stat has its own level progression with increasing requirements
- **Auto-Training**: Toggle auto-training for any stat (turns off when switching pages)
- **Total Value System**: Track total value earned from training for rebirth costs

### Navigation
- **Compact Buttons**: Navigate between different stat pages using the left sidebar (abbreviated labels)
- **7 Different Pages**: 
  - Str, End, Agi, Spd, Med (training pages)
  - Reb (rebirth/prestige system)
  - Asc (ascension/advanced prestige system)

### Layout (600x470)
- **Left Panel (0-120px)**: Compact navigation buttons
- **Center Panel (120-480px)**: Main content area with stat training, rebirth, or ascension pages
- **Right Panel (480-600px)**: Stats summary, class info, multiplier display
- **Top Bar**: Clickable progress bar with value display

### Progression Systems
- **Rebirth System**: Costs total value earned (resets total value) for permanent multipliers and class upgrades
- **Ascension System**: Costs rebirths and requires specific class levels, provides massive multiplier bonuses
- **Class System**: 8 different classes with increasing multipliers, rebirth costs, and ascension requirements

### UI Features
- **Real-time Stats**: Right panel shows current class, multiplier, and all stat values
- **Visual Progress Bars**: Each stat has a progress bar showing current level progress
- **Hover Effects**: Buttons highlight when you hover over them
- **Number Abbreviation**: Large numbers are displayed in abbreviated format (K, M, B, T, etc.)

## How to Run

1. Install pygame: `pip install pygame`
2. Run the game: `python3 main.py`

## Controls

- **Mouse**: Click on buttons and progress bars to interact
- **ESC**: Close the game (or click the X button)

## Game Mechanics

### Stat Training
- Click "Train [Stat]" buttons to increase progress
- Each level requires more progress than the previous one
- Leveling up increases your base stat value

### Rebirth
- Requires reaching specific value thresholds
- Resets all progress but provides permanent multipliers
- Unlocks new classes with better bonuses

### Ascension
- Requires 10+ rebirths to unlock
- Provides even greater multipliers
- Resets rebirth count but keeps ascension count

### Classes
- **Noob**: 1x multiplier, 100K total value cost, 0 ascensions needed
- **Noober**: 2x multiplier, 500K total value cost, 0 ascensions needed
- **Noob Beginner**: 4x multiplier, 2M total value cost, 0 ascensions needed
- **Noober Beginner**: 7x multiplier, 10M total value cost, 1 ascension needed
- **Noob Good**: 12x multiplier, 50M total value cost, 1 ascension needed
- **Noober Good**: 18x multiplier, 200M total value cost, 2 ascensions needed
- **Noob Pro**: 25x multiplier, 1B total value cost, 2 ascensions needed
- **Noober Pro**: 33x multiplier, 5B total value cost, 3 ascensions needed

### Ascension Costs
- **Noob/Noober/Noob Beginner**: Not available
- **Noober Beginner**: 5 rebirths
- **Noob Good**: 10 rebirths
- **Noober Good**: 20 rebirths
- **Noob Pro**: 50 rebirths
- **Noober Pro**: 100 rebirths

## Tips

1. Focus on training all stats evenly for balanced progression
2. Use auto-training to passively level up stats while you're away
3. Save up total value for rebirths to increase your multiplier and unlock better classes
4. Save up rebirths for ascensions to get massive multiplier boosts (2x per ascension)
5. Click the progress bar frequently to gain value faster
6. Higher classes provide better multipliers and unlock ascension options
7. Auto-training turns off when switching pages, so remember to re-enable it

Enjoy the game!