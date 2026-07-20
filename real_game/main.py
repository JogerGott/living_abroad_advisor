# -*- coding: utf-8 -*-
"""
ESCAPE THE CULTURE SHOCK
Juego educativo de sopa de letras para clases de ingles (B1-B2), tema "Culture Shock".

Como ejecutarlo:
    pip install pygame
    python main.py

Controles:
    - Clic y arrastra sobre la cuadricula para seleccionar una palabra
      (horizontal, vertical o diagonal, en cualquier direccion).
    - Botones del panel derecho para usar Power-Ups.
    - Enter / clic para avanzar en pantallas de texto (historia, misiones,
      tarjetas sorpresa, boss challenge, reflexion).

Novedades de esta version:
    - Pantalla de NIVEL (Easy / Medium / Hard) antes de la historia.
    - Sidebar reorganizado: la lista de palabras ya no se desborda (2 columnas,
      tipografia mas compacta) y el cronometro ya no queda tapado por el titulo.
    - Animaciones: transicion con fundido entre pantallas, texto de puntos
      flotante, brillo/pulso en las palabras recien encontradas y botones
      que "laten" levemente al pasar el mouse encima.
"""
import math
import random
import sys
import textwrap
import asyncio

import pygame

from game_data import (
    GAME_TITLE, SUBTITLE, STORY_INTRO, SURPRISE_CARDS, POINTS, RANKS,
    POWER_UPS, boss_instructions, SECRET_PHRASE, REFLECTION_QUESTIONS,
    LEVELS, words_for_level, groups_for_level,
)
from word_search import WordSearchGenerator

# --------------------------------------------------------------------------- #
# CONFIG / THEME
# --------------------------------------------------------------------------- #
GRID_SIZE = 18
# Semilla fija -> el tablero en modo "Hard" coincide exactamente con
# docs/grid_solution.md. Ponla en None si quieres un tablero aleatorio
# distinto cada vez que se ejecuta el juego.
PUZZLE_SEED = 7
CELL = 34
GRID_PIXELS = GRID_SIZE * CELL
MARGIN = 24
SIDEBAR_W = 420
WIDTH = MARGIN * 3 + GRID_PIXELS + SIDEBAR_W
HEIGHT = 880          # <- antes 760: se agranda para que quepa todo sin cortes
FPS = 60

TRANSITION_MS = 260     # duracion del fundido entre pantallas
GLOW_MS = 500            # duracion del pulso al encontrar una palabra
POPUP_MS = 1100          # duracion del texto de puntos flotante

# Paleta "pasaporte / viaje" - vivos y modernos
NAVY = (24, 42, 74)
SKY = (86, 168, 227)
SUNSET = (247, 127, 65)
GOLD = (240, 191, 79)
STAMP_RED = (214, 69, 65)
WHITE = (247, 247, 245)
LIGHT_BG = (238, 243, 247)
GREY = (150, 160, 170)
GREEN = (95, 179, 122)
CELL_BG = (255, 255, 255)
FOUND_COLOR = (149, 213, 178)
SECRET_COLOR = GOLD

pygame.init()
pygame.display.set_caption(GAME_TITLE)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

FONT_XL = pygame.font.SysFont("georgia", 40, bold=True)
FONT_L = pygame.font.SysFont("georgia", 26, bold=True)
FONT_M = pygame.font.SysFont("arial", 20)
FONT_S = pygame.font.SysFont("arial", 16)
FONT_S_BOLD = pygame.font.SysFont("arial", 15, bold=True)
FONT_XS = pygame.font.SysFont("arial", 13)
FONT_MONO = pygame.font.SysFont("consolas", 20, bold=True)
FONT_SIDEBAR_TITLE = pygame.font.SysFont("georgia", 21, bold=True)


