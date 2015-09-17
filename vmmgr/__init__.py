# ~/py/vmmgr/__init__.py

import os, sys, time
import boto

__all__ = [ '__version__',              '__version_date__',
            'REGIONS',      'GROUP_IDS',    
            'VPC_IDS',      'VPC_CIDRS',
            'ZONES',    
            'SUBNET_IDS',   'SUBNET_CIDRS', 
            'IGATEWAY_IDS',
            # FUNCTIONS ---------------------------------------------
            '_validRegion',
            # CLASSES -----------------------------------------------
            'VMMgr',
            'Host', 'EC2Host', 'LinuxBox',
          ]

__version__      = '0.4.3'
__version_date__ = '2015-09-16'

# CONSTANTS #########################################################
# regions of interest at this time
REGIONS     = ['eu-west-1',     'us-east-1',    
               'us-west-1',     'us-west-2', ]

# these are IDs for vpc-binders in each region
GROUP_IDS   = ['sg-2c1ccd49',   'sg-56374833',  
               'sg-f8a6579d',   'sg-adeb52c8', ]

VPC_IDS     = ['vpc-e248bc87',      'vpc-e975af8c',     
               'vpc-07e70762',      'vpc-6ffb050a', ]

VPC_CIDRS   = ['192.168.192.0/20', '192.168.208.0/20', 
               '192.168.224.0/20', '192.168.240.0/20', ]

# only zones us-east-{c,d,e} are actually available!
ZONES       = [['eu-west-1a',],     
               ['us-east-1c',    'us-east-1d', ],
               ['us-west-1c',],
               ['us-west-2c',],
               ]

SUBNET_CIDRS= [ ['192.168.192.0/24', ], 
                ['192.168.208.0/24', '192.168.209.0/24', ], 
                ['192.168.224.0/24', ],
                ['192.168.240.0/24', ]
                    ]

SUBNET_IDS     = [ ['subnet-4f9f6c38', ],
                   ['subnet-9ef237e9', 'subnet-cd3ed994',  ],
                   ['subnet-8085b3c6', ],
                   ['subnet-19e2eb5f', ],
                   ]

IGATEWAY_IDS     = ['igw-cf32d6aa', 'igw-fb3bff9e', 
                   'igw-948d91f6', 'igw-9809e2fd']

# a default route (and so igw) has been added to each table
ROUTE_TABLES    = ['rtb-f1649994', 'rtb-5d17cc38', 
                   'rtb-6e4dae0b', 
                   # the main table, then the local
                   ['rtb-cf7f84aa', 'rtb-d1708bb4'],
                   ]

# This is not accurate (a) the 'main' associations are missing and
# (b) the eu-west 'main' association is in any case with the wrong
# rtb.  Returns a list rather than a single value; the list maps to
# zones rather than regions.
RTB_ASSOCS      = [['rtbassoc-afc833ca',],
                   ['rtbassoc-de69c7bb', 'rtbassoc-9669c7f3',],
                   ['rtbassoc-e3769486',],
                   # this is for the local rtb
                   ['rtbassoc-09d7176c',],
                   ]

# FUNCTIONS #########################################################

def _validRegion(region):
    """
    Whether a region name is valid.

    :param region: The name of an EC2 region.
    :type region: str
    :return: True if parameter is the name of a valid EC2 region.
    :rtype: bool
    """
    valid = False
    for r in REGIONS:
        if region == r:
            valid = True
            break
    return valid

# CLASS #############################################################

class VMMgr(object):
    """

    :ivar _regions: List of valid EC2 region names.
    :ivar _groupIDs: A list of security group IDs (strings).
    :ivar _vpcIDs: A list of Virtual Private Cloud (VPC) IDs.
    :ivar _vpcCIDRS: List of CIDR block specs, dotted quad followed by prefix
        length.
    :ivar _zones: List of availability zones within region.
    :ivar _subnetCIDRs: List of CIDR blocks associated with respective subnets.
    :ivar _subnetIDs: List of subnet IDs.
    :ivar _igatewayIDs: List of internet gateways associated with respective
        subnets.
    """
    def __init__(self):
        self._regions       = REGIONS
        self._groupIDs      = GROUP_IDS
        self._vpcIDs        = VPC_IDS
        self._vpcCIDRs      = VPC_CIDRS
        self._zones         = ZONES 
        self._subnetCIDRs   = SUBNET_CIDRS
        self._subnetIDs     = SUBNET_IDS
        self._igatewayIDs   = IGATEWAY_IDS
        self._routeTables   = ROUTE_TABLES
        self._rtbAssocs     = RTB_ASSOCS

    def region(self, ndx):
        """ 
        Region name.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: the EC2 region name corresponding to the index.
        :rtype: str
        """
        return self._regions[ndx]

    def groupID(self, ndx):
        """ 
        ID of security group for region.

        :param ndx: zero-baseds index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: the security group ID corresponding to the index.
        :rtype: str
        """
        return self._groupIDs[ndx]

    def vpcID(self, ndx):
        """ 
        ID of virtual private cloud (VPD) for region.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: the virtual private cloud ID corresponding to the index.
        :rtype: str
        """
        return self._vpcIDs[ndx]

    def vpcCIDR(self, ndx):
        """ 
        Main CIDR block for the region.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: the VPC's CIDR block (dotted quad/prefix length)  
        :rtype: str
        """
        return self._vpcCIDRs[ndx]

    def zone(self, ndx):
        """ 
        Availability zones in use within the region.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: zones in use within the region
        :rtype: list of str
        """
        return self._zones[ndx]

    def subnetCIDR(self, ndx):
        """ 
        CIDR blocks used by subnets within the rgion.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: CIDR blocks associated with respective subnets in region. 
        :rtype: list of list of str
        """
        return self._subnetCIDRs[ndx]

    def subnetID(self, ndx):
        """ 
        IDs associated with region subnets.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: IDs of subnets in region. 
        :rtype: list of list of str
        """
        return self._subnetIDs[ndx]

    def igatewayID(self, ndx):
        """ 
        ID of internet gateway for a region.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: ID of internet gateway for an EC2 region. 
        :rtype: str
        """
        return self._igatewayIDs[ndx]

    def routeTable(self, ndx):
        """ 
        Route tables associated with a region.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: list of route table IDs for subnets in the region. 
        :rtype: list of str
        """
        return self._routeTables[ndx]

    def rtbAssoc(self, ndx):
        """ 
        Route table associations for a region.

        :param ndx: zero-based index of an EC2 region.
        :type ndx: int
        :raises IndexError: if there is no EC2 region with this index.
        :returns: list of route table association IDs for subnets in region. 
        :rtype: list of str
        """
        return self._rtbAssocs[ndx]

# CLASS #############################################################

class Host(object):
    def __init__(self, fqdn):
        self._fqdn = fqdn

    @property
    def fqdn(self):
        return self._fqdn

class EC2Host(Host):
    def __init__(self, fqdn):
        super(EC2Host, self).__init__(fqdn)

class LinuxBox(Host):
    def __init__(self, fqdn):
        super(LinuxBox, self).__init__(fqdn)
