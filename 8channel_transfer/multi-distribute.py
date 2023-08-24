#you got volume and columns, fun fact the columns go 0-11
# volume if need of larger quanties can fix pipette mount easily
volume=10
dest=[0,1]
source=[0]

from opentrons import protocol_api
metadata = {
    'protocolName': 'multi-channel distribute',
    'author': 'Parke',
    'description': 'Transfer from one column to multiple columns on other plate',
    'apiLevel': '2.10'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_multi_gen2","_pip_mount":"right","well_1":"nest_96_wellplate_200ul_flat","well_2":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    [pip_model, pip_mount, well_1, well_2] = get_values ( '_pip_model', '_pip_mount', 'well_1', 'well_2')

    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '1')] 
    pipette = protocol.load_instrument(pip_model, pip_mount, tip_racks=tips)
   
    plate_1 = protocol.load_labware(well_1,'2').columns()
    plate_2 = protocol.load_labware(well_2,'3').columns()

    for s, dests in zip(source,[dest]): 
        for d in dests:
            pipette.distribute(volume, plate_1[s], plate_2[d])
