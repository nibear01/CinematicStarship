# === Scene 1: Rocket Launch ===
from manim import *
import random

def s1_launch(scene: MovingCameraScene):
    # === BACKGROUND ===
    bg_width = config.frame_width * 2
    bg_height = config.frame_height * 2
    sky = Rectangle(width=bg_width, height=bg_height)
    sky.set_fill(color="#54acef", opacity=1)  # dark cinematic sky
    sky.set_stroke(width=0)

    ground = Rectangle(width=bg_width, height=2)
    ground.set_fill(color="#49d182", opacity=1)  # launch pad ground
    ground.set_stroke(width=0)
    ground.move_to(DOWN * 3.5)

    # Sun glow effect
    sun = Circle(radius=0.6, color=ORANGE, fill_opacity=1).to_corner(UR).shift(LEFT*1 + DOWN*1).set_stroke(color=ORANGE, width=2)

    # Clouds for depth
    clouds = VGroup(*[
        Ellipse(width=random.uniform(1.5,2.5), height=0.6, fill_color=WHITE, fill_opacity=1)
        .set_stroke(color=WHITE, width=2)
        .shift(UP*random.uniform(1,4) + LEFT*random.uniform(-6,6))
        for _ in range(10)
    ])

    scene.add(sky, sun, ground, clouds)
    
    # === ROCKET DESIGN ===
    body = Rectangle(width=0.7, height=2.5, fill_color=WHITE, fill_opacity=1).shift(UP*0.5).set_stroke(color=BLACK, width=0.5)
    nose = Triangle().scale(0.6).set_fill(GREY, 1).next_to(body, UP, buff=0)
    booster_left = Rectangle(width=0.25, height=1.2, fill_color=WHITE, fill_opacity=1).next_to(body, LEFT, buff=0.05).align_to(body, DOWN)
    booster_right = booster_left.copy().next_to(body, RIGHT, buff=0.05).align_to(body, DOWN)

    # Enhanced flame with two layers
    main_flame = Polygon([-0.3,0,0],[0,-1,0],[0.3,0,0], color=ORANGE, fill_opacity=1).scale(0.8).next_to(body, DOWN, buff=0)
    inner_flame = Polygon([-0.15,0,0],[0,-0.7,0],[0.15,0,0], color=YELLOW, fill_opacity=0.8).next_to(body, DOWN, buff=0)

    rocket = VGroup(body, nose, booster_left, booster_right, main_flame, inner_flame).move_to(DOWN*2).set_stroke(color=GREY, width=0.5)

    # Launch pad
    pad = Rectangle(width=2, height=1, fill_color="#4D4D4D", fill_opacity=1).move_to(DOWN*3.5).set_stroke(width=0.5)
    tower = Rectangle(width=0.3, height=3, fill_color="#4D4D4D", fill_opacity=1).next_to(pad, UP, buff=0).shift(LEFT*1.2).set_stroke(width=0.5)
    scene.add(pad, tower, rocket)

    # === CAMERA ===
    frame = scene.camera.frame
    frame.save_state()
    scene.play(frame.animate.scale(1.1), run_time=2)
    scene.wait(1)

    # === FLAME FLICKER BEFORE LAUNCH ===
    for _ in range(5):
        scene.play(
            main_flame.animate.set_fill(ORANGE, opacity=random.uniform(0.6,1)).scale(random.uniform(0.95,1.2)),
            inner_flame.animate.set_fill(YELLOW, opacity=random.uniform(0.5,0.9)).scale(random.uniform(0.9,1.1)),
            run_time=0.3
        )

    # === SMOKE TRAIL ===
    smokes = VGroup(*[
        Circle(radius=random.uniform(0.1,1.25), fill_color=GREY, fill_opacity=0.2, stroke_width=0)
        .next_to(main_flame, DOWN, buff=0)
        for _ in range(15)
    ])
    scene.add(smokes)

    def update_smoke(mob, dt):
        mob.shift(UP * dt * random.uniform(0.5,1.2) + LEFT*dt*random.uniform(-0.1,0.1))
        new_opacity = max(0, mob.get_fill_opacity() - dt*0.25)
        mob.set_fill(opacity=new_opacity)

    for s in smokes:
        s.add_updater(update_smoke)


    # === ROCKET LAUNCH ===
    # No camera movement, rocket launches straight up
    scene.play(
        rocket.animate.shift(UP * 8),
        run_time=8, rate_func=linear
    )

    
    # Rocket disappears into sky
    scene.play(FadeOut(rocket, shift=UP), run_time=1)
    scene.wait(1)

    all_elements = VGroup(sky, sun, ground, clouds, pad, tower, rocket)
    # Clouds drift slowly
    for c in clouds:
        c.add_updater(lambda m, dt: m.shift(LEFT*dt*0.2))
    scene.wait(2)

    scene.play(FadeOut(all_elements), run_time=3)
    scene.wait(1)


