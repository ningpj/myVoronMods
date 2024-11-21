# Enraged Rabbit Carrot Feeder v1.x (ERCF) MMU Build Guidance

ERCF is an awesome addition to any klipper based 3d printer but can take time to calibrate and tune to get it to operate reliably. As fluedddi said recently in discord, *Having one beats needing one!* :-) Taking extra care during assembly will eliminate much frustration later on :-)

## Preparation
* **`Manual:`**  Read the ERCF manual and familiarise yourself with overall build process before commencing assembly. 
<br>Docs for ERCF v1.x can be found here: https://github.com/EtteGit/EnragedRabbitProject/blob/main/Documentation/ERCF_Manual.pdf

* **`Printed Parts:`**  Like all other Voron printed parts, ERCF parts are designed to accommodate ABS shrinkage. If using other filaments like PLA YMMV, please check tolerances by printing the calibration part and test fitting 8mm rod, m5 nut, magnet and filament (refer Pg 6 of the ERCF Manual).
<br><br>Parts are printed using standard Voron print settings (Refer Pg 4 of ERCF manual)
  ```  0.2mm layers
    Forced 0.4mm width
    40% infill - Grid, Gyroid, Honeycomb, Triangle or Cubic
    4 walls
    5 top and bottom layers    
*  **`Extruder Bowden:`**  You will need a Clockwork 1/2 face plate (& latch) or extruder with EACS or PC8 connectors to secure the bowden during ERCF load operations. e.g Clockwork 2 alternate: 
https://github.com/EtteGit/EnragedRabbitProject/tree/main/usermods/CW2_with_ECAS_and_optional_sensor

* **`ERCF Software:`** While the ERCF Github repo includes macros and python klipper extension these aren't being actively maintained or enhanced and recommend you install the Happy Hare v3 driver. Happy Hare includes a custom klipper servo driver to work around klipper timing issues, automated run out management and setup, sensor-less and sensor based filament homing options, very useful debug and other highly evolved operational features to improve the overall user experience! Full details and setup instructions here: https://github.com/moggieuk/ERCF-Software-V3

## Build
* **`Filament Gates:`**  Check gate washers during assembly to make sure they are 1) magnetic and 2) are SMOOTH on both sides otherwise they can get stuck in the carrier and cause intermittent issues.  One side is usually smooth as they are manufactured using a die punch. Run the rough side across a fine file or sand paper to smoot.  Also check the washer carrier for any print artefacts / obstructions that could cause them to get stuck. <br> <br> You can also consider using upspec'd N52 magnets rather than more common N35 magnets for the encoder cart to improve gate reliability and operation.  Its not essential but will help eliminate load failures and a potential source of *~~frustration~~* friction from the filament path. 

* **`M5 Rods:`**  Leave tightening the main ERCF M5 rods until you have the ERCF on a flat surface or secured to a 2020 rail.  Its really easy to over tighten these and create a back bow which may prevent the main drive shaft form turning freely. The shaft should turn easily without any binding with the GT2 belt unattached. Remember when tightening, the rods only need to be snug not hulk tight.

* **`D-Drive Shaft:`**  During assembly check the main drive shaft spins freely. For example without the belt on it should be buttery smooth and spin for a 1/2-1+ revolution when you flick the knob. If you any feel resistance or binding (rubbing), your Gear stepper stalls and whines, recheck the following areas 
  * 80T is centred & has clearance and isnt rubbing on gear box or motor mount.
  * 80T GT2 20T hub is fully seated and you have used the correct button head screws to secure it (BHCS).
  * BMG gears are all centred in their carts and grub screws aren't catching or protruding.
  * Your D-Shaft isnt bent (hard to verify post installation.
  * GT2 belt isnt too tight or able to handle rotational variations of the printed 80T.
  * Insufficent tollerance/play between motor mount/gearbox and 80T causing it to bind (try loosening motor mount / gear box bolts to verify).
  * Manual D-shaft knob isnt pressing hard up against motor mount.
  * Asking too much of your gear stepper speed & accel wise (older steppers may not be able to support default load from buffer speeds and accels.  Also check stepper crimps to make sure both windings/pairs are connected to prevent stepper running running at reduced power.

* **`Drive Belt:`** There's a tendency to over tension the 80T GT2 belt …. don't, its not necessary.  In fact it needs to be looser than you think to compensate for rotational variations of the printed 80T part and hub.  Make sure the 80T wheel is as centred and square as you can get it and/or use a printed jig during assembly (https://github.com/Enraged-Rabbit-Community/ERCF_v2/blob/master/Stls/Tools/80T_Cog_Guide.stl)). Unfortunately you will never be able to get it perfectly true which is why the drive belt needs to be loose. If you don’t the Nema 14 will bind and make alarming noises when loading/unloading. Alot of people are critical of the printed 80T for the above reasons. However given its relatively low mass and a stock Nema 14, it can spin very quickly.    

* **`Top Hats:`**  Start with the same thickness e.g. One Dot and save tuning these until you have the ERCF secured to a 2020 rail or on a flat surface.  Assuming all BMG gears are from the same supplier all top hats "will" generally be the same thickness if the ERCF is true and flat.  Work your way up until your filament doesn’t slip. Its fine if one or two are thicker to account for part and BMG gear variations. However if you find you need thicker top hats on middle gates you may have a bowed ERCF.    

* **`Nema 14:`**  Contrary to popular belief the Nema 14 is plenty fast and has low rotation mass so it can spin very quickly. It just doesn’t have much torque when initially spinning up so you need to make sure the main belt and drive shaft spin freely.  I load filament at 300mm/sec with run_current @ 0.5A on a LDO Nema 14 (LDO-35STH28-1004AC3DT) without issue.

* **`Filament Passthrough Mount:`**  IMHO this user mod should be a standard part of the build as its really handy to be able to manually load filament from time to time.  Print and fit one passthrough (bypass) mount from the user mod directory during assembly as its much easier and less frustrating than tearing it down later and risk stripping BMG grub screws - ask me how I know :-( (https://github.com/EtteGit/EnragedRabbitProject/tree/main/usermods/Bearing_Block_Passthrough).

* **`ECAS:`**  Install the ECAS connectors by rocking them gently from side to side as you press them in.  If you press them in square you will almost always split the part.

* **`Latches:`**  Scrape and smooth extrusion layers on latch points with a blade if you find your latches are too hard to operate when test fitting them. They will eventually sort themselves out over time but is easier to clean them up during assembly. Also be careful when pushing down and latching top hats as its relatively easy to break the top hat guide posts on the cart. Just make sure the top hat is centred before latching. 

* **`Encoder Cart:`**  Make sure you install the captive M3x16 SHCS encoder adjustment screw correctly and the bolt is retained by the encoder_locker inserted from the side so you can adjust the encoder height up and down.  i.e. Insert the M3 fully then the retainer to lock it in place. Correct orientation:
<p align="center"> <img width="400" class="aligncenter" alt="image" src="https://user-images.githubusercontent.com/36124687/224508911-d9e111a0-70fb-4be7-b18c-306d11dffa7a.png"> </p>
 
* **`Encoder:`**  If the encoder TCRT board is too close to the BMG gear it might not read reliably. There's a sweet spot and may need to elevate it to get reliable readings.  In my experience close isn't always best in this instance. The TCRT sends pulses when it detects movement and the LED will flash and remain in its last state (on or off) until movement is detected.  Adjust and test using a piece of filament until you get the LED to blink reliably. I usually adjust it until it touches the BMG gear then back it off until the LED blinks reliabily before continuing calibration. <br><br>
If the encoder isn't reading accurately, try the following:
  * Check you have installed the cage/blackout box around the BMG gear ([black]_Encoder_Cage.stl).
  * Adjust TCRT height (up/down) and test with filament and ERCF_DISPLAY_ENCODER_POS (standard ERCF python driver) or ERCF_TEST_TRACKING (Happy Hare) to verify.
  * If you feel filament is slipping, you can temporarily apply more pressure to the filament roller while loading/unloading filament (use a finger or rubber band wrapped around the selector cart) to see if this helps. If it does, you can install an optional M3 bolt on the bottom of the cart to permanently increase tension. Be careful to use the correct length and not strip the plastic.  
  * Blacken the top of each tooth on the BMG gear with a permanent marker or paint to create a clear differentiation for the encoder to read.  <br><br>
Excellent encoder setup guide from the author of Happy Hare (https://github.com/moggieuk/ERCF-Software-V3/blob/master/doc/ENCODER.md).

## Servo Issues
* **`Easy BRD:`**  If you experience servo issues, replacing the 7805 linear voltage regulator with a buck convertor or bypassing it entirely and wiring 5v directly to the board will help as peak servo load can get close to exceeding 1A and triggering thermal limits of the 7805 package. I fitted a 7805 pin compatible 5v buck converter as a precaution to mitigate this.

* **`Savox:`**  Digital servos like the Gucci Savox option are proven to be less susceptible to 5v power issues or not holding position. In my experience Tower Pro clones can work reliably especially now there we have a custom Happy Hare servo driver and fix for Klipper PWM timing issue causing servos to move from their position when powering off. If you are using Happy Hare, make sure you are using an up-to-date version. The Savox also needs a small printed adaptor under the Options directory (Savox_Adapter.stl)

* Make sure the servo arm moves to the correct position on the top hat (refer Pg 104 in ERCF manual). Its difficult to see but the servo arm actually mechanically locks in place on a small indentation on the top hat and may not hold after power is turned off if the servo down angle / position isn't correctly tuned.

* Servo issues can also be caused by a stripped servo arm especially after playing around with high top hats to address slippage issues. Not always, but not alway obvious so useful to check and print a few spares to have on hand.

## Setup
* If not using Happy Hare software, set hold_currents for both steppers as they can get quite hot when idle. Happy Hare defaults are a good starting point (0.1 gear, 0.3 selector).  If using sensorless homing you "may" need to increase selector hold current to avoid TMC errors.  If not, hold current can be lower.
* Setting sync_unload to 40 and sync_unload_speed to 50 can help improve unload reliability and issues ejecting hot, fat tips as well as speeding up the overall process up.  I also load fast (50) though to the extruder, again to speed things up.
* **`Rapido:`** The Rapido hotend has a very narrow heatbreak tube and several points where filament can potentially get caught during load and tip forming functions.  You "may" find that you need to slightly chamfer the bottom of the PTFE well in the heatsink and the inner edge of the heat break tube by hand using a suitable drill bit to improve this. Use a square/blunt piece of filament to check catch points but be careful not to remove too much material (you have been warned). I strongly recommend sorting this out before stressing about filament tips as you need reliable filament loading / unloading as it can interfere with the tip forming process. In my case, this fixed random 1 in 15 load failures.
* Enabling Stallguard Senor-less homing on the selector stepper is recommended when using Happy Hare as it improves detection and recovery options if filament obstructs the encoder cart. Without this, should the cart gets obstructed ERCF will lose track of the gate and home position and will load the wrong filament unless paused and rehomed.
* Happy Hare sensor-less filament homing works well and is the easiest option to get going (non-stallguard option as Easy Bird can only map diag port for one driver and recommend you use sensor-less stall guard homing for the selector).  Adjust extruder_homing_current down to make it less intense and likely to grind filament.  If considering a toolhead sensor the ball bearing microswitch approach is far more reliable and easy to setup than the orginal HAL affect sensor (yes the washer can and will jam).  I also found plain BMG gears in the extruder worked better than gucci coated options (Both TL sourced - better bite on the filament perhaps?). 

## Filament Tips
Depending on hotend, filament, and temp, tips can be very difficult to tune as there are a number of variables to consider. Rapido in my experience, likely due to the large melt zone and very narrow heatbreak is quite difficult and prone to clog/jam if your filament tips aren't well formed or too fat.

ABS tips (@ 245c) with eSun filament, CW2, Rapido HF and sensor-less homing to BMG.  

Sensor-less homing - home position to nozzle (melt pool) is the last move before printing. This is usually tuned until you see ooze then back off a mm or so until this no longer happens. This is set to `home_position_to_nozzle: 65` for my CW2/Rapido HF and while it could be 1mm or so longer to reduce gaps on the purge block, I prefer an ooze-less approach when changing filament out of prints. Note if you are using a toolhead sensor this distance will usually be shorter by approximately 10mm. 

I'm running all tip forming and ramming in SuperSlicer so I can tune per filament. Happy Hare is set to only tip form...This is controlled by these settings in `Happy Hare ercf_software.cfg`:
```
   variable_standalone = 0 # 0 slicer, 1 Happy Hare macro (turn off in slicer)
   variable_ss_ramming: 1
 ```

You also need to make sure you call the correct ERCF macro in your custom Slicer Tool Change g-code section if you have been using Happy Hare standalone tip forming e.g. 
```
   T[next_extruder] or ERCF_CHANGE_TOOL TOOL=[next_extruder]
