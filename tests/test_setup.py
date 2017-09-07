#!/usr/bin/env python3
# testSetup.py

""" Test the vm_mgr_setup() function. """

import sys
import unittest

import boto3
from botocore import session

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

    # COMMENTED OUT, in effect
    def zzz_test_vm_mgr_setup_boto3(self):
        """ Python 3/boto3 version of the test code. """

        # ResourceWarning warning messages like
        #     "Resourcewarning: unclosed <ssl.SSLSocket ... ,443)>
        # are a known problem; there appears to be no way to easily
        # get rid of them.  Due to Python3/urllib3 connection pooling,
        # which is a Good Thing.

        # DEBUG
        print("BOTO3-BASED CODE")
        # END

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
            # print("region_info: %s" % region_info)
            # print("  cnx:      %s" % region_info.connection)
            # print("  endpoint: %s" % region_info.endpoint)
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
            #    print("    zone %s, cidr %s" % (
            #        zone, SUBNET_CIDRS[r_ndx][z_ndx]))
            # SUBNETS -----------------------
            #    #sub = vpc_cnx.create_subnet(VPC_IDS[r_ndx],
            #    #        SUBNET_CIDRS[r_ndx][z_ndx],
            #    #        availability_zone=zone)
            #    # print "SUBNET: %z" % sub

            # INSTANCES ---------------------

            # VOLUMES -----------------------

    def test_vm_mgr_setup_botocore(self):
        """ Python 3/botocore version of the test code. """

        # DEBUG
        print("\nBOTOCORE-BASED CODE")
        # END
        sss = session.get_session()

        for r_ndx, r_name in enumerate(REGIONS):

            # DEBUG
            print(("\n%s" % r_name.upper()))
            # END

            ec2 = sss.create_client('ec2', region_name=r_name)

            inst = ec2.describe_instances()['Reservations'][0]['Instances']
            icount = len(inst)
            print("There is/are %d instances" % icount)
            for ndx in range(icount):
                instance = inst[ndx]
                # there are 28 keys
                print('  instance ID:   %s' % instance['InstanceId'])
                print('  instance type: %s' % instance['InstanceType'])
                print('  image ID:      %s' % instance['ImageId'])
                print('  key name:      %s' % instance['KeyName'])
                print('  public IP:     %s' % instance['PublicIpAddress'])
                print('  private IP:    %s' % instance['PrivateIpAddress'])
                print('  subnet ID:     %s' % instance['SubnetId'])
                print('  root device:   %s' % instance['RootDeviceName'])

                ifaces = instance['NetworkInterfaces']
                print("  There is/are %d interfaces" % len(ifaces))
                for count, iface in enumerate(ifaces):
                    # there are 14 keys
                    print(
                        "    ID:            %s" %
                        iface['NetworkInterfaceId'])
                    print("    Status:        %s" % iface['Status'])
                    print("    SubnetId:      %s" % iface['SubnetId'])
                    print("    VpcId:         %s" % iface['VpcId'])
                    print("    priv ip addr:  %s" % iface['PrivateIpAddress'])
                    print("    association:")
                    assoc = iface['Association']
                    print("      IpOwnerId:   %s" % assoc['IpOwnerId'])
                    print("      PublicIp:    %s" % assoc['PublicIp'])
                    print("    groups:")
                    groups = iface['Groups']
                    for which, group in enumerate(groups):
                        print("      %d: id %s, name %s" % (
                            which, group['GroupId'], group['GroupName']))

                blkdev = instance['BlockDeviceMappings']
                print("  There is/are %d block devices" % len(blkdev))
                for count in range(len(blkdev)):
                    dev = blkdev[count]
                    name = dev['DeviceName']
                    ebs = dev['Ebs']
                    status = ebs['Status']
                    vol_id = ebs['VolumeId']
                    # del_on_term = ebs['DeleteOnTermination']    # boolean
                    print("    %d name %-9s status %s vol_id %s" % (
                        count, name, status, vol_id))

            volumes = ec2.describe_volumes()['Volumes']
            vcount = len(volumes)
            print("  There are %d volumes" % vcount)
            for ndx in range(vcount):
                volume = volumes[ndx]
                # there are 9 keys
                print('  volume ID:   %s' % volume['VolumeId'])
                print('  volume type: %s' % volume['VolumeType'])
                print('  size:        %s' % volume['Size'])
                print('  state:       %s' % volume['State'])
                print('  zone:        %s' % volume['AvailabilityZone'])
                print('  attachments:')
                att = volume['Attachments'][0]
                print('    volume ID:   %s' % att['VolumeId'])
                print('    device:      %s' % att['Device'])
                print('    state:       %s' % att['State'])
                print('    instance ID: %s' % att['InstanceId'])
                print('    del on term  %s' % att['DeleteOnTermination'])

            continue                # XXX
            # END

            # DEBUG
            # print("region_info: %s" % region_info)
            # print("  cnx:      %s" % region_info.connection)
            # print("  endpoint: %s" % region_info.endpoint)
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
            #    print("    zone %s, cidr %s" % (
            #        zone, SUBNET_CIDRS[r_ndx][z_ndx]))
            # SUBNETS -----------------------
            #    #sub = vpc_cnx.create_subnet(VPC_IDS[r_ndx],
            #    #        SUBNET_CIDRS[r_ndx][z_ndx],
            #    #        availability_zone=zone)
            #    # print "SUBNET: %z" % sub

            # INSTANCES ---------------------

            # VOLUMES -----------------------


if __name__ == '__main__':
    # suppress warnings about unclosed sockets
    unittest.main(warnings='ignore')
