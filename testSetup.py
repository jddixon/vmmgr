#!/usr/bin/python3

# testSetup.py

import os,  unittest

# SHOULD DROP:
import boto
import boto.ec2, boto.vpc
# END SHOULD

import boto3
import boto3.ec2

from vmmgr import *

class TestSetup (unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    def testVmMgrSetup(self):
        for rNdx, region in enumerate(REGIONS):
            regionInfo = boto.ec2.get_region(region)
            self.assertTrue(regionInfo is not None)

            vpcCnx = boto.vpc.VPCConnection(region=regionInfo)
            self.assertTrue(vpcCnx is not None)

            print("%-9s %s" % (regionInfo, VPC_CIDRS[rNdx]))
            
            print("  gateway: %s" % IGATEWAY_IDS[rNdx])
            
            # "Resourcewarning: unclosed <ssl.SSLSocket ... raddr=(178.236.6.52',443)>
            # 
            igws = vpcCnx.get_all_internet_gateways()   
            self.assertEqual(len(igws), 1)
            self.assertEqual(str(igws[0]), 
                                'InternetGateway:' +IGATEWAY_IDS[rNdx])

            for zNdx, zone in enumerate(ZONES[rNdx]):
                print("    zone %s, cidr %s" % (zone, SUBNET_CIDRS[rNdx][zNdx]))
                #sub = vpcCnx.create_subnet(VPC_IDS[rNdx],
                #        SUBNET_CIDRS[rNdx][zNdx],
                #        availability_zone=zone)
                #print "SUBNET: %z" % sub
            
            # HACK, no apparent effect
            vpcCnx.close()      
            # END HACK

if __name__ == '__main__':
    unittest.main()
