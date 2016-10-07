#!/usr/bin/env python3
# testSetup.py

""" Test the vm_mgr_setup() function. """

import sys
import unittest

import boto3

from vmmgr import IGATEWAY_IDS, REGIONS, VPC_IDS, VPC_CIDRS


class TestSetup(unittest.TestCase):
    """ Test the vm_mgr_setup() function. """

    def setUp(self):
        pass

    def tearDown(self):
        pass

#   # boto3 version drops this
#   def old_test_vm_mgr_setup(self):
#       """ Python 2.7 version of the test code. """

#       for r_ndx, region in enumerate(REGIONS):
#           region_info = boto.ec2.get_region(region)
#           self.assertTrue(region_info is not None)

#           vpc_cnx = boto.vpc.VPCConnection(region=region_info)
#           self.assertTrue(vpc_cnx is not None)

#           print("%-9s %s" % (region_info, VPC_CIDRS[r_ndx]))

#           print("  gateway: %s" % IGATEWAY_IDS[r_ndx])

#           # "Resourcewarning: unclosed <ssl.SSLSocket ... ,443)>
#           #
#           igws = vpc_cnx.get_all_internet_gateways()
#           self.assertEqual(len(igws), 1)
#           self.assertEqual(str(igws[0]),
#                            'InternetGateway:' + IGATEWAY_IDS[r_ndx])

#           for z_ndx, zone in enumerate(ZONES[r_ndx]):
#               print(
#                   "    zone %s, cidr %s" %
#                   (zone, SUBNET_CIDRS[r_ndx][z_ndx]))
#               # sub = vpc_cnx.create_subnet(VPC_IDS[r_ndx],
#               #        SUBNET_CIDRS[r_ndx][z_ndx],
#               #        availability_zone=zone)
#               # print "SUBNET: %z" % sub

#           # HACK, no apparent effect
#           vpc_cnx.close()
#           # END HACK

    def test_vm_mgr_setup3(self):
        """ Python 3 version of the test code. """

        # ResourceWarning warning messages like
        #     "Resourcewarning: unclosed <ssl.SSLSocket ... ,443)>
        # are a known problem; there appears to be no way to easily
        # get rid of them.  Due to Python3/urllib3 connection pooling,
        # which is a Good Thing.

        for r_ndx, r_name in enumerate(REGIONS):

            # DEBUG
            print(("\n%s" % r_name.upper()))
            # END
            # region_info = boto.ec2.get_region(r_name)
            # self.assertTrue(region_info is not None)

            ec2 = boto3.resource('ec2', region_name=r_name)

            # DEBUG
            for instance in ec2.instances.all():
                print("%s: tags '%s'" % (instance, instance.tags))
            continue                # XXX
            # END

            # DEBUG
            #print("region_info: %s" % region_info)
            #print("  cnx:      %s" % region_info.connection)
            #print("  endpoint: %s" % region_info.endpoint)
            # END

            # XXX THIS CODE IS NOW UNREACHABLE
            vpc = ec2.Vpc(VPC_IDS[r_ndx])    # gets a ResourceWarning
            self.assertTrue(vpc is not None)
            self.assertEqual(vpc.cidr_block, VPC_CIDRS[r_ndx])

            # alternative approach ----------------------------------

            # CLIENT --------------------------------------
            client = boto3.client('ec2', region_name=r_name)

            # GATEWAYS ------------------------------------
            desc = client.describe_internet_gateways()
            igws = desc['InternetGateways']
            self.assertEqual(len(igws), 1)
            igw = igws[0]
            # DEBUG
            print(("IGW: %s" % igws[0]['InternetGatewayId']))
            sys.stdout.flush()
            # END
            my_id = igw['InternetGatewayId']
            self.assertEqual(my_id, IGATEWAY_IDS[r_ndx])

            # AVAILABILITY ZONES --------------------------
            # for z_ndx, zone in enumerate(ZONES[r_ndx]):
            #    print("    zone %s, cidr %s" % (zone, SUBNET_CIDRS[r_ndx][z_ndx]))
            # SUBNETS -----------------------
            #    #sub = vpc_cnx.create_subnet(VPC_IDS[r_ndx],
            #    #        SUBNET_CIDRS[r_ndx][z_ndx],
            #    #        availability_zone=zone)
            #    #print "SUBNET: %z" % sub

            # INSTANCES ---------------------

            # VOLUMES -----------------------

if __name__ == '__main__':
    # suppress warnings about unclosed sockets
    unittest.main(warnings='ignore')
