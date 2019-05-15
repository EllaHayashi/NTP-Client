#!/usr/bin/env python
    # Python Network Programming Cookbook, Second Edition -- Chapter - 1
    # This program is optimized for Python 2.7.12 and Python 3.5.2.
    # It may run on any other version with/without modifications.
    
import datetime    
import time
from time import mktime
from datetime import datetime
import socket
import struct
import sys
import time
    
NTP_SERVER = "0.uk.pool.ntp.org"
TIME1970 = 2208988800
    
def sntp_client(x, c):
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = '\x1b' + 47 * '\0'
    client.settimeout(3)
    t3 = time.time()

    print('t3 time is: ')
    print datetime.fromtimestamp(t3)
    print('\n')
    client.sendto( data.encode('utf-8'), ( NTP_SERVER, 123 ))
    try:
	data, address = client.recvfrom( 1024 )

        if data:
      	    t0 = time.time()

	    NTP_PF = '!12I'
	    unpacked = struct.unpack(NTP_PF, data[0:struct.calcsize(NTP_PF)])
	    t1 = unpacked[10] + float(unpacked[11]) /2**32
	    t2 = unpacked[8] + float(unpacked[9]) /2**32
	    t2 -= TIME1970
	    t1 -= TIME1970

	    print ('t2 time is: ')
	    print datetime.fromtimestamp(t2)
	    print('\nt1 time is: ')
	    print datetime.fromtimestamp(t1)


        t = struct.unpack( '!12I', data )[10]
        t -= TIME1970
        print ('\nt0 time is: ')
        print datetime.fromtimestamp(t0)

	RTT = (t2-t3) + (t0-t1)
	Drift = ((t2-t3)-(t0-t1))/2
	
	line = [str(x),str(RTT),str(Drift),str(datetime.fromtimestamp(t0)),str(datetime.fromtimestamp(t1)),str(datetime.fromtimestamp(t2)),str(datetime.fromtimestamp(t3))]
	f.write(','.join(line)+'\n')
    except socket.timeout:
	print('\ntimeout\n')
	f.write(str(x) + 'timeout\n')

if __name__ == '__main__':
    x=0
    with open("462_smtp2.csv", 'w') as f:
	f.write('number, RTT, Drift, t0, t1, t2, t3\n')
	while x<1000:
	    x+=1
	    print("\n\n\n*******\n\n\n")	
    	    sntp_client(x, f)
  	    time.sleep(10)





