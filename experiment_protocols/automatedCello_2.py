#control + (GFP), - (blank), strain control
#vertical samples with inducer


#heater-shaker steadyState values
temp=37
rpm=1000
#timing of activation steps
overnight=15*60
dayTime=3*60
induceTime=5*60

#location in tempurature module (store)
kan_location=1
spec_location=2
IPTG=23
ATC=19
ARA=15
RPU=11

desired_replicates=4
desired_columns=8 #state based counting
colony1_start_dest_well=0
colony2_start_dest_well=desired_replicates
wells_used=[]

#volumes for transfers
well_media_volume=185
colony_transfer_volume=15
state_volume=2 
antibiotic_volume=150
media_volume=well_media_volume*desired_replicates*(desired_columns+1)
culture_volume=colony_transfer_volume*desired_replicates*(desired_columns+1)
colony_volume=colony_transfer_volume+well_media_volume


desired_replicates=4
desired_columns=8
colony1_start_dest_well=0
colony2_start_dest_well=4
wells_used=[]

from opentrons import protocol_api
metadata = {
    'protocolName': 'Automated Part Characterization',
    'author': 'Parker',
    'description': 'bro just dilute, also mmm inducers ',
    'apiLevel': '2.15' 
}
from threading import Event
global exit
exit = Event()

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"left","well_1":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):

    [pip_model, pip_mount, well_1] = get_values ( '_pip_model', '_pip_mount', 'well_1')
    tips_20=[protocol.load_labware('opentrons_96_tiprack_20ul', '9')] 
    #tips2_20=[protocol.load_labware('opentrons_96_filtertiprack_20ul', '10')]
    pipette = protocol.load_instrument(pip_model, pip_mount,tip_racks=tips_20)
    tips_300=[protocol.load_labware('opentrons_96_filtertiprack_200ul', '8')]
    
    pip=protocol.load_instrument('p300_single_gen2', 'right', tip_racks=tips_300)
    res='nest_1_reservoir_195ml'
    tubeRack= protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical','5')
    plate_2 = protocol.load_labware('nest_96_wellplate_200ul_flat','2')
    media_plate = protocol.load_labware( 'nest_1_reservoir_195ml','6')
    temp_mod = protocol.load_module('temperature module gen2', '7')
    store =temp_mod.load_labware('opentrons_24_aluminumblock_nest_1.5ml_screwcap')
    #heater-shaker setup
    hs_mod = protocol.load_module("heaterShakerModuleV1", "1")
    hs_adapter = hs_mod.load_adapter("opentrons_96_flat_bottom_adapter")
    hs_plate = hs_adapter.load_labware("nest_96_wellplate_200ul_flat")

    #protocol run through commands
    
    
    #step 3, overnight growth
    incubate(protocol, hs_mod, overnight)

    #step 4, double dilution
    estimateCountTip(tips_300, protocol, 96, pip, desired_columns, desired_replicates, 0)
    doubleDilution(hs_mod, hs_plate, media_plate, tubeRack, pip, store, kan_location, spec_location, 0, 1, desired_columns, colony1_start_dest_well, plate_2)
    estimateCountTip(tips_300, protocol, 96, pip, desired_columns, desired_replicates, 0)
    doubleDilution(hs_mod, hs_plate, media_plate, tubeRack, pip, store, kan_location, spec_location, 2, 3, desired_columns, colony2_start_dest_well, plate_2)
    #96 well-plate set up with 2 colonies with 3 repeats   

    #step5, incubate for 3 hrs
    incubate(protocol, hs_mod, dayTime)
      
    #step 6, dilution 1 more time
    estimateCountTip(tips_300, protocol, 96, pip, desired_columns, desired_replicates, 0)
    singleDilution(hs_mod, hs_plate, media_plate, tubeRack, pip, store, kan_location, spec_location, 4, desired_columns, colony1_start_dest_well, plate_2)
    estimateCountTip(tips_300, protocol, 96, pip, desired_columns, desired_replicates, 0)
    singleDilution(hs_mod,hs_plate, media_plate, tubeRack, pip, store, kan_location, spec_location, 5, desired_columns, colony2_start_dest_well,plate_2)

    #step 7,Inducer set-up/movement
    estimateCountTip(tips_20, protocol, 96, pipette, desired_columns, desired_replicates, 1)
    inducerTransfer(store, IPTG, ATC, ARA, plate_2, pipette, desired_columns, colony1_start_dest_well,desired_replicates)
    estimateCountTip(tips_20, protocol, 96, pipette, desired_columns, desired_replicates, 1)
    inducerTransfer(store, IPTG, ATC, ARA, plate_2, pipette, desired_columns, colony2_start_dest_well,desired_replicates)
    estimateCountTip(tips_20, protocol, 96, pipette, desired_columns, desired_replicates, 0)
    controlTransfer(store, RPU,pip, pipette,desired_columns, desired_replicates, media_plate, plate_2)
    #inducer concentration should be 1uL/100uL of media (w/ culture and antibiotics) 

    #step8, inducer activation

    incubate(protocol, hs_mod, induceTime)


    #step 9, PBS mixture
    #stop state PBS as media, freeze the bois 
    
    estimateCountTip(tips_20, protocol, 96, pipette, desired_columns, desired_replicates*2, 0)
    stopState(pip,pipette, hs_mod, hs_plate, plate_2, desired_columns, desired_replicates, colony1_start_dest_well,colony2_start_dest_well)
    countTips(tips_20,protocol, 96, pipette)
    countTips(tips_300,protocol,96,pip)
    hsDisengage(hs_mod)

    
    
