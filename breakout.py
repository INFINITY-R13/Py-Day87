import turtle
import time

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 20
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 10

class Paddle:
    def __init__(self):
        self.paddle = turtle.Turtle()
        self.paddle.shape("square")
        self.paddle.color("white")
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.penup()
        self.paddle.goto(0, -250)
        self.speed = 20
    
    def move_left(self):
        x = self.paddle.xcor()
        if x > -350:
            self.paddle.setx(x - self.speed)
    
    def move_right(self):
        x = self.paddle.xcor()
        if x < 350:
            self.paddle.setx(x + self.speed)

class Ball:
    def __init__(self):
        self.ball = turtle.Turtle()
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.penup()
        self.ball.goto(0, -200)
        self.ball.dx = 3
        self.ball.dy = 3
    
    def move(self):
        new_x = self.ball.xcor() + self.ball.dx
        new_y = self.ball.ycor() + self.ball.dy
        self.ball.goto(new_x, new_y)
    
    def bounce_x(self):
        self.ball.dx *= -1
    
    def bounce_y(self):
        self.ball.dy *= -1
    
    def reset_position(self):
        self.ball.goto(0, -200)
        self.ball.dy = abs(self.ball.dy)

class Brick:
    def __init__(self, x, y, color):
        self.brick = turtle.Turtle()
        self.brick.shape("square")
        self.brick.color(color)
        self.brick.shapesize(stretch_wid=1, stretch_len=3.5)
        self.brick.penup()
        self.brick.goto(x, y)
        self.is_destroyed = False
    
    def destroy(self):
        self.brick.goto(1000, 1000)  # Move off screen
        self.is_destroyed = True

class Game:
    def __init__(self):
        # Setup screen
        self.screen = turtle.Screen()
        self.screen.title("Breakout Game")
        self.screen.bgcolor("black")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)
        
        # Game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        
        # Create bricks
        self.create_bricks()
        
        # Setup score display
        self.score_display = turtle.Turtle()
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-350, 250)
        
        # Setup controls
        self.screen.listen()
        self.screen.onkey(self.paddle.move_left, "Left")
        self.screen.onkey(self.paddle.move_right, "Right")
        self.screen.onkey(self.paddle.move_left, "a")
        self.screen.onkey(self.paddle.move_right, "d")
    
    def create_bricks(self):
        colors = ["red", "orange", "yellow", "green", "blue"]
        start_x = -337.5
        start_y = 200
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + (col * 75)
                y = start_y - (row * 30)
                color = colors[row % len(colors)]
                brick = Brick(x, y, color)
                self.bricks.append(brick)
    
    def update_score_display(self):
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}  Lives: {self.lives}", 
                               font=("Arial", 16, "normal"))
    
    def check_ball_wall_collision(self):
        # Top wall
        if self.ball.ball.ycor() > 290:
            self.ball.bounce_y()
        
        # Left and right walls
        if self.ball.ball.xcor() > 390 or self.ball.ball.xcor() < -390:
            self.ball.bounce_x()
        
        # Bottom wall (lose a life)
        if self.ball.ball.ycor() < -290:
            self.lives -= 1
            if self.lives > 0:
                self.ball.reset_position()
            return True
        return False
    
    def check_ball_paddle_collision(self):
        if (self.ball.ball.ycor() > -260 and self.ball.ball.ycor() < -240 and
            self.ball.ball.xcor() > self.paddle.paddle.xcor() - 50 and
            self.ball.ball.xcor() < self.paddle.paddle.xcor() + 50):
            self.ball.bounce_y()
            
            # Add some angle based on where ball hits paddle
            hit_pos = (self.ball.ball.xcor() - self.paddle.paddle.xcor()) / 50
            self.ball.ball.dx = hit_pos * 3
    
    def check_ball_brick_collision(self):
        for brick in self.bricks:
            if not brick.is_destroyed:
                if (self.ball.ball.xcor() > brick.brick.xcor() - 37 and
                    self.ball.ball.xcor() < brick.brick.xcor() + 37 and
                    self.ball.ball.ycor() > brick.brick.ycor() - 10 and
                    self.ball.ball.ycor() < brick.brick.ycor() + 10):
                    
                    brick.destroy()
                    self.ball.bounce_y()
                    self.score += 10
                    break
    
    def all_bricks_destroyed(self):
        return all(brick.is_destroyed for brick in self.bricks)
    
    def game_over_screen(self, won=False):
        game_over = turtle.Turtle()
        game_over.color("white")
        game_over.penup()
        game_over.hideturtle()
        game_over.goto(0, 0)
        
        if won:
            message = "YOU WIN!"
        else:
            message = "GAME OVER"
        
        game_over.write(f"{message}\nFinal Score: {self.score}\nPress 'r' to restart", 
                       align="center", font=("Arial", 24, "normal"))
        
        self.screen.onkey(self.restart_game, "r")
    
    def restart_game(self):
        # Clear screen and reset
        self.screen.clear()
        self.screen.bgcolor("black")
        
        # Reset game state
        self.score = 0
        self.lives = 3
        
        # Recreate all game objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        
        # Create bricks
        self.create_bricks()
        
        # Setup score display
        self.score_display = turtle.Turtle()
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(-350, 250)
        
        # Setup controls
        self.screen.listen()
        self.screen.onkey(self.paddle.move_left, "Left")
        self.screen.onkey(self.paddle.move_right, "Right")
        self.screen.onkey(self.paddle.move_left, "a")
        self.screen.onkey(self.paddle.move_right, "d")
    
    def run(self):
        game_running = True
        
        while game_running:
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
                game_running = False
            
            # Check lose condition
            if self.lives <= 0:
                self.game_over_screen(won=False)
                game_running = False
        
        self.screen.exitonclick()

if __name__ == "__main__":
    game = Game()
    game.run()