```
Tip forming settings for _ERCF_FORM_TIP_STANDALONE macro have been tested with eSUN ABS and attempt to confine filament tip and cooling moves within the Rapido heat sink and PTFE / narrow heat break tube. To work out where the tip is formed, manually insert a peice of filament until it extrudes, mark the top at a known reference point (e.g. the top of the ECAS connector) and extract the filament and measure / overlay this on a 1:1 scale view of the extruder.  In my case the tip pulls away from the melt zone just below the heater block, maybe 2mm below.  This is important as all tip forming distances are relative to this point.  Also IMHO Rapido HF values mentioned in the comments and discord spreadsheet retract too far with cooling moves happening nearer the extruder than Rapido heat sink.  
```# Unloading and Ramming values - Initial moves to form and shape tip
variable_unloading_speed_start: 100    # Fast here to seperate the filament from meltzone (Very intitial retract SS uses distance of E-15)
variable_unloading_speed: 30           # Too fast forms excessively long tip or hair. Slow is better here UNLOADING_SPEED_START/COOLING_MOVES seems a good start
variable_ramming_volume: 10            # in mm3 SS default values = 2, 5, 9, 13, 18, 23, 27. Only Used to Simulate SS Ramming during standalone
variable_ss_ramming: 1                 # Set to 0 when using standalone or for tuning (RAMMING_VOLUME). After tuning input RAMMING_VOLUME into SS and set this to 1

