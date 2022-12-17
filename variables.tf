variable "aws_region" {
  description = "The AWS region to deploy the EC2 instance in."
  default   = "us-west-2"
}


variable "instance_type" {
  type = list(string)
  description = "instance type for ec2"
  default   =  ["p4d.24xlarge", "p3.2xlarge", "p3.8xlarge", "p3.16xlarge", "p3dn.24xlarge", "g5.xlarge"]
}

variable "key_name" {
    description = "aws keypair name"
    default = "charlie_ssh"
}


