# -*- coding: utf-8 -*-
"""
game_data.py
Contenido pedagógico de "ESCAPE THE CULTURE SHOCK"
Todo el contenido educativo (vocabulario, misiones, tarjetas, reflexión) vive aquí,
separado del motor del juego, para que un profesor pueda editarlo sin tocar el código.
"""

GAME_TITLE = "ESCAPE THE CULTURE SHOCK"
SUBTITLE = "A Global Explorer's Word Challenge (B1-B2)"

# ---------------------------------------------------------------------------
# 1. STORYLINE
# ---------------------------------------------------------------------------
STORY_INTRO = [
    "You are an exchange student who just landed in a brand-new country.",
    "Your suitcase is heavy, your phone has no signal, and everyone around",
    "you speaks a language you barely understand.",
    "",
    "Your mission: survive the four stages of CULTURE SHOCK, complete daily",
    "challenges, react to unexpected events, and finally prove you can",
    "adapt, respect, and connect with a new culture.",
    "",
    "Find the hidden words in your Survival Map (the word search).",
    "Each group of words unlocks a MISSION. Some tiles hide SURPRISE CARDS.",
    "Collect points, use Power-Ups wisely, and get ready for the BOSS",
    "CHALLENGE at the airport gate: your final interview before you can",
    "officially say... 'I made it. I belong here.'",
]

# ---------------------------------------------------------------------------
# 2. WORD GROUPS  ->  each group unlocks one MISSION when fully found
# ---------------------------------------------------------------------------
WORD_GROUPS = [
    {
        "name": "Stages of Culture Shock",
        "words": ["CULTURESHOCK", "HONEYMOON", "FRUSTRATION", "ADJUSTMENT", "ADAPTATION"],
        "mission": "Describe a moment when someone could experience culture shock.",
    },
    {
        "name": "Culture & Society",
        "words": ["CUSTOMS", "TRADITIONS", "ETIQUETTE", "CULTURE", "IDENTITY", "VALUES"],
        "mission": "Share a tradition from your country.",
    },
    {
        "name": "Communication",
        "words": ["LANGUAGE", "COMMUNICATION", "GREETINGS", "STEREOTYPES"],
        "mission": "Explain one cultural difference you find interesting.",
    },
    {
        "name": "Travel & Global Life",
        "words": ["HOMESICK", "EXCHANGE", "TRAVEL", "GLOBAL", "COMMUNITY"],
        "mission": "Give advice to a new exchange student.",
    },
    {
        "name": "Values for a Connected World",
        "words": ["DIVERSITY", "RESPECT", "INCLUSION", "EMPATHY", "TOLERANCE", "FESTIVALS"],
        "mission": "Compare two cultures you know (food, greetings, or traditions).",
    },
]

ALL_WORDS = [w for group in WORD_GROUPS for w in group["words"]]  # 26 words total

# ---------------------------------------------------------------------------
# 2b. DIFFICULTY LEVELS
# ---------------------------------------------------------------------------
# easy   = total_words // 3
# medium = total_words // 2
# hard   = total_words (todas)
LEVELS = {
    "easy":   {"label": "Easy",   "divisor": 3, "desc": "Quick round, fewer words."},
    "medium": {"label": "Medium", "divisor": 2, "desc": "Balanced challenge."},
    "hard":   {"label": "Hard",   "divisor": 1, "desc": "All 26 words. Full experience."},
}


def words_for_level(level):
    """
    Devuelve el subconjunto de palabras para el nivel elegido.
    Se reparten en 'round robin' entre los grupos tematicos, para que
    incluso en Easy se toquen todos los temas del vocabulario.
    """
    divisor = LEVELS[level]["divisor"]
    target = len(ALL_WORDS) // divisor
    selected = []
    iterators = [iter(g["words"]) for g in WORD_GROUPS]
    active = list(range(len(WORD_GROUPS)))
    while len(selected) < target and active:
        for gi in list(active):
            try:
                selected.append(next(iterators[gi]))
            except StopIteration:
                active.remove(gi)
                continue
            if len(selected) >= target:
                break
    return selected


def groups_for_level(level):
    """
    WORD_GROUPS filtrado para que cada grupo solo contenga las palabras
    que en verdad pertenecen al nivel elegido (las misiones se disparan
    con ese subconjunto). Los grupos que quedarian vacios se omiten.
    """
    chosen = set(words_for_level(level))
    groups = []
    for g in WORD_GROUPS:
        words = [w for w in g["words"] if w in chosen]
        if words:
            groups.append({"name": g["name"], "words": words, "mission": g["mission"]})
    return groups