# === Scene 2: Orbit Rendezvous / Travel to Mars ===
def s2_orbit(scene: MovingCameraScene):
    # === SPACE BACKGROUND LARGER THAN SCREEN ===
    bg_width = config.frame_width * 2
    bg_height = config.frame_height * 2
    sky = Rectangle(width=bg_width, height=bg_height)
    sky.set_fill(color="#0b1a36", opacity=1)  # deep space
    sky.set_stroke(width=0)

    # Stars with twinkle effect
    stars = VGroup(*[
        Dot(point=[random.uniform(-bg_width/2, bg_width/2), random.uniform(-bg_height/2, bg_height/2),0], 
            radius=random.uniform(0.02,0.05), color=WHITE)
        for _ in range(150)
    ])
    def twinkle(mob, dt):
        mob.set_opacity(random.uniform(0.3,1))
    for star in stars:
        star.add_updater(twinkle)

    # Earth
    earth = Circle(radius=2.5, color=BLUE, fill_opacity=0.8).shift(DOWN*3.5)
    earth_label = Text("Earth", font_size=20, color=BLUE).next_to(earth, DOWN)

    # Refuel Station (enhanced design)
    station_center = Circle(radius=0.4, color=GREY, fill_opacity=1)  # central hub
    station_hub = station_center

    # Add solar panels / docking arms
    panel_left = Rectangle(width=0.1, height=1.2, fill_color=BLUE, fill_opacity=0.7).next_to(station_hub, LEFT, buff=0)
    panel_right = panel_left.copy().next_to(station_hub, RIGHT, buff=0)
    panel_top = Rectangle(width=1.2, height=0.1, fill_color=BLUE, fill_opacity=0.7).next_to(station_hub, UP, buff=0)
    panel_bottom = panel_top.copy().next_to(station_hub, DOWN, buff=0)

    # Combine all parts into a VGroup
    station = VGroup(station_hub, panel_left, panel_right, panel_top, panel_bottom).move_to(UP*2 + LEFT*3)

    # Optional: small rotation animation for panels to simulate movement
    for panel in [panel_left, panel_right, panel_top, panel_bottom]:
        panel.add_updater(lambda m, dt: m.rotate(dt*0.3, about_point=station_hub.get_center()))

    station_label = Text("Refuel Station", font_size=18, color=WHITE).next_to(station, UP)


    # Mars
    mars = Circle(radius=1, color=RED, fill_opacity=1).shift(UP*2 + RIGHT*5)
    mars_label = Text("Mars", font_size=24, color=RED).next_to(mars, DOWN)

    # === SMALL ROCKET DESIGN ===
    rocket_scale = 0.20
    body = Rectangle(width=0.7, height=2.5, fill_color=WHITE, fill_opacity=1).scale(rocket_scale).shift(UP*0.5).set_stroke(color=BLACK, width=0.5)
    nose = Triangle().scale(0.6*rocket_scale).set_fill(GREY,1).next_to(body, UP, buff=0)
    booster_left = Rectangle(width=0.25, height=1.2, fill_color=WHITE, fill_opacity=1).scale(rocket_scale).next_to(body, LEFT, buff=0.02).align_to(body, DOWN)
    booster_right = booster_left.copy().next_to(body, RIGHT, buff=0.02).align_to(body, DOWN)

    # Flame
    main_flame = Polygon([-0.3,0,0],[0,-1,0],[0.3,0,0], color=ORANGE, fill_opacity=1).scale(0.8*rocket_scale).next_to(body, DOWN, buff=0)
    inner_flame = Polygon([-0.15,0,0],[0,-0.7,0],[0.15,0,0], color=YELLOW, fill_opacity=0.8).scale(rocket_scale).next_to(body, DOWN, buff=0)

    rocket = VGroup(body, nose, booster_left, booster_right, main_flame, inner_flame)
    rocket.move_to(earth.get_top() + UP*0.5).set_stroke(color=GREY, width=0.3)

    # HUD speed tracker
    t = ValueTracker(0)
    hud = always_redraw(lambda: Text(f"v = {int(t.get_value())} m/s", font_size=24, color=YELLOW).to_corner(UR))

    scene.add(sky, stars, earth, earth_label, station, station_label, mars, mars_label, rocket, hud)

    # === CAMERA SETUP ===
    frame = scene.camera.frame
    frame.save_state()

    # Intro zoom out
    scene.play(frame.animate.scale(1.2).move_to(earth.get_center()), run_time=3)
    scene.wait(1)

    # === FLAME FLICKER UPDATER ===
    def flame_flicker(mob, dt):
        mob.set_opacity(random.uniform(0.6,1))
        mob.scale(random.uniform(0.95,1.05))
    main_flame.add_updater(flame_flicker)
    inner_flame.add_updater(flame_flicker)

    # === ROCKET TRAVEL TO REFUEL STATION ===
    path_to_station = Line(start=rocket.get_center(), end=station.get_center() + DOWN*0.1)
    def camera_follow(mob, dt):
        frame.move_to(rocket.get_center())
    frame.add_updater(camera_follow)

    scene.play(
        MoveAlongPath(rocket, path_to_station),
        t.animate.set_value(5000),
        run_time=8, rate_func=smooth
    )

    # Hover / docking at station
    frame.clear_updaters()  # camera stops following
    for _ in range(3):
        scene.play(rocket.animate.shift(UP*0.05), run_time=0.3, rate_func=there_and_back)
    scene.wait(5)  # refueling pause

    # Rotate rocket to x-axis for Mars travel
    scene.play(rocket.animate.rotate(-PI/2), run_time=1)

    # === ROCKET TRAVEL TO MARS ===
    path_to_mars = Line(start=rocket.get_center(), end=mars.get_center())
    frame.add_updater(lambda f, dt: f.move_to(rocket.get_center()))
    scene.play(
        MoveAlongPath(rocket, path_to_mars),
        t.animate.set_value(12000),
        run_time=10, rate_func=smooth
    )

    # Subtle zoom out as rocket approaches Mars
    scene.play(frame.animate.scale(0.8), run_time=2)

    # Fade out rocket and HUD
    scene.play(FadeOut(VGroup(rocket, hud)), run_time=2)

    # Fade out stars, station, Earth, and Mars for cinematic ending
    scene.play(FadeOut(VGroup(stars, station, station_label, earth, earth_label, mars, mars_label)), run_time=3)

    # Restore camera
    scene.play(Restore(frame), run_time=2)


