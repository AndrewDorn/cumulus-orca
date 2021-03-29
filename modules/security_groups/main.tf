## Terraform Requirements
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.5.0"
    }
  }
}


## AWS Provider Settings
provider "aws" {
  region  = var.region
  profile = var.aws_profile
}


## Local Variables
locals {
  tags = merge(var.tags, { Deployment = var.prefix })
}


## Security Group Resources

## vpc_postgres_ingress_all_egress - PostgreSQL security Group
## ==============================================================================
resource "aws_security_group" "vpc-postgres-ingress-all-egress" {
  ## OPTIONAL
  description = "ORCA security group to allow PostgreSQL access."
  name        = "${var.prefix}-vpc-ingress-all-egress"
  tags        = local.tags
  vpc_id      = var.vpc_id

  ingress {
    from_port = var.database_port
    to_port   = var.database_port
    protocol  = "TCP"
    self      = true
  }

}
