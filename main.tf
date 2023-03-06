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
  image_id                    = "ami-0c55b159cbfafe1f0"
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

#AWS ECS cluster task definition 
resource "aws_ecs_task_definition" "ecs_task" {
  family                   = "${var.app_name}-tesk-def"
  container_definitions    = jsonencode([
    {
      name  = "${var.app_name}-container"
      image = "${aws_ecr_repository.ecs_repo.repository_url}:latest"
      portMappings = [
        {
          containerPort = 8080
          hostPort      = 8080
        }
      ]
    }
  ])
  requires_compatibilities = ["EC2"]
  cpu                      = "256"
  memory                   = "512"
}

#AWS ECS cluster service
resource "aws_ecs_service" "example_service" {
  name            = "example-service"
  cluster         = aws_ecs_cluster.ecs_cluster.id
  task_definition = aws_ecs_task_definition.ecs_task.arn
  desired_count   = 1

  network_configuration {
    assign_public_ip = true

    security_groups = [
      aws_security_group.ecs_sg.id,
    ]

    subnets = [
      aws_subnet.ecs_subnet.id
    ]
  }
}