def release(hs_mod, protocol):
    protocol.home()
    hsTransferMod(hs_mod)
    protocol.pause("Change out the heater-shaker plate with plate in slot 2, and prepare next steps")    
    
def steadyState(hs_mod):
    hs_mod.set_and_wait_for_temperature(temp)
    hs_mod.close_labware_latch()
    hs_mod.set_and_wait_for_shake_speed(rpm)    
    
def hsDisengage(hs_mod):
    hs_mod.deactivate_heater()
    hs_mod.deactivate_shaker()
    hs_mod.open_labware_latch()      
    
def transfer_sample(hs_plate, plate_2, pipette,source_well,hs_mod):
    hs_mod.close_labware_latch()
    hs_mod.deactivate_shaker()
    for s in (plate_2.wells()):
        length=len(wells_used)
        up=0
        for d in (wells_used):
            if(s!=d): #don't transfer into already transfered wells
                up=up+1
        if (length==up):
            pipette.transfer(volume, hs_plate.wells(source_well), s)   
            wells_used.extend([s])
            return #kick out of transfer function when transfer is complete
            
def transfer_media(media_plate, plate_1, pip,location):
    pip.transfer(media_volume, media_plate.wells(0), plate_1.wells(location))
    
def transfer_culture(culture_plate,cul_loc, dest_plate,dest_loc, pip):
    tempVol=culture_volume
    while tempVol>1:
        while (tempVol>200):
            pip.transfer(200,culture_plate.wells(cul_loc), dest_plate.wells(dest_loc), mix_after=(2, 100))
            tempVol=tempVol-200
        pip.transfer(tempVol,culture_plate.wells(cul_loc), dest_plate.wells(dest_loc), mix_after=(2, 150))
        tempVol=0 

def hsTransfer(hs_mod):
    hs_mod.deactivate_shaker()
    
def hsTransferMod(hs_mod):
    hs_mod.close_labware_latch() 
    hs_mod.deactivate_shaker()
    hs_mod.open_labware_latch()
    
def transfer_antibiotic(source, destination, pip, location, dest_loc):
    tempVol=antibiotic_volume
    while tempVol>1:
        while (tempVol>200):
            pip.transfer(200,source.wells(location), destination.wells(dest_loc))
            tempVol=tempVol-200
        pip.transfer(tempVol,source.wells(location), destination.wells(dest_loc))
        tempVol=0

def coolBlock(temp_mod):
    temp_mod.set_temperature(celsius=4)
    temp_mod.status
    
