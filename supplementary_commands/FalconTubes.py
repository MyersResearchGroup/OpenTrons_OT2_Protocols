inputted_tube_value=50 #input tube value in mL
height=0
replicate_amount=3
DNA_amount=4
dilution_factor=5 # 9 uL of media to 1 uL of solution

# note:code needs adjustment to automatically switch heights when pipetting from the falcon tubes
# this can be done with a switch statement that gets run based off of a "media_used" variable
# ran out of time to test exacts for this type of protocol

from opentrons import protocol_api
from opentrons.types import Point
metadata = {
    'protocolName': 'Tube rack Protocol 50 mL with plate',
    'author': 'Parker',
    'description': 'Protocol for implementing usage of falcon tubes without overflowing the tube. Meaning the height of aspiration changes according to volume used or inputted volume of the falcon tube' ,
    'apiLevel': '2.22' 
}




def run(protocol):
    
    
    tubeRack= protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical','5')
    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '6')] 
    pip = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips)
    
    plate_2 = protocol.load_labware('nest_96_wellplate_200ul_flat','2')
    petri_dish = protocol.load_labware('axygen_1_reservoir_90ml','3')
    #pip.transfer(15, petri_dish.wells(0), plate_2.wells(1))
    k=0
    while(k<DNA_amount):
        transferFromFalcon(tubeRack, plate_2, pip, dilution_factor,petri_dish,k)
        k=k+1
    

        
def transferFromFalcon(media_loc, plate_1, pip,dilution_factor,petri_dish,k):
    # tube to plateS
    # 50 mL to plate w/ desired columns and replicates
    #falcon tube 114 mm tall
    starting_tube_volume=inputted_tube_value*1000
    tube_used=0
    
    pip.pick_up_tip()
    i=0
    while(i<replicate_amount):
        height = int(.4)  #23 mm is to 10 mL, 13 mm is ~5 mL. 93 is ~47.5 90 is on the 45 mL line exactly 37.5 mL is 84 
# 70 viable to 45  60 to 35 50 to 25 (a bit close on the pipetting for 25...) 30 to 15? 10 to 5 .4 till end
        if (starting_tube_volume>500):
            
            pip.transfer(dilution_factor-1, media_loc.well(tube_used).bottom(height), petri_dish.well(0).bottom().move(Point(x=-(k*10)-10, y=-(10*i), z=.001)), new_tip='never')
            # min distance between samples == 10 mm nmin 4 uL per sample usage of 30mL of media for plate
            starting_tube_volume=starting_tube_volume-(dilution_factor-1)
            
        else:
            starting_tube_volume=inputted_tube_value*1000 # 50 mL to uL
            tube_used=tube_used+1
        print(starting_tube_volume)
        i=i+1
    pip.drop_tip()
    
    
    