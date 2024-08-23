# Universal Servo Horn for ERCF v2 Community MMU.

## Description

This is a new and improved, universal ERCF v2 Community Edition servo horn for Savox, GDW, and SG90 servos commingly used on this mmu.
Unlike the existing horn, this is printed on its side with layers running in the same direction as the ERCF tophats to reduce friction when its engaged.
Print as oriented, install 10mm BHCS and semi-captive nut before installing on the servo. Use a fine file or sandpaper to very lightly smooth and knock off any high layers / points on the sole of the horn where it engages with the tophat.

I find it easier to install by first setting the ERCF servo to the move position (``MMU_SERVO pos=move``), attaching and positioning the horn on the servo until you can move the carriage without it catching or rubbing on tophats while still in the move position. Once you are happy, seat the horn using the servo screw before tightening the m3 SHCS sufficiently to clamp and imprint the horn on the servo splines so it doesnt move or wiggle. The servo screw only needs to be tight enough to seat the horn as the bulk of the load is carried by the clamp and M3 compression screw. While it needs to be reasonably tight, take care not to overtighten it too far and deform the shape of the horn. Once its secure, check and update servo up, move, and down positions (``MMU_SERVO ANGLE=<angle>`` followed by ``MMU_SERVO POS=<up|down|move> SAVE=1`` to update the configuration)

If you are unfortunate enough to strip the splines you should be able to retighten the M3 clamp 1-2 times before needing to reprint and replace it.

![Universal Servo Horn.png](images/Servo_Horn_1.png)
![Universal Servo Horn.png](images/Servo_Horn_2.jpeg)

## Change Log


* Published
