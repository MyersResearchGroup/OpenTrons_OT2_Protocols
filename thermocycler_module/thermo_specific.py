#This protocol moves the liquid from a 96-well plate to the 96-well plate of the TC and runs the TC

#it is one to one transfer in this code, can change it to do different settings, but ya

#notes on tempurature limitations
#block temp range 4-99 degrees C
#Lid temp range 37-110 degrees C
    
#DEACTIVATE BEFORE THE END OF EACH PROTOCOL SINCE THERMOCYCLER HOLDS TEMPURATURE EVEN WHILE NOT RUNNING PROTOCOL

#selfnote has not been run on OPT, but works in simulation

def get_values(*names):
    import json
    _all_values = json.loads("""{"well_vol":50,"lid_temp":110,"init_temp":96,"init_time":30,"d_temp":96,"d_time":15,"a_temp":60,"a_time":30,"e_temp":74,"e_time":30,"num_cycles":1,"fe_temp":74,"fe_time":30,"final_temp":4}""")
    return [_all_values[n] for n in names]


metadata = {
    'protocolName': 'Thermocycler Specific move Example Protocol',
    'author': 'Parke and Opentrons',
    'source': 'Protocol Library',
    'apiLevel': '2.0'
    }


def run(protocol):
    [well_vol, lid_temp, init_temp, init_time,
        d_temp, d_time, a_temp, a_time,
        e_temp, e_time, num_cycles,
        fe_temp, fe_time, final_temp] = get_values(  # noqa: F821
        'well_vol', 'lid_temp', 'init_temp', 'init_time', 'd_temp', 'd_time',
        'a_temp', 'a_time', 'e_temp', 'e_time', 'num_cycles',
        'fe_temp', 'fe_time', 'final_temp')

    tc_mod = protocol.load_module('thermocycler')

    """
    Add liquid transfers here, if interested (make sure TC lid is open)
    Example (Transfer 50ul of Sample from plate to Thermocycler):
   """
    tips = [protocol.load_labware('opentrons_96_tiprack_300ul', '2')]
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=tips)
    tc_plate = tc_mod.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    sample_plate = protocol.load_labware('nest_96_wellplate_200ul_flat', '1')
#sets up the fact that the TC and plate exists


    tc_wells = ['A1','B1', 'C1']
    sample_wells = ['A3', 'B3', 'C3']
    #this is where the wells are defined, samples need to be equal to tc wells in this code
   
   

    if tc_mod.lid_position != 'open':
        tc_mod.open_lid()

    pipette.pick_up_tip()
    for t, s in zip(tc_wells, sample_wells):
        pipette.transfer(50,sample_plate.wells(s), tc_plate.wells(t), new_tip='never')
        #always for transfering from A1 to A1 for all the wells within the well plates
 

    pipette.drop_tip()
    
    # Close lid
    if tc_mod.lid_position != 'closed':
        tc_mod.close_lid()

    # lid temperature set
    tc_mod.set_lid_temperature(lid_temp)

    # initialization
    tc_mod.set_block_temperature(init_temp, hold_time_seconds=init_time,
                                 block_max_volume=well_vol)

    # run profile
    profile = [
        {'temperature': d_temp, 'hold_time_seconds': d_time},
        {'temperature': a_temp, 'hold_time_seconds': a_temp},
        {'temperature': e_temp, 'hold_time_seconds': e_time}
    ]

    tc_mod.execute_profile(steps=profile, repetitions=num_cycles,
                           block_max_volume=well_vol)

    # final elongation

    tc_mod.set_block_temperature(fe_temp, hold_time_seconds=fe_time,
                                 block_max_volume=well_vol)

    # final hold
    tc_mod.deactivate_lid()
    tc_mod.set_block_temperature(final_temp)
    
    
    
