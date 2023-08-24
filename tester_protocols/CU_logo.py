#selfnote working CU logo, please comment the additional code so that it is clear
#Submit this one to GitHub

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"left","_dp_type":"nest_96_wellplate_200ul_flat","_dye_type":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]


from opentrons import protocol_api
import math

metadata = {
    'protocolName': 'CULogo',
    'author': 'parke',
    'description':'This protocol uses 2 dyes to pipe out the CU logo',
    'apiLevel':'2.10'
    }


def run(ctx: protocol_api.ProtocolContext):
    [_pip_model, _pip_mount, _dp_type, _dye_type] = get_values(  # noqa: F821
        '_pip_model', '_pip_mount', '_dp_type', '_dye_type')

    # customizable parameters
    pip_model = _pip_model
    pip_mount = _pip_mount
    dp_type = _dp_type
    dye_type = _dye_type

    # create pipette and tiprack
    tip_size = pip_model.split('_')[0][1:]
    tip_size = '300' if tip_size == '50' else tip_size
    tip_name = 'opentrons_96_tiprack_'+tip_size+'ul'
    tips = [ctx.load_labware(tip_name, '1', 'Opentrons Tips')]

    pipette = ctx.load_instrument(
        pip_model, pip_mount, tip_racks=tips)

    # create plates and pattern list
    output = ctx.load_labware(dp_type, '3', 'Destination Plate')

    dye_container = ctx.load_labware(dye_type, '2', 'Dye Source')

    # Well Location set-up
    dye1_wells = [ 'G2','A3', 'A4', 'A5' , 'H3', 'B2', 'B6', 'C1'] 
    
    dye1_1_wells=[ 'D1', 'E1', 'F2','F7', 'G3', 'G6','H4','H5']

    dye1_dest = [output[x] for x in dye1_wells]
    dye1_1_dest= [output[x] for x in dye1_1_wells]
    
    dye2_wells = ['B7', 'B12', 'C7', 'C12', 'D7', 'D12', 'E7']
    dye2_2_wells=['E12','F8', 'F11', 'G8', 'G11', 'H9', 'H10']

    dye2_dest = [output[x] for x in dye2_wells]
    dye2_2_dest =[output[x] for x in dye2_2_wells]


#assigning the dest wells to dye storage wells

    if 'reservoir' in dye_type:
        dye1 = [dye_container.wells()[0]] * 2
        dye1_2 = [dye_container.wells()[2]] * 2
        dye2 = [dye_container.wells()[4]] * 2
        dye2_2 = [dye_container.wells()[6]] * 2
    else:
        dye1 = dye_container.wells()[:2]
        dye1_2= dye_container.wells()[2:4]
        dye2 = dye_container.wells()[4:6]
        dye2_2 = dye_container.wells()[6:8]

    dye_vol = 200 if tip_size == '1000' else 50

    # distribution function
    def pip_pickup():
        pipette.pick_up_tip()
    
    def pip_drop():
        pipette.drop_tip()
    
    def logo_distribute(srcs, dests):
        """
        This is a function that will perform the pick_up_tip(), transfers(),
        and drop_tip() 
        :param srcs: source wells (should be a list)
        :param dests: destination wells (should be a list)
        """
        halfDests = math.ceil(len(dests)/2)
        
        for src, dest in zip(srcs, [dests[:halfDests], dests[halfDests:]]):
            for d in dest:
                pipette.transfer(dye_vol, src, d, new_tip='never')
        
    pip_pickup()
    logo_distribute(dye1, dye1_dest)
    logo_distribute(dye1_2, dye1_1_dest)
    pip_drop()
    #switches from one dye to the other doing this makes it possible to run multiple filling up wells with the same tip
    pip_pickup()
    logo_distribute(dye2, dye2_dest)
    logo_distribute(dye2_2, dye2_2_dest)
    pip_drop()
