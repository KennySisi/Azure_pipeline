# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

variable "prefix" {
  description = "The prefix which should be used for all resources in this example"
  default = "kenny"
}

variable "location" {
  description = "The Azure Region in which all resources in this example should be created."
  default = "Japan East"
}

variable "username" {
  description = "user name"
  default = "azureuser"
}

variable "password" {
  description = "password."
  default = "Zs850605:)"
}

variable "github_run_number" {
  description = "git hub run number"
  default = 16
}