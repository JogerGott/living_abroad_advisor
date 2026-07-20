# ESCAPE THE CULTURE SHOCK
### A Global Explorer's Word Challenge — Juego de sopa de letras para inglés B1-B2

---

## 0. Cómo ejecutarlo

```bash
pip install -r requirements.txt   # solo pygame
python main.py
```

Controles:
- **Clic + arrastrar** sobre la cuadrícula para seleccionar una palabra (horizontal, vertical o diagonal, en cualquier dirección).
- **Clic** en los botones del panel derecho para usar Power-Ups.
- **Clic / Enter** para avanzar en pantallas de historia, misión, tarjeta sorpresa, boss challenge y reflexión.
- En el **Boss Challenge**, clic en el recuadro blanco y escribe con el teclado.

Estructura de archivos:

```
culture_shock_game/
├── main.py            # motor del juego (Pygame): pantallas, input, reglas
├── word_search.py      # generador procedural de la sopa de letras (18x18)
├── game_data.py         # TODO el contenido pedagógico (editable sin tocar el motor)
├── requirements.txt
└── docs/
    ├── grid_plain.md          # la cuadrícula limpia (para imprimir a los estudiantes)
    ├── grid_solution.md       # la misma cuadrícula con la solución marcada (*letra*)
    │                           # y el código secreto en negrita (**letra**)
    └── solution_coords.txt    # coordenadas exactas de cada palabra y de la frase secreta
```

> **Nota técnica:** la cuadrícula no fue escrita a mano. `word_search.py` la genera
> con un algoritmo que coloca cada palabra en una dirección aleatoria (8 direcciones)
> y reintenta automáticamente si alguna no cabe, así que las 26 palabras siempre
> quedan colocadas sin errores. El juego usa `PUZZLE_SEED = 7` (ver la parte
> superior de `main.py`), la misma semilla usada para generar `docs/grid_solution.md`,
> así que el tablero que ven tus estudiantes en pantalla es **exactamente** el que
> tienes en tu clave de respuestas impresa. Si quieres un tablero nuevo cada partida,
> cambia `PUZZLE_SEED = 7` a `PUZZLE_SEED = None`.

### Integración con tu PWA
El juego está desacoplado en 3 módulos (`game_data.py` = contenido, `word_search.py`
= lógica del puzzle, `main.py` = interfaz Pygame). Si tu PWA es web (JS/HTML), lo más
directo es:
1. Reusar `word_search.py` tal cual para pre-generar el puzzle en el servidor (o
   con Pyodide/Brython) y exportarlo como JSON (`grid`, `solution`, `secret_cells`).
2. Reescribir solo la capa visual en Canvas/JS conservando `game_data.py` como
   fuente única de verdad del contenido.
3. Alternativa rápida: empaquetar el juego Pygame tal cual a WebAssembly con
   **pygbag** (`pip install pygbag && pygbag main.py`) y embeberlo en un `<iframe>`
   dentro de tu PWA.

---

## 1. Título
**ESCAPE THE CULTURE SHOCK** — *A Global Explorer's Word Challenge*

## 2. Historia
Eres un estudiante de intercambio que acaba de aterrizar en un país nuevo: la maleta
pesa, el celular no tiene señal, y todos hablan un idioma que apenas entiendes.
Tu misión es sobrevivir las cuatro etapas del *culture shock*, completar retos diarios,
reaccionar ante eventos inesperados y demostrar, al final, en la entrevista de
migración (el Boss Challenge), que aprendiste a adaptarte, respetar y conectar con
una cultura nueva.

## 3. Sopa de letras (18×18, 26 palabras)
La cuadrícula completa, la lista de palabras y la solución marcada están en:
- `docs/grid_plain.md` → para repartir a los estudiantes.
- `docs/grid_solution.md` → clave del profesor (`*letra*` = parte de una palabra,
  `**letra**` = parte del código secreto).
- `docs/solution_coords.txt` → coordenadas exactas fila/columna de cada palabra.

**Las 26 palabras**, agrupadas por tema (cada grupo desbloquea una misión):

| Grupo | Palabras |
|---|---|
| Stages of Culture Shock | CULTURESHOCK, HONEYMOON, FRUSTRATION, ADJUSTMENT, ADAPTATION |
| Culture & Society | CUSTOMS, TRADITIONS, ETIQUETTE, CULTURE, IDENTITY, VALUES |
| Communication | LANGUAGE, COMMUNICATION, GREETINGS, STEREOTYPES |
| Travel & Global Life | HOMESICK, EXCHANGE, TRAVEL, GLOBAL, COMMUNITY |
| Values for a Connected World | DIVERSITY, RESPECT, INCLUSION, EMPATHY, TOLERANCE, FESTIVALS |

