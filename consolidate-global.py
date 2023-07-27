#you got volume and columns, fun fact the wells go A1-H12
# volume if need of larger quanties can fix pipette mount easily
volume=10
dest=['A1']
source=['A2','H11']


from opentrons import protocol_api
metadata = {
    'protocolName': 'global variable consolidare',
    'author': 'Parke',
    'description': 'Transfer from multiple wells to one well on other plate',
    'apiLevel': '2.10'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"right","well_1":"nest_96_wellplate_200ul_flat","well_2":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    [pip_model, pip_mount, well_1, well_2] = get_values ( '_pip_model', '_pip_mount', 'well_1', 'well_2')

    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '1')] 
    pipette = protocol.load_instrument(pip_model, pip_mount, tip_racks=tips)
   
    plate_1 = protocol.load_labware(well_1,'2')
    plate_2 = protocol.load_labware(well_2,'3')

    dest_well=[plate_2[x] for x in dest]
    source_well=[plate_1[x] for x in source]

    for src, d in zip([source_well],[dest_well]): 
        for s in src:
            pipette.consolidate(volume, s, d)