def draw_text(surface, text, font, color, pos, max_width=None, line_spacing=6):
    """Dibuja texto con salto de linea automatico si max_width esta definido.
    Devuelve el nuevo valor de Y (justo debajo del texto dibujado), por lo
    que SIEMPRE hay que capturar el retorno si algo se dibuja despues,
    para que nada se superponga."""
    x, y = pos
    if max_width is None:
        surf = font.render(text, True, color)
        surface.blit(surf, (x, y))
        return y + surf.get_height() + line_spacing
    approx_chars = max(10, max_width // max(1, font.size("A")[0]))
    wrapped = textwrap.wrap(text, approx_chars) or [""]
    for line in wrapped:
        surf = font.render(line, True, color)
        surface.blit(surf, (x, y))
        y += surf.get_height() + line_spacing
    return y


def draw_button(surface, rect, label, font=FONT_M, base=SKY, hover=SUNSET, disabled=False):
    """Boton con un leve 'latido' (grow) al pasar el mouse por encima."""
    mouse = pygame.mouse.get_pos()
    is_hover = rect.collidepoint(mouse) and not disabled
    if is_hover:
        pulse = 3 + 2 * math.sin(pygame.time.get_ticks() / 130)
        draw_rect = rect.inflate(pulse, pulse)
    else:
        draw_rect = rect
    color = GREY if disabled else (hover if is_hover else base)
    pygame.draw.rect(surface, color, draw_rect, border_radius=10)
    pygame.draw.rect(surface, NAVY, draw_rect, width=2, border_radius=10)
    text_surf = font.render(label, True, WHITE)
    surface.blit(text_surf, text_surf.get_rect(center=draw_rect.center))
    return is_hover


# --------------------------------------------------------------------------- #
# GAME STATE
# --------------------------------------------------------------------------- #
class Game:
    def __init__(self):
        self.state = "MENU"
        self.level = None
        self.words = []
        self.groups = []
        self.score = 0
        self.found_words = set()
        self.selected_cells = []
        self.dragging = False
        self.drag_start = None
        self.message = ""
        self.message_timer = 0
        self.double_points_charges = 0
        self.power_up_uses = {k: v["uses"] for k, v in POWER_UPS.items()}
        self.frozen_until = 0
        self.hinted_cells = set()
        self.shown_missions = set()
        self.current_mission = None
        self.current_card = None
        self.cards_shown = 0
        self.next_card_threshold = random.randint(2, 4)
        self.boss_text = ""
        self.boss_input_active = False
        self.reflection_index = 0
        self.start_ticks = 0
        self.grid = [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.solution = {}
        self.secret_cells = []
        self.generator = None
        self.surprise_deck = list(SURPRISE_CARDS)   # copia propia (no se agota el modulo)
        # ---- animacion ----
        self.popups = []          # [{"text","pos","start","color"}]
        self.found_glow = {}      # word -> tick en que se encontro

    # ------------------------------------------------------------ level ---
    def set_level(self, level):
        self.level = level
        self.words = words_for_level(level)
        self.groups = groups_for_level(level)
        self._build_puzzle()

    def _build_puzzle(self):
        self.generator = WordSearchGenerator(
            GRID_SIZE, self.words, secret_phrase=SECRET_PHRASE,
            seed=PUZZLE_SEED if PUZZLE_SEED is not None else random.randint(0, 10 ** 6),
        )
        self.generator.generate()
        self.grid = self.generator.grid
        self.solution = self.generator.solution
        self.secret_cells = self.generator.secret_cells

    # ------------------------------------------------------------ feedback #
    def flash(self, text, ms=1800):
        self.message = text
        self.message_timer = pygame.time.get_ticks() + ms

    def add_popup(self, text, pos, color=GOLD):
        self.popups.append({"text": text, "pos": pos, "start": pygame.time.get_ticks(), "color": color})

    def add_points(self, base, reason="", pos=None):
        mult = 2 if self.double_points_charges > 0 else 1
        gained = base * mult
        self.score += gained
        if self.double_points_charges > 0:
            self.double_points_charges -= 1
        self.flash(f"+{gained} pts  {reason}".strip())
        popup_pos = pos or (MARGIN * 2 + GRID_PIXELS + SIDEBAR_W // 2, 90)
        self.add_popup(f"+{gained}", popup_pos, color=GOLD if mult == 1 else SUNSET)

    def rank(self):
        for lo, hi, name in RANKS:
            if lo <= self.score <= hi:
                return name
        return RANKS[-1][2]

    # ---------------- word search interaction ---------------- #
    def cell_at_pos(self, pos):
        gx = MARGIN
        gy = MARGIN
        x, y = pos
        if gx <= x < gx + GRID_PIXELS and gy <= y < gy + GRID_PIXELS:
            col = (x - gx) // CELL
            row = (y - gy) // CELL
            return int(row), int(col)
        return None

    def start_drag(self, cell):
        self.dragging = True
        self.drag_start = cell
        self.selected_cells = [cell]

    def update_drag(self, cell):
        if not self.dragging or self.drag_start is None or cell is None:
            return
        r0, c0 = self.drag_start
        r1, c1 = cell
        dr, dc = r1 - r0, c1 - c0
        steps = max(abs(dr), abs(dc))
        if steps == 0:
            self.selected_cells = [self.drag_start]
            return
        if dr != 0 and dc != 0 and abs(dr) != abs(dc):
            return
        step_r = (dr > 0) - (dr < 0)
        step_c = (dc > 0) - (dc < 0)
        self.selected_cells = [(r0 + step_r * i, c0 + step_c * i) for i in range(steps + 1)]

    def end_drag(self):
        self.dragging = False
        if len(self.selected_cells) >= 2:
            self._check_selection(self.selected_cells)
        self.selected_cells = []
        self.drag_start = None

    def _mark_found(self, word, coords):
        self.found_words.add(word)
        self.found_glow[word] = pygame.time.get_ticks()
        mid = coords[len(coords) // 2]
        pos = grid_rect_for(*mid).center
        self.add_points(POINTS["find_word"], f"Found {word}!", pos=pos)
        self._maybe_trigger_card()
        self._check_group_completion()

    def _check_selection(self, cells):
        cell_set = set(cells)
        for word, coords in self.solution.items():
            if word in self.found_words:
                continue
            if set(coords) == cell_set:
                self._mark_found(word, coords)
                return

    def _maybe_trigger_card(self):
        self.cards_shown += 1
        if self.cards_shown >= self.next_card_threshold and self.surprise_deck:
            card = self.surprise_deck.pop(random.randrange(len(self.surprise_deck)))
            self.current_card = card
            self.state = "CARD"
            self.cards_shown = 0
            self.next_card_threshold = random.randint(2, 4)

    def _check_group_completion(self):
        for group in self.groups:
            gname = group["name"]
            if gname in self.shown_missions:
                continue
            if all(w in self.found_words for w in group["words"]):
                self.shown_missions.add(gname)
                self.current_mission = group
                self.state = "MISSION"
                return
        if self.words and len(self.found_words) == len(self.words):
            self.state = "SECRET"

    # ---------------- power ups ---------------- #
    def use_power_up(self, key):
        if self.power_up_uses.get(key, 0) <= 0:
            self.flash("No charges left for this power-up.")
            return
        self.power_up_uses[key] -= 1
        if key == "time_freeze":
            self.frozen_until = pygame.time.get_ticks() + 20000
            self.flash("Time Freeze activated (20s)!")
        elif key == "extra_hint":
            remaining = [w for w in self.words if w not in self.found_words]
            if remaining:
                w = random.choice(remaining)
                first_cell = self.solution[w][0]
                self.hinted_cells.add(first_cell)
                self.flash(f"Hint: look for the first letter of a {len(w)}-letter word!")
        elif key == "double_points":
            self.double_points_charges = 3
            self.flash("Double Points active for your next 3 words!")
        elif key == "skip_challenge":
            if self.state == "MISSION" and self.current_mission:
                self.add_points(POINTS["complete_mission"] // 2, "Mission skipped")
                self.current_mission = None
                if self.words and len(self.found_words) == len(self.words):
                    self.state = "SECRET"
                else:
                    self.state = "PLAY"
            else:
                self.flash("Save this for your next mission!")
                self.power_up_uses[key] += 1
        elif key == "mystery_bonus":
            bonus = random.randint(5, 20)
            self.score += bonus
            self.flash(f"Mystery Bonus: +{bonus} pts!")
            self.add_popup(f"+{bonus}", (MARGIN * 2 + GRID_PIXELS + SIDEBAR_W // 2, 90), color=SUNSET)


game = Game()

# --------------------------------------------------------------------------- #
# SCREENS
# --------------------------------------------------------------------------- #

def screen_menu():
    screen.fill(NAVY)
    bounce = math.sin(pygame.time.get_ticks() / 300) * 5
    draw_text(screen, GAME_TITLE, FONT_XL, GOLD, (MARGIN, 90 + bounce))
    draw_text(screen, SUBTITLE, FONT_L, WHITE, (MARGIN, 150))
    draw_text(
        screen,
        "Find hidden vocabulary about Culture Shock, unlock missions, react to "
        "surprise cards, and survive the final Boss Challenge at the airport gate.",
        FONT_M, LIGHT_BG, (MARGIN, 210), max_width=WIDTH - MARGIN * 2,
    )
    btn = pygame.Rect(MARGIN, 320, 260, 60)
    draw_button(screen, btn, "START YOUR JOURNEY", FONT_M, base=SUNSET, hover=GOLD)
    return {"start": btn}


def screen_level():
    screen.fill(NAVY)
    draw_text(screen, "CHOOSE YOUR DIFFICULTY", FONT_XL, GOLD, (MARGIN, 70))
    draw_text(screen, "How many words do you want to hunt for?", FONT_M, WHITE, (MARGIN, 130))

    colors = {"easy": GREEN, "medium": SUNSET, "hard": STAMP_RED}
    buttons = {}
    y = 200
    for key in ("easy", "medium", "hard"):
        info = LEVELS[key]
        count = len(words_for_level(key))
        rect = pygame.Rect(MARGIN, y, WIDTH - MARGIN * 2, 92)
        draw_button(screen, rect, "", base=colors[key], hover=GOLD)
        draw_text(screen, f"{info['label'].upper()}  —  {count} words", FONT_L, WHITE, (rect.x + 20, rect.y + 14))
        draw_text(screen, info["desc"], FONT_S, LIGHT_BG, (rect.x + 20, rect.y + 52))
        buttons[key] = rect
        y += 112
    return {"levels": buttons}


def screen_story():
    screen.fill(SKY)
    draw_text(screen, "YOUR STORY", FONT_XL, NAVY, (MARGIN, 50))
    y = 130
    for line in STORY_INTRO:
        y = draw_text(screen, line if line else " ", FONT_M, NAVY, (MARGIN, y), max_width=WIDTH - MARGIN * 2)
    btn = pygame.Rect(MARGIN, HEIGHT - 90, 220, 55)
    draw_button(screen, btn, "Let's go! ->", FONT_M, base=SUNSET, hover=GOLD)
    return {"continue": btn}


def grid_rect_for(row, col):
    x = MARGIN + col * CELL
    y = MARGIN + row * CELL
    return pygame.Rect(x, y, CELL, CELL)


def draw_word_list(sx, y, width):
    """Lista de palabras en 2 columnas y letra compacta, para que quepa
    completa sin salirse del panel (arregla el desborde reportado)."""
    col_w = (width - 12) // 2
    for group in game.groups:
        y = draw_text(screen, group["name"], FONT_S_BOLD, SKY, (sx, y), line_spacing=1)
        words = group["words"]
        row_h = 17
        for i, w in enumerate(words):
            col = i % 2
            row = i // 2
            found = w in game.found_words
            label = ("v " if found else "- ") + w
            color = GREEN if found else NAVY
            surf = FONT_XS.render(label, True, color)
            screen.blit(surf, (sx + 4 + col * col_w, y + row * row_h))
        rows_used = (len(words) + 1) // 2
        y += rows_used * row_h + 10
    return y


def draw_power_ups(sx, y, width):
    """Power-ups en 2 columnas para ahorrar espacio vertical."""
    col_w = (width - 12) // 2
    buttons = {}
    keys = list(POWER_UPS.keys())
    for i, key in enumerate(keys):
        info = POWER_UPS[key]
        uses = game.power_up_uses[key]
        col = i % 2
        row = i // 2
        rect = pygame.Rect(sx + col * (col_w + 4), y + row * 40, col_w, 34)
        label = f"{info['label']} ({uses})"
        draw_button(screen, rect, label, FONT_XS, base=(NAVY if uses > 0 else GREY), disabled=(uses <= 0))
        buttons[key] = rect
    rows_used = (len(keys) + 1) // 2
    return buttons, y + rows_used * 40


def draw_popups():
    """Texto de puntos flotante: sube y se desvanece."""
    now = pygame.time.get_ticks()
    alive = []
    for p in game.popups:
        elapsed = now - p["start"]
        if elapsed > POPUP_MS:
            continue
        alive.append(p)
        progress = elapsed / POPUP_MS
        alpha = max(0, 255 - int(255 * progress))
        rise = int(progress * 34)
        surf = FONT_L.render(p["text"], True, p["color"])
        surf.set_alpha(alpha)
        rect = surf.get_rect(center=(p["pos"][0], p["pos"][1] - rise))
        screen.blit(surf, rect)
    game.popups = alive


def draw_transition(elapsed):
    if elapsed >= TRANSITION_MS:
        return
    alpha = max(0, 255 - int(255 * elapsed / TRANSITION_MS))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 15, 25, alpha))
    screen.blit(overlay, (0, 0))


def screen_play():
    screen.fill(LIGHT_BG)

    # ---- grid ----
    pygame.draw.rect(screen, WHITE, (MARGIN - 4, MARGIN - 4, GRID_PIXELS + 8, GRID_PIXELS + 8), border_radius=8)
    found_cells = set()
    for w in game.found_words:
        found_cells.update(game.solution[w])
    selected_set = set(game.selected_cells)

    now = pygame.time.get_ticks()
    # celdas en pulso (recien encontradas)
    glow_cells = {}
    for word, t0 in list(game.found_glow.items()):
        elapsed = now - t0
        if elapsed > GLOW_MS:
            del game.found_glow[word]
            continue
        pulse = abs(math.sin(elapsed / 70))
        for cell in game.solution[word]:
            glow_cells[cell] = pulse

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = grid_rect_for(r, c)
            bg = CELL_BG
            if (r, c) in found_cells:
                bg = FOUND_COLOR
            if (r, c) in game.hinted_cells and (r, c) not in found_cells:
                bg = GOLD
            if (r, c) in glow_cells:
                t = glow_cells[(r, c)]
                bg = tuple(int(FOUND_COLOR[i] + (GOLD[i] - FOUND_COLOR[i]) * t) for i in range(3))
            if (r, c) in selected_set:
                bg = SUNSET
            draw_rect = rect.inflate(2, 2) if (r, c) in glow_cells else rect
            pygame.draw.rect(screen, bg, draw_rect)
            pygame.draw.rect(screen, (220, 224, 228), rect, width=1)
            letter = game.grid[r][c]
            color = NAVY
            if (r, c) in selected_set:
                color = WHITE
            surf = FONT_MONO.render(letter, True, color)
            screen.blit(surf, surf.get_rect(center=rect.center))

    # ---- sidebar ----
    sx = MARGIN * 2 + GRID_PIXELS
    y = MARGIN

    # titulo compacto en una sola linea (evita el desborde que tapaba el timer)
    y = draw_text(screen, GAME_TITLE, FONT_SIDEBAR_TITLE, NAVY, (sx, y), max_width=SIDEBAR_W)
    y += 6

    level_label = LEVELS[game.level]["label"] if game.level else "-"
    secs = max(0, (now - game.start_ticks) // 1000)
    frozen = now < game.frozen_until
    timer_label = f"Level: {level_label}   |   Time: {secs}s" + ("  (FROZEN)" if frozen else "")
    y = draw_text(screen, timer_label, FONT_M, SUNSET if frozen else NAVY, (sx, y))
    y = draw_text(screen, f"Score: {game.score}   Rank: {game.rank()}", FONT_M, NAVY, (sx, y))
    y += 10

    y = draw_text(screen, "WORD LIST", FONT_L, NAVY, (sx, y))
    y = draw_word_list(sx, y, SIDEBAR_W)

    y += 6
    y = draw_text(screen, "POWER-UPS", FONT_L, NAVY, (sx, y))
    buttons, y = draw_power_ups(sx, y, SIDEBAR_W)

    if game.message and pygame.time.get_ticks() < game.message_timer:
        pygame.draw.rect(screen, GOLD, (sx, HEIGHT - 60, SIDEBAR_W - 10, 40), border_radius=8)
        draw_text(screen, game.message, FONT_S, NAVY, (sx + 10, HEIGHT - 50), max_width=SIDEBAR_W - 30)

    return {"powerups": buttons}


def screen_mission():
    screen.fill(SUNSET)
    mission = game.current_mission
    draw_text(screen, "MISSION UNLOCKED!", FONT_XL, WHITE, (MARGIN, 80))
    draw_text(screen, mission["name"], FONT_L, NAVY, (MARGIN, 150))
    y = 210
    y = draw_text(screen, mission["mission"], FONT_M, WHITE, (MARGIN, y), max_width=WIDTH - MARGIN * 2)
    y += 20
    draw_text(
        screen,
        "Talk about it with your partner or teacher in English. When you are "
        "done, click Completed to earn your points.",
        FONT_S, WHITE, (MARGIN, y), max_width=WIDTH - MARGIN * 2,
    )
    btn = pygame.Rect(MARGIN, HEIGHT - 100, 260, 55)
    draw_button(screen, btn, "Mission Completed (+10)", FONT_M, base=GREEN, hover=GOLD)
    return {"complete": btn}


def screen_card():
    screen.fill(NAVY)
    draw_text(screen, "SURPRISE CARD!", FONT_XL, GOLD, (MARGIN, 90))
    y = 180
    y = draw_text(screen, game.current_card, FONT_L, WHITE, (MARGIN, y), max_width=WIDTH - MARGIN * 2)
    y += 20
    draw_text(screen, "Answer out loud in English, then continue.", FONT_S, LIGHT_BG, (MARGIN, y))
    btn = pygame.Rect(MARGIN, HEIGHT - 100, 220, 55)
    draw_button(screen, btn, "Done (+8)", FONT_M, base=SUNSET, hover=GOLD)
    return {"done": btn}


def screen_secret():
    screen.fill(GOLD)
    draw_text(screen, "EXTRA CHALLENGE: SECRET CODE!", FONT_XL, NAVY, (MARGIN, 40))
    draw_text(
        screen,
        "Look at the golden letters around the border of your Survival Map. "
        "Read them in order to reveal a message.",
        FONT_M, NAVY, (MARGIN, 100), max_width=WIDTH - MARGIN * 2,
    )
    scale = 20
    ox, oy = MARGIN, 170
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            rect = pygame.Rect(ox + c * scale, oy + r * scale, scale, scale)
            is_secret = (r, c) in game.secret_cells
            bg = SECRET_COLOR if is_secret else WHITE
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, (210, 210, 210), rect, width=1)
            if is_secret:
                surf = pygame.font.SysFont("consolas", 14, bold=True).render(game.grid[r][c], True, NAVY)
                screen.blit(surf, surf.get_rect(center=rect.center))
    y = oy + GRID_SIZE * scale + 40
    draw_text(screen, f'Secret message: "{SECRET_PHRASE}"', FONT_L, NAVY, (MARGIN, y), max_width=WIDTH - MARGIN * 2)
    btn = pygame.Rect(MARGIN, HEIGHT - 90, 260, 55)
    draw_button(screen, btn, "Go to Boss Challenge ->", FONT_M, base=SUNSET, hover=NAVY)
    return {"continue": btn}


def screen_boss():
    screen.fill(NAVY)
    y = 40
    min_words = min(10, len(game.words)) if game.words else 10
    for line in boss_instructions(min_words):
        y = draw_text(screen, line, FONT_M, WHITE, (MARGIN, y), max_width=WIDTH - MARGIN * 2)
    box = pygame.Rect(MARGIN, y + 10, WIDTH - MARGIN * 2, 150)
    pygame.draw.rect(screen, WHITE, box, border_radius=8)
    pygame.draw.rect(screen, GOLD if game.boss_input_active else GREY, box, width=3, border_radius=8)
    draw_text(screen, game.boss_text or "Click here and start typing...", FONT_S, NAVY, (box.x + 10, box.y + 10), max_width=box.width - 20)
    btn = pygame.Rect(MARGIN, box.bottom + 20, 220, 55)
    draw_button(screen, btn, "Submit Paragraph", FONT_M, base=SUNSET, hover=GOLD)
    return {"box": box, "submit": btn}


def screen_reflection():
    screen.fill(SKY)
    draw_text(screen, "FINAL REFLECTION", FONT_XL, NAVY, (MARGIN, 60))
    idx = game.reflection_index
    q = REFLECTION_QUESTIONS[idx]
    draw_text(screen, f"Question {idx + 1}/{len(REFLECTION_QUESTIONS)}", FONT_S, NAVY, (MARGIN, 130))
    draw_text(screen, q, FONT_L, NAVY, (MARGIN, 170), max_width=WIDTH - MARGIN * 2)
    btn = pygame.Rect(MARGIN, HEIGHT - 100, 220, 55)
    label = "Next Question ->" if idx < len(REFLECTION_QUESTIONS) - 1 else "Finish Game"
    draw_button(screen, btn, label, FONT_M, base=SUNSET, hover=GOLD)
    return {"next": btn}


def screen_end():
    screen.fill(NAVY)
    draw_text(screen, "WELCOME HOME!", FONT_XL, GOLD, (MARGIN, 90))
    draw_text(screen, f"Final Score: {game.score}", FONT_L, WHITE, (MARGIN, 160))
    draw_text(screen, f"Rank: {game.rank()}", FONT_L, WHITE, (MARGIN, 200))
    draw_text(
        screen,
        "You survived culture shock and learned to see the world with empathy "
        "and respect. Great job, Global Explorer!",
        FONT_M, LIGHT_BG, (MARGIN, 250), max_width=WIDTH - MARGIN * 2,
    )
    btn = pygame.Rect(MARGIN, HEIGHT - 100, 220, 55)
    draw_button(screen, btn, "Play Again", FONT_M, base=SUNSET, hover=GOLD)
    return {"restart": btn}


# --------------------------------------------------------------------------- #
# MAIN LOOP
# --------------------------------------------------------------------------- #
def restart_game():
    global game
    game = Game()
    game.state = "MENU"


async def main():
    global game
    hitboxes = {}
    last_state = game.state
    state_change_tick = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if game.state == "MENU" and hitboxes.get("start") and hitboxes["start"].collidepoint(pos):
                    game.state = "LEVEL"
                elif game.state == "LEVEL":
                    for key, rect in hitboxes.get("levels", {}).items():
                        if rect.collidepoint(pos):
                            game.set_level(key)
                            game.state = "STORY"
                            break
                elif game.state == "STORY" and hitboxes.get("continue") and hitboxes["continue"].collidepoint(pos):
                    game.state = "PLAY"
                    game.start_ticks = pygame.time.get_ticks()
                elif game.state == "PLAY":
                    powerup_hit = False
                    for key, rect in hitboxes.get("powerups", {}).items():
                        if rect.collidepoint(pos):
                            game.use_power_up(key)
                            powerup_hit = True
                            break
                    if not powerup_hit:
                        cell = game.cell_at_pos(pos)
                        if cell:
                            game.start_drag(cell)
                elif game.state == "MISSION" and hitboxes.get("complete") and hitboxes["complete"].collidepoint(pos):
                    game.add_points(POINTS["complete_mission"], f"Mission: {game.current_mission['name']}")
                    game.current_mission = None
                    if game.words and len(game.found_words) == len(game.words):
                        game.state = "SECRET"
                    else:
                        game.state = "PLAY"
                elif game.state == "CARD" and hitboxes.get("done") and hitboxes["done"].collidepoint(pos):
                    game.add_points(POINTS["surprise_card"], "Surprise card")
                    game.current_card = None
                    game.state = "PLAY"
                elif game.state == "SECRET" and hitboxes.get("continue") and hitboxes["continue"].collidepoint(pos):
                    game.state = "BOSS"
                elif game.state == "BOSS":
                    if hitboxes.get("box") and hitboxes["box"].collidepoint(pos):
                        game.boss_input_active = True
                    elif hitboxes.get("submit") and hitboxes["submit"].collidepoint(pos):
                        if len(game.boss_text.strip()) < 10 or game.boss_text == "Click here and start typing...":
                            game.flash("Please write a short paragraph first!")
                        else:
                            used = sum(1 for w in game.words if w.lower() in game.boss_text.lower())
                            bonus = min(used, 15) * POINTS["boss_challenge_word_bonus"]
                            game.add_points(POINTS["boss_challenge_base"] + bonus, f"Boss challenge ({used} key words)")
                            game.state = "REFLECTION"
                    else:
                        game.boss_input_active = False
                elif game.state == "REFLECTION" and hitboxes.get("next") and hitboxes["next"].collidepoint(pos):
                    if game.reflection_index < len(REFLECTION_QUESTIONS) - 1:
                        game.reflection_index += 1
                    else:
                        game.state = "END"
                elif game.state == "END" and hitboxes.get("restart") and hitboxes["restart"].collidepoint(pos):
                    restart_game()

            elif event.type == pygame.MOUSEMOTION and game.state == "PLAY" and game.dragging:
                cell = game.cell_at_pos(event.pos)
                if cell:
                    game.update_drag(cell)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and game.state == "PLAY":
                game.end_drag()

            elif event.type == pygame.KEYDOWN and game.state == "BOSS" and game.boss_input_active:
                if event.key == pygame.K_BACKSPACE:
                    game.boss_text = game.boss_text[:-1]
                elif event.key == pygame.K_RETURN:
                    game.boss_text += "\n"
                elif event.unicode and event.unicode.isprintable():
                    game.boss_text += event.unicode

        if game.state != last_state:
            state_change_tick = pygame.time.get_ticks()
            last_state = game.state

        if game.state == "MENU":
            hitboxes = screen_menu()
        elif game.state == "LEVEL":
            hitboxes = screen_level()
        elif game.state == "STORY":
            hitboxes = screen_story()
        elif game.state == "PLAY":
            hitboxes = screen_play()
        elif game.state == "MISSION":
            hitboxes = screen_mission()
        elif game.state == "CARD":
            hitboxes = screen_card()
        elif game.state == "SECRET":
            hitboxes = screen_secret()
        elif game.state == "BOSS":
            hitboxes = screen_boss()
        elif game.state == "REFLECTION":
            hitboxes = screen_reflection()
        elif game.state == "END":
            hitboxes = screen_end()

        draw_popups()
        draw_transition(pygame.time.get_ticks() - state_change_tick)

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())