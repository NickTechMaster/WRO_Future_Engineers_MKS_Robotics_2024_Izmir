**Motorization**

We used a Funduino kit as the foundation, specifically designed for Future Engineers. However, from this kit, we only used the base plates, distance sleeves, and the steering mechanism. The exact dimensions and measurements of the plates, screws, and other components can be found in the assembly instructions (e. Assembly Instructions).

**Steering**  
For steering, we use a 20-kg servo steering motor. This motor is mounted horizontally on our base plate. A small rod, secured with screws, runs from the servo’s thread to the actual steering axle. This axle connects the two front wheels. When the servo turns in one direction, the entire steering axle shifts, which in turn moves the wheels.

**Drive Motor**  
As the drive motor, we use a standard DC motor, which is operated via the motor controller "L298N." It is directly connected to the 18V battery. The motor is then powered by the motor driver. Three wires extend from the motor controller, which we use to control the motor, and they are connected directly to the controlling Raspberry Pi. The Pi sends a PWM signal. A PWM signal (Pulse Width Modulation) is an electrical signal that varies the "On" and "Off" duration to control power. To drive both wheels simultaneously, we use a gear transmission that transfers the motor’s rotations to a gear firmly attached to the drive axle. The drive axle is split in the middle, but the two ends are connected with a coupling sleeve. This allows one wheel to rotate freely. Previously, we encountered a problem where the car’s wheels would lock due to power issues. Now, with one wheel able to rotate freely, this issue occurs less frequently.
