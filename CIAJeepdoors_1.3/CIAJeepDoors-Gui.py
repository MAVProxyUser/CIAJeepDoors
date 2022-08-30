#!/usr/bin/python3
import struct
import sys
import base64
import time
import serial
import PySimpleGUI as sg
import serial.tools.list_ports
import re
import binascii

sys.path.insert(0, './')
from comm_serialtalk import (
  do_send_request, do_receive_reply, open_usb
)
from comm_mkdupc import *

class ParamObject():
    def __init__(self):
        self.seq_num = 0
        self.timeout = 2000
        self.verbose = 0
        self.baudrate = 9600
        self.loose_response = False
        self.sender_type = COMM_DEV_TYPE(10)
        self.sender_index = 1
        self.receiver_type = COMM_DEV_TYPE(8)
        self.receiver_index = 1

        self.pack_type = parse_packet_type('Request')
        self.ack_type = parse_ack_type('ACK_AFTER_EXEC')
        self.encrypt_type = parse_encrypt_type('NO_ENC')

        self.cmd_set = parse_cmd_set('GENERAL')
        self.cmd_id = 1
        self.payload = bytes('', 'utf-8')
        self.port = None
        self.bulk = None

def serial_ports():
    values = serial.tools.list_ports.comports()
    if values:
        return values
    else:
        return ["No Ports found"]

def get_port_num(text):
    values = serial.tools.list_ports.comports()
    for port in values:
        if text == port:
            return port.device

def send_duml_receive_reply(po):
    global ser
    pktrpl = None

    pktreq = do_send_request(po, ser, po)

    pktrpl = do_receive_reply(po, ser, pktreq, seqnum_check=(not po.loose_response))

    if pktrpl is not None:
        if (po.verbose > 0):
            print("Received response packet:")
            print(' '.join('{:02x}'.format(x) for x in pktrpl))
        return pktrpl, pktrpl[11:-2]
    else:
        print("No response received.")
        return None, None

def get_device_version(po):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(8)
    po.receiver_index = 1
    po.cmd_id = 1
    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')
    po.cmd_set = parse_cmd_set('GENERAL')
    po.seq_num += 1
    po.payload = bytes('', 'utf-8')

def get_device_version_fc(po):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 6
    po.cmd_id = 1
    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')
    po.cmd_set = parse_cmd_set('GENERAL')
    po.seq_num += 1
    po.payload = bytes('', 'utf-8')

def fc_monitor_set_purpose(po, purpose):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 6

    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')

    po.cmd_set = parse_cmd_set('FLYCONTROLLER')
    po.cmd_id = 218
    po.seq_num += 1
    po.payload = bytes.fromhex('01') + bytes([len(purpose)]) + purpose.encode('utf-8')

def fc_monitor_get_purpose(po):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 6

    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')

    po.cmd_set = parse_cmd_set('FLYCONTROLLER')
    po.cmd_id = 218
    po.seq_num += 1
    po.payload = bytes.fromhex('02')

def fc_monitor_set_droneid(po, droneid):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 6

    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')

    po.cmd_set = parse_cmd_set('FLYCONTROLLER')
    po.cmd_id = 218
    po.seq_num += 1
    po.payload = bytes.fromhex('03') + bytes([len(droneid)]) + droneid.encode('utf-8')

def fc_monitor_get_droneid(po):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 6

    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')

    po.cmd_set = parse_cmd_set('FLYCONTROLLER')
    po.cmd_id = 218
    po.seq_num += 1
    po.payload = bytes.fromhex('04')

def fc_monitor_set_privacy(po, privacy):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 6

    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')

    po.cmd_set = parse_cmd_set('FLYCONTROLLER')
    po.cmd_id = 218
    po.seq_num += 1

    po.payload = bytes.fromhex('05') + privacy

def fc_monitor_get_privacy(po):
    po.sender_type = COMM_DEV_TYPE(10)
    po.sender_index = 1
    po.receiver_type = COMM_DEV_TYPE(3)
    po.receiver_index = 0

    po.pack_type = parse_packet_type('Request')
    po.ack_type = parse_ack_type('ACK_AFTER_EXEC')
    po.encrypt_type = parse_encrypt_type('NO_ENC')

    po.cmd_set = parse_cmd_set('FLYCONTROLLER')
    po.cmd_id = 218
    po.seq_num += 1
    po.payload = bytes.fromhex('06')

