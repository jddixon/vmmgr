#!/usr/bin/python

# testSetup.py

import boto, os,  unittest
import boto.vpc

from vmmgr import *

class TestSetup (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testVmMgrSetup(self):
        for rNdx, region in enumerate(REGIONS):
            vpcCnx = boto.vpc.VPCConnection(region)
            print "%-9s %s" % (region, VPC_CIDRS[rNdx])
            # igw = vpcCnx.create_internet_gateway()
            print "  gateway: %s" % GATEWAY_IDS[rNdx]
            for zNdx, zone in enumerate(ZONES[rNdx]):
                print "    zone %s, cidr %s" % (zone, SUBNET_CIDRS[rNdx][zNdx])
                sub = vpcCnx.create_subnet(VPC_IDS[rNdx],
                        SUBNET_CIDRS[rNdx][zNdx],
                        availability_zone=zone)
                print "SUBNET: %z" % sub

if __name__ == '__main__':
    unittest.main()
