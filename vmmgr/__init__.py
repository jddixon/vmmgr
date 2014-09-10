# ~/py/vmmgr/__init__.py

import os, sys, time
import boto

__all__ = [ '__version__',              '__version_date__',
            'REGIONS',      'GROUP_IDS',    
            'VPC_IDS',      'VPC_CIDRS',
            'ZONES',    
            'SUBNET_IDS',   'SUBNET_CIDRS', 
            'GATEWAY_IDS',
            # FUNCTIONS
            # CLASSES
            'VMMgr',
            'Host', 'EC2Host', 'LinuxBox',
          ]

__version__      = '0.2.0'
__version_date__ = '2014-09-10'

# CONSTANTS #########################################################
# regions of interest at this time
REGIONS     = ['eu-west-1',     'us-east-1',    
               'us-west=1',     'us-west-2', ]

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

GATEWAY_IDS     = ['igw-cf32d6aa', 'igw-fb3bff9e', 
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
# CLASS #############################################################
class VMMgr(object):
    def __init__(self):
        self._regions       = REGIONS
        self._groupIDs      = GROUP_IDS
        self._vpcIDs        = VPC_IDS
        self._vpcCIDRs      = VPC_CIDRS
        self._zones         = ZONES 
        self._subnetCIDRs   = SUBNET_CIDRS
        self._subnetIDs     = SUBNET_IDS
        self._gatewayIDs    = GATEWAY_IDS
        self._routeTables   = ROUTE_TABLES
        self._rtbAssocs     = RTB_ASSOCS

    def region(self, ndx):
        """ raises IndexError"""
        return self._regions[ndx]

    def groupID(self, ndx):
        """ raises IndexError"""
        return self._groupIDs[ndx]

    def vpcID(self, ndx):
        return self._vpcIDs[ndx]

    def vpcCIDR(self, ndx):
        return self._vpcCIDRs[ndx]

    def zone(self, ndx):
        return self._zones[ndx]

    def subnetCIDR(self, ndx):
        return self._subnetCIDRs[ndx]

    def subnetID(self, ndx):
        return self._subnetIDs[ndx]

    def gatewayID(self, ndx):
        return self._gatewayIDs[ndx]

    def routeTable(self, ndx):
        return self._routeTables[ndx]

    def rtbAssoc(self, ndx):
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
