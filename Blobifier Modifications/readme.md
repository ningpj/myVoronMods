# *** Work in progress ***  Blobifier Modifications

## Description

This is a work in progress and dumping ground for sharing Blobifier modifications to support left and right hand Voron v2.4 installation and prototypes of silicon gantry and fixed nozzle wipe / rest options. 
The gantry Wipe / Rest redesign is derived and based on the excellent work @igannakas (Discord) has pioneered to eliminate colour contamination when changing / purging filaments during mmu prints.<br />


## Design Goals

- **Gantry & Static Nozzle Wipe Rest**.

  Redesign to incorporate:
  - Dovetail sliders to make it easier to adjust, reduce mounting hardware and improve rigidity **(DONE)**
  - Internal mount and arm voids to improve rigidity - 0.1mm 2x voids (flex is inherent in designs like this and need it as rigid as possible to cap and prevent nozzle ooze) **(DONE)**
  - More material to secure m3 heat sets **(DONE)**
  - A1 Mini silicon wiper block. While easier to secure and replace, its smaller and has shorter, more closely spaced knobs than the original Bambu A1 wiper (zig zag pattern may overcome size limitation) **(DONE - Discarded in preference to chunker, full size Bambu A1 wiper)**
  - Experiment with high temp silicon tubing as nozzle rest with filament pin to secure (Dubro aero/heli silicon fuel tubing - 180c-ish temp) **(DONE - Discarded due to ABS softening after prolonged exposure to 255c+ nozzle temp)** 
  - Evaluate 250c silicon syringe and button hole plugs from aliexpress as alternatives. Interestingly "most" silicon HE socks are only rated to 280c **(DONE Silicon button plug works well with 3mm/4mm ID/OD PTFE tube sleeve as mount to allow replacement)**
  - Additional options to detach filament klingons / blobs before final wipe (e.g. double silicon rest, angled edge and cutaways on mount, etc)  **(DONE - Discarded in preference to chunker, full size Bambu A1 wiper)**
  - Redesign and experiment with static wipe / rest extending over Blobifier tray to maximise print area. **(DONE)** Appears to work ok although blobs can stack up behind / between the static wipe / mount and blobifier base.  Still managed to fill the tray.  Changed logic to retract the tray before shaking the bucket to release any blobs trapped until the tray
 
- **Blobifier**
  - Ambidextrous motion logic to handle left and right hand installation (optimise moves based on install orientation e.g. towards and away from Blobifier)  **(DONE)**
  - Incorporate additional maximum print area bounds checking where it makes sense 
  - Implement Zig zag wiper motion to improve wipe efficacy  **(DONE)** - Maybe consider combo zig zag & swipe wiping action option 3 (e.g. 40/60 rounded ratio so 3 = 1 zigzag, 2 wipes, 4 = 2 zigzags, 2 wipes)
  - Customisable nozzle shake option to help detach belligerent blobs (default: off)  **(DONE)**
  - Customizable tray iterations to help detach belligerent blobs (default: 1)  **(DONE)**
  - Move servo dwell setting to main Blobifier configuration block  **(DONE)**
  - Zero and restore PA before / after purging  **(DONE)**
  - Support chaining of fixed (static) and optional 2.4 gantry mounted nozzle wipe & rest options. Use of one or both options in tandem  **(DONE)**
  - Bucket shaker profile for Yavoth hotend  **(DONE)**
  - Improve depressor pin avoidance logic (base on HH tip cut location and settings if configured) **(DONE)**
  - Klicky dock and handling unexpected attached probe **(DONE)** Wrapper macros provided for klicky users BLOBIFIER_SAFE and BLOBIFIER_SAFE_PARK
  - Convert all speeds from mm/min to mm/sec to be consistent with Happy Hare **(DONE)**
  - Consider park position randomiser (+/- 1.5mm) to prolong rest longevity (moggieuk suggestion)
  - Always extend the tray when descending to home or purge **(DONE)**
  - Retract tray and extend after bucket shake in case blobs are accumulating and getting caught underneath **(DONE)**
  - Switch accels to use max_accels as defined or user provided whichever is the lower as default is to set it well above what most printers can comfortably accomodate without skipping e.g. use shake_accels,printer.configfile.config.printer.max_accel to cap it **(DONE)**
  - Additional sanity checks of user defined parameters - reset to sane values to prevent missadventure and issues if possible
  - Calculate and display slicer bed exclusion settings to prevent placement of parts that would colide with features **(DONE)** // BLOBIFIER: Slicer bed exclusion zone: 265x278, 300x278, 300x310, 265x310
  - Add x safety move if we only have a tray parking option and we are in print1) move out behind shaker and potentially the 2) depressor pin
  - Final QA test RH operation end to end
  - Final QA test LH operation end to end 

