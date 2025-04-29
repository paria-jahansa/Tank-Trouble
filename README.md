# Tank-Trouble
This Python Code is designed for a two-player tank battle game that uses a randomly generated maze as the battleground. Here’s a quick summary of its key features:

1. Maze Generation (DFS-inspired):

    Randomly chooses horizontal or vertical bias (a == 0 or 1).
    Ensures sparse connectivity to create a playable, yet challenging, maze.

2. Tank Movement:

  Player 1 uses arrow keys (↑↓←→) + M to fire.
  Player 2 uses E/D/S/F + Q to fire.
  Tanks can rotate and move forward/backward.

3. Bullet Physics:

  Bullets bounce off walls.
  Bullets are limited (5 max per tank).
  After a certain time or collision, bullets disappear.
  A direct hit disables a tank and ends the round.

4. Walls & Collision:

  Wall sprites are used for physical boundaries.
  spritecollide() checks are done to prevent players or bullets from passing through them.

5. Visual Feedback:

  Display score and winning tank after each round.
  Game waits for a click to restart.
