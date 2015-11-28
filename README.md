# vmmgr

Configuration files and Python3 scripts for managing the configuration
of networks, instances, and volumes in Amazon's
[EC2 cloud.](https://aws.amazon.com/ec2)

The python scripts use
[boto,](https://github.com/boto/boto)
a package for communicating with
[Amazon Web Services](https://aws.amazon.com)
(AWS), which include the EC2 cloud.

The particular network described by the configuration files in this
package includes
EC2 instances in a zone in each of four resions:
eu-west-1, us-east-1, us-west-1, and us-west-2.

* **eu-west-1** is in Ireland and serves the European Union (EU) area
* **us-east-1** is on the US East Coast (in or attached to MAE East)
* **us-west-1** is in California
* **us-west-2** is in Oregon.

We have **VPCs** (virtual private clouds) in each of these zones.

A `/20` is set up for each VPC.  This is 16 class Cs.  It must be properly
aligned.

A VPC has to be defined for each region used.  This is done by executing
a command like

	ec2addvpc 192.168.240.0/20 --region us-west-2 >> vpcx

A **security group** has been defined for each region.  This is done by
adding a line to make.groups after commenting out the preceding line(s)
and then executing the command.

## Project Status

Just a hint of a sketch.  Tests get AuthFailures.

## On-line Documentation

More information on the **vmmgr** project can be found
[here](https://jddixon.github.io/vmmgr)
