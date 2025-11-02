import turtle
import time
import random

# Game constants
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
BALL_SIZE = 15
BRICK_WIDTH = 80
BRICK_HEIGHT = 25
BRICK_ROWS = 6
BRICK_COLS = 10

# Modern color palette with distinct brick colors
COLORS = {
    'bg': '#0a0a0a',
    'paddle': '#00ff88',  # Bright green paddle
    'ball': '#ff4757',    # Bright red ball
    'text': '#ffffff',
    'bricks': [
        '#ff3838',  # Bright red (top row)
        '#ff9500',  # Bright orange
        '#ffdd00',  # Bright yellow
        '#00ff00',  # Bright green
        '#0099ff',  # Bright blue
        '#9933ff'   # Bright purple (bottom row)
    ],
    'glow': '#00ffff'
}

class Paddle:
    def __init__(self):
        # Create glow effect first (drawn behind)
        self.glow = turtle.Turtle()
        self.glow.shape("square")
        self.glow.color("#004d40")  # Darker cyan for subtle glow
        self.glow.shapesize(stretch_wid=1.5, stretch_len=7)
        self.glow.penup()
        self.glow.goto(0, -280)
        
        # Create main paddle (drawn on top)
        self.paddle = turtle.Turtle()
        self.paddle.shape("square")
        self.paddle.color(COLORS['paddle'])
        self.paddle.shapesize(stretch_wid=0.8, stretch_len=6)
        self.paddle.penup()
        self.paddle.goto(0, -280)
        self.speed = 25
    
    def move_left(self):
        x = self.paddle.xcor()
        if x > -380:
            new_x = x - self.speed
            self.paddle.setx(new_x)
            self.glow.setx(new_x)
    
    def move_right(self):
        x = self.paddle.xcor()
        if x < 380:
            new_x = x + self.speed
            self.paddle.setx(new_x)
            self.glow.setx(new_x)

class Ball:
    def __init__(self):
        # Create glow effect first (drawn behind)
        self.glow = turtle.Turtle()
        self.glow.shape("circle")
        self.glow.color("#660000")  # Darker red for subtle glow
        self.glow.penup()
        self.glow.goto(0, -220)
        self.glow.shapesize(2.0)
        
        # Create main ball (drawn on top)
        self.ball = turtle.Turtle()
        self.ball.shape("circle")
        self.ball.color(COLORS['ball'])
        self.ball.penup()
        self.ball.goto(0, -220)
        self.ball.dx = 4
        self.ball.dy = 4
        
        # Add trail effect
        self.trail = []
        self.max_trail = 8
    
    def move(self):
        # Update trail
        self.update_trail()
        
        new_x = self.ball.xcor() + self.ball.dx
        new_y = self.ball.ycor() + self.ball.dy
        self.ball.goto(new_x, new_y)
        self.glow.goto(new_x, new_y)
    
    def update_trail(self):
        # Add current position to trail
        if len(self.trail) >= self.max_trail:
            # Remove oldest trail point
            old_trail = self.trail.pop(0)
            old_trail.goto(1000, 1000)
        
        # Create new trail point
        trail_point = turtle.Turtle()
        trail_point.shape("circle")
        trail_point.color(COLORS['ball'])
        trail_point.penup()
        trail_point.goto(self.ball.xcor(), self.ball.ycor())
        trail_point.shapesize(0.3)
        self.trail.append(trail_point)
    
    def bounce_x(self):
        self.ball.dx *= -1
    
    def bounce_y(self):
        self.ball.dy *= -1
    
    def reset_position(self):
        # Clear trail
        for trail_point in self.trail:
            trail_point.goto(1000, 1000)
        self.trail.clear()
        
        self.ball.goto(0, -220)
        self.glow.goto(0, -220)
        self.ball.dy = abs(self.ball.dy)
        # Add some randomness to restart
        self.ball.dx = random.choice([-4, -3, 3, 4])

class Brick:
    def __init__(self, x, y, color):
        # Create border first (drawn behind)
        self.border = turtle.Turtle()
        self.border.shape("square")
        self.border.color("#333333")  # Dark gray border for better contrast
        self.border.shapesize(stretch_wid=1.4, stretch_len=4)
        self.border.penup()
        self.border.goto(x, y)
        
        # Create main brick (drawn on top)
        self.brick = turtle.Turtle()
        self.brick.shape("square")
        self.brick.color(color)
        self.brick.shapesize(stretch_wid=1.1, stretch_len=3.6)
        self.brick.penup()
        self.brick.goto(x, y)
        self.is_destroyed = False
    
    def destroy(self):
        # Create destruction effect
        self.create_particles()
        self.brick.goto(1000, 1000)
        self.border.goto(1000, 1000)
        self.is_destroyed = True
    
    def create_particles(self):
        # Simple particle effect
        for _ in range(3):
            particle = turtle.Turtle()
            particle.shape("circle")
            particle.color(self.brick.color()[0])
            particle.penup()
            particle.goto(self.brick.xcor() + random.randint(-20, 20), 
                         self.brick.ycor() + random.randint(-10, 10))
            particle.shapesize(0.3)
            # Particles will fade by moving off screen after a delay
            particle.goto(1000, 1000)

