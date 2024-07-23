tipLocation=5

from opentrons import protocol_api
metadata = {
    'protocolName': 'tip_start',
    'author': 'Parker',
    'description': 'start tip @ tipLocation',
    'apiLevel': '2.15' 
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"left","well_1":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    
    [pip_model, pip_mount, well_1] = get_values ( '_pip_model', '_pip_mount', 'well_1')
    
    tips_300=[protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')]    
    pip=protocol.load_instrument('p300_single_gen2', 'right', tip_racks=tips_300)
    plate_2 = protocol.load_labware('nest_96_wellplate_200ul_flat','2')
    media_plate = protocol.load_labware('nest_1_reservoir_195ml','6')
    
    pip.starting_tip= tips_300[0].wells()[tipLocation]
    
    x=0
    while(x<3): #wells start count at 0
        pip.transfer(100,plate_2.wells(x), media_plate.wells(0)) 
        x=x+1
    
    #pip.starting_tip(tips_300[0].wells()[tipLocation])
    #pip.reset_tipracks()
    #print(pip.starting_tip()[5])
    
    
    countTips(tips_300,protocol, 96, tipLocation)
    
def countTips(tip_rack,protocol, max_tip_count,tipLocation):   
    tipCount=tipLocation
    while(tipCount<max_tip_count): # check wells 0-95
        if tip_rack[0].wells()[tipCount].has_tip is True: #in tipRack 0 (ie first one) check from wells 0-95 to see if it has_tip
            protocol.comment("next tip location ")
            
            word=str(tipCount)
            protocol.comment(word)
            return
        tipCount=tipCount+1

    
    