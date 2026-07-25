terraform {
  required_version = ">= 1.7.0"
}

variable "remote_access_hostname" {
  description = "Fictional hostname used in the reference blueprint."
  type        = string
  default     = "workstation.example.com"
}

locals {
  inference_address = "192.0.2.10"
  control_address   = "192.0.2.20"
}

output "reference_topology" {
  value = {
    inference = local.inference_address
    control   = local.control_address
    hostname  = var.remote_access_hostname
  }
}

