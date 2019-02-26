# Gripper Dataset.

![](./recon.gif)
We implemented only the end-effector rather than the entire robot arm since controlling the robot arm during a picking task is easily computable by calculating the inverse kinematics and inverse dynamics. Gripper is a 12-dimensional dataset: [joint x position, joint y position, finger1 joint position (angle), finger2 joint position (angle), box1 x position, box1 y position, box2 x position, box2 y position, ball1 x position, ball1 y position, ball2 x position, ball2 y position]. Eight factors are represented in this dataset: 1) color of ball to pick up, 2) initial location of red ball, 3) initial location of blue ball, 4) initial location of blue basket, 5) initial location of red basket, 6) plan for using end-effector to move to ball to pick it up [first, moving horizontally to the x-location of ball then descending horizontally to the y-location of ball, like the movement of the doll drawing machine (perpendicular motion); second, moving straight to the location of ball to pick it up (oblique motion)], 7) plan for using end-effector to move to point above basket after picking up ball (perpendicular or oblique motion), 8) plan for placing ball into basket (by dropping ball or descending to basket and gently placing ball into basket). The two balls and two baskets are placed randomly among the four initial positions. The movement of the robot is hard-coded on the basis of a goal-position-based script. To reduce collision-detection errors during the simulation, we used a large physical model (end-effector size ~1 m), which did not affect the overall validity. The length of the data-point sequence was 400.

## Label Table

| Degree of factors | Ground-truth factors               |
| ----------------- | ---------------------------------- |
| 4                 | Red ball initial position          |
| 4                 | Blue ball initial position         |
| 4                 | Red basket position                |
| 4                 | Blue basket position               |
| 2                 | Plan to reach target ball          |
| 2                 | Plan to reach corresponding basket |
| 2                 | Plan to place ball into basket     |

