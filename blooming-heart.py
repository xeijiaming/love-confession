import turtle
import math
import time

# ── Setup ──
turtle.setup(800, 700)
turtle.bgcolor('#0a0a1a')
turtle.tracer(0, 0)
turtle.title('🌹 绽放的爱心')

# ── Particle Class ──
class Particle:
    def __init__(self, t, size=1):
        self.t = t
        # Heart parametric equation: x = 16sin³t, y = 13cost - 5cos2t - 2cos3t - cos4t
        self.x = 16 * math.sin(t) ** 3
        self.y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        self.size = size
        # Colors from red to pink to gold
        hue = (t % (2*math.pi)) / (2*math.pi)
        if hue < 0.5:
            self.color = (1, hue * 2 * 0.6, hue * 2 * 0.3)  # red → pink
        else:
            self.color = (1, 0.6 - (hue-0.5) * 0.4, 0.3 + (hue-0.5) * 1.0)  # pink → gold

    def draw(self, scale, offset_x=0, offset_y=0):
        turtle.penup()
        turtle.goto(self.x * scale + offset_x, self.y * scale + offset_y)
        turtle.pendown()
        turtle.pencolor(self.color)
        turtle.pensize(self.size * scale * 0.4)
        turtle.dot(int(self.size * scale * 0.8))
        # Connect points for smoother line
        turtle.goto(self.x * scale + offset_x, self.y * scale + offset_y)


def draw_heart(scale, opacity=1.0, offset_y=0):
    """Draw a heart outline + fill at given scale."""
    points = 200
    turtles = []
    for i in range(points + 1):
        t_val = i / points * 2 * math.pi
        x = 16 * math.sin(t_val) ** 3
        y = 13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)
        turtles.append((x * scale, y * scale + offset_y))
    return turtles


def draw_filled_heart(scale, offset_y=0, color=(0.95, 0.18, 0.22)):
    """Draw a solid filled heart."""
    turtle.penup()
    start_x = 16 * math.sin(0) ** 3 * scale
    start_y = (13 * math.cos(0) - 5 * math.cos(0) - 2 * math.cos(0) - math.cos(0)) * scale + offset_y
    turtle.goto(start_x, start_y)

    # Fill the heart
    turtle.pencolor(color)
    turtle.fillcolor(color)
    turtle.begin_fill()

    points = 300
    for i in range(points + 1):
        t_val = i / points * 2 * math.pi
        x = 16 * math.sin(t_val) ** 3 * scale
        y = (13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)) * scale + offset_y
        turtle.goto(x, y)

    turtle.end_fill()


# ── Sparkle effect ──
sparkles = []
import random


def create_sparkle():
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(12, 22)
    sx = dist * math.sin(angle) ** 3
    sy = (13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle))
    return {
        'x': sx, 'y': sy,
        'size': random.uniform(1, 4),
        'life': random.uniform(0.5, 2.0),
        'age': 0,
        'color': random.choice([
            (1, 0.8, 0.2),  # gold
            (1, 0.3, 0.3),  # red
            (1, 0.5, 0.5),  # pink
            (1, 0.9, 0.6),  # light gold
            (1, 1, 0.8),    # white-gold
        ])
    }


def draw_sparkle(s, scale):
    alpha = 1 - s['age'] / s['life']
    if alpha <= 0:
        return False
    turtle.penup()
    sx = s['x'] * scale + random.uniform(-2, 2)
    sy = s['y'] * scale + random.uniform(-2, 2)
    turtle.goto(sx, sy)
    r, g, b = s['color']
    turtle.pencolor((r, g, b))
    turtle.pensize(s['size'] * scale * 0.3 * alpha)
    turtle.dot(int(s['size'] * scale * 0.6 * alpha))
    s['age'] += 0.03
    return s['age'] < s['life']


