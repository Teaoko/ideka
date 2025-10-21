# Incremental Training Game

A complete incremental/idle game built with Python and Pygame featuring stat progression, rebirth, and ascension systems.

## Features

### Core Gameplay
- **Clickable Progress Bar**: Click the blue progress bar at the top to gain value
- **Auto-Progression**: Value automatically increases over time
- **Stat Training**: Train 5 different attributes (Strength, Endurance, Agility, Speed, Meditation)
- **Level System**: Each stat has its own level progression with increasing requirements

### Navigation
- **Clickable Buttons**: Navigate between different stat pages using the left sidebar
- **7 Different Pages**: 
  - Strength, Endurance, Agility, Speed, Meditation (training pages)
  - Rebirth (prestige system)
  - Ascension (advanced prestige system)

### Progression Systems
- **Rebirth System**: Reset progress for permanent multipliers (requires reaching certain value thresholds)
- **Ascension System**: Advanced reset that requires multiple rebirths and provides even greater bonuses
- **Class System**: 8 different classes with increasing multipliers and requirements

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
- **Noob**: 1x multiplier (starting class)
- **Noober**: 2x multiplier (20K value required)
- **Noob Beginner**: 4x multiplier (2M value required)
- **Noober Beginner**: 7x multiplier (800M value + 1 ascension required)
- **Noob Good**: 12x multiplier (5T value + 1 ascension required)
- **Noober Good**: 18x multiplier (1AA value + 2 ascensions required)
- **Noob Pro**: 25x multiplier (1AB value + 2 ascensions required)
- **Noober Pro**: 33x multiplier (1AC value + 3 ascensions required)

## Tips

1. Focus on training all stats evenly for balanced progression
2. Use rebirths to increase your multiplier and unlock better classes
3. Save up for ascensions to get massive multiplier boosts
4. Click the progress bar frequently to gain value faster
5. Higher classes provide better multipliers for faster progression

Enjoy the game!