# VESSEL

**A psychological horror visual novel about bodily autonomy, control, and the quiet violence of care.**

---

## What Is Vessel?

You play as Lily, a twenty-three-year-old former valedictorian who wakes up eighteen weeks pregnant with quadruplets in a luxury "wellness facility." Your every need is attended to by devoted caretakers who bathe you, dress you, feed you, and never, ever let you be alone.

The horror isn't monsters or gore. It's the slow realization that you can't put on your own socks. That every act of tenderness is a form of control. That the warm milk they bring you every night is why you can't think straight. That when they call you a "good girl," they mean it the way a farmer means it.

Vessel explores:
- **Bodily autonomy** — what happens when your body is no longer yours
- **Reproductive coercion** — pregnancy as product, motherhood as labor
- **Infantilization** — how care becomes a cage
- **Institutional control** — the facility that looks like a resort and functions like a farm
- **Complicity and resistance** — the choices you make when none of them are free

## Content Warning

This game contains depictions of reproductive coercion, forced pregnancy, medical violation, drugging, loss of autonomy, and psychological manipulation. It is intended for mature audiences. If you find the content distressing, please take breaks as needed.

---

## Download & Run

### Requirements
- [Ren'Py SDK](https://www.renpy.org/latest.html) (free — Windows, Mac, Linux)
- Git (to clone the repo)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/sentarot/Vessel.git

# 2. Download and extract Ren'Py from https://www.renpy.org/latest.html

# 3. Copy the game folder into your Ren'Py projects directory
cp -r Vessel/vessel_game /path/to/renpy/

# 4. Launch Ren'Py, select "vessel_game", and click "Launch Project"
```

### Alternative — Command Line
```bash
/path/to/renpy/renpy.sh /path/to/Vessel/vessel_game
```

On Windows:
```
\path\to\renpy\renpy.exe \path\to\Vessel\vessel_game
```

### No Git?
Click the green **Code** button on the GitHub page and select **Download ZIP**. Extract it, then follow from step 2 above.

---

## What's In the Game

### Cycle One: Awakening
The first pregnancy. You don't understand what's happening yet. You experience:
- Morning routines where two women bathe and dress you
- "Prenatal yoga" that amounts to lying on pillows while others exercise
- Pool therapy — the only time your body feels like your own
- A doctor who talks about you like livestock
- Overheard conversations that don't add up
- The birth, the separation, and the horrifying truth about what comes next

### Cycle Two: The Knowing
You're pregnant again. This time, you're awake. Cycle Two introduces:
- **Elena** — a woman on her fourth cycle who has spent eight months planning an escape
- **Escape mechanics** — study the walls, the staff shifts, the cameras
- **A midnight escape sequence** — drag your pregnant body through a drainage gap under a twelve-foot wall
- **Three endings**:
  - **Escaped** — you make it over the wall and into the night
  - **Recaptured** — they catch you, and the drugs take everything back
  - **Enduring** — you stay, but you remember, and you plan

### Mechanics
- **Fatigue / Dignity / Resistance** — tracked throughout, shifted by your choices
- **Hope / Compliance** — introduced in Cycle Two as the stakes change
- **Status Screen** — view your deteriorating physical condition at any time
- **Inventory** — your dress has no pockets; everything you need is in Aria's tote bag

---

## Project Structure

```
Vessel/
└── vessel_game/
    └── game/
        ├── script.rpy        # Cycle One (~640 lines)
        ├── cycle_two.rpy     # Cycle Two (~700 lines)
        ├── screens.rpy       # Status, inventory, and UI screens
        ├── gui.rpy           # GUI configuration
        ├── options.rpy       # Game settings
        ├── gui/              # GUI assets
        └── images/           # Background images
```

**Version**: 0.2 — Cycles One & Two playable (~1,800 lines of script)

**Note**: The game currently uses text-based scene labels (e.g., "bg bedroom morning") rather than illustrated backgrounds. Ren'Py displays these as text, which works fine for playing through the full story. Art assets can be added later.

---

## Roadmap

- Cycle Three and beyond
- Cross-cycle consequence tracking
- Background art and character sprites
- Sound design and music

## Credits

Built with [Ren'Py](https://www.renpy.org/).

---

*This is a work of fiction. It is designed to make you uncomfortable — not because discomfort is the point, but because the things it depicts should never be comfortable.*
