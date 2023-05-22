import tkinter as tk


def start(e):
    global x
    win.unbind('<1>')
    x = (canvas.coords(paddle)[0] + canvas.coords(paddle)[2]) // 2
    win.bind('Motion', paddle_move)
    ball_move()


def bounce(ball_pos, paddle_pos):
    """ A function for bouncing of the paddle. The closer to the right paddle edge is,
    the more rightwards the bounce is and vice versa.
    :param ball_pos: current position of ball
    :param paddle_pos: current position of the paddle
    :return: new movement vector
    """
    ball_mid = (ball_pos[0] + ball_pos[2]) // 2
    paddle_mid = (paddle_pos[0] + paddle_pos[2]) // 2
    difference = ball_mid - paddle_mid
    return [difference // 3, -4]


def ball_move():
    global vector, WIDTH, HEIGHT, paddle, bricks
    canvas.move(ball, vector[0], vector[1])
    ball_pos = canvas.coords(ball)
    paddle_pos = canvas.coords(paddle)
    overlaps = canvas.find_overlapping(ball_pos[0], ball_pos[1], ball_pos[2], ball_pos[3])
    collided_bricks = []
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
        if collision in bricks:
            brick_pos = canvas.coords(collision)
            collided_bricks.append(collision)
            if ball_pos[0] - vector[0] > brick_pos[2]:
                # Right side collision
                right = True
            elif ball_pos[2] - vector[0] < brick_pos[0]:
                # Left side collision
                left = True
            if ball_pos[1] - vector[1] >= brick_pos[3] or ball_pos[3] - vector[1] <= brick_pos[1]:
                # Top or bottom collision
                top_or_bottom = True

    for collision in collided_bricks:
        bricks.remove(collision)
        canvas.delete(collision)
    if right and not left:
        vector[0] = abs(vector[0])
    elif left and not right:
        vector[0] = - abs(vector[0])
    if top_or_bottom:
        vector[1] *= -1


#    for i in overlaps:
#        if i in bricks:
#            brick_pos = canvas.coords(i)
#            if ball_pos[0] - vector[0] >= brick_pos[2] or ball_pos[2] - vector[0] <= brick_pos[0]:
#                v_change[0] = -1
#            if ball_pos[1] - vector[1] <= brick_pos[3] or ball_pos[3] - vector[1] >= brick_pos[1]:
#                v_change[1] = -1
#            vector[0] *= v_change[0]
#            vector[1] *= v_change[1]

            # bricks_ball_pos = canvas.coords(overlaps[1])
            # bricks.remove()

        # bricks.remove(canvas.find_overlapping(pos[0], pos[1], pos[2], pos[3]))

    # TODO: brick breaking

    canvas.after(10, ball_move)


def paddle_move(e):
    global x
    x2 = e.x
    if x != 0:
        mouse = x2-x
        canvas.move(paddle, mouse, 0)
        x = e.x


def checkkey(e):
    print(e.char)


def checker(e):
    win.focus_set()
    win.bind('Key', checkkey)


WIDTH = 906
HEIGHT = 502
vector = [0, -3]
x = 0

win = tk.Tk()
win.geometry(f'{WIDTH}x{HEIGHT}')

canvas = tk.Canvas(width=WIDTH, height=HEIGHT, bg='#212121')
canvas.pack()
ball = canvas.create_oval(WIDTH // 2 - 9, HEIGHT - 60, WIDTH // 2 + 10, HEIGHT - 41, fill='blue')

paddle = canvas.create_rectangle(WIDTH // 2 - 40, HEIGHT - 40, WIDTH // 2 + 40, HEIGHT - 20, fill='#782F1D')

bricks = []
brick_width = 39
brick_height = 21
for i in range(0, 20):
    for j in range(0, 5):
        bricks.append(canvas.create_rectangle(6 + i*(brick_width + 6), 6 + j*(brick_height + 4), 6 + i*(brick_width + 6)
                                              + brick_width, 6 + j*(brick_height + 4) + brick_height))

win.bind('<1>', start)
win.bind('<2>', checker)

tk.mainloop()
