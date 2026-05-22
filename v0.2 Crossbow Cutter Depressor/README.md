# v0.2 Crossbow Cutter Depressor

## Description

CNC Crossbow, toolhead filament cutters are awesome. Up for a challenge, I fitted one to my v0.2 to support EMU as a convienent filament changer rather than multi material printer.
I was originally intended designing a servo actuated arm but given the bed magnet allows the build plate to lift when printing edge to edge parts, IMO losing a few mm of print space up front isn't going to be the end of the world :-). 
Two options created that mount front left to the 1515 extrusion. Im using the MK II mid-body option to minimise lost build space. Unfortunately it's more height dependent than MK I so may need to be adjusted to suit different setups depending on the hot ends used (I use it with Yavoth). MK I is more universal at the expense of a little more build space.

x needs to be at least 4.7mm so the crossbow arm doesn't connect with the 1515 extrusion when cutting.  

With MK I you lose approximately 7mm x 25mm and masked this in my slicer (`0x0, 0x25, 7x25, 7x0, 0x0`).  Happy-Hare cutting settings:
```
variable_cutting_axis           : "y"
variable_pin_loc_xy             : 4.7, 2
variable_pin_park_dist          : -2
variable_pin_loc_compressed_xy  : 4.7, 16.5
```
Happy-Hare settings for MK II are the same with lost build space reduced to 7mm x 14mm (`0x0, 0x14, 7x14, 7x0, 0x0`)

<img width="560" height="285" alt="image" src="https://github.com/user-attachments/assets/239462fb-e24c-4d38-ab25-0c6ffd28fcc8" />

## Change Log

* Published

