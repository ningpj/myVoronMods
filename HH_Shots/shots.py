# The screenshots the documentation needs.
#
#   make shots                        # regenerate every session's images
#   make shots ARGS='--list'          # the sessions, and what each one covers
#   make shots ARGS='--only getting-started-boxturtle'
#   make shots ARGS='--seed ~/printer_data/.mmu_config'   # against a real machine
#
# A SESSION IS ONE menuconfig, MANY IMAGES. Parsing the Kconfig tree costs several
# seconds, so a session starts the installer once, walks it, and captures along the
# way - `shot('name')` writes name.png under the session's 'outdir' and carries on
# from where it is. Group screens that belong to the same walkthrough into one
# session; start a new one when the seed or the unit has to change.
#
# EVERY SESSION NAMES A REAL PAGE. There is no shared demo pool: a session exists
# because doc/Something.md embeds its images, and its 'outdir' is that page's own
# folder (see doc_tools/README.md). Falling back to the shared doc/images/ default
# is for CAPTURE=1 exploration only - don't add a session that writes there, or
# `make shots` starts regenerating pictures nothing reads.
#
# HEIGHT LOOKS AFTER ITSELF. Each shot() fits the terminal to the screen in front of
# it, so no image contains menuconfig's row of scroll arrows and none carries a band
# of dead space either - subject to a 30-row floor, so a two-item menu still looks like
# the installer rather than a cropped fragment. Sessions do not set 'rows'; pass
# 'min_rows' to change the floor, or 'fit': False and a 'rows' to pin a height.
#
# ALWAYS ASSERT THE LANDING SCREEN. Use mc.enter()/mc.edit()/mc.step(), which raise
# when the expected screen does not arrive, rather than mc.key(), which tolerates a
# keypress that changed nothing. A missed key produces a perfectly plausible PNG of
# the WRONG screen, and nobody reviewing an image can tell that is what happened.
#
# EDITS ARE CANCELLED, NOT APPLIED. mc.edit() opens a parameter's editor so it can be
# photographed; mc.cancel() closes it without changing anything, so the screens after
# it still show the machine the seed described. (Applying would be harmless to the
# real config - the session works on a copy - but not to the rest of the session.)
#
# This file may be distributed under the terms of the GNU GPLv3 license.

from __future__ import annotations

import argparse
import os
import sys
import traceback

from .capture import DEFAULT_COLS, DEFAULT_SEED, DOC, IMAGES, MIN_ROWS, Menuconfig, ScreenError

# ---------------------------------------------------------------------------
# The sessions. Extend these; the runner needs no changes.
#
#   name     --only key, and the prefix for anything the session does not name
#   caption  what the session covers, for whoever writes the prose
#   scenes   f(mc, shot) - navigate, calling shot('image-name') at each screen
#   outdir   where this session's images go, relative to doc/ - name it after the
#            page (e.g. 'GettingStarted-BoxTurtle'). Every session should set
#            this; see the header above.
#   seed     a config to start from - a built-in name or a path (default: boxturtle)
#   min_rows shortest a fitted screenshot may be (default 30, for a consistent set)
#   fit      False to stop autofitting and honour 'rows' instead
#   rows     starting height; only meaningful with 'fit': False
#   unit_name / multi_unit / entry_point - inferred from the seed, override here
# ---------------------------------------------------------------------------


def _getting_started_boxturtle(mc, shot):
    """
    For doc/GettingStarted-BoxTurtle.md - the installer screens a first-time Box
    Turtle owner walks through, in that order. Runs from a bare Kconfig ('seed': None)
    rather than the boxturtle seed used elsewhere, because the page is about DRIVING
    menuconfig - selecting MMU Type is the first real thing a reader does with it,
    and the root-warnings screen is only informative if the warnings visibly clear as
    a result of that choice, which requires starting before it happens.
    """
    mc.select('MMU Type')
    shot('01-first-run')  # every field still a placeholder

    mc.enter('MMU Type')
    mc.select('Box Turtle')
    mc.toggle()
    shot('02-mmu-type-boxturtle')  # (X) Box Turtle; Turtle Neck now offered

    mc.enter('Turtle Neck')
    shot('03-turtleneck-buffer')  # v2 is the default - nothing to change
    mc.back()
    mc.back()  # -> (Top)

    mc.select('MMU Type')
    shot('04-root-warnings')  # only the (later-page) toolhead warning remains

    mc.enter('Board type')
    shot('05-board-type')  # AFC Lite v1.0 - the board this MMU shipped with
    mc.back()

    mc.enter('MCU connection')
    shot(
        '06-mcu-connection')  # Serial - already right for a USB-attached board
    mc.back()

    mc.enter('MMU Features / Additions')
    shot('07-mmu-features')  # LEDs/eSpooler/buffer already on; nothing to add
    mc.back()

    mc.enter('Pins / TMC')
    mc.enter('Gear pins')
    shot('08-gear-pins')  # every gate's step/dir/enable/diag pin

    mc.edit('Gear dir pin')
    shot('09-gear-dir-editor')  # the pin nobody can predict from a drawing
    mc.write('!unit0:PD3')
    shot('10-gear-dir-inverted')  # '!' reverses it - no rewiring, no cfg edits
    mc.cancel()  # this page only shows the move; it does not make it
    mc.back()
    mc.back()  # -> (Top)

    mc.enter('Toolhead')
    mc.select('Stealthburner Clockwork2 Revo Voron')
    mc.toggle()
    # settle the resize (24 items don't fit the
    # starting height) BEFORE re-selecting - it
    # re-homes the cursor to the top, and shot()'s
    # own autofit is a no-op once already fitted
    mc.autofit()
    mc.select('Stealthburner Clockwork2 Revo Voron')
    shot('11-toolhead-selected')  # (X) on the choice, highlight on it too
    mc.back()  # -> (Top)

    mc.enter('Toolhead sensors/settings')
    shot(
        '12-toolhead-dimensions')  # extruder-to-nozzle/residual filled in from
    mc.back()  # the choice above - the sensor-gated ones
    # (toolhead/extruder sensor distances) stay
    # hidden since this Box Turtle has neither
    # -> (Top)

    mc.enter('Software Options')
    mc.enter('Select spoolman spool manager support')
    mc.select('Read-only')
    mc.toggle()
    shot('13-spoolman-readonly')  # the one setting this page actually changes


