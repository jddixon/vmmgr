<h1 class="libTop">vmmgr</h1>

We are set up to operate in four zones: eu-west-1, us-east-1, us-west-1,
and us-west-2.  

A /20 is set up for each VPC.  This is 16 class Cs.  It must be properly
aligned.

A VPC has to be defined for each region used.  This is done by executing
a command like 
    ec2addvpc 192.168.240.0/20 --region us-west-2 >> vpcx

A security group has been defined for each region.  This is done by 
adding a line to make.groups after commenting out the preceding line(s)
and then executing the command.
