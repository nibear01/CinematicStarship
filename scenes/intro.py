from manim import *
import random

class IntroScene(Scene):
    def construct(self):
        # === Background Layers (Parallax) ===
        base_bg = Rectangle(width=config.frame_width * 2, height=config.frame_height * 2)
        base_bg.set_stroke(width=0)
        base_bg.set_fill(color="#0f1c3f", opacity=1)
        self.add(base_bg)

        grad_bg = Rectangle(width=config.frame_width * 2, height=config.frame_height * 2)
        grad_bg.set_stroke(width=0)
        grad_bg.set_fill(color=[BLUE_D, BLUE_E, PURPLE_D, PINK], opacity=0.7)
        # grad_bg.rotate(PI/4)
        grad_bg.shift(DOWN * 2)
        self.add(grad_bg)

        stars_layer = VGroup(*[
            Dot(point=[random.uniform(-7, 7), random.uniform(-4, 4), 0],
                radius=random.uniform(0.015, 0.04),
                color=random.choice([WHITE, GREY_B]))
            for _ in range(40)
        ])
        self.add(stars_layer)

        # Parallax effect
        # grad_bg.add_updater(lambda m, dt: m.shift(UP * 0.02))
        stars_layer.add_updater(lambda m, dt: m.shift(UP * 0.05))

        # === Particle Sparkles ===
        particles = VGroup(*[
            Dot(point=[random.uniform(-6, 6), random.uniform(-3, 3), 0],
                radius=random.uniform(0.03, 0.07),
                color=random.choice([WHITE, PINK, BLUE_B]))
            for _ in range(20)
        ])
        self.add(particles)

        for p in particles:
            p.add_updater(lambda mob, dt, v=random.uniform(0.2, 0.6): mob.shift(UP * v * dt))
            p.add_updater(lambda mob: mob.set_opacity(random.uniform(0.3, 1)))

        ## === Logo with Bounce + Glow ===
        logo = ImageMobject("assets/logo.png")
        logo.scale(0.5)

        glow = Circle(radius=2, color=BLUE, stroke_opacity=0.4)
        glow.set_fill(color=BLUE, opacity=0.25)

        # Place logo exactly at the center of glow
        logo.move_to(glow.get_center())

        self.play(FadeIn(glow, scale=2), run_time=1)
        self.play(logo.animate.shift(DOWN * 0.2).scale(1.1), run_time=1.2, rate_func=there_and_back)
        self.play(logo.animate.scale(0.9), run_time=0.5)

        # === Title with Underline Sweep ===
        title = Text("Imran's Lab Presents", font_size=48, color=WHITE)
        title.next_to(glow, DOWN * 1.5)

        underline = Line(start=LEFT, end=RIGHT, stroke_color=BLUE, stroke_width=5)
        underline.set_width(title.width * 1.1)
        underline.next_to(title, DOWN, buff=0.2)

        self.play(Write(title), run_time=1.5)
        self.play(Create(underline), run_time=0.7)
        self.wait(1)

        self.play(FadeOut(title, shift=UP*0.5), FadeOut(underline), run_time=1)

        # === Tagline with Letter Stagger ===
        tagline = Text("Cinematic Starship in Manim 2D",
                       font_size=52, gradient=(BLUE, PINK))
        tagline.next_to(glow, DOWN * 1.5)
        # tagline.move_to(DOWN * 0.5)

        # Animate letters one by one
        self.play(LaggedStart(*[FadeIn(c, shift=DOWN*0.5) for c in tagline], lag_ratio=0.05), run_time=2)

        # Glow pulse + drift
        tagline.add_updater(lambda m, dt: m.scale(1 + 0.002 * np.sin(self.time * 2)))

        self.play(tagline.animate.shift(UP * 0.2).rotate(-PI/90), run_time=2)

        # Exit everything
        self.play(FadeOut(tagline, scale=0.5), FadeOut(logo), FadeOut(glow), run_time=1.5)
        self.wait(1)
