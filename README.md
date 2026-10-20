# Regolith

An early prototype of a life and base-building game on the Moon, built with Pygame.

## Running the game

With the environment ready, run `make run`. To set it up from scratch, run `make install`.

## Controls

- **WASD / arrow keys:** move the character.
- **B:** switch between exploration and construction modes.
- **1–5 / click a toolbar slot:** select one of the first five inventory slots.
- **Click the board:** place the selected module in construction mode.
- **Tab:** open or close the inventory. Click two slots to swap their contents.
- **E:** inspect a nearby module; press E again to close its window.
- **R in the module window:** return the module to the inventory.
- **Escape:** close the current window, leave construction mode, or exit the game.

Each session starts with three units of every module. Placing a module consumes
one unit; picking it up returns it. The toolbar displays the same quantities as
the inventory. Open windows pause movement and block construction.

This version supports placing modules, exploring, inspecting buildings, and
picking them up. Resource production, stat depletion, and game saving are not
yet implemented.

## Code style

Python files use four spaces, double quotes, and an 88-character line length.
Imports are grouped into standard library, third-party, and project imports.

Source code is organized into `core` (shared game systems), `entities` (world
objects and the player), and `ui` (interface rendering and interaction).