def _getting_started_vivid(mc, shot):
    """
    For doc/GettingStarted-ViViD.md - the installer screens a first-time BTT ViViD
    owner walks through. Like the Box Turtle session, starts from a bare Kconfig
    ('seed': None) so selecting MMU Type is the first real action, not something the
    seed already decided.

    Deliberately NOT entered further: the "Select serial device for ..." rows visible
    on the 03/04 shots below. They list live /dev/serial/by-id/* entries (see
    capture.py's REPRODUCIBILITY note) - on this capture machine that is empty, so
    entering one just shows "Other / manually entered" and nothing else, not the
    illustrative device names the page's prose uses. The "MCU connection"/"Buffer MCU
    connection" screens captured here are the reproducible part of that same story -
    each shows its connection-type row (Serial, already right for a USB board) and
    the resolved-device row alongside it, without depending on what is plugged in.
    """
    mc.enter('MMU Type')
    mc.select('BTT ViViD')
    mc.toggle()
    shot('01-mmu-type-vivid')  # (X) BTT ViViD; buffer sub-option auto-checked
    mc.back()  # -> (Top)

    mc.enter('Board type')
    shot('02-board-type')  # BTT ViViD MCU - the only board this type uses
    mc.back()

    mc.enter('MCU connection')
    shot('03-mcu-connection'
         )  # Serial - already right for the ViViD unit's own MCU
    mc.back()

    mc.enter('Buffer MCU connection')
    shot('04-mcu-connection-buffer'
         )  # a SECOND, separate MCU connection - the buffer's own
    mc.back()  # -> (Top)

    mc.enter('MMU Features / Additions')
    shot('05-mmu-features')  # LEDs/env sensor/heater/NFC readers already on
    mc.back()  # -> (Top)

    mc.enter('Toolhead')
    mc.select('Stealthburner Clockwork2 Revo Voron')
    mc.toggle()
    mc.autofit()  # settle the resize before re-selecting (see the
    # Box Turtle session's identical comment)
    mc.select('Stealthburner Clockwork2 Revo Voron')
    shot('06-toolhead-selected')  # same generic choice, not ViViD-specific
    mc.back()  # -> (Top)

    mc.enter('Software Options')
    mc.select('Auto-create a Spoolman spool from an unknown NFC/RFID tag?')
    mc.toggle()
    shot('07-spoolman-nfc-autocreate'
         )  # worth having, since ViViD ships NFC readers already
    # No mc.enter('Spoolman') step - "Spoolman" is a `comment` section divider on this
    # same Software Options screen, not a submenu; the item above is selectable in place.

def _getting_started_ercf(mc, shot):
    """
    For doc/GettingStarted-Tradrack.md - the installer screens a first-time Tradrack
    owner walks through, in that order. 
    """
    mc.select('MMU Type')
    shot('01-first-run')
    
    mc.enter('MMU Type')
    mc.select('ERCF - Enraged Rabbit Carrot Feeder')
    mc.toggle()
    shot('02-mmu-type-ercf')

    mc.enter('Version')
    shot('02-ercf-version')
    mc.back()

    mc.select('Number of gates/lanes?')
    mc.edit('Number of gates/lanes?')
    mc.write('6')
    shot('03-lanes')
    mc.cancel()  

    mc.select('Selector servo type')
    mc.enter('Selector servo type')
    mc.select('Savox SH-0255MG')
    mc.toggle()
    shot('04-selector-servo-type')
    mc.back()

    mc.select('Project Options')
    mc.enter('Project Options')
    shot('05-project-options')
    mc.back()
    mc.back()

    mc.select('MMU Features / Additions')
    mc.enter('MMU Features / Additions')
    shot('12-mmu-features')
    mc.back()

    mc.select('Board type')
    shot('06-root-warnings')
    
    mc.enter('Board type')
    shot('07-board-type')
    mc.back()

    mc.enter('MMU Features / Additions')
    mc.select('Encoder config')
    shot('12-mmu-features')  
    mc.enter('Encoder config')
    shot('12-mmu-encoder')  
    mc.enter('Type')
    shot('12-mmu-encoder-settings')  
    mc.back()

    mc.enter('MCU connection')
    shot('08-mcu-connection')
    mc.enter('MCU connection')
    mc.select('CANbus')
    shot('08-mcu-connection-canbus')
    mc.toggle()
    mc.enter('Select canbus UUID for MMU')
    shot('08-mcu-connection-canbus-uuids')
    mc.back()
    mc.back()     
    
    mc.enter('Pins / TMC')
    mc.enter('Gear pins')
    shot('09-gear-pins')  
    
    mc.edit('Gear dir pin')
    mc.write('!unit0:PD3')
    shot('09-gear-dir-inverted')  
    mc.cancel()  
    mc.back()
    mc.back()  
    
    mc.enter('Toolhead')
    mc.select('A4T WWBMG for A4T Dragon Ace')
    mc.toggle()
    mc.autofit()                                       
    shot('10-toolhead-selected')
    mc.back()
    
    mc.enter('Toolhead sensors/settings')
    shot('10-toolhead-dimensions')
    mc.select('Has toolhead sensor?')
    mc.toggle()
    mc.select('Has extruder (entry) sensor?')
    mc.toggle()
    shot('10-all-toolhead-dimensions')
    mc.back()

    mc.enter('Endstops and Bowden movement')
    mc.select('Gate homing endstop')
    shot('11-Endstops')  
    mc.back()
        
    
