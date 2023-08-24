# This set of commands is to grab for inputting into protocls

#This set up is for the diperse command which is the 1 to many well command

#distrubute command, not working yet TypeError(loc) whatever that means

from opentrons import protocol_api
metadata = {
    'protocolName': 'Distribute',
    'author': 'Parke',
    'description': '',

    'apiLevel': '2.10' #this is the apilevel that OPT uses
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"right","well_1":"nest_96_wellplate_200ul_flat","well_2":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    [pip_model, pip_mount, well_1, well_2] = get_values ( '_pip_model', '_pip_mount', 'well_1', 'well_2')

    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '1')] 
    pipette = protocol.load_instrument(pip_model, pip_mount, tip_racks=tips)
   
    #sample_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', '2')
    
    
    plate_1 = protocol.load_labware(well_1,'2').rows(3)
    plate_2 = protocol.load_labware(well_2,'3').wells('A1')
    
    pipette.distribute(2,plate_2,plate_1)
    