def set_privacy(po, flags):
    priv = bytes([int(flags, 2)]) + bytes(3)
    fc_monitor_set_privacy(po, priv)
    pkt, payload = send_duml_receive_reply(po)

def get_privacy(po):
    fc_monitor_get_privacy(po)
    pkt, payload = send_duml_receive_reply(po)
    if payload is not None:
        privacy = bin(int.from_bytes(payload[2:], byteorder='little'))[2:].zfill(8)
        return privacy
    else:
        return None

def set_purpose(po, purpose):
    fc_monitor_set_purpose(po, purpose)
    pkt, payload = send_duml_receive_reply(po)

def get_purpose(po):
    fc_monitor_get_purpose(po)
    pkt, payload = send_duml_receive_reply(po)
    if len(payload) > 2:
        return payload[3:].decode('utf-8')
    else:
        return None

def set_droneid(po, droneid):
    fc_monitor_set_droneid(po, droneid)
    pkt, payload = send_duml_receive_reply(po)

def get_droneid(po):
    fc_monitor_get_droneid(po)
    pkt, payload = send_duml_receive_reply(po)
    if len(payload) > 2:
        return payload[3:].decode('utf-8')
    else:
        return ''

def get_droneid_state(po):
    state = get_privacy(po)
    if state != '00000000':
        return state, 'DroneID is enabled'
    else:
        return state, 'DroneID is disabled'

def replace_non_ascii(text):
    repl = re.sub(r'[^\w\s.]+', '', text)
    return repl


def get_device(po):
    get_device_version(po)
    pkt, payload = send_duml_receive_reply(po)
    if payload:
        return replace_non_ascii(payload.decode('utf-8', errors="replace"))
    else:
        return None

def get_fc_version(po):
    get_device_version_fc(po)
    pkt, payload = send_duml_receive_reply(po)
    if payload:
        deviceSerial = payload[2:16].decode(encoding='utf-8', errors='ignore')
        tempval =  binascii.hexlify(payload[22:26][::-1])
        one = str(int(tempval[0:2], 16)).zfill(2)
        two = str(int(tempval[2:4], 16)).zfill(2)
        three = str(int(tempval[4:6], 16)).zfill(2)
        four = str(int(tempval[6:8], 16)).zfill(2)
        fcVersion = one + "." + two + "." + three + "." + four
        return deviceSerial, fcVersion
    else:
        return None

def switchElementState(window, state):
    window.Element('-disableDID-').update(disabled = state)
    window.Element('-enableDID-').update(disabled = state)
    window.Element('-readCurrentValue-').update(disabled = state)

