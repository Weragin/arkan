import pgzero as p0
import tkinter as tk


WIDTH = 906
HEIGHT = 502
vector = [-5, -5]
x = 0


def start(e):
    global x
    vector = [-5, -5]
    win.unbind('<1>')
    x = (canvas.coords(paddle)[0] + canvas.coords(paddle)[2]) // 2
    win.bind('Motion', paddle_move)
    ball_move()


def ball_move():
    global vector, WIDTH, HEIGHT
    canvas.move(ball, vector[0], vector[1])
    coords = canvas.coords(ball)
    paddle_coords = canvas.coords(paddle)
    ball_mid = (coords[0] + coords[2]) // 2
    if coords[0] <= 2 or coords[2] >= WIDTH - 2:
        vector[0] *= -1
    if coords[1] <= 2 or coords[3] >= HEIGHT - 2:
        vector[1] *= -1
    if (coords[3] > paddle_coords[1]) and (paddle_coords[0] < ball_mid < paddle_coords[2]):
        vector[1] *= -1
    overlaps = canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3])
    if len(overlaps) > 1:
        bricks_coords = canvas.coords(overlaps[1])

        # bricks.remove(canvas.find_overlapping(coords[0], coords[1], coords[2], coords[3]))

    # TODO: brick breaking

    canvas.after(20, ball_move)


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
