#! /usr/bin/env python3
'''\
Opens selected serial port and reads two lines.
'''

import serial
#import time
import random
import string

def scan():
    '''scan for avaiable ports. return a list of tuples (num, name)'''
    available = []
    for i in range(256):
        try:
            s = serial.Serial(i)
            available.append( (i,s.portstr))
            s.close()   # explicit close 'caue of delayed GC in java
        except serial.SerialException:
            pass
    return available

def input_int_default_range(instr = 'Input value',default = 0,value_range=None):
    ''' inputs integer - return input integer value
    if not integer value input - return "default"
    if value_range defined and input value not in range - return "defalut"
    if default not in value_range (and it's defined) - raise exception'''
    input_value = input('{1} [{0}]:'.format(default,instr))
    try:
        input_value = int(input_value)
    except:
        input_value = default
    if not (value_range == None):
        if default not in value_range:
            raise ValueError('Default value not defined in range')
        if input_value not in value_range:
            input_value = default
    return input_value

if __name__ == '__main__':
    #get all serial ports
    list_of_ports = scan()
    number_of_ports = len(list_of_ports)
    print ('Found %d port(s):' % number_of_ports)
    if number_of_ports < 1:
        raise ValueError('no serial port found')

    #list ports
    i = 0
    for n,s in list_of_ports:
        print ('    port %d: (%d) %s' % (i,n,s))
        i = i+1

    #select port
    list_of_possible_choices = list(range(0,number_of_ports))
    port0_num = input_int_default_range('Select port {0}'.format(tuple(list_of_possible_choices)),list_of_possible_choices[0],list_of_possible_choices)
    print('Port: {0}'.format(list_of_ports[port0_num][1]))
    del list_of_possible_choices[list_of_possible_choices.index(port0_num)]

    #port openning (verbose)
    print('Openning serial port: %s' % list_of_ports[port0_num][1])
    with serial.Serial(list_of_ports[port0_num][1],interCharTimeout=0.2,timeout=2.0,baudrate=4800) as serial_port:
        serial_port.readline() #waste the first line
        #test the second line
        try:
            line = str(serial_port.readline().rstrip(),encoding='ascii')
            if line[0:4]=='$GPG':
                print(line)
            else:
                print('No GPS data')
        except:
            print('No valid ascii string')

    print('Finished ...')
