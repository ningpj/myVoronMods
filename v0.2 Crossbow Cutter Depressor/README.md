# v0.2 Crossbow Cutter Depressor

## Description

CNC Crossbow toolhead filament cutters are awesome. For a bit of fun, I fitted one to my V0.2 so EMU can act as a convenient filament changer rather than a full multi‑material setup.

I originally planned a servo‑actuated arm, but since the bed magnet already lets the build plate lift when printing edge‑to‑edge parts, losing a few millimetres of front print area isn’t the end of the world IMO.

I’ve created several mounting options that bolt to the front‑left 1515 extrusion. I’m using the MK II mid‑body version currently to minimise lost build space. It's more height‑sensitive than MK I, so depending on your hotend (I’m using Yavoth), you may need to tweak the height. MK I is more universal, but costs a little more build volume.

X needs to be at least 4.7 mm so the Crossbow arm doesn’t hit the 1515 extrusion during a cut.

With MK I you lose roughly 7 mm × 25 mm of usable area; I masked this in my slicer using `0x0, 0x25, 7x25, 7x0, 0x0`.

Happy‑Hare cutting settings:
```
variable_cutting_axis           : "y"
variable_pin_loc_xy             : 4.7, 2
variable_pin_park_dist          : -2
variable_pin_loc_compressed_xy  : 4.7, 16.5
```
Happy-Hare settings for MK II are the same with lost build space reduced to 7mm x 14mm (`0x0, 0x14, 7x14, 7x0, 0x0`)

> [!NOTE]
> A new variation of MK I has been added (MK III) with a larger depressor face and clearance on top of mount to minimise lost build space. Now its the same as MK II - 7mm x 14mm.

<img width="560" height="285" alt="image" src="https://github.com/user-attachments/assets/239462fb-e24c-4d38-ab25-0c6ffd28fcc8" />
<img width="466" height="458" alt="iV0 2 Crossbow Depressor MK III" src="https://github.com/user-attachments/assets/f0ac2c15-5c70-4097-90f3-92412606a75c" />

## Change Log

* Published

