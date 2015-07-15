#!/usr/bin/python
import hid
import time
import sys
import getopt

# Global Variables #
VENDOR_ID = 0x0801
PRODUCT_ID = 0x0003
DATA_SIZE = 338
enc_formats = ('ISO/ABA', 'AAMVA', 'CADL', 'Blank', 'Other', 'Undetermined', 'None')

vervose = False
output_file = False
last_status = ''

def process_data(data,last_status,vervose):
    status = '0'
    if(data[len(data)-1]):
        if vervose:
            print "Card In"
        if bool(not data[0]) and bool(not data[6]):
            card_data = ''.join(map(chr, data[7:116]))
            if(last_status != card_data):
                status = card_data
        else:
            if(last_status != '1'):
                status = '1'
        if vervose:
            print "Card Encoding Type: %s" % enc_formats[data[6]]
            print "Track 1 Decode Status: %r" % bool(not data[0])
            print "Track 1 Data: %s" % ''.join(map(chr, data[7:116]))
        
    elif(last_status != '0'):
        if vervose:
            print "Card Out"
        status = '0'
        
    return status



def read_hid_device():
    global last_status
    global vervose
    while 1:
        if output_file:
            f = open(output_file,'w')
            f.write('0')
            f.close()
        print 0
        try:
            h = hid.device(VENDOR_ID, PRODUCT_ID)
            h.open(VENDOR_ID, PRODUCT_ID)
            print "Device opened..."

            ### non-blocking mode
            #h.set_nonblocking(1)

            while 1:
                d = h.read(338)
                if d:
                    last_status = process_data(d,last_status,vervose)
                    if not vervose: 
                        print last_status
                    if output_file:    
                        f = open(output_file,'w')
                        f.write(last_status)
                        f.close()
                time.sleep(0.05)

            h.close()

        except IOError, ex:
            print "Searching for device..."
            time.sleep(5)    


def getargs(argv):
    try:
        opts, args = getopt.getopt(argv,"h:vo:",["ofile="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-v", "--vervose"):
            global vervose
            vervose = True
        elif opt in ("-o", "--ofile"):
            global output_file
            output_file = arg

def usage():
    print """
NAME
     magtek-reader.py -- HID Magtek Card Reader

SYNOPSIS

     magte-reader.py [-o output.txt] [-v] [-h]

DESCRIPTION
     
     This program is a simple example to use the Magtek 99875205 Rev 13 card
     reader (doc: https://www.magtek.com/docs/99875205.pdf), but may be used
     by other HID compatible hardware.

     Without -v (vervose) option, the outout shows a 0 if the device has not
     detected any input, 1 if there was any error reading the card and the
     card ID (on track 1) if the card has been read succesfully.

     The options are as follows:

     -o,--ofile output
     
             Sends the output to a  file. Sets a 0 if
             the device has not detected any input, 1 if there was a reading
             error and the card ID if the card has been read succesfully. 

     -v,--vervose      
             Produce a verbose output of all tracks and indicates whether the
             card was inserted or removed.

     -h,--help
             Displays this help message.

GPL                               Jun 2015                                   GPL
"""



if __name__ == "__main__":
    
    getargs(sys.argv[1:])

    read_hid_device()
