## finish this for all 18 states states 1-8 for strain 4/8 and RPU and BLANK and incorporate camera so that
## add states for ??
## adjust locations, create toggable state pippette system (IPTG, ATC, ERROR) 1-8 (ie 0-7)

volume=200

volume_states=10
volume_antibiotics=1

dest_4state1=['A1','B1','C1','D1']
source_4state1=['A1']

dest_4state2=['A2','B2','C2','D2']
source_4state2=['A2']

dest_4state3=['A3','B3','C3','D3']
source_4state3=['A3']

dest_4state4=['A4','B4','C4','D4']
source_4state4=['A4']

dest_4state5=['A5','B5','C5','D5']
source_4state5=['A5']

dest_4state6=['A6','B6','C6','D6']
source_4state6=['A6']

dest_4state7=['A7','B7','C7','D7']
source_4state7=['B1']

dest_4state8=['A8','B8','C8','D8']
source_4state8=['B2']

dest_8state1=['E1','F1','G1','H1']
source_8state1=['C1']

dest_8state2=['E2','F2','G2','H2']
source_8state2=['C2']

dest_8state3=['E3','F3','G3','H3']
source_8state3=['C3']

dest_8state4=['E4','F4','G4','H4']
source_8state4=['C4']

dest_8state5=['E5','F5','G5','H5']
source_8state5=['C5']

dest_8state6=['E6','F6','G6','H6']
source_8state6=['C6']

dest_8state7=['E7','F7','G7','H7']
source_8state7=['D1']

dest_8state8=['E8','F8','G8','H8']
source_8state8=['D2']

dest_RPU=['A9','B9','C9','D9']
source_RPU=['B4']

dest_blank=['E9','F9','G9','H9']
source_blank=['D5']


antibiotics_on=1
dest_kan=['A1','A2','A3','A4','A5','A6','B1','B2','B4','C1','C2','C3','C4','C5','C6','D1','D2']
source_kan=['B6']

dest_spec=['A1','A2','A3','A4','A5','A6','B1','B2','C1','C2','C3','C4','C5','C6','D1','D2']
source_spec=['D6']

states_on=1

dest_IPTG=['A2','C2','A4','C4','A6','C6','B2','D2']
source_IPTG=['D3']

dest_ATC=['A3','C3','A4','C4','B1','D1','B2','D2']
source_ATC=['D4']

dest_ERROR=['A5','C5','A6','C6','B1','D1','B2','D2']
source_ERROR=['D5']

all_wells=['A1','A2','A3','A4','A5','A6','B1','B2','B4','B5','C1','C2','C3','C4','C5','C6','D1','D2']

mix_on=1
repitions=2
volume_mix=100

