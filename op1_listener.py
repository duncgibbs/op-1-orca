import mido
import socket
import string

UDP_IP = "127.0.0.1"
UDP_PORT = 49160
orca_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

keys = ['F', 'f', 'G', 'g', 'A', 'a', 'B', 'C', 'c', 'D', 'd', 'E']

number_translations = {
    50: '1',
    51: '2',
    52: '3',
    21: '4',
    22: '5',
    23: '6',
    24: '7',
    25: '8',
    26: '9',
    49: '0'
}

modifier_keys = {
    6: 'tempo',
    8: 'midi_io',
    9: 'frame',
    11: 'lower_case_letters',
    12: 'upper_case_letters',
    13: 'special_characters',
    14: 'numbers'
}

modifiers = {
    'tempo': False,
    'midi_io': False,
    'frame': False,
    'lower_case_letters': False,
    'upper_case_letters': False,
    'special_characters': False,
    'numbers': False
}

lower_case_letters = list(string.ascii_lowercase)
upper_case_letters = list(string.ascii_uppercase)
special_characters = [':', '%', '!', '?', ';', '=', '$']
numbers = range(10)

currentSpecialCharacterIdx = 0

tempo = {
    'knob': 0,
    'bpm': 100
}

midi_io = {
    'input': -1,
    'input_knob': 0,
    'output': -1,
    'output_knob': 0
}

frame_knob_value = 0

knob_values = {
    1: 0,
    2: 0,
    3: 0,
    4: 0
}

position = {
    'x': 0,
    'y': 0,
    'width': 0,
    'height': 0
}

def updateX(message):
    global knob_values, position
    value = message.value
    if value == 127 and knob_values[1] == 127:
        position['x'] += 1
    elif value == 0 and knob_values[1] == 0:
        if position['x'] > 0:
            position['x'] -= 1
    else:
        if value > knob_values[1]:
            position['x'] += 1
        else:
            if position['x'] > 0:
                position['x'] -= 1
    
    knob_values[1] = value
    position['width'] = 0
    send_message_to_orca(f"select:{position['x']};{position['y']}")

def updateY(message):
    global knob_values, position
    value = message.value
    if value == 127 and knob_values[2] == 127:
        position['y'] += 1
    elif value == 0 and knob_values[2] == 0:
        if position['y'] > 0:
            position['y'] -= 1
    else:
        if value > knob_values[2]:
            position['y'] += 1
        else:
            if position['y'] > 0:
                position['y'] -= 1
    
    knob_values[2] = value
    position['height'] = 0
    send_message_to_orca(f"select:{position['x']};{position['y']}")

def updateWidth(message):
    global knob_values, position
    value = message.value
    if value == 127 and knob_values[3] == 127:
        position['width'] += 1
    elif value == 0 and knob_values[3] == 0:
        if position['width'] > 0:
            position['width'] -= 1
    else:
        if value > knob_values[3]:
            position['width'] += 1
        else:
            if position['width'] > 0:
                position['width'] -= 1
    
    knob_values[3] = value
    send_message_to_orca(f"select:{position['x']};{position['y']};{position['width']};{position['height']}")

def updateHeight(message):
    global knob_values, position
    value = message.value
    if value == 127 and knob_values[4] == 127:
        position['height'] += 1
    elif value == 0 and knob_values[4] == 0:
        if position['height'] > 0:
            position['height'] -= 1
    else:
        if value > knob_values[4]:
            position['height'] += 1
        else:
            if position['height'] > 0:
                position['height'] -= 1
    
    knob_values[4] = value
    send_message_to_orca(f"select:{position['x']};{position['y']};{position['width']};{position['height']}")

def resetPosition(message):
    global position
    if message.value == 127:
        position['x'] = 0
        position['y'] = 0
        position['width'] = 0
        position['height'] = 0
        send_message_to_orca(f"select:{position['x']};{position['y']}")

def selectAll(message):
    global position
    if message.value == 127:
        position['x'] = 0
        position['y'] = 0
        position['width'] = 1000000
        position['height'] = 1000000
        send_message_to_orca(f"select:{position['x']};{position['y']};{position['width']};{position['height']}")

def copy(message):
    if message.value == 127:
        send_message_to_orca("copy")

def paste(message):
    if message.value == 127:
        send_message_to_orca("paste")

def erase(message):
    if message.value == 127:
        send_message_to_orca("erase")

def run(message):
    if message.value == 127:
        send_message_to_orca("run")

def play(message):
    if message.value == 127:
        send_message_to_orca("play")

def stop(message):
    if message.value == 127:
        send_message_to_orca("stop")

def resetFrame(message):
    if message.value == 127:
        send_message_to_orca("frame:0")

def comment(message):
    if message.value == 127:
        send_message_to_orca("write:#")

def cycleSpecialCharacters(message):
    global currentSpecialCharacterIdx
    if message.value == 127:
        send_message_to_orca(f"write:{special_characters[currentSpecialCharacterIdx % 7]}")
        currentSpecialCharacterIdx += 1

def send_message_to_orca(message_bytes):
    global UDP_IP, UDP_PORT, orca_socket
    #print(message_bytes)
    orca_socket.sendto(message_bytes.encode("utf-8"), (UDP_IP, UDP_PORT))

