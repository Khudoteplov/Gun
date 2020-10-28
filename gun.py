from random import randrange as rnd, choice
import tkinter as tk
import math
import time

score = 0

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
width = 800
height = 600
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class Ball:
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'black', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 80
        print('\n')

    def set_coords(self):
        """
        Перерисовка мяча
        """
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть,
        обновляет значения self.x и self.y с учетом скоростей self.vx и
        self.vy, силы гравитации, действующей на мяч, и стен по краям окна
        (размер окна 800х600).
        """
        g = 1
        self.live -= 1

        if self.x < 0:
            self.vx = -0.5 * self.vx
            self.vy *= 0.5
            self.x = 0
        elif self.y < 0:
            self.vy = -0.5 * self.vy
            self.vx *= 0.5
            self.y = 0
        elif self.x > width:
            self.vx = -0.5 * self.vx
            self.vy *= 0.5
            self.x = width
        elif self.y > height:
            self.vy = -0.5 * self.vy
            self.vx *= 0.5
            self.y = height
        else:
            self.x += self.vx
            self.y -= self.vy
            self.vy -= g
        self.set_coords()

    def hit_test(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью,
        описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели.
                В противном случае возвращает False.
        """

        t = ((self.vx - obj.vx) * (obj.x - self.x) - (self.vy - obj.vy) * (
                obj.y - self.y)) / \
            ((self.vy - obj.vy) ** 2 + (self.vx - obj.vx) ** 2)

        k = (((self.x + self.vx * t - obj.vx * t - obj.x) ** 2 +
              (self.y + self.vy * t - obj.vy * t + obj.y) ** 2) ** 0.5 <=
             self.r + obj.r)

        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (
                self.r + obj.r) ** 2:
            return True
        elif 0 <= t < 1:
            return k

        else:
            return False


class Gun:
    def __init__(self):
        """
        Инициализация новой пушки.
        """
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        """
        Метод заряжает пушку
        """
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.Начальные значения компонент
        скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 20

    def targeting(self, event=None):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )


class Target:
    def __init__(self):
        """ Инициализация новой цели. """

        color = self.color = 'red'
        self.r = rnd(2, 50)
        self.y = rnd(300, 550)
        self.x = rnd(600, 780)
        self.vx = rnd(-7, 7)
        self.vy = rnd(-7, 7)
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r,
                    self.y + self.r)
        canv.itemconfig(self.id, fill=color)

    def move(self):
        """
        Переместить цель по прошествии единицы времени.

        Метод описывает перемещение цели за один кадр перерисовки. То есть,
        обновляет значения self.x и self.y с учетом скоростей self.vx и
        self.vy, а также стен по краям окна (размер окна 800х600).
        """
        if self.x < 0:
            self.vx = -0.5 * self.vx
            self.vy *= 0.5
            self.x = 0
        elif self.y < 0:
            self.vy = -0.5 * self.vy
            self.vx *= 0.5
            self.y = 0
        elif self.x > width:
            self.vx = -0.5 * self.vx
            self.vy *= 0.5
            self.x = width
        elif self.y > height:
            self.vy = -0.5 * self.vy
            self.vx *= 0.5
            self.y = height
        else:
            self.x += self.vx
            self.y -= self.vy

        canv.coords(self.id, self.x - self.r, self.y - self.r, self.x + self.r,
                    self.y + self.r)

    def hit(self, i=True, points=1):
        """Попадание шарика в цель."""
        if i:
            canv.coords(self.id, -10, -10, -10, -10)
        global score
        score += points
        canv.itemconfig(global_score, text=score)


global_score = canv.create_text(30, 30, text=score, font='28')
screen1 = canv.create_text(400, 300, text='', font='28')
g1 = Gun()
bullet = 0
balls = []
targets = []
max_targets = 2
timer = -1


def new_game():
    global screen1, balls, bullet, timer
    if len(targets) < max_targets:
        f = Target()
        f.hit(False, 0)
        f.live = 1
        targets.append(f)

    bullet = 0
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targeting)
    z = 0.03  # delay   in seconds between loop iterations
    while targets or balls:
        if len(targets) < max_targets:
            f = Target()  # creates a new target
            f.hit(False, 0)
            f.live = 1
            targets.append(f)
        for b in balls:
            b.move()
        for t in targets:
            t.move()
        for b in balls:
            if b.live < 0:
                canv.delete(b.id)
                balls.remove(b)
            for t in targets:
                if b.hit_test(t) and t.live:
                    t.live = 0
                    t.hit()
                    targets.remove(t)
                    canv.itemconfig(screen1,
                                    text='Вы уничтожили цель за ' +
                                         str(bullet) + ' выстрелов')
                    timer = 1.2  # time in seconds before text will disappear
                    bullet = 0
        if timer > 0:
            timer -= z
        else:
            canv.itemconfig(screen1, text='')  # screen1 text disappears
        canv.update()
        time.sleep(z)
        g1.targeting()
    canv.itemconfig(screen1, text='')
    canv.delete(Gun)
    for t in targets:
        canv.delete(t.id_points)
    root.after(750, new_game)


new_game()

tk.mainloop()
