#!/usr/bin/env python3

# testSetup.py

import os
import sys
import unittest

# SHOULD DROP:
import boto
import boto.ec2
import boto.vpc
# END SHOULD

import boto3

from vmmgr import *


class TestSetup (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # boto3 version drops this
    def old_testVmMgrSetup(self):
        for rNdx, region in enumerate(REGIONS):
            regionInfo = boto.ec2.get_region(region)
            self.assertTrue(regionInfo is not None)

            vpcCnx = boto.vpc.VPCConnection(region=regionInfo)
            self.assertTrue(vpcCnx is not None)

            print("%-9s %s" % (regionInfo, VPC_CIDRS[rNdx]))

            print("  gateway: %s" % IGATEWAY_IDS[rNdx])

            # "Resourcewarning: unclosed <ssl.SSLSocket ... ,443)>
            #
            igws = vpcCnx.get_all_internet_gateways()
            self.assertEqual(len(igws), 1)
            self.assertEqual(str(igws[0]),
                             'InternetGateway:' + IGATEWAY_IDS[rNdx])

            for zNdx, zone in enumerate(ZONES[rNdx]):
                print(
                    "    zone %s, cidr %s" %
                    (zone, SUBNET_CIDRS[rNdx][zNdx]))
                # sub = vpcCnx.create_subnet(VPC_IDS[rNdx],
                #        SUBNET_CIDRS[rNdx][zNdx],
                #        availability_zone=zone)
                # print "SUBNET: %z" % sub

            # HACK, no apparent effect
            vpcCnx.close()
            # END HACK

    def testVmMgrSetup3(self):

        # ResourceWarning warning messages like
        #     "Resourcewarning: unclosed <ssl.SSLSocket ... ,443)>
        # are a known problem; there appears to be no way to easily
        # get rid of them.  Due to Python3/urllib3 connection pooling,
        # which is a Good Thing.

        for rNdx, rName in enumerate(REGIONS):

            # DEBUG
            print(("\n%s" % rName.upper()))
            # END
            # regionInfo = boto.ec2.get_region(rName)
            # self.assertTrue(regionInfo is not None)

            ec2 = boto3.resource('ec2', region_name=rName)

            # DEBUG
            #print("regionInfo: %s" % regionInfo)
            #print("  cnx:      %s" % regionInfo.connection)
            #print("  endpoint: %s" % regionInfo.endpoint)
            # END

            vpc = ec2.Vpc(VPC_IDS[rNdx])    # gets a ResourceWarning
            self.assertTrue(vpc is not None)
            self.assertEqual(vpc.cidr_block, VPC_CIDRS[rNdx])

            # alternative approach ----------------------------------

            # CLIENT --------------------------------------
            client = boto3.client('ec2', region_name=rName)

            # GATEWAYS ------------------------------------
            desc = client.describe_internet_gateways()
            igws = desc['InternetGateways']
            self.assertEqual(len(igws), 1)
            igw = igws[0]
            # DEBUG
            print(("IGW: %s" % igws[0]['InternetGatewayId']))
            sys.stdout.flush()
            # END
            id = igw['InternetGatewayId']
            self.assertEqual(id, IGATEWAY_IDS[rNdx])

            # AVAILABILITY ZONES --------------------------
            # for zNdx, zone in enumerate(ZONES[rNdx]):
            #    print("    zone %s, cidr %s" % (zone, SUBNET_CIDRS[rNdx][zNdx]))
            # SUBNETS -----------------------
            #    #sub = vpcCnx.create_subnet(VPC_IDS[rNdx],
            #    #        SUBNET_CIDRS[rNdx][zNdx],
            #    #        availability_zone=zone)
            #    #print "SUBNET: %z" % sub

            # INSTANCES ---------------------

            # VOLUMES -----------------------

if __name__ == '__main__':
    unittest.main()
