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
          ]

__version__      = '0.1.0'
__version_date__ = '2014-07-19'

# 
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
               ['us-west=1c',],
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

# this is not accurate (a) the 'main' associations are missing and
# (b) the eu-west 'main' association is in any case with the wrong
# rtb 
RTB_ASSOCS      = [['rtbassoc-afc833ca',],
                   ['rtbassoc-de69c7bb', 'rtbassoc-9669c7f3',],
                   ['rtbassoc-e3769486',]
                   # this is for the local rtb
                   ['rtbassoc-09d7176c',]
                   ]