# Cooling Move Values - To cool the tip formed and separate from strings
variable_cooling_tube_position: 19     # Dragon ST: 35, Dragon HF: 30, Mosquito: 3, Revo: 35, Phaetus Rapido HF: 43;  Measured from Top of Heater Block to Top of Heatsink
variable_cooling_tube_length: 22       # Dragon ST: 15, Dragon HF: 10, Mosquito: 20, Revo: 10, Phaetus Rapido HF: 22; Measured from Nozzle to Top of Heater Block
variable_initial_cooling_speed: 20     # Slow to solidify tip and cool string if formed.
variable_final_cooling_speed: 100      # High speed break the string formed. Too fast = tip deformation during eject. Too Slow = long string/no seperation
variable_toolchange_temp: 0            # Used if you want to lower temp during toolchanges default 0
variable_cooling_moves: 4              # 2-4 is a good start

# SkinnyDip values - To burn off VERY FINE hairs only (This is NOT for long tip reshaping)
variable_use_skinnydip: 1              # Tune this LAST, this is for removal of VERY FINE hairs only (Different than a long tip)
variable_skinnydip_distance: 30        # Start just under Cooling_tube_position and increase - Will depend on how much Ramming Volume is used
variable_dip_insertion_speed: 30       # Medium-Slow - Just long enough to melt the fine hairs. Too slow will pull up molten filament
variable_dip_extraction_speed: 100     # Around 2x Insertion speed, Prevents forming new hairs
variable_melt_zone_pause: 0            # in milliseconds - default 0
variable_cooling_zone_pause: 1000      # in milliseconds - default 0 - If you need to adjust here its possible Dip Insertion too slow
variable_use_fast_skinnydip: 0         # default 0
```

Standalone tip forming command line and arguments for you to tune and play around with (CW2, Rapido HF) 
```
_ERCF_FORM_TIP_STANDALONE COOLING_TUBE_LENGTH=22 COOLING_TUBE_POSITION=19 INITIAL_COOLING_SPEED=20 FINAL_COOLING_SPEED=100 COOLING_MOVES=4 USE_SKINNYDIP=1 USE_FAST_SKINNYDIP=0 SKINNYDIP_DISTANCE=30 DIP_INSERTION_SPEED=30 DIP_EXTRACTION_SPEED=100 MELT_ZONE_PAUSE=0 COOLING_ZONE_PAUSE=1000 UNLOADING_SPEED_START=100 UNLOADING_SPEED=30 RAMMING_VOLUME=10 FINAL_EJECT=1 SS_RAMMING=0
```
Slicer (SS in my case) filament PARKING_POS_RETRACTION (Filament parking position) and EXTRA_LOADING_MOVE (Extra loading distance) are actually a simple calc once you have worked out cooling tube length and position. e.g. COOLING_TUBE_RETRACTION + (COOLING_TUBE_LENGTH / 2).  This is basically the upper bound and maximum retract distance from the melt zone. If you increase this your slicer will insert an unnecessary move.  Doesn't seem to have any useful purpose that I can tell. For the above setup, these are set to 30 & 29.9 respectively. Also make sure the extra load distance is a negative value and is  slightly smaller to avoid a div 0 slicer bug.

<img width="377" alt="image" src="https://user-images.githubusercontent.com/36124687/232972450-78bda438-f9b6-42cb-8d8d-221b671cff7d.png">


Also in SS, RETRACT_LENGTH_TOOLCHANGE on each extruder defaults to 10mm and suspect this "may" possibly explain why some see occasional differences between standalone tip forming and in-print standalone tip forming when using this setup.  I have this set to 0 on all extruders....that said, Im not sure under what circumstances the slicer will actually generate the extra retraction as I havent spotted it in generated gcode so far.

Purge block gaps can be tuned by increasing home_position_to_nozzle but don't cause any problems in practice.  If you see blobs on unload, you are likely dipping too far. If you see blobs on load, you may need to reduce home_position_to_nozzle or you have left off the negative sign on your extra loading distance setting.

Tips for eSUN ABS Fire Engine Red, Grey and Natural White @ 245c

<img width="396" alt="image" src="https://user-images.githubusercontent.com/36124687/232974232-21193760-b80c-447c-8148-212633126fac.png">
<img width="243" alt="image" src="https://user-images.githubusercontent.com/36124687/232974554-fd5a6c22-eb6a-4d67-ac5a-41017a78f250.png">

Can they be improved....sure....are they good enough ABSOLUTELY!!!!   

The goal here is getting reliable tips that dont cause jams, clogs, or leave whisps and junk in the extruder.

## Resource Summary
|Resource|Link
|-|-
|Enraged Rabbit Project Home|                        https://github.com/EtteGit/EnragedRabbitProject
|Discord Channel|                                    https://discord.com/channels/460117602945990666/909743915475816458
|Happy Hare v3 ERCF Driver|                          https://github.com/moggieuk/ERCF-Software-V3
|Excellent moggieuk encoder setup and tuning guide|  https://github.com/moggieuk/ERCF-Software-V3/blob/master/doc/ENCODER.md
|Toolhead Dimensions and Tip Forming Settings|       https://docs.google.com/spreadsheets/d/1FcpQ37Cf5g9mw04MGYQnhk4WGluIm2uXc-2plKwKrf0/edit?usp=sharing         

