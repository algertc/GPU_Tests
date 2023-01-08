variable "aws_region" {
  description = "The AWS region to deploy the EC2 instance in."
  default   = "us-east-1"
}


variable "instance_type" {
  type = list(string)
  description = "instance type for ec2"
  default   =  ["p3.2xlarge", "p3.8xlarge", "g5.24xlarge"]
}

variable "key_name" {
    description = "aws keypair name"
    default = "charlie_ssh"
}


variable "ansible_hosts_dir" {
    description = "Where is ansible/hosts?"
    default = "etc/ansible/hosts"
}