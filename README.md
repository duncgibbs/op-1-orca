# op-1-orca
A Python script for converting OP-1 MIDI inputs to Orca commands.

## Installation and Running
Make sure to install `mido` and `python-rtmidi`.

Then just run `python op1_listener.py` with the OP-1 plugged in and in MIDI Mode.

## Layout

### Movement

Movement is done like an etch a sketch.

- Blue Knob - controls your x coordinates
- Green Knob - controls your y coordinates
- White Knob - controls your selection width
- Red Knob - controls your selection height

### Notes

The keyboard corresponds to note values.

- F - writes "F" to your current coordinates
- F# - writes "f" to your current coordinates
- etc.

### Numbers
The sound number buttons write numbers.

- 1 - writes "1" to your current coordinates
- and so on
- Sequencer - writes "9" to your current coordinates
- Album/Com writes "0" to your current coordinates

### Special Characters
The Synth Mode Button will cycle through Orcas IO special characters:

[ :, %, !, ?, ;, =, $ ]

### Miscellaneous
Other buttons have various functions

- Lift - copies your current selection
- Drop - pastes your current copied values at your current coordinates
- Split - erases your current selection
- Mic/Input - resets the frame to 0
- Record - runs the current frame
- Play - plays
- Stop - stops
- Blue Knob Click - resets your coordinates to 0,0
- Green Knob Click - selects all

## Modifier Keys
The real meat and potatoes, holding specific modifier keys will put you into different modes.

- Tape 1 - lower case letter mode
- Tape 2 - upper case letter mode
- Tape 3 - special character mode
- Tape 4 - number mode
- Tempo - tempo mode
- Drum Mode - Midi I/O selection mode
- Tape Mode - frame mode

#### Lower Case Letter Mode
In lower case letter mode, the play, stop, and keyboard keys now all correspond to a lower case letter.

The Blue Knob will also cycle through all lower case letters.

#### Upper Case Letter Mode
The same as lower case mode, except with upper case letters.

#### Special Character Mode
The same as lower case mode, except with special characters. The play and stop buttons no longer correspond to anything.

#### Number Mode
The same as special character mode.

#### Tempo Mode
In tempo mode, the blue knob will now adjust the BPM.

#### MIDI I/O Selection Mode
In I/O selection mode, the blue knob will cycle through MIDI inputs, and the green knob through MIDI outputs.

#### Frame Mode
In Frame mode, the blue knob will allow you to skip and rewind through frames.
