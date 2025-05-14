# petri dish== 30 mL of media

from opentrons import protocol_api
from opentrons.types import Point
metadata = {
    'protocolName': 'Culture Transformation Protocol location test',
    'author': 'Parker',
    'description': 'Protocol for implementing plating of the cultures',
    'apiLevel': '2.22' 
}


def run(protocol):
    plate_2 = protocol.load_labware('nest_96_wellplate_200ul_flat','2')
    petri_dish = protocol.load_labware('axygen_1_reservoir_90ml','3')
    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '6')]
    pip = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips)
    pip.transfer(15, petri_dish.wells(0), plate_2.wells(1))
    
    
  
    pip.transfer(10, plate_2.wells(1),  petri_dish.well(0).bottom().move(Point(x=-21.0, y=-2.0, z=15.9)))
    
    # cartesian coordinates are best for square plate
    # the coordinates are in mm starting from the middle of the "well" at the bottom of the plate(the bottom of the plate is not exactly the tip touching the bottom of the well plate, but like a bit above that)
    # with the measurements of 128x86 we can have the grid be 120x80 which means that well 0 = -60, -40, 15.9 (left/right, forward/back, up/down) well 1 = -60,-30,15.9 well 9 = -50, -40, 15.9 well 96= 60,40,15.9 (every well change is a change in 10 mm in a direction
    # min distance between samples == 10 mm for min 4 uL per sample usage of 30mL of agar media for plate
    
