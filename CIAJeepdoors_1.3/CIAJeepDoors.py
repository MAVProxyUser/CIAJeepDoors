#!/usr/bin/python3
import struct
import sys
import base64
import time
import serial

sys.path.insert(0, './')
from comm_serialtalk import (
  do_send_request, do_receive_reply, open_usb
)
from comm_mkdupc import *

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
    privacy = bin(int.from_bytes(payload[2:], byteorder='little'))[2:].zfill(8)
    return privacy

def set_purpose(po, purpose):
    fc_monitor_set_purpose(po, purpose)
    pkt, payload = send_duml_receive_reply(po)

def get_purpose(po):
    fc_monitor_get_purpose(po)
    pkt, payload = send_duml_receive_reply(po)
    if len(payload) > 2:
        return payload[3:].decode('utf-8')
    else:
        return ''

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

def print_droneid_state(po):
    state = get_privacy(po)
    print('=+=+=+=+=+=+=+=+=+=+=+=+')
    if state != '00000000':
        print('--> DroneID is enabled')
    else:
        print('--> DroneID is disabled')
    print('=+=+=+=+=+=+=+=+=+=+=+=+')

def main():
    print("CIA Jeep Doors")
    print("DJI DroneID adjustment tool v1.3")
    print('======================================')
    print("this software is based on the work of the DJI OG's")
    print("it is free software and should never be sold")
    print('======================================')
    print("greetings from Bin4ry")

    global ser
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)

    subparser = parser.add_mutually_exclusive_group(required=True)

    subparser.add_argument('--port', type=str,
            help='the serial port to write to and read from')

    subparser.add_argument('--bulk', action='store_true',
            help='use usb bulk instead of serial connection')

    parser.add_argument('-p', '--privacy', type=str, default='',
                help='provide privacy flags\n'
                '.......x  Show/Hide serial number\n'
                '......x.  Show/Hide state like position, roll, yaw, imu data, ...\n'
                '.....x..  Show/Hide ReturnToHome position\n'
                '....x...  Show/Hide droneID\n'
                '...x....  Show/Hide flight purpose\n'
                '..x.....  Show/Hide UUID\n'
                '.x......  Show/Hide Pilot Position\n'
                'x.......  Show/Hide Unknown\n'
                '\n'
                '00000000 Will disable all broadcasts\n'
                '11111111 Will enable all broadcasts\n'
                '\n')

    parser.add_argument('-d', '--droneid', type=str, default='',
                help='provide the droneID')
    parser.add_argument('-f', '--flightpurpose', type=str, default='',
                help='provide the flight purpose')
    parser.add_argument('--disable', action='store_true',
            help='disable droneid')
    parser.add_argument('--enable', action='store_true',
            help='enable droneid')

    po = parser.parse_args()
    po.seq_num = 0
    po.timeout = 2000
    po.verbose = 0
    po.baudrate = 9600
    po.loose_response = False

    if not po.bulk:
        # Open serial port
        ser = serial.Serial(po.port, baudrate=po.baudrate, timeout=0)
    else:
        ser = open_usb(po)


    print_droneid_state(po)

    if po.disable:
        po.privacy = '00000000'
        print('--> Disabling DroneID')

    if po.enable:
        po.privacy = '11111111'
        print('--> Enabling DroneID')

    if po.privacy:
        set_privacy(po, '01000000') # M300 workaround
        time.sleep(0.1)
        set_privacy(po, po.privacy)
        time.sleep(0.1)
        print('--> Done')
        print_droneid_state(po)

    if po.droneid:
        set_droneid(po, po.droneid)
        time.sleep(0.1)
        print('New DroneID name:', get_droneid(po))

    if po.flightpurpose:
        set_purpose(po, po.flightpurpose)
        time.sleep(0.1)
        print('New Flight Purpose:', get_purpose(po))

    print('')
    print('++++++++++++++++++++++++++++++++++++++')
    print('Please only use Android DJI Fly 1.5.10, the later versions or iOS version will reset the privacy bits.')
    print('++++++++++++++++++++++++++++++++++++++')
    set.close()

if __name__ == "__main__":
    main()
