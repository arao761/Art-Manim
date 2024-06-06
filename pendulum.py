from manim import *

class PendulumWithEnergy(Scene):
    def construct(self):
        # Constants
        length = 3
        angle = PI / 4
        bob_radius = 0.2
        pendulum_origin = UP * 2
        gravity = 9.8
        mass = 1
        simulation_time = 10

        # Calculations
        omega = np.sqrt(gravity / length)
        period = 2 * PI / omega

        # Pendulum components
        rod = Line(pendulum_origin, pendulum_origin + length * np.array([np.sin(angle), -np.cos(angle), 0]), stroke_width=3)
        bob = Dot(rod.get_end(), radius=bob_radius, color=RED)
        pendulum_group = VGroup(rod, bob)
        
        # Energy texts
        kinetic_energy_text = Text("K.E. = 0.00 J", font_size=24).to_corner(UL)
        potential_energy_text = Text("P.E. = 0.00 J", font_size=24).to_corner(UR)
        
        # Energy bars
        kinetic_energy_bar = Rectangle(height=0.2, width=0.1, color=BLUE).next_to(kinetic_energy_text, DOWN, buff=0.2, aligned_edge=LEFT)
        potential_energy_bar = Rectangle(height=0.2, width=0.1, color=GREEN).next_to(potential_energy_text, DOWN, buff=0.2, aligned_edge=LEFT)

        self.add(pendulum_group, kinetic_energy_text, potential_energy_text, kinetic_energy_bar, potential_energy_bar)

        # Timer for tracking elapsed time
        self.elapsed_time = 0

        # Pendulum trail
        trail = TracedPath(bob.get_center, stroke_color=YELLOW, stroke_width=2)
        self.add(trail)

        def update_pendulum(mob, dt):
            # Updates the elapsed time
            self.elapsed_time += dt
            
            # Updates rod and bob positions
            time = self.elapsed_time % period
            current_angle = angle * np.cos(omega * time)
            rod.put_start_and_end_on(
                pendulum_origin,
                pendulum_origin + length * np.array([np.sin(current_angle), -np.cos(current_angle), 0])
            )
            bob.move_to(rod.get_end())

            # Calculates kinetic and potential energy
            velocity = length * omega * np.sin(angle) * np.sin(omega * time)
            kinetic_energy = 0.5 * mass * velocity**2
            height = length * (1 - np.cos(current_angle))
            potential_energy = mass * gravity * height

            # Updates energy texts
            kinetic_energy_text.become(Text(f"K.E. = {kinetic_energy:.2f} J", font_size=24).to_corner(UL))
            potential_energy_text.become(Text(f"P.E. = {potential_energy:.2f} J", font_size=24).to_corner(UR))

            # Updates energy bars
            kinetic_energy_bar.become(Rectangle(height=0.2, width=kinetic_energy / 5, color=BLUE).next_to(kinetic_energy_text, DOWN, buff=0.2, aligned_edge=LEFT))
            potential_energy_bar.become(Rectangle(height=0.2, width=potential_energy / 5, color=GREEN).next_to(potential_energy_text, DOWN, buff=0.2, aligned_edge=LEFT))

        pendulum_group.add_updater(update_pendulum)
        self.wait(simulation_time)
        pendulum_group.clear_updaters()  # Clears the updater after the wait period

# To run the scene, save this script as pendulum.py and run the following command in your terminal:
# manim -pql pendulum.py PendulumWithEnergy
