# v0.2 Crossbow Cutter Depressor

## Description

CNC Crossbow toolhead filament cutters are awesome. For a bit of fun, I fitted one to my V0.2 so EMU can act as a convenient filament changer rather than a full multi‑material setup.

I originally planned a servo‑actuated arm, but since the bed magnet already lets the build plate lift when printing edge‑to‑edge parts, losing a few millimetres of front print area isn’t the end of the world IMO.

I’ve created several mounting options that bolt to the front‑left 1515 extrusion. MK II mid‑body and MK III evolved to minimise lost build space. 
X needs to be at least 4.7 mm so the Crossbow arm doesn’t hit the 1515 extrusion during a cut.

With MK I you lose roughly 7 mm × 25 mm of usable area; I masked this in my slicer using `0x0, 0x25, 7x25, 7x0, 0x0`.
MK II and MK III you only sacrifice 7mm x 14mm of space (`0x0, 0x14, 7x14, 7x0, 0x0`)

Happy‑Hare cutting settings for MK II & MK III:
```
variable_cutting_axis           : "y"
variable_pin_loc_xy             : 4.7, 2
variable_pin_park_dist          : -2
variable_pin_loc_compressed_xy  : 4.7, 16.5
```

> [!NOTE]
> A new variation of MK I has been added (MK III) with a larger depressor face and clearance on top of mount to clear arm to minimise lost build space (7mm x 14mm).

<img height="285" alt="V0 2 Crossbow Depressor MK I" src="https://github.com/user-attachments/assets/f2f62f9e-07c4-4288-913c-889fa987ec13" />
<img height="285" alt="V0 2 Crossbow Depressor MK II" src="https://github.com/user-attachments/assets/677140a0-af03-4067-9829-e5dd133c7620" />
<img height="285" alt="V0 2 Crossbow Depressor MK III" src="https://github.com/user-attachments/assets/b8305c89-a3b0-4a97-ae10-c197193d812a" />


## Change Log

* Published

