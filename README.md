# Breakout Game - Python Turtle Edition

A classic 80s arcade game recreation using Python's Turtle graphics library. Break all the bricks with your paddle and ball to win!

## 🎮 Game Features

- **Classic Breakout gameplay** with authentic 80s arcade feel
- **50 colorful bricks** arranged in 5 rows (red, orange, yellow, green, blue)
- **Physics-based ball movement** with paddle angle influence
- **Score system** - 10 points per brick destroyed
- **Lives system** - 3 lives to complete the game
- **Smooth controls** with keyboard input
- **Win/lose conditions** with restart functionality

## 🚀 How to Run

Make sure you have Python installed, then simply run:

```bash
python breakout.py
```

## 🎯 How to Play

### Controls
- **Left Arrow** or **A**: Move paddle left
- **Right Arrow** or **D**: Move paddle right
- **R**: Restart game (after game over)
- **Click anywhere**: Exit game

### Objective
- Use your paddle to keep the ball bouncing
- Destroy all 50 bricks to win the game
- Don't let the ball fall off the bottom - you only have 3 lives!

### Tips
- Hit the ball with different parts of the paddle to control its direction
- Aim for the edges of the paddle to create sharper angles
- Clear the top rows first for better access to remaining bricks

## 🛠 Technical Details

### Requirements
- Python 3.x
- Turtle graphics (included with Python)

### Game Architecture
- **Object-oriented design** with separate classes for game components
- **Paddle class**: Handles player movement and boundaries
- **Ball class**: Manages physics, movement, and bouncing
- **Brick class**: Individual brick objects with destruction states
- **Game class**: Main game loop, collision detection, and state management

### Game Constants
- Screen: 800x600 pixels
- Paddle: 100x20 pixels
- Ball: 20x20 pixels circle
- Bricks: 75x20 pixels each
- Grid: 10 columns × 5 rows

## 📁 Project Structure

```
├── breakout.py           # Main game file
├── game_instructions.md  # Detailed game instructions
└── README.md            # This file
```

## 🎨 Game Screenshots

The game features:
- Black background for that classic arcade look
- White paddle and ball for high contrast
- Colorful brick rows (red, orange, yellow, green, blue)
- Real-time score and lives display
- Game over and victory screens

## 🔧 Customization

You can easily modify the game by changing constants at the top of `breakout.py`:

- `SCREEN_WIDTH/HEIGHT`: Adjust game window size
- `BRICK_ROWS/COLS`: Change number of bricks
- `PADDLE_WIDTH`: Make paddle bigger or smaller
- Ball speed by modifying `dx` and `dy` values

## 🏆 Scoring

- **10 points** per brick destroyed
- **Maximum score**: 500 points (50 bricks × 10 points)
- Score resets on game restart

## 🎯 Future Enhancements

Potential improvements you could add:
- Power-ups (multi-ball, larger paddle, etc.)
- Different brick types with varying point values
- Sound effects
- High score persistence
- Multiple levels with increasing difficulty

---

**Enjoy your retro gaming experience!** 🕹️

*Created as part of Python learning journey - Day 87 project*