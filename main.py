from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

import random

from Personaje import Experience as hero
from Personaje import Experience, Enemy

app = FastAPI(title="The devil may DIE")

class StartRequest(BaseModel):
    player_name: Optional[str] = "Jugador"
    player_hp: Optional[int] = 100
    player_strength: Optional[int] = 10
    player_damage: Optional[int] = 8

game_state: Dict[str, Any] = {
    "started": False,
    "player": None,
    "monster": None,
    "log": []
}

class action(BaseModel):
    action: str  # ataque, heal, etc.


@app.get("/")
def root():
    return {"message": "API funcionando. Usa /start para iniciar el juego."}


# ------------------------------
#  🚀 RUTA CORRECTA /start
#  Swagger envía nombre como Query → SE ACEPTA COMO QUERY
# ------------------------------
@app.post("/start")
def start_game(name: str = Query(..., description="Nombre del jugador")):
    """Inicializa un jugador y un enemigo aleatorio."""

    player = hero(
        name=name,
        health=20,
        strength=5,
        special_weapon="wood Sword",
        damage=8
    )

    player.easter_name()

    monster = Enemy(
        name="skeleton",
        health=500,
        strength=3,
        special_weapon="rusty bones",
        damage=4,
        loot="potion"
    )

    game_state["player"] = player
    game_state["monster"] = monster

    return {
        "message": f"Juego iniciado para {name}",
        "player": str(player),
        "monster": str(monster)
    }


@app.post("/action")
def player_action(action: action):

    if game_state["player"] is None or game_state["monster"] is None:
        raise HTTPException(status_code=400, detail="El juego no ha sido iniciado. Usa /start.")

    player = game_state["player"]
    monster = game_state["monster"]

    if action.action == "attack":

        result = player.attack(monster)

        if not monster.is_alive():
            xp = monster.experience_reward()
            player.gain_experience(xp)
            loot = monster.drop_loot()

            return {
                "message": result,
                "monster": "El monstruo fue derrotado",
                "xp_gained": xp,
                "loot": loot
            }

        enemy_hit = monster.attack(player)

        if not player.is_alive():
            return {
                "message": "Has sido derrotado",
                "enemy_attack": enemy_hit
            }

        return {
            "player_attack": result,
            "enemy_attack": enemy_hit,
            "player_hp": player.health,
            "monster_hp": monster.health
        }

    else:
        raise HTTPException(400, "Acción no válida")


@app.get("/status")
def game_status():
    """Retorna el estado actual del jugador y del enemigo."""

    if game_state["player"] is None or game_state["monster"] is None:
        raise HTTPException(status_code=400, detail="El juego no está iniciado")

    player = game_state["player"]
    monster = game_state["monster"]

    return {
        "player": {
            "name": player.name,
            "health": player.health,
            "strength": player.strength,
            "weapon": player.special_weapon,
            "damage": player.damage,
            "level": getattr(player, "level", None),
            "experience": getattr(player, "experience", None),
        },
        "monster": {
            "name": monster.name,
            "health": monster.health,
            "strength": monster.strength,
            "weapon": monster.special_weapon,
            "damage": monster.damage,
            "loot": monster.loot,
        }
    }
