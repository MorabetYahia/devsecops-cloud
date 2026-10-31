resource "azurerm_resource_group" "rg" {
  name     = "${var.prefix}-rg"
  location = var.location
  tags     = { project = "devsecops-cloud" }
}

resource "azurerm_virtual_network" "vnet" {
  name                = "${var.prefix}-vnet"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.10.0.0/16"]
}

resource "azurerm_subnet" "aks" {
  name                 = "aks-nodes"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.10.1.0/24"]
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "${var.prefix}-aks"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "${var.prefix}aks"
  sku_tier            = "Free" # plan de contrôle sans frais

  default_node_pool {
    name                        = "system"
    node_count                  = 1
    vm_size                     = var.node_vm_size
    os_disk_size_gb             = 32
    os_disk_type                = "Managed"
    vnet_subnet_id              = azurerm_subnet.aks.id
    temporary_name_for_rotation = "tmpsystem"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin      = "azure"
    network_plugin_mode = "overlay"
    pod_cidr            = "192.168.0.0/16"
    service_cidr        = "10.20.0.0/16" # ne doit pas chevaucher le VNet
    dns_service_ip      = "10.20.0.10"
    load_balancer_sku   = "standard"
  }

  tags = { project = "devsecops-cloud" }
}

# Le cluster gère le réseau de son sous-réseau (Load Balancer, IP)
resource "azurerm_role_assignment" "aks_network" {
  scope                = azurerm_subnet.aks.id
  role_definition_name = "Network Contributor"
  principal_id         = azurerm_kubernetes_cluster.aks.identity[0].principal_id
}
