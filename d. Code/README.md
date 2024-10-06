**In this folder, you will find the programming for the robotic car.**

We are using two different Raspberry Pis, so we have a total of four scripts: two for the opening race and two for the obstacle race.

- **f = driving Raspberry Pi**
- **k = camera Raspberry Pi**

### Programming for the Opening Race

In this year's opening race, we are using the basic idea from last year. While driving, the robot continuously measures the values from the ultrasonic sensors located at the front, left, and right. Based on the values from the left and right sensors, the robot calculates the center point and steers the autonomous car proportionally to return it to the middle as efficiently as possible. This means that the further the car is from the center, the stronger it steers to get back to it.

For example: If the left ultrasonic sensor reads 10 and the right ultrasonic sensor reads 50, the left sensor is showing a very short distance, meaning the car is quite far to the left near the barrier. If we take the sum of both values, we get 60. Half of that is 30. When both sensors read 30, we know that the robot is exactly in the center. To reach this center, we calculate the percentage difference and steer accordingly.

Since this process is repeated very quickly and frequently, the car may sometimes sway slightly, but this is corrected by the system. To ensure the car stops perfectly after 3 laps, it increases a variable each time it takes a turn. We detect a turn when the color sensor detects orange or blue. The upper Raspberry Pi, which receives this data, sends it to the driving Raspberry Pi. The driving Raspberry Pi counts 12 turns and then continues until the front ultrasonic sensor detects a certain distance, at which point the car stops.

### Programming for the Obstacle Race

For the obstacle race, we use the programming from the opening race as the foundation, since we also need to drive autonomously here. Only when the camera detects a colored block does the upper Raspberry Pi send a signal to the driving Raspberry Pi, which then performs a corresponding evasive maneuver. We go around red blocks to the right and around green blocks to the left. Additionally, we detect turns using the color sensor, where we perform a realignment maneuver.

For color detection of the blocks, we use filters/masks to only see the relevant colors and filter out other potential errors the camera might detect. We then detect the contours of the objects. To adjust the color values of the masks, we wrote an additional script with sliders.