def handle_modified_note(midi_message):
    global modifiers, lower_case_letters, upper_case_letters, numbers
    if modifiers['lower_case_letters']:
        letter = lower_case_letters[(((midi_message.note - 5) % 24) + 2)]
        send_message_to_orca(f"write:{letter}")
    elif modifiers['upper_case_letters']:
        letter = upper_case_letters[(((midi_message.note - 5) % 24) + 2)]
        send_message_to_orca(f"write:{letter}")
    elif modifiers['special_characters']:
        character = special_characters[((midi_message.note - 5) % 7)]
        send_message_to_orca(f"write:{character}")
    elif modifiers['numbers']:
        number = numbers[((midi_message.note - 5) % 10)]
        send_message_to_orca(f"write:{number}")

def handle_tempo_modifier(midi_message):
    global tempo
    value = midi_message.value
    if value == 127 and tempo['knob'] == 127:
        tempo['bpm'] += 1
    elif value == 0 and tempo['knob'] == 0:
        if tempo['bpm'] > 0:
            tempo['bpm'] -= 1
    else:
        if value > tempo['knob']:
            tempo['bpm'] += 1
        else:
            if tempo['bpm'] > 0:
                tempo['bpm'] -= 1
    
    tempo['knob'] = value
    if tempo['bpm'] > 59 and tempo['bpm'] < 301:
        send_message_to_orca(f"bpm:{tempo['bpm']}")
    else:
        if tempo['bpm'] == 59:
            tempo['bpm'] = 60
        elif tempo['bpm'] == 301:
            tempo['bpm'] = 300

def handle_special_character_modifier(midi_message):
    if midi_message.control == 1:
            character = special_characters[midi_message.value % 7]
            send_message_to_orca(f"write:{character}")

def handle_midi_io_modifier(midi_message):
    global midi_io
    if midi_message.control == 1:
        io = "input"
    elif midi_message.control == 2:
        io = "output"

    value = midi_message.value
    if value == 127 and midi_io[f"{io}_knob"] == 127:
        midi_io[io] += 1
    elif value == 0 and midi_io[f"{io}_knob"] == 0:
        if midi_io[io] > -1:
            midi_io[io] -= 1
    else:
        if value > midi_io[f"{io}_knob"]:
            midi_io[io] += 1
        else:
            if midi_io[io] > -1:
                midi_io[io] -= 1
        
    midi_io[f"{io}_knob"] = value
    send_message_to_orca(f"midi:{midi_io['output']};{midi_io['input']}")

def handle_frame_modifier(midi_message):
    global frame_knob_value
    value = midi_message.value
    frame_change = ""
    if value == 127 and frame_knob_value == 127:
        frame_change = "skip"
    elif value == 0 and frame_knob_value == 0:
        frame_change = "rewind"
    else:
        if value > frame_knob_value:
            frame_change = "skip"
        else:
            frame_change = "rewind"
    
    frame_knob_value = value
    send_message_to_orca(f"{frame_change}:1")

def handle_modified_control_change(midi_message):
    global modifiers, lower_case_letters, upper_case_letters, numbers
    if modifiers['tempo']:
        handle_tempo_modifier(midi_message)
    elif modifiers['special_characters']:
        handle_special_character_modifier(midi_message)
    elif modifiers['midi_io']:
        handle_midi_io_modifier(midi_message)
    elif modifiers['frame']:
        handle_frame_modifier(midi_message)
    elif modifiers['lower_case_letters']:
        if midi_message.control == 1:
            letter = lower_case_letters[midi_message.value % 26]
            send_message_to_orca(f"write:{letter}")
    elif modifiers['upper_case_letters']:
        if midi_message.control == 1:
            letter = upper_case_letters[midi_message.value % 26]
            send_message_to_orca(f"write:{letter}")
    elif modifiers['numbers']:
        if midi_message.control == 1:
            number = numbers[midi_message.value % 10]
            send_message_to_orca(f"write:{number}")

def handle_note_on(midi_message):
    if any(v for v in modifiers.values()):
        handle_modified_note(midi_message)
    else:
        note = keys[(midi_message.note - 5) % 12]
        send_message_to_orca(f"write:{note}")

def handle_control_change(midi_message):
    if midi_message.control in modifier_keys:
        modifier = modifier_keys[midi_message.control]
        if midi_message.value == 127:
            modifiers[modifier] = True
        else:
            modifiers[modifier] = False
    elif midi_message.control in number_translations:
        if midi_message.value == 127:
            send_message_to_orca(f"write:{number_translations[midi_message.control]}")
    else:
        if any(v for v in modifiers.values()):
            handle_modified_control_change(midi_message)
        else: 
            handler = control_behaviors.get(midi_message.control)
            if (callable(handler)):
                handler(midi_message)
            else:
                print(f"No behavior defined for: {midi_message}")

key_behaviors = {
    'note_on': handle_note_on,
    'control_change': handle_control_change,
    'note_off': (lambda x: x)
}

control_behaviors = {
    1: updateX,
    2: updateY,
    3: updateWidth,
    4: updateHeight,
    5: comment,
    7: cycleSpecialCharacters,
    15: copy,
    16: paste,
    17: erase,
    38: run,
    39: play,
    40: stop,
    48: resetFrame,
    64: resetPosition,
    66: selectAll
}

send_message_to_orca("bpm:100")
send_message_to_orca("select:0;0")

with mido.open_input('OP-1 Midi Device') as inport:
    for message in inport:
        handler = key_behaviors.get(message.type)
        if (callable(handler)):
            handler(message)
        else:
            print(f"No behavior defined for: {message}")