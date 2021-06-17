from OpenHub.globals import accessories

for accessory in accessories:
    if accessory.calibrator != None:
        accessory.calibrator.calibrate()