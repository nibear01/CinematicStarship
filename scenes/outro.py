from manim import *
import random
import numpy as np

class OutroScene(Scene):
    def construct(self):
        # === Background Layers (Parallax) ===
        bg_width = config.frame_width * 2
        bg_height = config.frame_height * 2

        # Base deep-space background
        base_bg = Rectangle(width=bg_width, height=bg_height)
        base_bg.set_fill("#0b1a36", opacity=1).set_stroke(width=0)
        self.add(base_bg)

        # Gradient overlay
        grad_bg = Rectangle(width=bg_width, height=bg_height)
        grad_bg.set_fill([BLUE_D, BLUE_E, PURPLE_D, PINK], opacity=0.7).set_stroke(width=0)
        grad_bg.shift(DOWN * 2)
        self.add(grad_bg)

        # === Stars Layer ===
        stars_layer = VGroup(*[
            Dot(point=[random.uniform(-7, 7), random.uniform(-4, 4), 0],
                radius=random.uniform(0.015, 0.04),
                color=random.choice([WHITE, GREY_B]))
            for _ in range(60)
        ])
        self.add(stars_layer)

        # Stars parallax
        grad_bg.add_updater(lambda m, dt: m.shift(UP * 0.01))
        stars_layer.add_updater(lambda m, dt: m.shift(UP * 0.03))

        # === Particles Sparkles ===
        particles = VGroup(*[
            Dot(point=[random.uniform(-6, 6), random.uniform(-3, 3), 0],
                radius=random.uniform(0.03, 0.06),
                color=random.choice([WHITE, PINK, BLUE_B]))
            for _ in range(30)
        ])
        self.add(particles)
        for p in particles:
            p.add_updater(lambda mob, dt, v=random.uniform(0.1, 0.3): mob.shift(UP * v * dt))
            p.add_updater(lambda mob: mob.set_opacity(random.uniform(0.3, 1)))

        # === Glow Circle (above center) ===
        glow = Circle(radius=2, color=BLUE, stroke_opacity=0.4)
        glow.set_fill(BLUE, opacity=0.25)
        glow.move_to(DOWN*1.5)
        self.add(glow)

        # Glow floating animation
        glow.add_updater(lambda m, dt: m.shift(UP*0.02*np.sin(self.time*2)))

        # === Logo (centered in glow) ===
        logo = ImageMobject("assets/logo.png")
        logo.scale(0.4)
        logo.move_to(glow.get_center())
        self.add(logo)

        # Logo subtle floating
        logo.add_updater(lambda m, dt: m.shift(UP*0.01*np.sin(self.time*3)))

        # Fade in glow and logo
        self.play(FadeIn(glow, scale=2), run_time=1)
        self.play(logo.animate.scale(1.1).shift(DOWN*0.05), run_time=1.2, rate_func=there_and_back)
        self.play(logo.animate.scale(0.95), run_time=0.5)

        # === Outro Text ===
        thanks_text = Text("Thanks for Watching!", font_size=50, color=YELLOW)
        thanks_text.next_to(glow, DOWN * 1.5)

        company_text = Text("Visit ImransLab at https://imranslab.org/ for more!", font_size=20, color=WHITE)
        company_text.next_to(thanks_text, DOWN, buff=0.5)

        # Animate texts with smooth fade
        self.play(FadeIn(thanks_text, shift=UP*0.5), run_time=2)
        self.play(Write(company_text), run_time=1.5)

        # Pulse animation for texts
        for _ in range(3):
            self.play(
                thanks_text.animate.scale(1.05),
                company_text.animate.scale(1.05),
                run_time=0.5
            )
            self.play(
                thanks_text.animate.scale(0.95),
                company_text.animate.scale(0.95),
                run_time=0.5
            )

        # Floating for texts
        thanks_text.add_updater(lambda m, dt: m.shift(UP*0.005*np.sin(self.time*2)))
        company_text.add_updater(lambda m, dt: m.shift(UP*0.003*np.sin(self.time*2.5)))

        self.wait(2)

        # Drift stars diagonally
        for s in stars_layer:
            s.add_updater(lambda m, dt: m.shift(LEFT*dt*0.05 + DOWN*dt*0.03))

        # Fade out everything smoothly
        all_objects = Group(base_bg, grad_bg, stars_layer, particles, glow, logo, thanks_text, company_text)
        self.play(FadeOut(all_objects), run_time=3)
        self.wait(1)