def dual3Plate(source, source_loc, destination, dest_loc, pip, desired_columns, desired_replicates):
    #start location, +1, +2, dest_loc*8 ,+1 , +2 with dest_loc increasing for the desired columns
    column=0
    pip.pick_up_tip()
    while (column<(desired_columns+1)):
        x=0
        while(x<desired_replicates):
            pip.transfer(colony_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc),new_tip='never')
            x=x+1
        column=column+1
    pip.drop_tip()

def dual3Tube(source, source_loc, destination, dest_loc, pip, desired_columns, desired_replicates):
    column=0
    pip.pick_up_tip()
    while (column<(desired_columns+1)):
        x=0
        while(x<desired_replicates):
            pip.transfer(colony_transfer_volume, source.wells(column*desired_columns +source_loc+x), destination.wells(dest_loc),new_tip='never')
            x=x+1
        column=column+1
    pip.drop_tip()

def leastSigInduce(source,source_loc,destination,dest_loc,pip,desired_columns, desired_replicates):
    column=0
    while (column<desired_columns):
        x=0
        if(column == 1):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 3):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 5):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 7):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1           
        column=column+1
        
def midSigInduce(source,source_loc,destination,dest_loc,pip,desired_columns, desired_replicates):
    column=0
    while (column<desired_columns):
        x=0
        if(column == 3):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 4):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 6):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 7):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        column=column+1
        
def mostSigInduce(source,source_loc,destination,dest_loc,pip,desired_columns, desired_replicates):
    column=0
    while (column<desired_columns):
        x=0
        if(column == 4):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 5):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 6):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        elif(column == 7):
            while(x<desired_replicates):
                pip.transfer(state_volume, source.wells(source_loc), destination.wells(column*desired_columns +dest_loc+x))
                x=x+1
        column=column+1
        
def incubate(protocol, hs_mod, time):   
    release(hs_mod,protocol)
    steadyState(hs_mod)
    protocol.delay(minutes=time)     

def doubleDilution(hs_mod, hs_plate, media_plate_loc, tubeRack_loc, pip,temp_mod_loc, antibiotic1_loc, antibiotic2_loc, tube1_loc, tube2_loc, desired_columns, start_dest_well, final_plate_loc):
    hsTransfer(hs_mod)
    transfer_media(media_plate_loc, tubeRack_loc, pip, tube1_loc) #0
    transfer_media(media_plate_loc, tubeRack_loc, pip,tube2_loc) #1
    
    transfer_antibiotic(temp_mod_loc, tubeRack_loc, pip, antibiotic1_loc, tube2_loc) #spec_location,1
    transfer_antibiotic(temp_mod_loc, tubeRack_loc, pip, antibiotic2_loc, tube2_loc) #kan_location 1
    
    dual3Tube(hs_plate,tube1_loc,tubeRack_loc,tube1_loc,pip,desired_columns,desired_replicates) #96 to tuberack  
    transfer_culture(tubeRack_loc,tube1_loc, tubeRack_loc,tube2_loc,pip) #tuberack to tuberack
    dual3Plate(tubeRack_loc, tube2_loc, final_plate_loc, start_dest_well, pip, desired_columns,desired_replicates) #tuberack to 96
    
def singleDilution(hs_mod, hs_plate, media_plate_loc, tubeRack_loc, pip,temp_mod_loc, antibiotic1_loc, antibiotic2_loc, tube1_loc, desired_columns, start_dest_well, plate_2):
    hsTransfer(hs_mod)
    transfer_media(media_plate_loc, tubeRack_loc, pip, tube1_loc)   
    transfer_antibiotic(temp_mod_loc, tubeRack_loc, pip, antibiotic1_loc, tube1_loc) 
    transfer_antibiotic(temp_mod_loc, tubeRack_loc, pip, antibiotic2_loc, tube1_loc)
    dual3Tube(hs_plate,tube1_loc,tubeRack_loc,tube1_loc,pip,desired_columns,desired_replicates) #96 to tuberack  
    dual3Plate(tubeRack_loc, tube1_loc, plate_2, start_dest_well, pip, desired_columns,desired_replicates) #tuberack to 96