# === Scene 3: Mars Landing (Refined) ===
def s3_transfer(scene: MovingCameraScene):
    # === BACKGROUND: Mars landscape larger than screen ===
    bg_width = config.frame_width * 2
    bg_height = config.frame_height * 2
    mars_sky = Rectangle(width=bg_width, height=bg_height)
    mars_sky.set_fill(color="#b14d34", opacity=1)  # reddish Mars sky
    mars_sky.set_stroke(width=0)

    mars_ground = Rectangle(width=bg_width, height=2)
    mars_ground.set_fill(color="#8c3b2d", opacity=1)
    mars_ground.set_stroke(width=0)
    mars_ground.move_to(DOWN * 3.5)

    # Stars
    stars = VGroup(*[
        Dot(point=[random.uniform(-bg_width/2, bg_width/2), random.uniform(0, bg_height/2),0], 
            radius=random.uniform(0.02,0.04), color=WHITE)
        for _ in range(50)
    ])
    def twinkle(mob, dt):
        mob.set_opacity(random.uniform(0.3,1))
    for star in stars:
        star.add_updater(twinkle)

    # Mars surface: rocks, craters, hills
    rocks = VGroup(*[
        Circle(radius=random.uniform(0.05,0.15), fill_color="#5e2e1e", fill_opacity=1)
        .move_to(DOWN*3.5 + LEFT*random.uniform(-7,7) + UP*random.uniform(0,0.3))
        for _ in range(25)
    ])
    craters = VGroup(*[
        Ellipse(width=random.uniform(0.3,0.6), height=random.uniform(0.1,0.2), fill_color="#6b3a2f", fill_opacity=0.7)
        .move_to(DOWN*3.5 + LEFT*random.uniform(-7,7))
        for _ in range(5)
    ])
    hills = VGroup(*[
        Polygon([-1,0,0],[0,0.5,0],[1,0,0],[0,0.5,0],[0,0.5,0],[0,0.5,0], fill_color="#4f190c", fill_opacity=1).scale(random.uniform(1,1.5))
        .move_to(DOWN*2.2 + LEFT*random.uniform(-6,6) + UP*0.1).set_stroke(width=0.5)
        for _ in range(30)
    ])
    
    # Landing pad
    mars_land = Rectangle(width=2, height=0.2, fill_color="#5e2e1e", fill_opacity=1).move_to(DOWN*3.5 + UP*0.1)

    # === ROCKET DESIGN (scaled like s1_launch) ===
    rocket_scale = 0.7
    body = Rectangle(width=0.7, height=2.5, fill_color=WHITE, fill_opacity=1).scale(rocket_scale).set_stroke(color=BLACK, width=0.5)
    nose = Triangle().scale(0.6*rocket_scale).set_fill(GREY,1).next_to(body, UP, buff=0)
    booster_left = Rectangle(width=0.25, height=1.2, fill_color=WHITE, fill_opacity=1).scale(rocket_scale).next_to(body, LEFT, buff=0.02).align_to(body, DOWN)
    booster_right = booster_left.copy().next_to(body, RIGHT, buff=0.02).align_to(body, DOWN)

    # Flame
    main_flame = Polygon([-0.3,0,0],[0,-1,0],[0.3,0,0], color=ORANGE, fill_opacity=1).scale(0.8*rocket_scale).next_to(body, DOWN, buff=0)
    inner_flame = Polygon([-0.15,0,0],[0,-0.7,0],[0.15,0,0], color=YELLOW, fill_opacity=0.8).scale(rocket_scale).next_to(body, DOWN, buff=0)

    rocket = VGroup(body, nose, booster_left, booster_right, main_flame, inner_flame)
    rocket.move_to(UP*4)
    rocket.set_stroke(color=GREY, width=0.3)

    # Shadow under rocket
    shadow = rocket.copy().set_fill(BLACK, opacity=0.2).set_stroke(width=0).flip(axis=UP).rotate(PI/12)
    shadow.move_to(mars_land.get_top() + DOWN*0.05)
    shadow.scale(0.6, about_point=shadow.get_center())

    # Atmospheric haze
    haze = VGroup(*[
        Ellipse(width=random.uniform(1,2), height=random.uniform(0.3,0.6), fill_color="#d37f65", fill_opacity=0.15)
        .move_to(mars_land.get_center() + UP*random.uniform(0,0.3) + LEFT*random.uniform(-0.5,0.5))
        for _ in range(6)
    ])

    # Dust particles reacting to flame
    dust_particles = VGroup(*[
        Circle(radius=random.uniform(0.03,0.08), fill_color="#c27c5a", fill_opacity=0.6)
        .move_to(mars_land.get_center())
        for _ in range(20)
    ])
    for d in dust_particles:
        d.add_updater(lambda m, dt: m.shift(UP*dt*0.2 + random.uniform(-0.05,0.05)*RIGHT))

    # Add hills first so they stay behind rocket
    scene.add(mars_sky, mars_ground, stars, hills, mars_land, rocks, craters, shadow, haze, dust_particles, rocket)

    # Camera setup
    frame = scene.camera.frame
    frame.save_state()
    frame.add_updater(lambda f, dt: f.move_to(rocket.get_center()))

    # Flame flicker + heat shimmer
    def flame_flicker(mob, dt):
        scale_factor = random.uniform(0.98,1.02)
        mob.set_opacity(random.uniform(0.3,0.8))
        mob.stretch(scale_factor, 1)  # vertical shimmer
    main_flame.add_updater(flame_flicker)
    inner_flame.add_updater(flame_flicker)

    # === ROCKET DESCENT ===
    scene.play(
        rocket.animate.move_to(mars_land.get_top() + UP*0.5),
        shadow.animate.move_to(mars_land.get_top() + DOWN*0.05),
        run_time=8, rate_func=smooth
    )

    # Landing bounce for realism
    for _ in range(2):
        scene.play(
            rocket.animate.shift(DOWN*0.05),
            shadow.animate.scale(0.95, about_point=shadow.get_center()),
            run_time=0.2,
            rate_func=there_and_back
        )
    scene.wait(4)

    # Fade out rocket, flame, shadow
    # scene.play(FadeOut(VGroup(shadow, rocket )), run_time=2)
    # Fade out background elements
    scene.play(FadeOut(VGroup(mars_sky, mars_ground, stars, mars_land, rocks, craters, hills, haze, dust_particles, shadow, rocket)), run_time=3)

    # Restore camera
    scene.play(Restore(frame), run_time=2)

# # === Master Scene (One-Command Render) ===
# class MasterScene(MovingCameraScene):
#     def construct(self):
#         IntroScene.construct(self)
#         s1_launch(self)       # Scene 1
#         s2_orbit(self)        # Scene 2
#         s3_transfer(self)     # Scene 3
#         OutroScene.construct(self)
