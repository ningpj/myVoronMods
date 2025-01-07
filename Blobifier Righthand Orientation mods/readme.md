# *** Work in progress ***  Blobifier Modifications

## Description

This is a work in progress and dumping ground for sharing Blobifier modifications to support left and right hand Voron 2.4 installation and concepts for silicon gantry and fixed nozzle wipes / rest options.
The gantry Wipe / Rest is derived from the excellent work @igannakas (Discord) pioneered to reduce colour contamination when changing and purging filaments for mmu prints.<br />
<br />


*Design Goals*
- **Gantry Nozzle Wipe Rest**. Redesign to incorporate
  - Dovetail sliders to make it easier to adjust, reduce mounting hardware and improve rigidity
  - Internal mount and arm voids to improve rigidity - 0.1mm 2x voids (printed parts will always flex to an extent)
  - More material to secure m3 heat sets
  - A1 Mini silicon wiper block. While easier to secure and replace, its smaller and has shorter knobs than the original A1 wiper (zig zag wipe option may help overcome size limitations)
  - Experiment with high temp silicon tubing as nozzle rest with filament pin to secure (Dubro aero/heli silicon fuel tubing - 180c-ish temp). Evaluate 250c silicon syringe and hole plugs from aliexpress as alternatives
  - Additional options to detach filament klingons / blobs before final wipe (e.g. double silicon rest, angled edge and cutaways on mount, etc)  
 
- **Blobifier**
  - Ambidextrous macro logic to handle left and right hand installation (optimise moves based on install orientation e.g. towards and away from Blobifier)
  - Incorporate additional maximum print area bounds checking where it makes sense 
  - Implement Zig zag wiper motion to improve wipe efficacy
  - Customisable nozzle shake option to help detach belligerent blobs (default: off)
  - Customizable tray iterations to help detach belligerent blobs (default: 1)
  - Move servo dwell setting to main Blobifier configuration block
  - Zero and restore PA before / after purging 
  - Support fixed (static) and optional 2.4 gantry mounted nozzle wipe & rest options. Allow use of one or both options
  - Redesign and experiment with fixed wipe and park mount that extends over Blobifier tray to maximise print area
  - Design bucket shaker option for Yavoth hotend
  - Improve depressor pin avoidance logic (base on HH tip cut location and settings)

*MK II Gantry Wipe Rest* <br /> 
![v2.4_Gantry_Wipe_Rest_MK_II](images/v2.4_Gantry_Wipe_Rest_MK_II.png)
![v2.4_Gantry_Wipe_Rest_MK_II_Double_Rest](images/v2.4_Gantry_Wipe_Rest_MK_II_Double_Rest.png)
![v2.4_Extended_Static_Wipe_Rest](images/v2.4_Extended_Static_Wipe_Rest.png)

<br />
<br />
*ERCF with Savox 0255MG Servo* <br /> 
![Universal Servo Horn.png](images/Servo_Horn_2.jpeg)
<br />
<br />

##Current Printer setup
Voron 2.4 300mm. Klicky PCB dock on the extreme left, z-endstop, blobifier gantry nozzle wipe rest (needs to be move closer to blobifier once design/modifications are finalised), Blobifier on right, EREC (no toolhead cutter or depressor pin), and Yavoth hotend.

##Nozzle Tip Temp
Measurements of actual external nozzle tip temperature from 300c - 240c (started at 300c and dropping to lower temps).  Measured with multimeter and thermocouple between silicon tube and nozzle. <br />
External nozzle tip temperatures consistently 40c or so below actual HE temperature target.

![Nozzle_Tip_Temperatures](images/Nozzle_Tip_Temperatures.png)