def _getting_started_tradrack(mc, shot):
    """
    For doc/GettingStarted-Tradrack.md - the installer screens a first-time Tradrack
    owner walks through, in that order. 
    """
    mc.select('MMU Type')
    shot('01-first-run')
    
    mc.enter('MMU Type')
    mc.select('Tradrack')
    mc.toggle()
    shot('02-mmu-type-tradrack') 

    mc.select('Number of gates/lanes?')
    mc.edit('Number of gates/lanes?')
    mc.write('12')
    shot('03-lanes')
    mc.cancel()  

    mc.select('Selector servo type')
    mc.enter('Selector servo type')
    mc.select('JX PS-1171MG')
    mc.toggle()
    shot('04-selector-servo-type')
    mc.back()

    mc.select('Project Options')
    mc.enter('Project Options')
    shot('05-project-options')
    mc.back()
    mc.back()

    mc.select('MMU Features / Additions')
    mc.enter('MMU Features / Additions')
    shot('12-mmu-features')
    mc.back()

    mc.select('Board type')
    shot('06-root-warnings')
    
    mc.enter('Board type')
    shot('07-board-type')
    mc.back()

    mc.enter('MCU connection')
    shot('08-mcu-connection')
    mc.enter('MCU connection')
    mc.select('CANbus')
    shot('08-mcu-connection-canbus')
    mc.toggle()
    mc.enter('Select canbus UUID for MMU')
    shot('08-mcu-connection-canbus-uuids')
    mc.back()
    mc.back()     
    
    mc.enter('Pins / TMC')
    mc.enter('Gear pins')
    shot('09-gear-pins')  
    
    mc.edit('Gear dir pin')
    mc.write('!unit0:gpio8')
    shot('09-gear-dir-inverted')  
    mc.cancel()  
    mc.back()
    mc.back()  
    
    mc.enter('Toolhead')
    mc.select('A4T WWBMG for A4T Dragon Ace')
    mc.toggle()
    mc.autofit()                                       
    shot('10-toolhead-selected')
    mc.back()
    
    mc.enter('Toolhead sensors/settings')
    shot('10-toolhead-dimensions')
    mc.select('Has toolhead sensor?')
    mc.toggle()
    mc.select('Has extruder (entry) sensor?')
    mc.toggle()
    shot('10-all-toolhead-dimensions')
    mc.back()

    mc.enter('Endstops and Bowden movement')
    mc.select('Gate homing endstop')
    shot('11-Endstops')  
    mc.back()
        
    mc.enter('MMU Features / Additions')
    shot('12-mmu-features')  
    mc.back()


def _getting_started_emu(mc, shot):
    """
    For doc/GettingStarted-EMU.md - the installer screens a first-time EMU
    owner walks through, in that order. Runs from a bare Kconfig ('seed': None)
    rather than the boxturtle seed used elsewhere, because the page is about DRIVING
    menuconfig - selecting MMU Type is the first real thing a reader does with it,
    and the root-warnings screen is only informative if the warnings visibly clear as
    a result of that choice, which requires starting before it happens.
    """
    mc.select('MMU Type')
    shot('01-first-run')  # every field still a placeholder

    mc.enter('MMU Type')
    mc.select('EMU')
    mc.toggle()
    shot('02-mmu-type-emu')  # (X) EMU; PSF now offered

    mc.select('Number of gates/lanes?')
    shot('03-num-gates')
    mc.back()  # -> (Top)

    # mc.select('MMU Type')
    # shot('04-root-warnings')                        # only the (later-page) toolhead warning remains
    #
    # mc.enter('Board type')
    # shot('05-board-type')                           # AFC Lite v1.0 - the board this MMU shipped with
    # mc.back()
    #
    # mc.enter('MCU connection')
    # shot('06-mcu-connection')                        # Serial - already right for a USB-attached board
    # mc.back()
    mc.enter('MCU connection')
    shot('06-mcu-connection')
    #mc.enter('MCU connection')
    #mc.select('CANbus')
    #shot('08a-mcu-connection-canbus')
    #mc.toggle()
    mc.enter('Select canbus UUID for MMU')
    shot('06-canbus-uuids')
    #
    # mc.enter('MMU Features / Additions')
    # shot('07-mmu-features')                          # LEDs/eSpooler/buffer already on; nothing to add
    # mc.back()
    #
    # mc.enter('Pins / TMC')
    # mc.enter('Gear pins')
    # shot('08-gear-pins')                             # every gate's step/dir/enable/diag pin
    #
    # mc.edit('Gear dir pin')
    # shot('09-gear-dir-editor')                       # the pin nobody can predict from a drawing
    # mc.write('!unit0:PD3')
    # shot('10-gear-dir-inverted')                     # '!' reverses it - no rewiring, no cfg edits
    # mc.cancel()                                      # this page only shows the move; it does not make it
    # mc.back()
    # mc.back()                                        # -> (Top)
    #
    # mc.enter('Toolhead')
    # mc.select('Stealthburner Clockwork2 Revo Voron')
    # mc.toggle()
    # mc.autofit()                                       # settle the resize (24 items don't fit the
    #                                                     # starting height) BEFORE re-selecting - it
    #                                                     # re-homes the cursor to the top, and shot()'s
    #                                                     # own autofit is a no-op once already fitted
    # mc.select('Stealthburner Clockwork2 Revo Voron')
    # shot('11-toolhead-selected')                       # (X) on the choice, highlight on it too
    # mc.back()                                          # -> (Top)
    #
    # mc.enter('Toolhead sensors/settings')
    # shot('12-toolhead-dimensions')                   # extruder-to-nozzle/residual filled in from
    # mc.back()                                        # the choice above - the sensor-gated ones
    #                                                   # (toolhead/extruder sensor distances) stay
    #                                                   # hidden since this Box Turtle has neither
    #                                                   # -> (Top)
    #
    # mc.enter('Software Options')
    # mc.enter('Select spoolman spool manager support')
    # mc.select('Read-only')
    # mc.toggle()
    # shot('13-spoolman-readonly')                     # the one setting this page actually changes


