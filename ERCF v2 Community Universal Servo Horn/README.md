# Universal Servo Horn for ERCF v2 Community MMU.

## Description

This is an enhanced, universal ERCF v2 Community Edition servo horn designed for Savox, GDW, and SG90 servos commonly used with this MMU. Unlike the existing horn, this one is printed on its side with layers running in the same direction as the ERCF tophats, reducing friction when engaged.

This is a more robust universal ERCF v2 Community Edition servo horn for Savox, GDW, and SG90 servos commonly used with this mmu. Unlike the existing horn this is printed on its side with layers running in the same direction as the ERCF tophats to reduce friction when its engaged. Instead of using printed splines, once positioned you simply clamp it down to imprint and lock it securely in place.

Print as oriented in ABS or ABS equilvent filament. Install the 10mm BHCS and semi-captive M3 hex nut before installing the horn on the servo and inspect the sole of the horn where it engages with the tophat for any high spots. If necessary, use a fine file or sandpaper to lightly smooth them to make the sole more uniform. 

Installation: I find it easier to set the ERCF servo to the move position (``MMU_SERVO pos=move``) then attach and position the horn on the servo until you can move the carriage without it catching or rubbing on tophats while the servo is in the move position. Check the sole of the horn is parallel to the servo and once happy, secure and seat the horn using the provided servo screw before tightening the M3 SHCS to clamp and imprint the servo splines so it doesn’t move or wiggle. As the Savox servo screw is reasonably short, you may need to press and rock the horn a little before you can get the screw to engage properly.  The servo screw only needs to be tight enough to seat the horn as all the load and force is handled by the M3 and clamp. While the M3 compression screw needs to be reasonably tight, take care not to overtighten as you may end up deforming the horn if you get carried away.

Once its secured in place, check and update you servo up, move, and down positions as these may have changed (``MMU_SERVO ANGLE=<angle>`` followed by ``MMU_SERVO POS=<up|down|move> SAVE=1`` for each position you want to update).

If you are unfortunate enough to strip the splines, you should be able to retighten the M3 clamp 1-2 times before needing to reprint and replace it.

![Universal Servo Horn.png](images/Servo_Horn_1.png)
![Universal Servo Horn.png](images/Servo_Horn_2.jpeg)

## Change Log


* Published
