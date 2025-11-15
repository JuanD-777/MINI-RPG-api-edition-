class create_hero:
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
    
    def easter_name(self, name,strength,special_weapon):
        if name == "dante":
            strength += 10,
            special_weapon += "rebellion"
            damage += 50
            health += 20
            return "devil hunter"
        elif name == "nero":
            strength += 15
            damage += 40
            health += 30
            special_weapon += "red queen"
            return "devil bringer"
        elif name == "vergil":
            strength += 20
            damage += 60
            health += 25
            special_weapon += "yamato"
            return "alfa and omega"

class hero:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength

    def attack(self, other):
        damage = self.strength
        other.health -= damage
        return f"{self.name} attacks {other.name} for {damage} damage!"

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"{self.name}: {self.health} HP, {self.strength} STR"
    
    
class enemy(hero):
    def __init__(self, name, health, strength, loot):
        super().__init__(name, health, strength)
        self.loot = loot

    def drop_loot(self):
        return self.loot if not self.is_alive() else None