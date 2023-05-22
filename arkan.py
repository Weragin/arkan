import tkinter as tk


def start(e):
    global canvas
    win.unbind('<1>')
    win.bind('Motion', paddle_move)
    canvas.after(10, paddle_move)
    canvas.after(10, ball_move)


def bounce(ball_pos, paddle_pos):
    """ A function for bouncing of the paddle. The closer to the right paddle edge is, the more rightwards the bounce is and vice versa.
    :param ball_pos: current position of ball
    :param paddle_pos: current position of the paddle
    :return: new movement vector
    """
    ball_mid = (ball_pos[0] + ball_pos[2]) // 2
    paddle_mid = (paddle_pos[0] + paddle_pos[2]) // 2
    difference = ball_mid - paddle_mid
    return [difference // 4, -4]


def paddle_move():
    global paddle, key_states, tick_length
  # Check the key states and move the object accordingly
    if key_states['a'] or key_states["Left"]:
        canvas.move(paddle, -3, 0)
    if key_states['d'] or key_states["Right"]:
        canvas.move(paddle, 3, 0)
    win.after(tick_length, paddle_move)


def on_key_press(e):
    # Update the key state when a key is pressed
    if e.keysym in key_states:
        key_states[e.keysym] = True
    print(e.keysym)

def on_key_release(e):
    # Update the key state when a key is released
    if e.keysym in key_states:
        key_states[e.keysym] = False
      

def ball_move():
    global vector, WIDTH, HEIGHT, paddle, bricks, tick_length
    canvas.move(ball, vector[0], vector[1])
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)
    overlaps = canvas.find_overlapping(ball_pos[0], ball_pos[1], ball_pos[2], ball_pos[3])
    collided_bricks = [[],[],[],[],[]]
    right = False
    left = False
    top_or_bottom = False

    if ball_pos[0] <= 2 or ball_pos[2] >= WIDTH - 2:
        vector[0] *= -1
    if ball_pos[1] <= 2 or ball_pos[3] >= HEIGHT - 2:
        vector[1] *= -1
    if paddle in overlaps:
        vector = bounce(ball_pos, paddle_pos)

    for collision in overlaps:
        for i in range(5):
            if collision in bricks[i]:
                brick_pos = canvas.coords(collision)
                collided_bricks[i].append(collision)
                if ball_pos[0] - vector[0] > brick_pos[2]:
                    # Right side collision
                    right = True
                elif ball_pos[2] - vector[0] < brick_pos[0]:
                    # Left side collision
                    left = True
                if ball_pos[1] - vector[1] >= brick_pos[3] or ball_pos[3] - vector[1] <= brick_pos[1]:
                    # Top or bottom collision
                    top_or_bottom = True
    for collision in collided_bricks[4]:
        bricks[4].remove(collision)
        canvas.delete(collision)
    for i in range(0,4):
        for collision in collided_bricks[i]:
            bricks[i].remove(collision)
            bricks[i + 1].append(collision)
            canvas.itemconfig(collision, fill = COLOURS[i + 1])
    if right and not left:
        vector[0] = abs(vector[0])
    elif left and not right:
        vector[0] = - abs(vector[0])
    if top_or_bottom:
        vector[1] *= -1

    canvas.after(tick_length, ball_move)


WIDTH = 906
HEIGHT = 502
vector = [0, -3]
COLOURS = ["#800000", "#922222", "#D03030", "#FA8072", "#FFA098"]
key_states = {'a': False, 'd': False, 'Left': False, 'Right': False}
tick_length = 7

win = tk.Tk()
win.geometry(f'{WIDTH}x{HEIGHT}')
win.focus_set()

canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg='#212121')
canvas.pack()
ball = canvas.create_oval(WIDTH // 2 - 9, HEIGHT - 60, WIDTH // 2 + 10, HEIGHT - 41, fill='blue')

paddle = canvas.create_rectangle(WIDTH // 2 - 40, HEIGHT - 40, WIDTH // 2 + 40, HEIGHT - 20, fill='#782F1D')

bricks = [[],[],[],[],[]]
brick_width = 39
brick_height = 21
for i in range(0, 20):
    for j in range(0, 5):
      bricks[j].append(canvas.create_rectangle(6 + i*(brick_width + 6), 6 + j*(brick_height + 4), 6 + i*(brick_width + 6)
                                              + brick_width, 6 + j*(brick_height + 4) + brick_height, fill=COLOURS[j]))

win.bind('<1>', start)
win.bind('<KeyPress>', on_key_press)
win.bind("<KeyRelease>", on_key_release)

tk.mainloop()
