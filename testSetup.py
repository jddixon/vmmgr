#!/usr/bin/python

# testSetup.py

import boto, os,  unittest
import boto.ec2, boto.vpc

from vmmgr import *

class TestSetup (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testVmMgrSetup(self):
        for rNdx, region in enumerate(REGIONS):
            regionInfo = boto.ec2.get_region(region)
            self.assertTrue( regionInfo is not None)

            # This was yielding a very misleading AuthFailure further
            # down the line because a string like 'eu-west-1' was supplied
            # instead of the corresponding EC2RegionInfo object
            vpcCnx = boto.vpc.VPCConnection(region=regionInfo)
            self.assertTrue(vpcCnx is not None)

            print "%-9s %s" % (regionInfo, VPC_CIDRS[rNdx])
            
            print "  gateway: %s" % IGATEWAY_IDS[rNdx]
            igws = vpcCnx.get_all_internet_gateways()   # AuthFailure !
            self.assertEqual(len(igws), 1)
            self.assertEqual(str(igws[0]), 'InternetGateway:' +IGATEWAY_IDS[rNdx])

            for zNdx, zone in enumerate(ZONES[rNdx]):
                print "    zone %s, cidr %s" % (zone, SUBNET_CIDRS[rNdx][zNdx])
                #sub = vpcCnx.create_subnet(VPC_IDS[rNdx],
                #        SUBNET_CIDRS[rNdx][zNdx],
                #        availability_zone=zone)
                #print "SUBNET: %z" % sub

if __name__ == '__main__':
    unittest.main()