from opentrons import protocol_api
metadata = {
    'protocolName': 'transfer for pLB001',
    'author': 'Parker',
    'description': 'enjoy saving your hands Lukas',
    'apiLevel': '2.10'
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p300_single_gen2","_pip_mount":"right","well_1":"opentrons_24_aluminumblock_nest_1.5ml_snapcap","well_2":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    [pip_model, pip_mount, well_1, well_2] = get_values ( '_pip_model', '_pip_mount', 'well_1', 'well_2')

    tips=[protocol.load_labware('opentrons_96_tiprack_300ul', '6')] 
    pipette = protocol.load_instrument(pip_model, pip_mount, tip_racks=tips)
    
    tips_20=[protocol.load_labware('opentrons_96_tiprack_20ul', '5')] 
    pip_20 = protocol.load_instrument('p20_single_gen2', 'left', tip_racks=tips_20)
   
    plate_1 = protocol.load_labware(well_1,'2')
    plate_2 = protocol.load_labware(well_2,'3')

    ## if antibiotics_on=1 setup below
    
    if antibiotics_on==1:
        source_kan_well=[plate_1[x] for x in source_kan]
        dest_kan_well=[plate_1[x] for x in dest_kan]
        
        for s, d in zip([source_kan_well],[dest_kan_well]): 
            pip_20.transfer(volume_antibiotics, s, d, new_tip='always')
            
        source_spec_well=[plate_1[x] for x in source_spec]
        dest_spec_well=[plate_1[x] for x in dest_spec]
        
        for s, d in zip([source_spec_well],[dest_spec_well]): 
            pip_20.transfer(volume_antibiotics, s, d, new_tip='always')

    ## if states_on=1 setup below
    
    if states_on==1:
    
        source_IPTG_well=[plate_1[x] for x in source_IPTG]
        dest_IPTG_well=[plate_1[x] for x in dest_IPTG]

        for s, d in zip([source_IPTG_well],[dest_IPTG_well]): 
                pip_20.transfer(volume_states, s, d, new_tip='always')
                
        source_ATC_well=[plate_1[x] for x in source_ATC]
        dest_ATC_well=[plate_1[x] for x in dest_ATC]

        for s, d in zip([source_ATC_well],[dest_ATC_well]): 
                pip_20.transfer(volume_states, s, d, new_tip='always')
                
        source_ERROR_well=[plate_1[x] for x in source_ERROR]
        dest_ERROR_well=[plate_1[x] for x in dest_ERROR]

        for s, d in zip([source_ERROR_well],[dest_ERROR_well]): 
                pip_20.transfer(volume_states, s, d, new_tip='always')


## add mix step

    if mix_on==1:
        mix_wells=[plate_1[x] for x in all_wells]
    
        for s in (mix_wells):
            pipette.pick_up_tip()
            pipette.mix(repitions,volume_mix, s)
            pipette.drop_tip()
    

## Transfer to 96-well plate below

    source41_well=[plate_1[x] for x in source_4state1]
    dest41_well=[plate_2[x] for x in dest_4state1]
    

    for s, d in zip([source41_well],[dest41_well]): 
        pipette.transfer(volume, s, d)
         
        
    source42_well=[plate_1[x] for x in source_4state2]
    dest42_well=[plate_2[x] for x in dest_4state2]
    

    for s, d in zip([source42_well],[dest42_well]): 
        pipette.transfer(volume, s, d)
        
        
    source43_well=[plate_1[x] for x in source_4state3]
    dest43_well=[plate_2[x] for x in dest_4state3]
    

    for s, d in zip([source43_well],[dest43_well]): 
        pipette.transfer(volume, s, d)
        
    source44_well=[plate_1[x] for x in source_4state4]
    dest44_well=[plate_2[x] for x in dest_4state4]
    

    for s, d in zip([source44_well],[dest44_well]): 
        pipette.transfer(volume, s, d)
        
        source45_well=[plate_1[x] for x in source_4state5]
    dest45_well=[plate_2[x] for x in dest_4state5]
    

    for s, d in zip([source45_well],[dest45_well]): 
        pipette.transfer(volume, s, d)
        
    source46_well=[plate_1[x] for x in source_4state6]
    dest46_well=[plate_2[x] for x in dest_4state6]
    

    for s, d in zip([source46_well],[dest46_well]): 
        pipette.transfer(volume, s, d)
        
        source47_well=[plate_1[x] for x in source_4state7]
    dest47_well=[plate_2[x] for x in dest_4state7]
    

    for s, d in zip([source47_well],[dest47_well]): 
        pipette.transfer(volume, s, d)
        
    source48_well=[plate_1[x] for x in source_4state8]
    dest48_well=[plate_2[x] for x in dest_4state8]
    

    for s, d in zip([source48_well],[dest48_well]): 
        pipette.transfer(volume, s, d)
        
    source81_well=[plate_1[x] for x in source_8state1]
    dest81_well=[plate_2[x] for x in dest_8state1]
    

    for s, d in zip([source81_well],[dest81_well]): 
        pipette.transfer(volume, s, d)
        
        
    source82_well=[plate_1[x] for x in source_8state2]
    dest82_well=[plate_2[x] for x in dest_8state2]
    

    for s, d in zip([source82_well],[dest82_well]): 
        pipette.transfer(volume, s, d)
        
    source83_well=[plate_1[x] for x in source_8state3]
    dest83_well=[plate_2[x] for x in dest_8state3]
    

    for s, d in zip([source83_well],[dest83_well]): 
        pipette.transfer(volume, s, d)
        
        
    source84_well=[plate_1[x] for x in source_8state4]
    dest84_well=[plate_2[x] for x in dest_8state4]
    

    for s, d in zip([source84_well],[dest84_well]): 
        pipette.transfer(volume, s, d)  
        
        source85_well=[plate_1[x] for x in source_8state5]
    dest85_well=[plate_2[x] for x in dest_8state5]
    

    for s, d in zip([source85_well],[dest85_well]): 
        pipette.transfer(volume, s, d)
        
        
    source86_well=[plate_1[x] for x in source_8state6]
    dest86_well=[plate_2[x] for x in dest_8state6]
    

    for s, d in zip([source86_well],[dest86_well]): 
        pipette.transfer(volume, s, d)
        
    source87_well=[plate_1[x] for x in source_8state7]
    dest87_well=[plate_2[x] for x in dest_8state7]
    

    for s, d in zip([source87_well],[dest87_well]): 
        pipette.transfer(volume, s, d)
        
        
    source88_well=[plate_1[x] for x in source_8state8]
    dest88_well=[plate_2[x] for x in dest_8state8]
    

    for s, d in zip([source88_well],[dest88_well]): 
        pipette.transfer(volume, s, d)
    
    
    sourceRPU_well=[plate_1[x] for x in source_RPU]
    destRPU_well=[plate_2[x] for x in dest_RPU]
    
    for s, d in zip([sourceRPU_well],[destRPU_well]): 
        pipette.transfer(volume, s, d)
        
        
    sourceBlank_well=[plate_1[x] for x in source_blank]
    destBlank_well=[plate_2[x] for x in dest_blank]
    

    for s, d in zip([sourceBlank_well],[destBlank_well]): 
        pipette.transfer(volume, s, d)