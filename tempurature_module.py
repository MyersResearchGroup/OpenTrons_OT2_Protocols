 #tempurature range is 4-95 degrees C
 #we use a GEN2 tempurature module
 
    #tolerance on read about 5 degrees for heating (at least with IR thermometer)
    # can hold steady at a tempurature really well though would need to test more at differing tempurature
    #idling tempurature 55 C can hold within .5 C of tempurature since readout is in integers
    

from opentrons import protocol_api

metadata = {
    'protocolName': 'Temp_module_test_cooling',
    'author': 'parke',
    'description':'protocol to run temp_module',
    'apiLevel':'2.10'
    }
    
def run(protocol: protocol_api.ProtocolContext):
    temp_mod = protocol.load_module('temperature module gen2', '4')
    plate = temp_mod.load_labware('corning_96_wellplate_360ul_flat')
   
    temp_mod.set_temperature(celsius=4)
   
    temp_mod.status  # 'holding at target'
    temp_mod.deactivate()
    temp_mod.status  # 'idle'
        