## 4. Misiones (una por grupo, se desbloquean automáticamente)
1. *Describe a moment when someone could experience culture shock.*
2. *Share a tradition from your country.*
3. *Explain one cultural difference you find interesting.*
4. *Give advice to a new exchange student.*
5. *Compare two cultures you know (food, greetings, or traditions).*

## 5. Tarjetas sorpresa (15)
Aparecen aleatoriamente cada 2–4 palabras encontradas (ver `SURPRISE_CARDS` en
`game_data.py`). Ejemplos: ofender a alguien sin querer, no entender el slang local,
recibir una invitación a una celebración tradicional, extrañar a la familia, probar
comida extraña, perderse en una ciudad nueva, malinterpretar un chiste, etc. Cada
una exige responder en inglés en voz alta.

## 6. Sistema de puntos
| Acción | Puntos |
|---|---|
| Encontrar palabra | ⭐ 5 |
| Completar misión | ⭐ 10 |
| Buena pronunciación *(el profesor la otorga manualmente)* | ⭐ 5 |
| Respuesta creativa *(el profesor la otorga manualmente)* | ⭐ 10 |
| Ayudar a un compañero *(el profesor la otorga manualmente)* | ⭐ +5 bonus |
| Tarjeta sorpresa respondida | ⭐ 8 |
| Boss Challenge | ⭐ 20 base + 3 por cada palabra clave usada (máx. 15) |

> Los puntos de pronunciación, creatividad y ayuda a compañeros dependen de una
> evaluación humana (el profesor los observa hablando), así que se otorgan verbalmente
> en clase; el marcador del juego lleva automáticamente todo lo demás.

**Rangos finales:** Confused Tourist → Curious Traveler → Cultural Explorer →
Global Citizen → World Ambassador.

## 7. Power-ups
- ⏱️ **Time Freeze** — congela el cronómetro 20 segundos.
- 💡 **Extra Hint** — revela la primera letra de una palabra (2 usos).
- ✨ **Double Points** — duplica puntos en las próximas 3 palabras.
- ⏭️ **Skip Challenge** — salta una misión y aun así da la mitad de puntos.
- 🎁 **Mystery Bonus** — bono instantáneo de 5 a 20 puntos.

## 8. Boss Challenge (desafío final)
En la "puerta de migración", el estudiante debe usar **al menos 10 palabras
encontradas** para escribir un párrafo (o preparar una respuesta oral de 1-2 min)
a la pregunta: *"How can a person overcome culture shock and adapt to a new
country?"*. El juego cuenta automáticamente cuántas palabras clave se usaron y
otorga el bono correspondiente.

## 9. Diseño visual
Temática de viaje: pasaportes, aviones, maletas, mapas del mundo, banderas, sellos
de viaje, globos terráqueos y brújulas. Paleta viva y moderna implementada en el
juego: azul cielo (`SKY`), azul pasaporte (`NAVY`), naranja atardecer (`SUNSET`),
dorado (`GOLD`, reservado para el código secreto y power-ups), rojo sello (`STAMP_RED`)
y verde de "encontrado" (`FOUND_COLOR`).

## 10. Extra Challenge — código secreto
Algunas letras del **borde** de la cuadrícula están resaltadas en dorado. Leídas en
orden forman la frase: **"RESPECT ALL CULTURES"** — una variación optimizada para
caber perfectamente en el borde del tablero de 18×18 del mensaje original que
inspiró este juego: *"Different cultures make the world stronger."* (puedes usar
esa frase más larga como cierre motivacional oral en clase). El juego revela el
código automáticamente en la pantalla "EXTRA CHALLENGE" al completar toda la sopa
de letras, justo antes del Boss Challenge.

## 11. Reflexión final (discusión grupal)
1. What surprised you the most about this activity?
2. Which stage of culture shock do you think is the hardest? Why?
3. How can people avoid stereotypes about other cultures?
4. Why is empathy important when meeting people from other cultures?
5. What would you do if you moved to a new country tomorrow?

## 12. Flujo completo del juego
`MENU → STORY → PLAY (sopa de letras + misiones + tarjetas + power-ups) →
SECRET CODE → BOSS CHALLENGE → REFLECTION → END (puntaje + rango)`

---

### Ideas para extender el juego (opcional)
- Modo multijugador local: dos cronómetros y comparar rangos al final.
- Exportar el puzzle a PDF con `docs/grid_plain.md` convertido vía Pandoc para
  imprimir en papel como respaldo sin computador.
- Guardar `game.score` en un archivo JSON por estudiante para llevar un ranking
  de toda la clase a lo largo del semestre.
