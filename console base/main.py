import customtkinter as ctk
import json
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DeadlockBuildCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Deadlock Build Calculator")
        self.geometry("600x850")

        # Load raw data immediately
        self.hero_json = {}
        self.hero_map = {}
        self.load_hero_data()

        # --- Top Section: Hero Selection ---
        self.title_label = ctk.CTkLabel(
            self, text="Deadlock Hero Stat Calculator", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=10)

        self.hero_combobox = ctk.CTkComboBox(
            self, values=list(self.hero_map.keys()), command=self.on_input_changed, width=350, height=35
        )
        self.hero_combobox.pack(pady=5)
        if self.hero_map:
            self.hero_combobox.set(list(self.hero_map.keys())[0])

        # --- Slider Section: Boons / Level (0-35) ---
        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.pack(pady=10, padx=20, fill="x")

        self.slider_label = ctk.CTkLabel(self.slider_frame, text="Hero Boons (Level): 0", font=ctk.CTkFont(size=14, weight="bold"))
        self.slider_label.pack(pady=5)

        self.level_slider = ctk.CTkSlider(
            self.slider_frame, from_=0, to=35, number_of_steps=35, command=self.on_slider_changed
        )
        self.level_slider.set(0)
        self.level_slider.pack(pady=5, padx=20, fill="x")

        # --- Stats Display Section (Scrollable Frame) ---
        self.stats_scroll_frame = ctk.CTkScrollableFrame(self, width=520, height=500)
        self.stats_scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Dictionary to hold dynamic labels for quick text updates
        self.stat_labels = {}
        
        stat_keys = [
            ("Hero Name", "Hero Name"),
            ("Spirit Power", "Spirit Power"),
            ("Bullet Damage", "Bullet Damage"),
            ("Ammo", "Ammo"),
            ("Rounds Per Second", "Rounds Per Second"),
            ("Reload Time", "Reload Time"),
            ("Bullet Velocity", "Bullet Velocity"),
            ("Light Melee Damage", "Light Melee Damage"),
            ("Heavy Melee Damage", "Heavy Melee Damage"),
            ("Health", "Health"),
            ("Health Regen", "Health Regen"),
            ("Bullet Resist", "Bullet Resist"),
            ("Spirit Resist", "Spirit Resist"),
            ("Move Speed", "Move Speed"),
            ("Sprint Speed", "Sprint Speed"),
            ("Dash Speed (Ground)", "Dash Speed (Ground)"),
            ("Dash Speed (Air)", "Dash Speed (Air)"),
            ("Stamina", "Stamina"),
            ("Stamina Regen", "Stamina Regen")
        ]

        for label_text, key in stat_keys:
            lbl = ctk.CTkLabel(
                self.stats_scroll_frame, text=f"{label_text}: --", font=ctk.CTkFont(size=13), anchor="w"
            )
            lbl.pack(fill="x", pady=3, padx=10)
            self.stat_labels[key] = lbl

        # Trigger initial calculation for the default selection
        self.update_calculations()

    def load_hero_data(self):
        try:
            json_path = os.path.join("data", "hero-data.json")
            with open(json_path, "r", encoding="utf-8") as file:
                self.hero_json = json.load(file)

            active_heroes = [
                (hero_id, details) for hero_id, details in self.hero_json.items() 
                if details.get("IsDisabled", True) is False
            ]
            sorted_heroes = sorted(active_heroes, key=lambda x: x[1].get("name", x[0]))

            for hero_id, details in sorted_heroes:
                name = details.get("Name", hero_id)
                display_text = f"{name} ({hero_id})"
                self.hero_map[display_text] = hero_id

        except Exception as e:
            print(f"Error loading JSON data: {e}")

    def on_slider_changed(self, value):
        level = int(value)
        self.slider_label.configure(text=f"Hero Boons (Level): {level}")
        self.update_calculations()

    def on_input_changed(self, choice):
        self.update_calculations()

    def update_calculations(self):
        selected_display = self.hero_combobox.get()
        name = self.hero_map.get(selected_display)
        if not name or name not in self.hero_json:
            return

        level = int(self.level_slider.get())
        h_data = self.hero_json.get(name, {})

        # Core Formulas mapped straight from your console script
        spirit_power = 0 + (h_data.get("LevelScaling", {}).get("TechPower", 0) * level)

        bullet_damage = h_data.get("Weapon", {}).get("BulletDamage", 0) + (h_data.get("LevelScaling", {}).get("BulletDamage", 0) * level) + (h_data.get("SpiritScaling", {}).get("BulletDamage", 0) * spirit_power)
        ammo = h_data.get("Weapon", {}).get("ClipSize", 0) + (h_data.get("LevelScaling", {}).get("ClipSize", 0) * level) + (h_data.get("SpiritScaling", {}).get("ClipSize", 0) * spirit_power)
        rounds_per_second = h_data.get("Weapon", {}).get("RoundsPerSecond", 0) + (h_data.get("LevelScaling", {}).get("RoundsPerSecond", 0) * level) + (h_data.get("SpiritScaling", {}).get("RoundsPerSecond", 0) * spirit_power)
        reload_time = h_data.get("Weapon", {}).get("ReloadTime", 0) + (h_data.get("LevelScaling", {}).get("ReloadTime", 0) * level) + (h_data.get("SpiritScaling", {}).get("ReloadTime", 0) * spirit_power)
        bullet_velocity = h_data.get("Weapon", {}).get("BulletSpeed", 0) + (h_data.get("LevelScaling", {}).get("BulletSpeed", 0) * level) + (h_data.get("SpiritScaling", {}).get("BulletSpeed", 0) * spirit_power)
        light_melee_damage = h_data.get("LightMeleeDamage", 0) + (h_data.get("LevelScaling", {}).get("LightMeleeDamage", 0) * level) + (h_data.get("SpiritScaling", {}).get("LightMeleeDamage", 0) * spirit_power)
        heavy_melee_damage = h_data.get("HeavyMeleeDamage", 0) + (h_data.get("LevelScaling", {}).get("HeavyMeleeDamage", 0) * level) + (h_data.get("SpiritScaling", {}).get("HeavyMeleeDamage", 0) * spirit_power)

        health = h_data.get("MaxHealth", 0) + (h_data.get("LevelScaling", {}).get("MaxHealth", 0) * level) + (h_data.get("SpiritScaling", {}).get("MaxHealth", 0) * spirit_power)
        health_regen = h_data.get("BaseHealthRegen", 0) + (h_data.get("LevelScaling", {}).get("BaseHealthRegen", 0) * level) + (h_data.get("SpiritScaling", {}).get("BaseHealthRegen", 0) * spirit_power)
        bullet_resist = h_data.get("BulletResist", 0) + (h_data.get("LevelScaling", {}).get("BulletResist", 0) * level) + (h_data.get("SpiritScaling", {}).get("BulletResist", 0) * spirit_power)
        spirit_resist = h_data.get("SpiritResist", 0) + (h_data.get("LevelScaling", {}).get("SpiritResist", 0) * level) + (h_data.get("SpiritScaling", {}).get("SpiritResist", 0) * spirit_power)
        move_speed = h_data.get("MaxMoveSpeed", 0) + (h_data.get("LevelScaling", {}).get("MaxMoveSpeed", 0) * level) + (h_data.get("SpiritScaling", {}).get("MaxMoveSpeed", 0) * spirit_power)
        sprint_speed = h_data.get("SprintSpeed", 0) + (h_data.get("LevelScaling", {}).get("SprintSpeed", 0) * level) + (h_data.get("SpiritScaling", {}).get("SprintSpeed", 0) * spirit_power)
        dash_speed_ground = h_data.get("GroundDashSpeed", 0) + (h_data.get("LevelScaling", {}).get("GroundDashSpeed", 0) * level) + (h_data.get("SpiritScaling", {}).get("GroundDashSpeed", 0) * spirit_power)
        dash_speed_air = h_data.get("AirDashSpeed", 0) + (h_data.get("LevelScaling", {}).get("AirDashSpeed", 0) * level) + (h_data.get("SpiritScaling", {}).get("AirDashSpeed", 0) * spirit_power)
        stamina = h_data.get("Stamina", 0) + (h_data.get("LevelScaling", {}).get("Stamina", 0) * level) + (h_data.get("SpiritScaling", {}).get("Stamina", 0) * spirit_power)
        stamina_regen = h_data.get("StaminaCooldown", 0) + (h_data.get("LevelScaling", {}).get("StaminaCooldown", 0) * level) + (h_data.get("SpiritScaling", {}).get("StaminaCooldown", 0) * spirit_power)

        hero_display_name = h_data.get("Name", name)

        # Push calculated metrics back into the UI labels
        self.stat_labels["Hero Name"].configure(text=f"Hero Name: {hero_display_name}")
        self.stat_labels["Spirit Power"].configure(text=f"Spirit Power: {round(spirit_power, 2)}")
        self.stat_labels["Bullet Damage"].configure(text=f"Bullet Damage: {round(bullet_damage, 2)}")
        self.stat_labels["Ammo"].configure(text=f"Ammo: {round(ammo, 2)}")
        self.stat_labels["Rounds Per Second"].configure(text=f"Rounds Per Second: {round(rounds_per_second, 2)}")
        self.stat_labels["Reload Time"].configure(text=f"Reload Time: {round(reload_time, 2)}")
        self.stat_labels["Bullet Velocity"].configure(text=f"Bullet Velocity: {round(bullet_velocity, 2)}")
        self.stat_labels["Light Melee Damage"].configure(text=f"Light Melee Damage: {round(light_melee_damage, 2)}")
        self.stat_labels["Heavy Melee Damage"].configure(text=f"Heavy Melee Damage: {round(heavy_melee_damage, 2)}")
        self.stat_labels["Health"].configure(text=f"Health: {round(health, 2)}")
        self.stat_labels["Health Regen"].configure(text=f"Health Regen: {round(health_regen, 2)}")
        self.stat_labels["Bullet Resist"].configure(text=f"Bullet Resist: {round(bullet_resist, 2)}")
        self.stat_labels["Spirit Resist"].configure(text=f"Spirit Resist: {round(spirit_resist, 2)}")
        self.stat_labels["Move Speed"].configure(text=f"Move Speed: {round(move_speed, 2)}")
        self.stat_labels["Sprint Speed"].configure(text=f"Sprint Speed: {round(sprint_speed, 2)}")
        self.stat_labels["Dash Speed (Ground)"].configure(text=f"Dash Speed (Ground): {round(dash_speed_ground, 2)}")
        self.stat_labels["Dash Speed (Air)"].configure(text=f"Dash Speed (Air): {round(dash_speed_air, 2)}")
        self.stat_labels["Stamina"].configure(text=f"Stamina: {round(stamina, 2)}")
        self.stat_labels["Stamina Regen"].configure(text=f"Stamina Regen: {round(stamina_regen, 2)}")

if __name__ == "__main__":
    app = DeadlockBuildCalculator()
    app.mainloop()