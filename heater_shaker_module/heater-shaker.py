#rpm of shaker is 200-3000 rpm
#heater range 37-95 degrees celsius

from opentrons import protocol_api
metadata = {
    'protocolName': 'heater_shaker_example',
    'author': 'Parker',
    'description': 'example code',
    'apiLevel': '2.15' #this is the apilevel that OPT uses
}

def get_values(*names):
    import json
    _all_values = json.loads("""{"_pip_model":"p20_single_gen2","_pip_mount":"left","well_1":"nest_96_wellplate_200ul_flat"}""")
    return [_all_values[n] for n in names]

def run(protocol):
    [pip_model, pip_mount, well_1] = get_values ( '_pip_model', '_pip_mount', 'well_1')

    tips=[protocol.load_labware('opentrons_96_tiprack_20ul', '6')] 
    pipette = protocol.load_instrument(pip_model, pip_mount, tip_racks=tips)
    hs_mod = protocol.load_module("heaterShakerModuleV1", "3")
    hs_mod.set_and_wait_for_temperature(75)
    hs_mod.close_labware_latch()
    hs_mod.set_and_wait_for_shake_speed(500)
    protocol.delay(minutes=1)
    hs_mod.deactivate_heater()
    hs_mod.deactivate_shaker()