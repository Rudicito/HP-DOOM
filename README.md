# HP-DOOM
Base of [StanislavPetrovV/DOOM-Level-Viewer](https://github.com/StanislavPetrovV/DOOM-Level-Viewer)

HP-DOOM is a DOOM port in Python on the HP Prime calculator. It's just a level viewer, no gameplay, no monster.

![doom](/screenshots/0.png)

## 🔧 Installation
1. [Download the ZIP archive](https://github.com/Rudicito/HP-DOOM/archive/refs/heads/main.zip).
2. Extract and move the `DOOM.hpappdir` folder into the **Applications** directory in the HP Connectivity Kit app.
3. On your calculator, open the **DOOM** app in Numeric view and enter: `import main`

If you want, you can change some settings in `settings.py` like the map (E1M1, E1M2, E1M3), player speed etc.

## 🎮 Controls

| Key               | Action                            |
|-------------------|-----------------------------------|
| Arrow keys        | Move                              |
| `Enter`           | Toggle screen **STRETCH**         |
| `+` / `-`         | Scale up / down                   |
| `1`               | Toggle **walls** rendering        |
| `2`               | Toggle **floors & ceilings**      |

## 📚 Documentation used
- [Youtube playlist "Recreating DOOM" by Coder Space (StanislavPetrovV)](https://youtube.com/playlist?list=PLi77irUVkDasNAYQPr3N8nVcJLQAlANva)
- [DOOM Open Source Release](https://github.com/id-Software/DOOM)
- [The Unofficial Doom Specs](https://www.gamers.org/dhs/helpdocs/dmsp1666.html)

## 📝 Licenses
All MIT except:
- DOOM1.WAD : The Doom 1 shareware WAD file is (C) Copyright id Software. The DOOM shareware wad is freely distributable.
