variable "egress_from_port" {
  type    = number
  default = 5432
}
variable "egress_to_port" {
  type    = number
  default = 5432
}
# variable "vpc_id" {     replace with your vpc id
#   type = string 
# }

variable "prefix" {
  type    = string
  default = "orca"
}

variable "tags" {
  type = map(string)
  description = "tags for ORCA project"   #added tags. 
  default = {
    Project = "ORCA"
  }
}