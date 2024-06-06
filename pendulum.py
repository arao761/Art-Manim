from manim import *

class Pendulum(Scene):
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
        
        # Energy texts
        kinetic_energy_text = Text("K.E. = 0.00 J").to_corner(UL)
        potential_energy_text = Text("P.E. = 0.00 J").to_corner(UR)

        self.add(rod, bob, kinetic_energy_text, potential_energy_text)

        # Timer for tracking elapsed time
        self.elapsed_time = 0

        def update_pendulum(mob, dt):
            # Update the elapsed time
            self.elapsed_time += dt
            
            # Update rod and bob positions
            time = self.elapsed_time % period
            current_angle = angle * np.cos(omega * time)
            rod.put_start_and_end_on(
                pendulum_origin,
                pendulum_origin + length * np.array([np.sin(current_angle), -np.cos(current_angle), 0])
            )
            bob.move_to(rod.get_end())

            # Calculate kinetic and potential energy
            velocity = length * omega * np.sin(angle) * np.sin(omega * time)
            kinetic_energy = 0.5 * mass * velocity**2
            height = length * (1 - np.cos(current_angle))
            potential_energy = mass * gravity * height

            # Update energy texts
            kinetic_energy_text.become(Text(f"K.E. = {kinetic_energy:.2f} J").to_corner(UL))
            potential_energy_text.become(Text(f"P.E. = {potential_energy:.2f} J").to_corner(UR))

        rod.add_updater(update_pendulum)
        bob.add_updater(update_pendulum)
        self.wait(simulation_time)
        rod.clear_updaters()  # Clear the updater after the wait period
        bob.clear_updaters()  # Clear the updater after the wait period

# To run the scene, save this script as pendulum.py and run the following command in your terminal:
# manim -pql pendulum.py Pendulum
