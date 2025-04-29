#!/bin/sh

# For linux
# Copy DOOM.hpappdir into the HP Prime emulator for faster test (Wine put me the HP Prime folder into my Documents folder)
rsync -av "$PWD/DOOM.hpappdir/" "/home/$USER/Documents/HP Prime/Calculators/Prime/DOOM.hpappdir/"