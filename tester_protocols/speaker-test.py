#this is not a protocol for audio files, not needed for running most protocols
def get_values(*names):
    import json
    _all_values = json.loads("""{"pip":"p20_single_gen2","mnt":"left","tips":"opentrons_96_tiprack_20ul"}""")
    return [_all_values[n] for n in names]


import subprocess
from opentrons import protocol_api

metadata = {
    'protocolName': 'OT-2 Speaker Test',
    'author': 'Parrish Payne <protocols@opentrons.com>',
    'description': 'Tests out the speaker system on the OT-2',
    'apiLevel': '2.11'
}

AUDIO_FILE_PATH = '/etc/audio/speaker-test.mp3'


def run_quiet_process(command):
    subprocess.check_output('{} &> /dev/null'.format(command), shell=True)


def test_speaker(protocol):
    print('Speaker')
    print('Next\t--> CTRL-C')
    try:
        if not protocol.is_simulating():
            run_quiet_process('mpg123 {}'.format(AUDIO_FILE_PATH))
        else:
            print('Not playing mp3, simulating')
    except KeyboardInterrupt:
        pass
        print()


def run(protocol: protocol_api.ProtocolContext):
    [pip, mnt, tips] = get_values(  # noqa: F821
      'pip', 'mnt', 'tips')

    tr2 = protocol.load_labware(tips, '1')
    pipette = protocol.load_instrument(pip, mnt, tip_racks=[tr2])
    pipette.pick_up_tip()
    pipette.drop_tip()
    test_speaker(protocol)
