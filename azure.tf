terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.94.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}

variable "sql_admin_login" {}
variable "sql_admin_password" {}

# Create a resource group
resource "azurerm_resource_group" "demo_rg" {
  name     = "demo-rg"
  location = "West Europe"
}

# Create container registry
resource "azurerm_container_registry" "demo_acr" {
  name                = "demoacr41235"
  resource_group_name = azurerm_resource_group.demo_rg.name
  location            = azurerm_resource_group.demo_rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

# Create AKS cluster
resource "azurerm_kubernetes_cluster" "demo_aks" {
  name                = "demo-aks"
  location            = azurerm_resource_group.demo_rg.location
  resource_group_name = azurerm_resource_group.demo_rg.name
  dns_prefix          = "demo-aks"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_DS2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "development"
  }
}

resource "azurerm_role_assignment" "aks_acr_role" {
  principal_id                     = azurerm_kubernetes_cluster.demo_aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.demo_acr.id
  skip_service_principal_aad_check = true
}


resource "azurerm_mssql_server" "azure_sql" {
  name                         = "demosql41235"
  resource_group_name          = azurerm_resource_group.demo_rg.name
  location                     = azurerm_resource_group.demo_rg.location
  version                      = "12.0"

  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password
}

resource "azurerm_sql_database" "sql_db" {
  name                = "demodb"
  resource_group_name = azurerm_resource_group.demo_rg.name
  location            = azurerm_resource_group.demo_rg.location
  server_name         = azurerm_mssql_server.azure_sql.name
  edition             = "Basic"
  collation           = "SQL_LATIN1_GENERAL_CP1_CI_AS"
}