def main():
    # Define the window's contents
    global ser
    ser = None
    po = ParamObject()

    layout = [[sg.Text("CIA Jeep Doors")],
             [sg.Text("DJI DroneID adjustment tool v1.3 - Gui")],
             [sg.Text('======================================')],
             [sg.Text("this software is based on the work of the DJI OG's")],
             [sg.Text("it is free software and should never be sold")],
             [sg.Text('======================================')],
             [sg.Text("greetings from Bin4ry")],
             [sg.Text("")],
             [sg.Text("Select Mode:")],
             [sg.Radio('Bulk',1, enable_events=True, key='bulk', default = True),sg.Radio('Com-Port', 1, enable_events=True, key='com')],
             [sg.Combo(values=serial_ports(), enable_events=True, key='-selectedCOM-', size=(40,10), visible = True, disabled = True)],
             [sg.Button('Refresh COM-Port list', key='-refreshCOM-', visible = True, disabled=True)],
             [sg.Button('Connect drone', key='-connect-', visible = True)],
             [sg.Text("Connected drone: ",key='-droneText-', visible=True),sg.Text("", size=(40,1), key='-Drone-', visible=True)],
             [sg.Text("Drone Serial: ",key='-droneSerialText-', visible=True),sg.Text("", size=(40,1), key='-DroneSerial-', visible=True)],
             [sg.Text("Drone FC-Version: ",key='-droneFcVersionText-', visible=True),sg.Text("", size=(40,1), key='-FcVersion-', visible=True)],
             [sg.Text("Current State: ", key='-currentStateText-', visible=True),sg.Text("", size=(40,1), key='-DroneIDState-', visible=True)],
             [sg.Text("Log: "),sg.Text("", size=(40,1), key='-LOG-')],
             [sg.Button('Send Disable Command', key='-disableDID-', visible=True,disabled=True),sg.Button('Send Enable Command', key='-enableDID-', visible=True, disabled=True)],
             [sg.Button('Read current value from drone', key='-readCurrentValue-', disabled = True), sg.Button('Quit')]]

    # Create the window
    window = sg.Window('CIA Jeep Doors v1.3 - Gui', layout)
    connected = False
    serialmode = False
    bulkmode = True
    warning_text = """Please keep in mind that on new drone firmware versions the setting will not work anymore.\n
If your privacy bits are still showing "DroneID enabled" after running the disable command, then your drone/firmware combination is simply not supported!\n
Also iOS versions of DJI FLY will reset the privacy bits to "DroneID enabled" once you connect DJI Fly to your drone.\n
Android DJI Fly versions up to 1.5.10 should work, also DJI Go4 up to 4.3.48"""

    while True:
        event, values = window.read()
        if event == '-connect-':
            #CHECK FOR COM
            try:
                if serialmode:
                    combo = values['-selectedCOM-']
                    port = get_port_num(combo)
                    if port is not None:
                        ser = serial.Serial(port, baudrate=po.baudrate, timeout=0)
                else:
                    bulkret = open_usb(po)
                    if bulkret is None:
                        window['-LOG-'].update('No device connected or device did not answer!')
                    ser = bulkret

                if (serialmode and ser) or (bulkmode and bulkret):
                    ret = get_device(po)
                    if ret:
                        connected = True
                        deviceSerial, fcVersion = get_fc_version(po)
                        state, text = get_droneid_state(po)

                        try:
                            switchElementState(window, False)
                            window['-Drone-'].update(ret)
                            window['-DroneIDState-'].update(text + ': ' + state)
                            window['-DroneSerial-'].update(deviceSerial)
                            window['-FcVersion-'].update(fcVersion)
                            window['-LOG-'].update("Read current state from drone")
                        except Exception as e:
                            print(e)


                    else:
                        window['-LOG-'].update('No device connected or device did not answer!')
                        connected = False
                        switchElementState(window, True)

            except Exception as e:
                print(e)
                window['-LOG-'].update('No device connected or device did not answer!')
                connected = False
                switchElementState(window, True)

        if event == '-refreshCOM-':
            window.Element('-selectedCOM-').Update(values=serial_ports())

        if event == 'com':
            window['-LOG-'].update("Selected COM Mode")
            serialmode = True
            bulkmode = False
            connected = False
            window.Element('-selectedCOM-').update(disabled = False)
            window.Element('-refreshCOM-').update(disabled = False)
            switchElementState(window, True)

        if event == 'bulk':
            window['-LOG-'].update("Selected BULK mode")
            serialmode = False
            bulkmode = True
            connected = False
            window.Element('-selectedCOM-').update(disabled = True)
            window.Element('-refreshCOM-').update(disabled = True)
            switchElementState(window, True)

        if event == sg.WINDOW_CLOSED or event == 'Quit':
            break

        if event == 'Read current value from drone':
            if ser is None:
                window['-LOG-'].update("You have to select a COM-Port or Bulk mode first")
            else:
                state, text = get_droneid_state(po)
                window['-DroneIDState-'].update(text + ': ' + state)
                window['-LOG-'].update("Read current state from drone")

        if event == '-disableDID-':
            set_privacy(po, '01000000') # M300 workaround
            time.sleep(0.1)
            set_privacy(po, '00000000')
            time.sleep(0.1)
            state, text = get_droneid_state(po)
            window['-DroneIDState-'].update(text + ': ' + state)
            window['-LOG-'].update("Command was send to drone!")
            sg.Popup(warning_text)


        if event == '-enableDID-':
            set_privacy(po, '01000000') # M300 workaround
            time.sleep(0.1)
            set_privacy(po, '11111111')
            time.sleep(0.1)
            state, text = get_droneid_state(po)
            window['-DroneIDState-'].update(text + ': ' + state)
            window['-LOG-'].update("Command was send to drone!")

    # Finish up by removing from the screen
    window.close()

if __name__ == "__main__":
    main()
