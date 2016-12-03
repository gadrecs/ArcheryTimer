# ArcheryTimer
An archery - Timer for FITA-tournaments using a Raspberry.

This application is designed for raspberry Pi 1 (or later) with an external Touchscreen (ideal: 5" 800x480 px)
Usage: steering of external hardware connected via external board-equipment
(Hardwarelayouts in PDF File)

all overall a very simple program using the Raspis GPIO Ports

The LED and beeper-sequences correspond with the FITA - given regulations.

Phase 1)  Beep and RED light for 10 Seconds    -> Preparation
Phase 2)  Beep and GREEN light for 210 Seconds -> Shooting
Phase 3)  no Beep, ORANGE light for 30 seconds -> Warning phase
Phase 4)  3 Beeps, RED light                   -> End of circle 

there is a possibility of "breaking" the shooting circle in case of emergency !

In one of the next versions i want to add wireless triggering of this.

If you need translations of the captions in the code, i can help
