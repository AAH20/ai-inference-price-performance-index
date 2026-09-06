terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  type    = string
  default = "eastus2"
}

variable "name" {
  type    = string
  default = "inferenceindex"
}

resource "azurerm_resource_group" "this" {
  name     = "rg-${var.name}"
  location = var.location
}

resource "azurerm_storage_account" "evidence" {
  name                            = replace("st${var.name}", "-", "")
  resource_group_name             = azurerm_resource_group.this.name
  location                        = azurerm_resource_group.this.location
  account_tier                    = "Standard"
  account_replication_type        = "LRS"
  min_tls_version                 = "TLS1_2"
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = false
}

resource "azurerm_storage_container" "evidence" {
  name                  = "benchmark-evidence"
  storage_account_id    = azurerm_storage_account.evidence.id
  container_access_type = "private"
}

output "evidence_storage_account_id" {
  value = azurerm_storage_account.evidence.id
}
