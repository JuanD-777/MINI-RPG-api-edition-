from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import Form
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import uvicorn

templates = Jinja2Templates(directory="templates")

from Personaje import Experience as hero
from Personaje import Enemy

app = FastAPI(title="The devil may DIE")

game_state: Dict[str, Any] = {
    "started": False,
    "player": None,
    "monster": None,
    "last_log": ""
}

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html") as f:
        return f.read()

@app.post("/start")
def start_game(name: str = Form(...)):
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
    game_state["last_log"] = "El combate ha comenzado."

    return RedirectResponse(url="/battle", status_code=303)

@app.get("/battle", response_class=HTMLResponse)
async def battle_page(request: Request):
    if not game_state["player"] or not game_state["monster"]:
        return "El juego no ha sido iniciado."

    return templates.TemplateResponse(
        "batalla.html",
        {
            "request": request,
            "player_name": game_state["player"].name,
            "player_hp": game_state["player"].health,
            "player_strength": game_state["player"].strength,
            "player_weapon": game_state["player"].special_weapon,

            "monster_name": game_state["monster"].name,
            "monster_hp": game_state["monster"].health,
            "monster_strength": game_state["monster"].strength,
            "monster_weapon": game_state["monster"].special_weapon,

            "log_message": game_state["last_log"]
        }
    )

@app.post("/action", response_class=HTMLResponse)
async def action(request: Request, action: str = Form(...)):
    player = game_state["player"]
    monster = game_state["monster"]

    if not player or not monster:
        return RedirectResponse("/", status_code=303)

    if monster.health <= 0:
        game_state["last_log"] = "¡El enemigo ya está derrotado!"
        return RedirectResponse("/battle", status_code=303)

    if action == "attack":
        player_damage = player.strength + player.damage
        monster.health -= player_damage

        if monster.health <= 0:
            game_state["last_log"] = (
                f"Atacaste e hiciste {player_damage} de daño. "
                f"¡Has derrotado al enemigo!"
            )
            return RedirectResponse("/battle", status_code=303)

        monster_damage = monster.strength + monster.damage
        player.health -= monster_damage

        if player.health <= 0:
            game_state["last_log"] = (
                f"Atacaste e hiciste {player_damage} de daño. "
                f"El enemigo te hizo {monster_damage} de daño. "
                f"Has sido derrotado..."
            )
            return RedirectResponse("/battle", status_code=303)

        game_state["last_log"] = (
            f"Atacaste e hiciste {player_damage} de daño. "
            f"El enemigo te hizo {monster_damage} de daño."
        )

    return RedirectResponse(url="/battle", status_code=303)



