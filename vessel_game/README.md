# VESSEL - A Psychological Horror Simulator

## About
Vessel is a Ren'Py visual novel exploring themes of bodily autonomy, reproductive control, and the horror of being reduced to a vessel. Cycles One and Two are now playable.

## Content Warning
This game contains mature themes including:
- Loss of bodily autonomy
- Reproductive coercion
- Medical violations
- Infantilization
- Psychological horror
- Pregnancy-related content

This game is intended for mature audiences and explores uncomfortable themes about autonomy and control.

## Installation & Running

### Requirements
- Ren'Py SDK (download from https://www.renpy.org/latest.html)
- Compatible with Windows, Mac, and Linux

### How to Play

1. Download and install the Ren'Py SDK from https://www.renpy.org/latest.html

2. Extract the Ren'Py SDK to a location on your computer

3. Place the entire `vessel_game` folder into the Ren'Py SDK folder

4. Launch the Ren'Py Launcher

5. Select "vessel_game" from the project list

6. Click "Launch Project" to play

### Alternative Method
You can also navigate to the `vessel_game` folder and run it directly with Ren'Py from the command line:
```
/path/to/renpy/renpy.sh /path/to/vessel_game
```

## Game Features

### Cycle One: Awakening
Experience the protagonist's first pregnancy cycle as she gradually discovers the true nature of the facility she's trapped in. The narrative focuses on:
- Daily life at the luxury wellness facility
- Increasing physical dependence
- Encounters with caretakers and other residents
- The horrifying revelation at the end

### Cycle Two: The Knowing
Lily is pregnant again — and this time she's aware of what's happening. Cycle Two introduces:
- **Elena** — a veteran on her fourth cycle who has been planning an escape for eight months
- **Escape mechanics** — gather clues, study staff patterns, find weaknesses in the facility
- **A midnight escape sequence** with real stakes and branching paths
- **Three distinct endings**:
  - **Escaped** — breach the wall and flee into the night
  - **Recaptured** — caught and drugged back into compliance
  - **Enduring** — stay behind, but carry the knowledge forward
- New stats: Hope, Compliance, Escape Clues, Ally Trust

### Game Mechanics
- **Status Screen**: Track the protagonist's physical deterioration and mental state
- **Inventory System**: Experience the frustration of limited autonomy through restricted inventory
- **Choice System**: Choices carry real weight — especially in Cycle Two where they determine your ending
- **Stat Tracking**: Monitor Fatigue, Dignity, Resistance, Hope, and Compliance

### UI Elements
- Press "Status" button to view physical condition
- Press "Inventory" button to see what you can/cannot access
- All choices affect internal stats and character development

## Technical Notes

### File Structure
```
vessel_game/
├── game/
│   ├── script.rpy          # Cycle One story script
│   ├── cycle_two.rpy       # Cycle Two story script
│   ├── screens.rpy         # Custom UI screens
│   ├── gui.rpy            # GUI configuration
│   ├── options.rpy        # Game options
│   ├── images/            # Background images
│   │   └── bg *.png       # Scene backgrounds
│   └── gui/               # GUI images
│       ├── main_menu.png
│       └── game_menu.png
```

### Customization
You can customize:
- Background images (replace files in `game/images/`)
- Character portraits (add to `game/images/` and reference in script)
- Sound effects and music (add to `game/audio/` when available)
- Text speed and other preferences in-game

## Development Status

**Current Version**: 0.2 - Cycles One & Two

**Completed**:
- Cycle One narrative arc (linear with dialogue choices)
- Cycle Two narrative arc (branching with three endings)
- Core game mechanics and stat tracking
- Status and inventory systems
- New characters: Elena, Nurse Patton
- Escape sequence with multiple paths
- ~1,800 lines of script

**Planned for Future Updates**:
- Cycle Three and beyond
- Consequences that carry across cycles
- Sound design and music
- Character sprite artwork
- Background art
- Additional UI polish

## Credits

Created as a psychological horror exploration of themes around autonomy, control, and the commodification of reproduction.

Built using Ren'Py Visual Novel Engine (https://www.renpy.org/)

## Feedback & Support

Cycle Two introduces meaningful branching and consequences. Future cycles will expand on:
- Outcomes of Lily's escape (or recapture)
- Deeper character development for caretakers and residents
- Cross-cycle consequence tracking
- Additional gameplay mechanics

## License

This is a creative work exploring difficult themes. Please engage with it thoughtfully.

---

**Remember**: This is a work of fiction designed to explore uncomfortable themes in a cathartic way. 
If you find the content distressing, please take breaks as needed.