def _feature_espooler(mc, shot):
    """
    For doc/Feature-Espooler.md - the per-gate pin entry screen for the eSpooler
    feature. Uses the boxturtle seed (default), which already has eSpooler enabled,
    so the menu is reachable without any setup in the scene itself.

    'eSpooler pins' used to be its own submenu, directly under 'MMU Features /
    Additions'. Since the eSpooler tuning options (assist/rewind burst, speed
    exponent, etc.) were exposed via menuconfig, the pins moved to being the tail
    section of the now much longer 'eSpooler config' menu instead - select into
    the first pin row rather than trying to enter a submenu that no longer exists.
    """
    mc.enter('MMU Features / Additions')
    mc.enter('eSpooler config')
    mc.select('eSpooler enable 0 pin')
    shot('espooler-pins')  # one row of rewind/forward/enable/trigger per gate


def _feature_sync_feedback_buffer(mc, shot):
    """
    For doc/Feature-Sync-Feedback-Buffer.md - the buffer hardware screen and the
    separate motor-sync screen. Uses the boxturtle seed (default), which already has
    a Turtle Neck v2 (dual switch) buffer fitted, so both menus are reachable without
    any setup in the scene itself.
    """
    mc.enter('MMU Features / Additions')
    mc.enter('Buffer config')
    shot('buffer-config'
         )  # range/maxrange, spring state, both switch pins fitted
    mc.back()
    mc.back()  # -> (Top)

    mc.enter('Other Settings')
    mc.enter('MMU/Extruder sync')
    shot('motor-sync')  # dynamic sync feedback + synchronized gear current


def _feature_nfc(mc, shot):
    """
    For doc/Feature-NFC.md - the shared-reader half of NFC reader config. Uses the
    'ercf' seed rather than the default boxturtle: NFC is opt-in and off by default
    for every MMU type (BETA), so enabling it is scene setup regardless of vendor -
    but ERCF's moving-carriage/servo design is the more natural fit for "present a
    spool to one shared reader by hand" than Box Turtle's gear-per-gate layout,
    matching how the page itself frames a shared reader.
    """
    mc.enter('MMU Features / Additions')
    mc.select('Has NFC reader(s) for RFID tag?')
    mc.toggle()
    mc.autofit()  # new items just appeared below
    mc.enter('NFC reader config')
    mc.select('Has common NFC reader?')
    mc.toggle()
    mc.autofit()  # reader name/type/pin fields just appeared
    mc.select('Has common NFC reader?')
    shot('shared-reader-config'
         )  # name/type/CS pin/SPI bus/speed - RC522 defaults


def _feature_leds(mc, shot):
    """
    For doc/Feature-LEDs.md - the Led config screen and the Neopixel pin
    prompt (a different menu entirely - Pins / TMC, not MMU Features /
    Additions). Uses the boxturtle seed (default), which already has LEDs
    enabled, so no scene setup is needed.
    """
    mc.enter('MMU Features / Additions')
    mc.enter('Led config')
    shot('led-config'
         )  # enable/animation, frame rate, chain count, color order, segments
    mc.back()
    mc.back()  # -> (Top)

    mc.enter('Pins / TMC')
    shot('neopixel-pin'
         )  # Misc pins section - just the Neopixel pin on this seed