# ── Main Animation ──
def animate():
    turtle.hideturtle()
    turtle.speed(0)

    # Phase 1: Drawing outline (0 - 3s)
    # Phase 2: Blooming fill (3 - 6s)
    # Phase 3: Sparkle burst (6 - 10s)

    start_time = time.time()
    frame = 0

    while True:
        turtle.clear()
        elapsed = time.time() - start_time

        if elapsed < 1.0:
            # ── Just a glow at center ──
            for i in range(20):
                r = i * 0.7
                alpha = 1 - i / 20
                turtle.penup()
                turtle.goto(0, r * 0.3)
                turtle.pencolor((0.95, 0.2, 0.3))
                turtle.fillcolor((0.95, 0.18, 0.22))
                turtle.pensize(2)

        elif elapsed < 3.0:
            # ── Heart outline being drawn ──
            progress = (elapsed - 1.0) / 2.0  # 0 to 1
            scale = 12 + progress * 2
            draw_heart_outline_animated(scale, progress)

        elif elapsed < 5.0:
            # ── Heart blooming + filling ──
            progress = (elapsed - 3.0) / 2.0
            scale = 14 + progress * 2
            # Easing: ease-out elastic
            eased = 1 - math.pow(1 - progress, 3)
            final_scale = 14 + eased * 2

            # Draw filled heart
            draw_filled_heart(final_scale, offset_y=-5, color=(0.95, 0.18 - eased * 0.08, 0.22 + eased * 0.1))

            # Pulsing outline
            pulse = 1 + math.sin(elapsed * 8) * 0.04 * (1 - progress)
            draw_heart_outline(final_scale * pulse, color=(1, 0.15 + eased * 0.15, 0.2 + eased * 0.2), offset_y=-5)

        elif elapsed < 8.0:
            # ── Full heart + growing sparkles ──
            progress = (elapsed - 5.0) / 3.0
            scale = 16

            # Subtle pulse
            pulse = 1 + math.sin(elapsed * 3) * 0.03
            current_scale = scale * pulse

            draw_filled_heart(current_scale, offset_y=-5, color=(0.95, 0.12, 0.25))
            draw_heart_outline(current_scale, color=(1, 0.25, 0.3), offset_y=-5)

            # Add new sparkles
            if random.random() < 0.4:
                sparkles.append(create_sparkle())
                sparkles.append(create_sparkle())

            # Draw sparkles
            sparkles[:] = [s for s in sparkles if draw_sparkle(s, current_scale)]

        else:
            # ── Steady state: beautiful heart with sparkles ──
            scale = 16
            pulse = 1 + math.sin(elapsed * 2.5) * 0.02
            current_scale = scale * pulse

            draw_filled_heart(current_scale, offset_y=-5, color=(0.95, 0.1, 0.28))

            # Shimmering outline
            shimmer = (math.sin(elapsed * 4) + 1) / 2
            r = 1
            g = 0.2 + shimmer * 0.3
            b = 0.25 + shimmer * 0.3
            draw_heart_outline(current_scale, color=(r, g, b), offset_y=-5)

            # Continuous sparkles
            if random.random() < 0.3:
                sparkles.append(create_sparkle())
            sparkles[:] = [s for s in sparkles if draw_sparkle(s, current_scale)]

            # Limit sparkles
            if len(sparkles) > 80:
                sparkles[:] = sparkles[-60:]

        turtle.update()
        time.sleep(0.016)  # ~60fps
        frame += 1


def draw_heart_outline(scale, color=(1, 0.3, 0.35), offset_y=0):
    """Draw heart outline."""
    turtle.penup()
    points = 200
    for i in range(points + 1):
        t_val = i / points * 2 * math.pi
        x = 16 * math.sin(t_val) ** 3 * scale
        y = (13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)) * scale + offset_y
        if i == 0:
            turtle.goto(x, y)
            turtle.pendown()
            turtle.pencolor(color)
            turtle.pensize(2.5)
        else:
            turtle.goto(x, y)


def draw_heart_outline_animated(scale, progress):
    """Draw heart outline being animated on."""
    points_to_draw = int(200 * progress)
    total_points = 200

    turtle.penup()
    turtle.pencolor((1, 0.3, 0.35))
    turtle.pensize(2.5 + progress)

    for i in range(min(points_to_draw, total_points) + 1):
        t_val = i / total_points * 2 * math.pi
        x = 16 * math.sin(t_val) ** 3 * scale
        y = (13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)) * scale
        if i == 0:
            turtle.goto(x, y)
            turtle.pendown()
        else:
            turtle.goto(x, y)

    # Glow dot at the leading edge
    if points_to_draw > 0:
        t_val = min(points_to_draw, total_points) / total_points * 2 * math.pi
        x = 16 * math.sin(t_val) ** 3 * scale
        y = (13 * math.cos(t_val) - 5 * math.cos(2*t_val) - 2 * math.cos(3*t_val) - math.cos(4*t_val)) * scale
        turtle.penup()
        turtle.goto(x, y)
        turtle.pencolor((1, 0.9, 0.6))
        turtle.pensize(8)
        turtle.dot(8 + int(progress * 6))


# ── Entry Point ──
if __name__ == '__main__':
    try:
        animate()
    except turtle.Terminator:
        pass
    except KeyboardInterrupt:
        print("\n💖 爱心已绽放！")
