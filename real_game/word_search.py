# -*- coding: utf-8 -*-
"""
word_search.py
Generador procedural de sopa de letras (word search).

Por que procedural y no una cuadricula escrita a mano:
- Garantiza que TODAS las palabras estan realmente colocadas y sin errores.
- Permite regenerar el puzzle con una nueva semilla (seed) cada clase.
- Con una semilla fija (seed=42) el resultado es 100% reproducible, por eso
  el "answer key" en puzzle_answer_key.md corresponde exactamente a lo que
  genera el juego si se usa esa misma semilla.
"""
import random
import string

DIRECTIONS = [
    (0, 1), (0, -1), (1, 0), (-1, 0),          # -> <- v ^
    (1, 1), (1, -1), (-1, 1), (-1, -1),        # diagonales
]


class WordSearchGenerator:
    def __init__(self, size, words, secret_phrase="", seed=None):
        self.size = size
        self.words = sorted({w.upper() for w in words}, key=len, reverse=True)
        self.secret_phrase = secret_phrase.upper().replace(" ", "")
        self.rng = random.Random(seed)
        self.grid = [["" for _ in range(size)] for _ in range(size)]
        self.solution = {}       # word -> [(row, col), ...] en orden
        self.secret_cells = []   # [(row, col), ...] en el orden de la frase
        self.failed_words = []

    # ------------------------------------------------------------------ #
    def _perimeter_path(self):
        """Devuelve las celdas del borde del tablero en un recorrido continuo."""
        n = self.size
        cells = []
        for c in range(n):
            cells.append((0, c))
        for r in range(1, n):
            cells.append((r, n - 1))
        for c in range(n - 2, -1, -1):
            cells.append((n - 1, c))
        for r in range(n - 2, 0, -1):
            cells.append((r, 0))
        return cells

    def _place_secret_phrase(self):
        if not self.secret_phrase:
            return
        perimeter = self._perimeter_path()
        n_letters = len(self.secret_phrase)
        step = max(1, len(perimeter) // n_letters)
        start = self.rng.randint(0, step - 1) if step > 1 else 0
        for i, letter in enumerate(self.secret_phrase):
            idx = (start + i * step) % len(perimeter)
            r, c = perimeter[idx]
            self.grid[r][c] = letter
            self.secret_cells.append((r, c))

    # ------------------------------------------------------------------ #
    def _fits(self, word, row, col, dr, dc):
        n = self.size
        for i, letter in enumerate(word):
            r, c = row + dr * i, col + dc * i
            if not (0 <= r < n and 0 <= c < n):
                return False
            current = self.grid[r][c]
            if current != "" and current != letter:
                return False
        return True

    def _place_word(self, word, max_attempts=400):
        for _ in range(max_attempts):
            dr, dc = self.rng.choice(DIRECTIONS)
            row = self.rng.randint(0, self.size - 1)
            col = self.rng.randint(0, self.size - 1)
            if self._fits(word, row, col, dr, dc):
                coords = []
                for i, letter in enumerate(word):
                    r, c = row + dr * i, col + dc * i
                    self.grid[r][c] = letter
                    coords.append((r, c))
                self.solution[word] = coords
                return True
        return False

    # ------------------------------------------------------------------ #
    def _attempt_full_generation(self):
        self.grid = [["" for _ in range(self.size)] for _ in range(self.size)]
        self.solution = {}
        self.secret_cells = []
        self._place_secret_phrase()
        failed = []
        for word in self.words:
            if not self._place_word(word):
                failed.append(word)
        return failed

    def generate(self, max_retries=60):
        """
        Intenta colocar todas las palabras. Si alguna no cabe (puede pasar
        por mala suerte en el orden aleatorio), se reintenta el tablero
        completo con una variacion de la semilla hasta max_retries veces.
        Esto hace que el generador sea robusto aunque el profesor cambie
        la lista de palabras en game_data.py.
        """
        base_seed = self.rng.randint(0, 10**9)
        best_failed = None
        for attempt in range(max_retries):
            self.rng = random.Random(base_seed + attempt)
            failed = self._attempt_full_generation()
            if not failed:
                best_failed = []
                break
            if best_failed is None or len(failed) < len(best_failed):
                best_failed = failed
        self.failed_words = best_failed or []

        alphabet = string.ascii_uppercase
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == "":
                    self.grid[r][c] = self.rng.choice(alphabet)
        return self.failed_words

    # ------------------------------------------------------------------ #
    def as_text(self, mark_solution=False, mark_secret=False):
        """Representacion en texto plano, util para depurar o exportar."""
        lines = []
        header = "   " + " ".join(f"{c:2d}" for c in range(self.size))
        lines.append(header)
        solved_cells = set()
        if mark_solution:
            for coords in self.solution.values():
                solved_cells.update(coords)
        secret_cells = set(self.secret_cells) if mark_secret else set()
        for r in range(self.size):
            row_out = [f"{r:2d} "]
            for c in range(self.size):
                ch = self.grid[r][c]
                if (r, c) in secret_cells:
                    row_out.append(f"[{ch}]")
                elif (r, c) in solved_cells:
                    row_out.append(f" {ch}*")
                else:
                    row_out.append(f" {ch} ")
            lines.append("".join(row_out))
        return "\n".join(lines)


if __name__ == "__main__":
    # prueba rapida / smoke test
    words = ["CULTURESHOCK", "HONEYMOON", "FRUSTRATION", "RESPECT", "EMPATHY"]
    gen = WordSearchGenerator(18, words, secret_phrase="RESPECT ALL CULTURES", seed=42)
    failed = gen.generate()
    print(gen.as_text(mark_solution=True, mark_secret=True))
    print("Failed:", failed)
