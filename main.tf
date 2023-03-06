# Provider configuration
provider "aws" {
  region = "eu-west-1"
}

# Variables
variable "app_name" {
  default = "terra-ecs-app"
}

# Create a VPC for the ECS cluster
resource "aws_vpc" "ecs_vpc" {
  cidr_block = "10.0.0.0/16"
}

# Create an Internet Gateway for the VPC
resource "aws_internet_gateway" "ecs_igw" {
  vpc_id = aws_vpc.ecs_vpc.id
}

# Create a public subnet for the ECS cluster
resource "aws_subnet" "ecs_subnet" {
  cidr_block = "10.0.1.0/24"
  vpc_id     = aws_vpc.ecs_vpc.id

  tags = {
    Name = "${var.app_name}-public-subnet"
  }
}

# Create a security group for the ECS instances
resource "aws_security_group" "ecs_sg" {
  name_prefix = "${var.app_name}-"
  vpc_id      = aws_vpc.ecs_vpc.id

  ingress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an ECS cluster
resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.app_name}-cluster"
}

# Create an EC2 launch configuration
resource "aws_launch_configuration" "ecs_lc" {
  name_prefix                 = "${var.app_name}-"
  instance_type               = "t2.micro"
  iam_instance_profile        = "ecsInstanceRole"
  security_groups             = [aws_security_group.ecs_sg.id]
  associate_public_ip_address = true

  lifecycle {
    create_before_destroy = true
  }
}

# Create an Auto Scaling group for the ECS instances
resource "aws_autoscaling_group" "ecs_asg" {
  name                      = "${var.app_name}-asg"
  launch_configuration      = aws_launch_configuration.ecs_lc.id
  min_size                  = 1
  max_size                  = 3
  desired_capacity          = 1
  vpc_zone_identifier       = [aws_subnet.ecs_subnet.id]
  health_check_grace_period = 300
  health_check_type         = "EC2"

  tag {
    key                 = "Name"
    value               = "${var.app_name}-ecs-instance"
    propagate_at_launch = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Create an ECR repository
resource "aws_ecr_repository" "ecs_repo" {
  name = "${var.app_name}-repo"

  lifecycle {
    create_before_destroy = true
  }
}