# ---------------------------------------------------------------------------
# 3. SURPRISE CARDS (15) — triggered randomly while playing
# ---------------------------------------------------------------------------
SURPRISE_CARDS = [
    "You accidentally offend someone. What do you say to fix it?",
    "You cannot understand the local slang. Ask someone to explain it to you.",
    "Someone invites you to a traditional celebration. How do you react?",
    "You miss your family a lot today. Describe how you feel and what helps you.",
    "You try a strange food for the first time. Describe the taste and your reaction.",
    "You learn a local custom that surprises you. Explain it to a friend.",
    "You get lost in a new city. Ask a stranger for directions politely.",
    "A classmate makes fun of your accent. How do you respond?",
    "You are invited to someone's home for dinner. What do you bring or say?",
    "You don't understand a joke everyone is laughing at. What do you do?",
    "You see people greeting each other in an unfamiliar way. Copy the greeting and describe it.",
    "You feel excited and nervous on your first day of class. Describe your feelings.",
    "Someone asks you a stereotype about your country. How do you politely correct them?",
    "You find a festival happening in the street. Describe what you see and ask a question about it.",
    "After a hard week, you finally start to feel at home. Describe what changed.",
]

# ---------------------------------------------------------------------------
# 4. POINTS SYSTEM
# ---------------------------------------------------------------------------
POINTS = {
    "find_word": 5,
    "complete_mission": 10,
    "good_pronunciation": 5,
    "creative_answer": 10,
    "help_classmate": 5,
    "surprise_card": 8,
    "boss_challenge_word_bonus": 3,   # per relevant word used, up to a cap
    "boss_challenge_base": 20,
}

RANKS = [
    (0, 60, "Confused Tourist"),
    (61, 120, "Curious Traveler"),
    (121, 200, "Cultural Explorer"),
    (201, 280, "Global Citizen"),
    (281, 10_000, "World Ambassador"),
]

# ---------------------------------------------------------------------------
# 5. POWER-UPS
# ---------------------------------------------------------------------------
POWER_UPS = {
    "time_freeze":   {"label": "Time Freeze",    "desc": "Pauses the timer for 20 seconds.",           "uses": 1},
    "extra_hint":    {"label": "Extra Hint",     "desc": "Reveals the first letter of one hidden word.", "uses": 2},
    "double_points":  {"label": "Double Points",  "desc": "Doubles points for the next 3 words found.",  "uses": 1},
    "skip_challenge": {"label": "Skip Challenge", "desc": "Skip one mission and still get half points.", "uses": 1},
    "mystery_bonus":  {"label": "Mystery Bonus",  "desc": "Instant random bonus between 5 and 20 points.", "uses": 1},
}

# ---------------------------------------------------------------------------
# 6. BOSS CHALLENGE (final)
# ---------------------------------------------------------------------------
def boss_instructions(min_words):
    """Genera las instrucciones del Boss Challenge con el minimo de
    palabras ajustado al nivel de dificultad (Easy no llega a 10 palabras)."""
    return [
        "FINAL GATE - THE IMMIGRATION OFFICER CHALLENGE",
        "",
        f"Using AT LEAST {min_words} of the words you found in the Survival Map,",
        "write a short paragraph (or prepare a 1-2 minute spoken answer) to:",
        "",
        '  "How can a person overcome culture shock and adapt to a new country?"',
        "",
        "Type your paragraph below. The game will count how many key words",
        "you used and award bonus points for each one.",
    ]

# ---------------------------------------------------------------------------
# 7. SECRET CODE (hidden around the border of the grid)
# ---------------------------------------------------------------------------
SECRET_PHRASE = "RESPECT ALL CULTURES"

# ---------------------------------------------------------------------------
# 8. FINAL REFLECTION QUESTIONS
# ---------------------------------------------------------------------------
REFLECTION_QUESTIONS = [
    "What surprised you the most about this activity?",
    "Which stage of culture shock do you think is the hardest? Why?",
    "How can people avoid stereotypes about other cultures?",
    "Why is empathy important when meeting people from other cultures?",
    "What would you do if you moved to a new country tomorrow?",
]

# ---------------------------------------------------------------------------
# 9. VISUAL THEME (reference for design.md / for reused colors in the game)
# ---------------------------------------------------------------------------
THEME_NOTES = """
Visual theme: passports, airplanes, suitcases, world maps, flags, travel
stamps, globes, compasses. Vivid, modern colors: sky blue, sunset orange,
passport-navy, gold accents for the secret code, stamp-red for alerts.
"""