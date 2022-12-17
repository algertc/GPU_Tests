terraform {

  required_providers {
    aws = {
    source  = "hashicorp/aws"

    version = "~> 3.27"

    }
  }

  required_version = ">= 0.14.9"

}

provider "aws" {

  region                = var.aws_region
  shared_credentials_file = "~/.aws/credentials"
  profile               = "default"

}

resource "aws_instance" "ec2_instance" {
  count = length(var.instance_type)
  ami = "ami-0c09c7eb16d3e8e70"
  instance_type = var.instance_type[count.index]
  key_name = var.key_name
  associate_public_ip_address = true
  root_block_device {
    volume_size = 30
  }
  tags = {
    Name = var.instance_type[count.index]
  }
  
}

output "IPAddress" {
  value = "${aws_instance.ec2_instance[*].public_ip}"
}


