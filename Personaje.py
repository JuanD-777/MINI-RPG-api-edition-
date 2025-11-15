import random

class Create_hero:
    def __init__(self, name, health, strength,special_weapon,damage):
        self.name = name
        self.health = health
        self.strength = strength
        self.special_weapon = special_weapon
        self.damage = damage

    def attack(self, other):
        damage = self.strength
        other.health -= damage
        return f"{self.name} attacks {other.name} for {damage} damage!"

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name}: {self.health} HP, {self.strength} STR"
    
    def easter_name(self):
      name = self.name.lower()

      if name == "dante":
        self.strength += 10
        self.damage += 50
        self.health += 140
        self.special_weapon = "Rebellion"
        return "Devil Hunter"

      elif name == "nero":
        self.strength += 15
        self.damage += 40
        self.health += 130
        self.special_weapon = "Red Queen"
        return "Devil Bringer"

      elif name == "vergil":
        self.strength += 20
        self.damage += 60
        self.health += 160
        self.special_weapon = "Yamato"
        return "Alpha and Omega"

      else:
        self.strength += 5
        self.damage += 8
        self.health += 20
        self.special_weapon = "Wood Sword"
        return "Normal Hero"

            
class Experience(Create_hero):
    def __init__(self, name, health, strength, special_weapon, damage, level=1, experience=0):
        super().__init__(name, health, strength, special_weapon, damage)
        self.level = level
        self.experience = experience

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= 100:
            self.experience -= 100
            self.level_up()

    def level_up(self):
        self.level += 1
        self.health += 10
        self.strength += 5
        return f"{self.name} leveled up to level {self.level}!"            
            
            
class Enemy(Create_hero):
    def __init__(self, name, health, strength, loot, special_weapon, damage,):
        super().__init__(name, health, strength, special_weapon, damage)
        self.loot = loot
        
    def experience_reward(self):
        return random.randint(20, 50)     

    def drop_loot(self):
        return self.loot if not self.is_alive() else None