- Silicon nozzle rest options (250c rated) 
  - 3.5mm button plug : https://www.aliexpress.com/item/1005006396026960.html?spm=a2g0o.order_list.order_list_main.89.320f1802CbTUYu
  - Syringe cap : https://www.aliexpress.com/item/1005006915852959.html?spm=a2g0o.order_list.order_list_main.83.320f1802CbTUYu

## MK II Gantry Nozzle Wipe Rest

Current design iteration for the 2.4 gantry mounted nozzle wipe rest. Silicon 250c button rest with 3mm/4mm ID/OD PTFE tube sleeve to make it easy to install and remove, insulate from surounding ABS and to make it height adjustable (min 7mm PTFE). Zeroed out additional silicon tube rest(s) as they don't seem necessary after switching to the beefier and larger Bambu A1 Nozzle Wipe (the A1 Mini is considerably smaller with tighter block pattern and is more likely to trap filament debris).

![250c_silicon_rest_A1_wiper](https://github.com/user-attachments/assets/c2528bf4-50ae-4b6f-8aa7-e38035895a0c)
![250c_silicon_rest_A1_wiper_Nozzle_Front](https://github.com/user-attachments/assets/04890cd5-dc0d-408a-bb15-0fdd417d6a0a)
![Adjustable PTFE silicon rest sleeve](https://github.com/user-attachments/assets/846e4019-8405-4fc8-b69d-15c47b051b73)

**Wear and Tear** This is after > 1500 changes and parking the nozzle up @ 290c for 45mins.  The the over temp dimple helps cap the nozzle but expect the silicon rest to deterorate further over time especially if the nozzle is left in a parked state for prolonged periods of time. No noticable wear and tear parking up while preheating or during printing and filament changes with default Happy Hare 5-minute HE timeout and 255c target temp.  As the silicon rest is only rated @ 250c and easily replacable it should be considered "consumable" and replaced as often as needed when its no longer able to restrict oozing.  Even though external nozzle temp measurements appeared to be 40-50c lower than target HE temps, if left sitting on the rest for prelonged periods (e.g. > 10mins), tip temp will gradually creep up, reducing the temp delta. 

Unless a higher temp option can be sourced from aliexpress this is likely the best option we have.  
![Silicon_Rest_Wear_ _Tear](https://github.com/user-attachments/assets/7495ade9-21d4-4504-9ef5-4139c742a4bd)

**Video of RH blob with cascading wipe (combo zigzag & straight motion - Option:2) from static to gantry with final park**

https://github.com/user-attachments/assets/15b4801e-78ad-42de-9327-dc3350addd9f


**Older silicon tube based designs**

![v2.4_Gantry_Wipe_Rest_MK_II](images/v2.4_Gantry_Wipe_Rest_MK_II.png)
![v2.4_Gantry_Wipe_Rest_MK_II_Double_Rest](images/v2.4_Gantry_Wipe_Rest_MK_II_Double_Rest.png)
![v2.4_Extended_Static_Wipe_Rest_Final_Layout](images/v2.4_Extended_Static_Wipe_Rest_Final_Layout.png)

## Yavoth Hotend Shaker Arm

![Yavoth_Shaker_Arm](images/Yavoth_Shaker_Arm.png)

## Voron v2.4 300mm Reference Dimensions

Reference dimensions of blobifier with depressor pins for left hand and right hand installs on a 300mm Voron 2.4.
![Voron_v2 4_300mm_Blobifier_Dimensions](https://github.com/user-attachments/assets/e85cabfd-395c-45b3-a0d2-2c027607976d)


## Current Printer setup
Voron 2.4 300mm. Klicky PCB dock on the extreme left, z-endstop, blobifier gantry nozzle wipe rest (needs to be move closer to Blobifier once design/modifications are finalised), Blobifier on right, EREC (no toolhead cutter or depressor pin), and Yavoth hotend. Blobifier tray 1.2mm above bed.

## Nozzle Tip Temperature Metrics
Measurements for external nozzle tip temperatures taken from 300c - 240c, started at 300c, waiting for 5mins and dropping to lower temps.  Measured with multimeter and thermocouple between silicon reset and nozzle tip. <br />
External nozzle tip temperatures consistently 40c or so below actual HE temperature target.

![Nozzle_Tip_Temperatures](images/Nozzle_Tip_Temperatures.png)
