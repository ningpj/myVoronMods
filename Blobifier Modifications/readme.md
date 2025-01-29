![407577316-29c66bfa-ff32-4045-abd8-8b417b14d90f](https://github.com/user-attachments/assets/60fe59b4-7534-4382-8fc5-44de2f252088)
# *** Work in progress ***  Blobifier Modifications

## Description

This is a dumping ground for sharing Blobifier modifications to support left and right hand Voron v2.4 installation and prototypes of silicon gantry and fixed nozzle wipe / rest options. 
The gantry Wipe / Rest redesign is derived and based on the excellent work @igannakas (Discord) pioneered to eliminate colour contamination when changing / purging filaments during mmu prints (https://www.printables.com/model/882364-adjustable-gantry-mounted-nozzle-seal-parking-and).<br />


## Design Goals

- **Gantry & Static Nozzle Wipe Rest**
:checked {
  filter: contrast(2);
}
  Redesign to incorporate:
  - [x] Dovetail sliders to make it easy to adjust, reduce mounting hardware (2 x SHCS/BHCS M3 8mm & 2 x M3 Heatsets) and improve rigidity
  - [x] Internal mount and arm voids to improve rigidity - 0.1mm 2x voids in arm &  mount (flex is inherent in designs like this and need it to be as rigid as possible to cap and prevent ooze)
  - [x] More material depth to secure m3 heat sets
  - [x] A1 Mini silicon wiper block Vs A1. While easier to secure and replace, the A1 Mini wiper is smaller and has shorter, more closely spaced knobs than the original Bambu A1 wiper and was more likely to trap filament debris during testing
        **(Bambu A1 wiper for the win!)**
  - [x] Experiment with high temp silicon tubing nozzle rests secured with filament pin (Dubro aero/heli silicon fuel tubing - 180c-ish.
        Tested and discarded due to ABS mount softening after prolonged exposure to 255c+ parked nozzle.  
  - [x] Evaluate 250c silicon hole plugs and syringe caps from aliexpress as alternatives. Interestingly "most" silicon HE socks are only rated to 280c.
        Silicon hole plug worked exceptionally well in conjunction with 3mm/4mm ID/OD PTFE tube sleeve for mounting, replacing and adjusting rest height. Silicon syringe caps were larger, and more difficult to install and work around. 
  - [x] Trial additional options to help detach blobs before final wipe (e.g. double silicon rest, angled edge, cutaways on top of mount, etc).
        Discarded in preference to chunker, full size Bambu A1 wiper
  - [x] Redesign and experiment with static wiper/rest extending over Blobifier tray to maximise print area.
        Works well although blobs will pile up more between the static wiper and blobifier base.  Still managed to fill the tray but did need to increase shake frequency.
        Also changed Blobifier macro shaker logic to retract the tray before shaking the bucket and extending it afterwards to help release any blobs that maybe trapped under the tray.
  - [x] Bucket shaker profile for Yavoth hotend
 
- **Blobifier**
  - [x] Ambidextrous motion logic to handle left and right hand installation with moves optimised according to the orientation e.g. towards and away from Blobifier.
  - [x] Implement additional wiper actions to improve wipe efficacy. 0: swipe, 1: zigzag, 2: combo zigzag. Ratio for combo is 40/60 with a minimum of 1 wipe for each option. e.g. 3 wipes will result in 1 zigzag & 2 swipes, 4 wipes 2 zigzags, 2 swipes. Zigzag wipe speed is capped @ 500mm/s to prevent unnecesary vibration or printer damage.
  - [x] Customisable nozzle shaker option to help detach belligerent blobs (x distance, iterations to shake)
  - [x] Customizable tray iterations to help detach belligerent blobs (default: 1 - iterations to retract and extend the tray)
  - [x] Rationalise static and gantry configuration using lists with independed settings for managing park and wiper geometry
  - [x] Make servo dwell setting configurable and move up to main Blobifier configuration block
  - [x] Zero and restore PA before/after purging
  - [x] Remove redundant variables where possible e.g. restore settings from the printer variables since the value doesnt change once the tempate is rendered 
  - [x] Support chaining of static and gantry nozzle wipe & rest options. All options are options and will use whatever is available.  Priortise parking on gantry, static, before falling back to tray.
  - [x] Improve depressor pin avoidance logic for LH & RH setups. Reference HH tip cut location and servo configuration to conditionally avoid if need be. e.g. if defined, no servo, move in board by depressor pin, park, and toolhead_width and up beside depressor if behind toolhead
  - [x] Add wrapper macros & logic to check if Klicky is still attached to prevent collisions with optional gantry mount - prompt users to manually remove.  (BLOBIFIER_SAFE and BLOBIFIER_SAFE_PARK macro entry points provided for klicky users)
  - [x] Convert all blobifier speeds from mm/min to mm/sec to be consistent with Happy Hare
  - [ ] Consider park position randomiser (+/- 1.5mm) to prolong silicon rest longevity (moggieuk suggestion).
        Given the likelihood of high temp related dimples, its likely  more effective to park up in the same spot to better cap the nozzle and prevent ooze.  
  - [x] Always extend the tray before descending to park or purge to reduce the risk of damaging the nozzle
  - [x] Retract the tray before shaking the bucket in case blobs are accumulating and getting caught underneath it
  - [x] Cap / alert when user accels (wipe and travel) are higher than printer limits e.g. printer.configfile.config.printer.max_accel
  - [x] Additional sanity checks of user defined parameters - reset to sane values if possible 
  - [x] Calculate and display slicer bed exclusion setting to paste into your slicer to prevent placement of parts in areas that would collide with configured blobifier features.
        // BLOBIFIER: Slicer bed exclusion zone: 265x278, 300x278, 300x310, 265x310
  - [ ] Review x safety move if tray is the only parking option and we are in print. E.g. move out from behind shaker and potentially the depressor pin if configured
  - [ ] QA test RH operation end to end
  - [ ] Final QA test LH operation end to end 

- Silicon nozzle rest options (250c rated) 
  - **3.5mm button plug : https://www.aliexpress.com/item/1005006396026960.html?spm=a2g0o.order_list.order_list_main.89.320f1802CbTUYu (RECOMMENDED OPTION)**
  - Syringe cap : https://www.aliexpress.com/item/1005006915852959.html?spm=a2g0o.order_list.order_list_main.83.320f1802CbTUYu

## MK II Gantry Nozzle Wipe Rest

Current design iteration for the 2.4 gantry mounted nozzle wipe rest. Silicon 250c button rest with 3mm/4mm ID/OD PTFE tube sleeve to make it easy to install and remove, insulate from surounding ABS and to make it height adjustable (min 7mm PTFE). Zeroed out additional silicon tube rest(s) as they don't seem necessary after switching to the beefier and larger Bambu A1 Nozzle Wipe (the A1 Mini is considerably smaller with tighter block pattern and is more likely to trap filament debris).

![250c_silicon_rest_A1_wiper](https://github.com/user-attachments/assets/c2528bf4-50ae-4b6f-8aa7-e38035895a0c)
![250c_silicon_rest_A1_wiper_Nozzle_Front](https://github.com/user-attachments/assets/04890cd5-dc0d-408a-bb15-0fdd417d6a0a)
![Adjustable PTFE silicon rest sleeve](https://github.com/user-attachments/assets/846e4019-8405-4fc8-b69d-15c47b051b73)


**Wear and Tear** This is after > 1500 changes and parking the nozzle up @ 290c for 45mins.  The over temp dimple helps cap the nozzle but expect the silicon rest to deterorate further over time especially if the nozzle is left in a parked state at high temp for prolonged periods of time. No noticable wear and tear parking up while preheating or during printing and filament changes with default Happy Hare 5-minute HE timeout and 255c target temp.  As the silicon rest is only rated @ 250c and easily replacable, it should be considered "consumable" and replaced as often as needed when its no longer able to restrict oozing.  Even though external nozzle temp measurements appeared to be 40-50c lower than target HE temps, if left sitting on the rest for prelonged periods (e.g. > 10mins), tip temp will gradually creep up, reducing the temp delta. 

Unless a higher temp option can be sourced from aliexpress, this is one of the best options Ive identified.  
![Silicon_Rest_Wear_ _Tear](https://github.com/user-attachments/assets/7495ade9-21d4-4504-9ef5-4139c742a4bd)


**Video of right hand blob action with nozzle shake, cascading wipe (combo zigzag & straight motion - Option:2) from static wiper through to gantry wiper and final park up**

https://github.com/user-attachments/assets/15b4801e-78ad-42de-9327-dc3350addd9f

**Slicer excluded bed region**

<img width="647" alt="image" src="https://github.com/user-attachments/assets/43a60c66-ab4b-4a2a-8edf-8a8f69523601" />



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