def _feature_gate_ttg_maps(mc, shot):
    """
    For doc/Feature-Gate-TTG-Maps.md - the automap strategy/reset-TTG screen.
    Generic macro-variable settings, not MMU-type-specific, so the boxturtle
    seed (default) needs no setup.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_SOFTWARE)')
    mc.select('Automap strategy')
    shot('automap-strategy'
         )  # strategy choice + reset-TTG-at-end-of-print checkbox


def _feature_filament_bypass(mc, shot):
    """
    For doc/Feature-Filament-Bypass.md - the "Associate bypass with this
    unit?" prompt. Lives under MMU Type -> <the selected type>'s own
    "Design attributes" submenu, not a general advanced-settings screen -
    confirmed by walking the real Kconfig node tree for BOOL_HAS_BYPASS
    rather than guessing, since it's nested differently per MMU type
    (Box Turtle's own path used here). Uses the boxturtle seed (default).
    """
    mc.enter('MMU Type')
    # Box Turtle is a choice radio button, already selected by the seed - its
    # own "Design attributes" submenu appears as a nested item directly below
    # it on this same screen, not behind entering "Box Turtle" itself.
    mc.enter('Design attributes')
    mc.select('Associate bypass with this unit?')
    shot('design-attributes-bypass')  # off by default on box turtle


def _feature_tip_forming_purging(mc, shot):
    """
    For doc/Feature-Tip-Forming-Purging.md - the base Tip Forming / Cutting
    and Purging screens. Both are unconditional menus (every MMU type gets
    them), so the boxturtle seed (default) needs no setup for the base
    view - servo cutter/Blobifier stay off, showing the plain form_tip/purge
    defaults.
    """
    mc.enter('Tip Forming / Cutting')
    shot('tip-forming-cutting'
         )  # servo cutter off, form_tip selected, force-standalone on
    mc.back()  # -> (Top)

    mc.enter('Purging')
    shot('purging')  # Blobifier off, simple bucket purge selected


def _feature_eject_buttons(mc, shot):
    """
    For doc/Feature-Eject-Buttons.md - the eject buttons config screen.
    Off by default on every MMU type including boxturtle, so toggled on here
    (same pattern as _feature_nfc/_feature_environment_manager).
    """
    mc.enter('MMU Features / Additions')
    mc.select('Has eject buttons?')
    mc.toggle()
    mc.autofit()  # "Mmu eject buttons" submenu just appeared
    mc.enter('Mmu eject buttons')
    shot('eject-buttons')  # one pin prompt per gate, all blank by default


def _feature_flowguard(mc, shot):
    """
    For doc/Feature-FlowGuard.md - the FlowGuard config screen. Uses the
    boxturtle seed (default), which already has a sync-feedback buffer
    fitted (same as _feature_sync_feedback_buffer), so this menu - gated on
    a buffer OR an encoder - is already visible with no scene setup.
    """
    mc.enter('Other Settings')
    mc.enter('FlowGuard')
    shot('flowguard-config'
         )  # relief threshold, tangle prevention, encoder mode


def _feature_environment_manager(mc, shot):
    """
    For doc/Feature-Environment-Manager.md - the environment-sensor and heater
    config screens. Both are off by default on every MMU type including
    boxturtle, so this scene toggles them on itself (same pattern as
    _feature_nfc) rather than needing a different seed.
    """
    mc.enter('MMU Features / Additions')
    mc.select('Has environment sensor(s)?')
    mc.toggle()
    mc.autofit()  # "Environment sensor config" submenu just appeared
    mc.enter('Environment sensor config')
    shot('environment-sensor-config'
         )  # i2c bus type/sensor type/address, single-sensor mode
    mc.back()  # -> MMU Features / Additions

    mc.select('Has enclosure heater(s)?')
    mc.toggle()
    mc.autofit()  # "Heater config" submenu just appeared
    mc.enter('Heater config')
    shot('heater-config'
         )  # per-gate toggle, heater name, drying temp/time/humidity defaults


def _feature_fan_control(mc, shot):
    """
    For doc/Feature-Fan-Control.md - the fan config and fan controls screens.
    Both MMU_HAS_FANS is off by default on every MMU type including boxturtle, and
    the feature's own _MMU_FAN_VARS block only renders when an environment sensor is
    ALSO enabled (config/base/mmu_macro_vars.cfg's `if MMU_HAS_FANS and
    MMU_HAS_ENVIRONMENT_SENSOR` guard - verified directly against the real Jinja
    template, not assumed) - so this scene toggles both, same pattern as
    _feature_environment_manager.
    """
    mc.enter('MMU Features / Additions')
    mc.select('Has environment sensor(s)?')
    mc.toggle()
    mc.autofit()  # still on "MMU Features / Additions" - no submenu entered

    mc.select('Has cooling fans?')
    mc.toggle()
    mc.autofit()  # "Fan config"/"Fan controls" submenus just appeared
    mc.enter('Fan config')
    shot('fan-config')  # max power, kick-start time, single fan pin
    mc.back()  # -> MMU Features / Additions

    mc.enter('Fan controls')
    shot('fan-controls')  # on/off temps, polling time, forced mode choice


def _feature_endless_spool_runout(mc, shot):
    """
    For doc/Feature-Endless-Spool-Runout.md - the EndlessSpool section of Software
    Options. Generic, not MMU-type-specific, so the boxturtle seed (default) needs
    no setup - this section is always present.
    """
    mc.enter('Software Options')
    mc.select('Enable EndlessSpool?')
    shot('endless-spool-options'
         )  # both EndlessSpool checkboxes, off by default


def _macro_print_start_end(mc, shot):
    """
    For doc/Macro-Print-Start-End.md - the _MMU_SOFTWARE macro-vars screen.
    Unconditional menu, so the boxturtle seed (default) needs no setup.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_SOFTWARE)')
    shot('print-start-end'
         )  # start-checks + automap strategy + end-of-print behavior


def _macro_state_change_hooks(mc, shot):
    """
    For doc/Macro-State-Change-Hooks.md - the _MMU_STATE macro-vars screen.
    Unconditional menu, so the boxturtle seed (default) needs no setup.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_STATE)')
    shot('state-change-hooks'
         )  # 3 extension hooks + servo/cutter consumption limits


def _macro_sequence(mc, shot):
    """
    For doc/Macro-Sequence.md - the _MMU_SEQUENCE macro-vars screen. Unconditional
    menu, so the boxturtle seed (default) needs no setup. Tall enough that autofit
    may need the full MAX_ROWS cap - one shot at the top, split further only if it
    still shows scroll arrows.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_SEQUENCE)')
    shot('sequence')  # park positions, restore-XY choice, user hooks


def _macro_client(mc, shot):
    """
    For doc/Macro-Client.md - the _MMU_CLIENT macro-vars screen. Gated on
    INSTALL_CLIENT_MACROS, which defaults to y - already visible on the
    boxturtle seed with no scene setup.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_CLIENT)')
    shot('client')  # cancel behavior + pause/resume/cancel extension hooks


def _macro_tip_forming(mc, shot):
    """
    For doc/Macro-Tip-Forming.md - the _MMU_FORM_TIP macro-vars screen.
    Kconfig.form_tip is sourced unconditionally in macro_vars/Kconfig (unlike
    cut_tip/servo_cutter/blobifier below), so this is visible on the boxturtle
    seed even though tip cutting, not forming, is the seed's actual choice.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_FORM_TIP)')
    shot('tip-forming')  # ramming/separation/cooling/skinnydip/parking steps


def _macro_toolhead_tip_cutting(mc, shot):
    """
    For doc/Macro-Toolhead-Tip-Cutting.md - the _MMU_CUT_TIP macro-vars screen.
    Gated on MMU_HAS_TOOLHEAD_CUTTER, which lives under Toolhead sensors/settings
    ("Has toolhead cutter?") - not under Tip Forming / Cutting itself. Only once
    that's on does "Tip cutting using toolhead cutter" even appear as a choice
    under Tip Forming / Cutting's standalone-option choice (it becomes the
    choice's new default, but is selected explicitly here anyway).
    """
    mc.enter('Toolhead sensors/settings')
    mc.select('Has toolhead cutter?')
    mc.toggle()
    mc.autofit()
    mc.back()  # -> (Top)

    mc.enter('Tip Forming / Cutting')
    mc.enter('Select standalone tip shaping option')
    mc.select('Tip cutting using toolhead cutter')
    mc.toggle()  # choice auto-closes back to Tip Forming / Cutting
    mc.autofit()
    mc.back()  # -> (Top)

    mc.enter('Macro Variables')
    mc.enter('(_MMU_CUT_TIP)')
    shot(
        'toolhead-tip-cutting')  # blade/pin geometry, cut speeds, gantry servo


def _macro_servo_cutter(mc, shot):
    """
    For doc/Macro-Servo-Cutter.md - the _MMU_SERVO_CUTTER macro-vars screen.
    Gated on MMU_HAS_SERVO_CUTTER, off by default - toggled on under Tip Forming /
    Cutting (same menu the base screenshot in _feature_tip_forming_purging shows
    with this off).
    """
    mc.enter('Tip Forming / Cutting')
    mc.select('Have servo cutter at MMU?')
    mc.toggle()
    mc.autofit()
    mc.back()  # -> (Top)

    mc.enter('Macro Variables')
    mc.enter('(_MMU_SERVO_CUTTER)')
    shot('servo-cutter')  # servo angles/timing + feed/cut length and attempts

def _config_selector_servo(mc, shot):
    """
    Custom selector servo settings.
    """
    mc.enter('Other Settings')
    mc.select('Selector servo')
    shot('01-selector-servo')
    mc.enter('Selector servo')
    shot('02-selector-servo')

def _macro_blobifier(mc, shot):
    """
    For doc/Macro-Blobifier.md - the _BLOBIFIER macro-vars screen. Gated on
    MMU_HAS_BLOBIFIER, off by default - toggled on under Purging (same menu the
    base screenshot in _feature_tip_forming_purging shows with this off).

    ~60 variables - looked too tall for one screenshot, but autofit's 96-row cap
    comfortably covers the whole menu (75 rows, no scroll arrows) in practice, so
    this is one shot rather than the split originally planned. Comment headers
    like "Blob Tuning" render in a distinct all-caps banner style and aren't
    themselves selectable, which is why this doesn't use mc.select() on them.
    """
    mc.enter('Purging')
    mc.select('Have Blobifier?')
    mc.toggle()
    mc.autofit()
    mc.back()  # -> (Top)

    mc.enter('Macro Variables')
    mc.enter('(_BLOBIFIER)')
    shot('blobifier')  # every _BLOBIFIER_VARS setting, one tall screen


def _macro_purge(mc, shot):
    """
    For doc/Macro-Purge.md - the _MMU_PURGE macro-vars screen. Unconditional
    menu, so the boxturtle seed (default) needs no setup.
    """
    mc.enter('Macro Variables')
    mc.enter('(_MMU_PURGE)')
    shot('purge')  # single reference-purge speed setting


SESSIONS = [
    {
        'name': 'getting-started-boxturtle',
        'caption':
        'doc/GettingStarted-BoxTurtle.md - first menuconfig pass for a Box Turtle',
        'scenes': _getting_started_boxturtle,
        'outdir': 'GettingStarted-BoxTurtle',
        'seed': 'none',
    },
    {
        'name': 'feature-espooler',
        'caption':
        'doc/Feature-Espooler.md - the eSpooler pins menuconfig screen',
        'scenes': _feature_espooler,
        'outdir': 'Feature-Espooler',
    },
    {
        'name': 'feature-endless-spool-runout',
        'caption':
        'doc/Feature-Endless-Spool-Runout.md - the EndlessSpool options screen',
        'scenes': _feature_endless_spool_runout,
        'outdir': 'Feature-Endless-Spool-Runout',
    },
    {
        'name': 'feature-sync-feedback-buffer',
        'caption':
        'doc/Feature-Sync-Feedback-Buffer.md - buffer hardware and motor-sync screens',
        'scenes': _feature_sync_feedback_buffer,
        'outdir': 'Feature-Sync-Feedback-Buffer',
    },
    {
        'name': 'feature-leds',
        'caption': 'doc/Feature-LEDs.md - Led config and Neopixel pin screens',
        'scenes': _feature_leds,
        'outdir': 'Feature-LEDs',
    },
    {
        'name': 'feature-gate-ttg-maps',
        'caption':
        'doc/Feature-Gate-TTG-Maps.md - automap strategy / reset-TTG screen',
        'scenes': _feature_gate_ttg_maps,
        'outdir': 'Feature-Gate-TTG-Maps',
    },
    {
        'name': 'feature-filament-bypass',
        'caption':
        "doc/Feature-Filament-Bypass.md - the bypass design-attribute screen",
        'scenes': _feature_filament_bypass,
        'outdir': 'Feature-Filament-Bypass',
    },
    {
        'name': 'feature-tip-forming-purging',
        'caption':
        'doc/Feature-Tip-Forming-Purging.md - Tip Forming/Cutting and Purging screens',
        'scenes': _feature_tip_forming_purging,
        'outdir': 'Feature-Tip-Forming-Purging',
    },
    {
        'name': 'feature-eject-buttons',
        'caption':
        'doc/Feature-Eject-Buttons.md - eject buttons config screen',
        'scenes': _feature_eject_buttons,
        'outdir': 'Feature-Eject-Buttons',
    },
    {
        'name': 'feature-flowguard',
        'caption': 'doc/Feature-FlowGuard.md - FlowGuard config screen',
        'scenes': _feature_flowguard,
        'outdir': 'Feature-FlowGuard',
    },
    {
        'name': 'feature-environment-manager',
        'caption':
        'doc/Feature-Environment-Manager.md - environment sensor and heater config screens',
        'scenes': _feature_environment_manager,
        'outdir': 'Feature-Environment-Manager',
    },
    {
        'name': 'feature-fan-control',
        'caption':
        'doc/Feature-Fan-Control.md - fan config and fan controls screens',
        'scenes': _feature_fan_control,
        'outdir': 'Feature-Fan-Control',
    },
    {
        'name': 'feature-nfc',
        'caption':
        'doc/Feature-NFC.md - shared NFC reader config screen (ercf seed)',
        'scenes': _feature_nfc,
        'outdir': 'Feature-NFC',
        'seed': 'ercf',
    },
    {
        'name': 'getting-started-vivid',
        'caption':
        'doc/GettingStarted-ViViD.md - first menuconfig pass for a BTT ViViD',
        'scenes': _getting_started_vivid,
        'outdir': 'GettingStarted-ViViD',
        'seed': 'none',
    },
    {
            'name': 'getting-started-ercf',
            'caption':
            'doc/GettingStarted-erf.md - first menuconfig pass for a ERCF',
            'scenes': _getting_started_ercf,
            'outdir': 'GettingStarted-ERCF',
            'seed': 'none'
            #'seed': '/Volumes/u01/dev/Happy-Hare/doc_tools/ercf',
        },
    {
        'name': 'getting-started-tradrack',
        'caption':
        'doc/GettingStarted-Tradrack.md - first menuconfig pass for a Tradrack',
        'scenes': _getting_started_tradrack,
        'outdir': 'GettingStarted-Tradrack',
        'seed': 'none'
        #'seed': '/Volumes/u01/dev/Happy-Hare/doc_tools/tradrack',
    },
    {
        'name': 'getting-started-emu',
        'caption':
        'doc/GettingStarted-EMU.md - first menuconfig pass for an EMU',
        'scenes': _getting_started_emu,
        'outdir': 'GettingStarted-EMU',
        'seed': 'none',
    },
    {
        'name': 'macro-print-start-end',
        'caption':
        'doc/Macro-Print-Start-End.md - the _MMU_SOFTWARE macro-vars screen',
        'scenes': _macro_print_start_end,
        'outdir': 'Macro-Print-Start-End',
    },
    {
        'name': 'macro-state-change-hooks',
        'caption':
        'doc/Macro-State-Change-Hooks.md - the _MMU_STATE macro-vars screen',
        'scenes': _macro_state_change_hooks,
        'outdir': 'Macro-State-Change-Hooks',
    },
    {
        'name': 'macro-sequence',
        'caption':
        'doc/Macro-Sequence.md - the _MMU_SEQUENCE macro-vars screen',
        'scenes': _macro_sequence,
        'outdir': 'Macro-Sequence',
    },
    {
        'name': 'macro-client',
        'caption': 'doc/Macro-Client.md - the _MMU_CLIENT macro-vars screen',
        'scenes': _macro_client,
        'outdir': 'Macro-Client',
    },
    {
        'name': 'macro-tip-forming',
        'caption':
        'doc/Macro-Tip-Forming.md - the _MMU_FORM_TIP macro-vars screen',
        'scenes': _macro_tip_forming,
        'outdir': 'Macro-Tip-Forming',
    },
    {
        'name': 'macro-toolhead-tip-cutting',
        'caption':
        'doc/Macro-Toolhead-Tip-Cutting.md - the _MMU_CUT_TIP macro-vars screen',
        'scenes': _macro_toolhead_tip_cutting,
        'outdir': 'Macro-Toolhead-Tip-Cutting',
    },
    {
        'name': 'macro-servo-cutter',
        'caption':
        'doc/Macro-Servo-Cutter.md - the _MMU_SERVO_CUTTER macro-vars screen',
        'scenes': _macro_servo_cutter,
        'outdir': 'Macro-Servo-Cutter',
    },
    {
        'name': 'macro-blobifier',
        'caption': 'doc/Macro-Blobifier.md - the _BLOBIFIER macro-vars screen',
        'scenes': _macro_blobifier,
        'outdir': 'Macro-Blobifier',
    },
    {
        'name': 'macro-purge',
        'caption': 'doc/Macro-Purge.md - the _MMU_PURGE macro-vars screen',
        'scenes': _macro_purge,
        'outdir': 'Macro-Purge',
    },
    {
        'name': 'config-selector-servo',
        'caption': 'doc/Config-Selector-Servo.md - the selector servo settings screen',
        'scenes': _config_selector_servo,
        'outdir': 'Config-Selector_Servo',
        'seed': '/Volumes/u01/dev/Happy-Hare/doc_tools/tradrack',
    },
]


def run_session(session,
                outdir,
                scale=2,
                seed=None,
                min_rows=None,
                verbose=False):
    """Run one session, returning the images it produced."""
    written = []
    context = {
        key: session[key]
        for key in ('unit_name', 'multi_unit', 'entry_point') if key in session
    }
    # A session with its own 'outdir' (a getting-started page's image folder) always
    # goes there; --outdir only redirects sessions that did not ask for a home.
    outdir = os.path.join(DOC,
                          session['outdir']) if 'outdir' in session else outdir

    with Menuconfig(cols=session.get('cols', DEFAULT_COLS),
                    rows=session.get('rows', 40),
                    seed=seed or session.get('seed', DEFAULT_SEED),
                    style=session.get('style'),
                    min_rows=min_rows or session.get('min_rows', MIN_ROWS),
                    **context) as mc:

        def shot(name):
            path = os.path.join(outdir, name + '.png')
            mc.shot(path,
                    trim=session.get('trim', True),
                    scale=scale,
                    fit=session.get('fit', True))
            if verbose:
                mc.dump()
            print('    %-24s %2dx%-3d %s' %
                  (name + '.png', mc.cols, mc.rows, mc.state()))
            written.append(path)

        session['scenes'](mc, shot)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='python -m doc_tools.shots',
        description=
        'Regenerate the menuconfig screenshots used by the documentation.')
    parser.add_argument('--only',
                        action='append',
                        default=[],
                        metavar='NAME',
                        help='just this session; repeatable')
    parser.add_argument('--outdir', default=IMAGES, help='where the PNGs go')
    parser.add_argument(
        '--seed',
        help='override every session\'s seed: a built-in name, '
        'or a path to a .mmu_config / .mmu_config_<unit>')
    parser.add_argument('--scale',
                        type=int,
                        default=2,
                        help='pixel scale (default 2)')
    parser.add_argument(
        '--min-rows',
        type=int,
        help='override every session\'s height floor (default %d)' % MIN_ROWS)
    parser.add_argument('--list',
                        action='store_true',
                        help='list the sessions and exit')
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='dump each captured screen as text too')
    args = parser.parse_args(argv)

    if args.list:
        width = max(len(session['name']) for session in SESSIONS)
        for session in SESSIONS:
            print('  %-*s  %s' % (width, session['name'], session['caption']))
        return 0

    known = {session['name'] for session in SESSIONS}
    unknown = [name for name in args.only if name not in known]
    if unknown:
        parser.error('no such session: %s (try --list)' % ', '.join(unknown))
    wanted = [s for s in SESSIONS if not args.only or s['name'] in args.only]

    # No pre-creation of args.outdir here: shot() (doc_tools/capture.py) already
    # makes whatever directory a PNG needs, and args.outdir is only the fallback
    # for a session with no 'outdir' of its own - creating it eagerly would recreate
    # exactly the unused doc/images/ this file's header says not to write to.
    failed, written = [], []
    for index, session in enumerate(wanted, 1):
        print('[%d/%d] %s' % (index, len(wanted), session['name']))
        try:
            written += run_session(session, args.outdir, args.scale, args.seed,
                                   args.min_rows, args.verbose)
        except (ScreenError, OSError) as exc:
            failed.append(session['name'])
            print(
                traceback.format_exc() if args.verbose else '    FAILED: %s' %
                exc,
                file=sys.stderr)

    if failed:
        print('\n%d of %d sessions failed: %s' %
              (len(failed), len(wanted), ', '.join(failed)),
              file=sys.stderr)
        return 1
    # Sessions each name their own 'outdir' (see the header above), so a run can
    # easily span several folders - naming just one, as if there were a single
    # shared pool, would be as misleading as recreating that pool would be.
    dirs = sorted({os.path.relpath(os.path.dirname(path)) for path in written})
    print('\n%d screenshot%s in %s' %
          (len(written), '' if len(written) == 1 else 's',
           ', '.join(dirs) if dirs else '(nothing written)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