def inducerTransfer(temp_mod_loc, IPTG_loc, ATC_loc, ARA_loc , final_plate_loc, pipette, desired_columns, start_dest_well,desired_replicates):
    leastSigInduce(temp_mod_loc,IPTG_loc,final_plate_loc,start_dest_well,pipette,desired_columns,desired_replicates)
    midSigInduce(temp_mod_loc,ATC_loc,final_plate_loc,start_dest_well,pipette,desired_columns, desired_replicates)
    mostSigInduce(temp_mod_loc,ARA_loc,final_plate_loc,start_dest_well,pipette,desired_columns,desired_replicates)
    
def stopState(pip,pipette, hs_mod, hs_plate, plate_2, desired_columns, desired_replicates, dest_loc1,dest_loc2):
    hsTransfer(hs_mod)
    column=0
    pip.pick_up_tip()
    while(column<desired_columns):
        x=0
        while(x<desired_replicates):
            pip.transfer(well_media_volume, hs_plate.wells(column*desired_columns +dest_loc1+x), plate_2.wells(column*desired_columns +dest_loc1+x),new_tip='never')
            pip.transfer(well_media_volume, hs_plate.wells(column*desired_columns +dest_loc2+x), plate_2.wells(column*desired_columns +dest_loc2+x),new_tip='never')
            x=x+1
        column=column+1
    pip.drop_tip()
    column=0
    while(column<desired_columns):
        x=0
        while(x<desired_replicates):
            pipette.transfer(colony_transfer_volume, hs_plate.wells(column*desired_columns +dest_loc1+x), plate_2.wells(column*desired_columns +dest_loc1+x))
            pipette.transfer(colony_transfer_volume, hs_plate.wells(column*desired_columns +dest_loc2+x), plate_2.wells(column*desired_columns +dest_loc2+x))
            x=x+1
        column=column+1

def tipReset(protocol, pip):
    protocol.pause('Change tiprack out with a new tiprack')
    pip.reset_tipracks()

def positiveControl(temp_mod, RPU_loc, desired_columns,desired_replicates, pipette, final_plate_loc):
    x=0
    while(x<desired_replicates):
        pipette.transfer(state_volume, temp_mod.wells(RPU_loc), final_plate_loc.wells((8*(desired_columns+1))+x)) 
        x=x+1
        
def negativeControl(pip, desired_columns,desired_replicates, media_plate, final_plate_loc):
    x=0
    pip.pick_up_tip()
    while(x<(desired_replicates*2)):
        pip.transfer(colony_volume, media_plate.wells(0), final_plate_loc.wells(8*(desired_columns+2)+x), new_tip='never')
        x=x+1
    pip.drop_tip()
    
def controlTransfer(temp_mod, RPU_loc,pip, pipette,desired_columns, desired_replicates, media_plate,final_plate_loc):
    positiveControl(temp_mod, RPU_loc, desired_columns,desired_replicates, pipette, final_plate_loc)
    negativeControl(pip, desired_columns,desired_replicates, media_plate, final_plate_loc)
    
def countTips(tip_rack,protocol, max_tip_count,pip):   
    tipCount=0
    
    while(tipCount<max_tip_count): # check wells 0-95
        if tip_rack[-1].wells()[tipCount].has_tip is True: #in tipRack 0 (ie first one) check from wells 0-95 to see if it has_tip
            protocol.comment("next tip location for ")
            pipette= str(pip)
            protocol.comment(pipette)
            word=str(tipCount)
            protocol.comment(word)
            return
        tipCount=tipCount+1
    tipReset(protocol, pip)
 
def estimateCountTip(tip_rack, protocol, max_tip_count, pip, desired_columns, desired_replicates, state_true): 
    tipCount=0
    column=0
    replicates=0
    if( state_true is True):
        desired_columns=12
    while(tipCount<max_tip_count): # check wells 0-95
        if tip_rack[-1].wells()[tipCount].has_tip is True: #in tipRack 0 (ie first one) check from wells 0-95 to see if it has_tip
            return
        tipCount=tipCount+1
    while(column<desired_columns):
        while(replicates<desired_replicates):
            tipCount=tipCount+1
            print(tipCount)
            if(tipCount > max_tip_count):
                pipette=str(pip)
                protocol.comment(pipette)
                protocol.pause(" will run out of tips during next steps")
                pip.reset_tipracks()
                return
    