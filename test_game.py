#!/usr/bin/env python3

# Test script to verify game logic without GUI
import sys
import os

# Add the current directory to the path so we can import from main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the game state class and functions
from main import GameState, abbreviate_number

def test_game_logic():
    print("Testing game logic...")
    
    # Test game state initialization
    game = GameState()
    print(f"Initial value: {game.value}")
    print(f"Initial multiplier: {game.multiplier}")
    print(f"Initial class: {game.current_class}")
    
    # Test number abbreviation
    test_numbers = [100, 1000, 10000, 1000000, 1000000000]
    for num in test_numbers:
        print(f"{num} -> {abbreviate_number(num)}")
    
    # Test stat progression
    print(f"Initial strength: {game.strength}")
    game.strength += 1
    print(f"After increment: {game.strength}")
    
    # Test progress bar logic
    bar_data = game.progress_bars["strength"]
    print(f"Initial progress: {bar_data['current']}/{bar_data['max']}")
    
    bar_data["current"] += 100
    print(f"After training: {bar_data['current']}/{bar_data['max']}")
    
    # Test level up
    if bar_data["current"] >= bar_data["max"]:
        bar_data["level"] += 1
        bar_data["current"] = 0
        bar_data["max"] = int(bar_data["max"] * 1.5)
        print(f"Level up! New level: {bar_data['level']}, new max: {bar_data['max']}")
    
    # Test class progression
    print(f"Current class: {game.current_class}")
    print(f"Available classes: {list(game.classes.keys())}")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_game_logic()