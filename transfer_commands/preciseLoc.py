from opentrons.types import Location, Point

metadata = {
    'protocolName': 'Precise Location',
    'author': 'parker',
    'description':'protocol basis for non-plate protocols',
    'apiLevel':'2.10'
    }


def run(ctx): 
# The coordinates are absolute
# with reference to the bottom left corner of slot 1 as origin.
# x, y, and z can be a float or integer
    loc = Location(Point(150, 100, 0), None)

#pipette and labware
    tiprack = ctx.load_labware('opentrons_96_tiprack_20ul', '11')
    pip = ctx.load_instrument('p20_single_gen2', 'right', tip_racks=[tiprack])

#commands
    pip.pick_up_tip()
    pip.move_to(loc)