
#cells are placed in slot A1, the goldengate/mini in A3 (can interchage which is using)

#can change time/tempurature and cell volume here

cold =4
hot=47
lid_temp=60
rest=25
start_time_min=20
hot_time_min=1
cold_time_min=3
start_time=start_time_min*60
hot_time=hot_time_min*60
cold_time=cold_time_min*60

from opentrons import protocol_api
metadata = {
    'protocolName': 'Heat Shock Protocol',
    'author': 'Parker',
    'description': 'Protocol for heat-shock',
    'apiLevel': '2.10' 
}

#need thermocycler and temperature module


def run(protocol):

    temp = protocol.load_module('temperature module gen2', '1')
    temp_block = temp.load_labware('opentrons_24_aluminumblock_nest_1.5ml_snapcap')
    #temp module setup (use of 1.5 mL snap caps in wells)
    
    thermo = protocol.load_module('thermocycler')
    thermo_plate=thermo.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')
    #thermocycler setup
    
    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '6')] 
    pipette = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips)
    #tiprack setup
    
    if thermo.lid_position != 'open':
        thermo.open_lid()
    
    cells= temp_block.wells()
    loc=thermo_plate.wells()
    
    
    pipette.transfer(40, cells[0], loc[0])
    #move cells into cycler slot A1
    
    
    
    def golden():
        solution= temp_block['A3']
        pipette.transfer(5,solution,loc[0])
    
    def mini():
        solution= temp_block['A3']
        pipette.transfer(.5,solution,loc[0])
    
    golden() #change this the mini() or golden() depending on which you want to use
    
    
    def thermo_():
        
        thermo.close_lid()
            
        thermo.set_lid_temperature(lid_temp)
        
        profile=[
            {'temperature': cold, 'hold_time_seconds': start_time},
            {'temperature': hot, 'hold_time_seconds': hot_time},
            {'temperature': cold, 'hold_time_seconds': cold_time}]
            
        thermo.execute_profile(steps=profile, repetitions=1,
                           block_max_volume=45)
        thermo.deactivate_lid()
        thermo.set_block_temperature(rest)
    
    
    thermo_()
    
    protocol.pause('place 1 mL of broth in D6')
    thermo.open_lid()
    pipette.transfer(40, cells[20], cells[23])
    
    