class Game:
    def __init__(self):
        # Setup screen
        self.screen = turtle.Screen()
        self.screen.title("🎮 Modern Breakout")
        self.screen.bgcolor(COLORS['bg'])
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)
        
        # Add background effects
        self.create_background_grid()
        
        # Game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        
        # Initialize combo counter
        self.combo_count = 0
        
        # Create bricks
        self.create_bricks()
        
        # Setup score display
        self.score_display = turtle.Turtle()
        self.score_display.color(COLORS['text'])
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-420, 300)
        
        # Setup title
        self.title_display = turtle.Turtle()
        self.title_display.color(COLORS['glow'])
        self.title_display.penup()
        self.title_display.hideturtle()
        self.title_display.goto(0, 300)
        self.title_display.write("MODERN BREAKOUT", align="center", 
                                font=("Arial", 24, "bold"))
        
        # Setup controls
        self.screen.listen()
        self.screen.onkey(self.paddle.move_left, "Left")
        self.screen.onkey(self.paddle.move_right, "Right")
        self.screen.onkey(self.paddle.move_left, "a")
        self.screen.onkey(self.paddle.move_right, "d")
    
    def create_background_grid(self):
        # Create subtle grid background
        grid_drawer = turtle.Turtle()
        grid_drawer.color("#1a1a1a")
        grid_drawer.pensize(1)
        grid_drawer.speed(0)
        grid_drawer.hideturtle()
        
        # Draw vertical lines
        for x in range(-400, 401, 50):
            grid_drawer.penup()
            grid_drawer.goto(x, -350)
            grid_drawer.pendown()
            grid_drawer.goto(x, 350)
        
        # Draw horizontal lines
        for y in range(-350, 351, 50):
            grid_drawer.penup()
            grid_drawer.goto(-400, y)
            grid_drawer.pendown()
            grid_drawer.goto(400, y)
        
        grid_drawer.penup()
    
    def create_bricks(self):
        start_x = -360
        start_y = 220
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + (col * 72)
                y = start_y - (row * 35)
                color = COLORS['bricks'][row % len(COLORS['bricks'])]
                brick = Brick(x, y, color)
                self.bricks.append(brick)
    
    def update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"SCORE: {self.score:04d}  ❤️ {self.lives}", 
                               font=("Arial", 18, "bold"))
    
    def check_ball_wall_collision(self):
        # Top wall
        if self.ball.ball.ycor() > 330:
            self.ball.bounce_y()
        
        # Left and right walls
        if self.ball.ball.xcor() > 430 or self.ball.ball.xcor() < -430:
            self.ball.bounce_x()
        
        # Bottom wall (lose a life)
        if self.ball.ball.ycor() < -330:
            self.lives -= 1
            if self.lives > 0:
                self.ball.reset_position()
            return True
        return False
    
    def check_ball_paddle_collision(self):
        if (self.ball.ball.ycor() > -290 and self.ball.ball.ycor() < -270 and
            self.ball.ball.xcor() > self.paddle.paddle.xcor() - 60 and
            self.ball.ball.xcor() < self.paddle.paddle.xcor() + 60):
            self.ball.bounce_y()
            
            # Add some angle based on where ball hits paddle
            hit_pos = (self.ball.ball.xcor() - self.paddle.paddle.xcor()) / 60
            
            # Maintain minimum speed while adding angle
            base_speed = 4
            angle_factor = hit_pos * 2  # Reduced angle influence
            
            # Keep the current speed magnitude but change direction
            current_speed = abs(self.ball.ball.dx)
            if current_speed < base_speed:
                current_speed = base_speed
            
            # Apply angle with minimum speed
            self.ball.ball.dx = angle_factor + (base_speed if angle_factor >= 0 else -base_speed)
            
            # Ensure minimum speed
            if abs(self.ball.ball.dx) < 3:
                self.ball.ball.dx = 3 if self.ball.ball.dx >= 0 else -3
            
            # Add speed increase over time
            if abs(self.ball.ball.dx) < 7:
                self.ball.ball.dx *= 1.05
            if abs(self.ball.ball.dy) < 7:
                self.ball.ball.dy *= 1.05
    
    def check_ball_brick_collision(self):
        for brick in self.bricks:
            if not brick.is_destroyed:
                if (self.ball.ball.xcor() > brick.brick.xcor() - 40 and
                    self.ball.ball.xcor() < brick.brick.xcor() + 40 and
                    self.ball.ball.ycor() > brick.brick.ycor() - 15 and
                    self.ball.ball.ycor() < brick.brick.ycor() + 15):
                    
                    brick.destroy()
                    self.ball.bounce_y()
                    self.score += 10
                    
                    # Add combo scoring
                    if hasattr(self, 'combo_count'):
                        self.combo_count += 1
                        if self.combo_count > 3:
                            self.score += self.combo_count * 5
                    else:
                        self.combo_count = 1
                    break
        else:
            # Reset combo if no collision
            self.combo_count = 0
    
    def all_bricks_destroyed(self):
        return all(brick.is_destroyed for brick in self.bricks)
    
    def game_over_screen(self, won=False):
        # Create overlay
        overlay = turtle.Turtle()
        overlay.shape("square")
        overlay.color("#000000")
        overlay.penup()
        overlay.goto(0, 0)
        overlay.shapesize(50, 60)
        
        game_over = turtle.Turtle()
        game_over.color(COLORS['glow'] if won else COLORS['ball'])
        game_over.penup()
        game_over.hideturtle()
        game_over.goto(0, 50)
        
        if won:
            message = "🎉 VICTORY! 🎉"
            color = COLORS['glow']
        else:
            message = "💥 GAME OVER 💥"
            color = COLORS['ball']
        
        game_over.color(color)
        game_over.write(message, align="center", font=("Arial", 32, "bold"))
        
        score_display = turtle.Turtle()
        score_display.color(COLORS['text'])
        score_display.penup()
        score_display.hideturtle()
        score_display.goto(0, 0)
        score_display.write(f"Final Score: {self.score:04d}", 
                           align="center", font=("Arial", 20, "normal"))
        
        restart_display = turtle.Turtle()
        restart_display.color(COLORS['text'])
        restart_display.penup()
        restart_display.hideturtle()
        restart_display.goto(0, -50)
        restart_display.write("Press 'R' to restart or click to exit", 
                             align="center", font=("Arial", 16, "normal"))
        
        # Make sure screen is listening for key events
        self.screen.listen()
        self.screen.onkey(self.restart_game, "r")
        self.screen.onkey(self.restart_game, "R")  # Also handle uppercase R
        self.screen.onclick(lambda x, y: self.screen.bye())  # Click to exit
    
    def restart_game(self):
        # Clear screen and reset
        self.screen.clear()
        self.screen.bgcolor(COLORS['bg'])
        self.screen.tracer(0)  # Re-enable animation control
        
        # Reset game state
        self.score = 0
        self.lives = 3
        self.combo_count = 0
        
        # Add background effects
        self.create_background_grid()
        
        # Recreate all game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        
        # Create bricks
        self.create_bricks()
        
        # Setup score display
        self.score_display = turtle.Turtle()
        self.score_display.color(COLORS['text'])
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-420, 300)
        
        # Setup title
        self.title_display = turtle.Turtle()
        self.title_display.color(COLORS['glow'])
        self.title_display.penup()
        self.title_display.hideturtle()
        self.title_display.goto(0, 300)
        self.title_display.write("MODERN BREAKOUT", align="center", 
                                font=("Arial", 24, "bold"))
        
        # Setup controls
        self.screen.listen()
        self.screen.onkey(self.paddle.move_left, "Left")
        self.screen.onkey(self.paddle.move_right, "Right")
        self.screen.onkey(self.paddle.move_left, "a")
        self.screen.onkey(self.paddle.move_right, "d")
        
        # Reactivate the game
        self.game_active = True
        self.run()
    
    def run(self):
        self.game_active = True
        
        while self.game_active:
            self.screen.update()
            time.sleep(0.01)
            
            # Move ball
            self.ball.move()
            
            # Check collisions
            self.check_ball_wall_collision()
            self.check_ball_paddle_collision()
            self.check_ball_brick_collision()
            
            # Update display
            self.update_score_display()
            
            # Check win condition
            if self.all_bricks_destroyed():
                self.game_over_screen(won=True)
                self.game_active = False
            
            # Check lose condition
            if self.lives <= 0:
                self.game_over_screen(won=False)
                self.game_active = False
        
        # Keep the window open for restart
        self.screen.mainloop()

if __name__ == "__main__":
    game = Game()
    game.run()