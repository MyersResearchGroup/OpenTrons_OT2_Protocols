volume=20

blue=0
red= 1
yellow=2
purple=3
orange=4
green=5
black=6
light_blue=7

#can use either 0-95 or 'A1'-'H12', change the destination wells to create a list of wells to transfer to
red_dest= [0,1] 
yellow_dest=['H11','H12']
orange_dest=[]
purple_dest=[] 
green_dest=[]
blue_dest=[]
black_dest=[]
wells_used=[]


from opentrons import protocol_api
metadata = {
    'protocolName': 'Pixel Art Protocol',
    'author': 'Parker',
    'description': 'adjust this code to make what you want',
    'apiLevel': '2.15' #this is the apilevel that OPT uses (this has adjusted a few times since this)
}


def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"left","well_1":"opentrons_24_aluminumblock_nest_1.5ml_snapcap","well_2":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    [pip_model, pip_mount, well_1, well_2] = get_values ( '_pip_model', '_pip_mount', 'well_1', 'well_2')

    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '1')] 
    pipette = protocol.load_instrument(pip_model, pip_mount, tip_racks=tips)
    
   
    plate_1 = protocol.load_labware(well_1,'2')
    plate_2 = protocol.load_labware(well_2,'3')
    
    transfer(plate_1,plate_2, pipette, red, red_dest)
    transfer(plate_1,plate_2, pipette, yellow, yellow_dest)
    transfer(plate_1,plate_2, pipette, purple, purple_dest)
    transfer(plate_1,plate_2, pipette, orange, orange_dest)
    transfer(plate_1,plate_2, pipette, green, green_dest)
    transfer(plate_1,plate_2, pipette, black, black_dest)
    #transfer(plate_1,plate_2, pipette, blue, blue_dest)
    blue_transfer(plate_1, plate_2, pipette)
    #add blue_transfer if you want to create a blue background and comment out the transfer function with blue
    #if you don't want a color just comment it out
    
#the function below takes all the wells within plate_2 i.e. the destination plate and cycles through to find all the wells without color in it
def blue_transfer(plate_1, plate_2, pipette): 
    pipette.pick_up_tip()
    for s in (plate_2.wells()):
        length=len(wells_used)
        up=0
        for d in (wells_used):
            if(s!=d): #if the wells aren't the same cycle iterate up up, this is so that it can compare to length and transfer color
                up=up+1
        if (length==up):
            pipette.transfer(volume, plate_1.wells(blue), s,new_tip='never')
    pipette.drop_tip()      
    
    
    
def transfer(plate_1, plate_2, pipette, source_well, dest_well):
    pipette.pick_up_tip()
    for s in dest_well: 
        pipette.transfer(volume,plate_1.wells(source_well),plate_2.wells(s),new_tip='never') 
        wells_used.extend(plate_2.wells(s)) #store well value into a list
    pipette.drop_tip()    