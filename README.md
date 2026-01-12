# Space Game 

A physics-based survival game built with Processing (Python Mode). Jump from planet to planet, collect stars, and try not to get lost in the void of space!

## 🚀 How to Play
1. **Start:** Click the mouse on the intro screen to begin.
2. **Jump:** Press the `SPACE` bar to launch the astronaut from the current rotating planet.
3. **Goal:** Land on the next planet to move forward. Collect stars along the way to increase your score.
4. **Game Over:** If you fly off the screen or miss a planet, the game ends. Click to restart!

## 🛠️ Setup Instructions
This game was developed using **Processing 3.5.4**. To run it locally:

1. Download and install [Processing 3.5.4](https://processing.org/download/releases).
2. Open Processing and install **Python Mode** (via the Mode dropdown > Add Mode).
3. Install the **Minim** audio library:
   - Go to `Sketch` -> `Import Library...` -> `Add Library...`
   - Search for **Minim** and click Install.
4. Clone this repository or download the ZIP file.
5. Open `SpaceGame.pyde` and press the **Run** button.

## 📁 Project Structure
* `SpaceGame.pyde`: The main source code.
* `data/`: Contains all game assets (images and audio files).

## 🌟 Features
* Dynamic planet generation.
* Real-time collision detection for stars and planets.
* Custom audio feedback for jumping, collecting coins, and game over.
