#selfnote use of transfer function for 2 96well plates


# Import the necessary libraries
from opentrons import protocol_api

# Metadata
metadata = {
    'protocolName': 'tester',
    'author': 'Parker',
    'description': 'Protocol for working with two Nest 96-Well Plate 200 µL flat plates',
    'apiLevel': '2.10'
}

# Define the protocol
def run(protocol: protocol_api.ProtocolContext):
    # Load the two 96-well plates
    plate_1 = protocol.load_labware('nest_96_wellplate_200ul_flat', '2')
    plate_2 = protocol.load_labware('nest_96_wellplate_200ul_flat', '3')

    # Define the pipettes
    left_pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=[protocol.load_labware('opentrons_96_tiprack_20ul', '1')])

    # Define the starting well position
    start_well = plate_1.wells('A1')
    
      # dye1_wells = [ 'A2', 'B1', 'B2', 'B6', 'C1', 'D1', 'E1', 'F2',
                    # 'F7', 'G3', 'G6','H4','H5']

   # for k in range(0,12):
       # dye1_dest = [plate_2.wells(dye1_wells[k])]

      # dye2_wells = ['B7', 'B12', 'C7', 'C12', 'D7', 'D12', 'E7', 'E12',
                  # 'F8', 'F11', 'G8', 'G11', 'H9', 'H10']

    # dye2_dest = [output[x] for x in dye2_wells]
   
   # Transfer liquid from plate 1 to plate 2
  # for j in range(0,1):
    left_pipette.transfer(20, start_well, plate_2.wells('A1'))

    # Move to the next row and repeat
    for i in range(1, 8):
        start_well = plate_1.wells(i, 0)
        left_pipette.transfer(20, start_well, plate_2.wells(i, 0))
