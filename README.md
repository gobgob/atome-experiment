# atome-experiment

## How it works

- The raspi execute `match.sh` after booting.
- It's waiting to be able to connect the robot.
- A soon as the experiment can open a connection, we run the motor for x seconds.
- After the script we `halt` to shutdown safely the raspi.

That's it!