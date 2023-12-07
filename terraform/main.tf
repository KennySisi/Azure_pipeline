# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

terraform {
  backend "azurerm" {
    resource_group_name   = "myTFResourceGroup"
    storage_account_name   = "tfstorageaccountkenny"
    container_name         = "tfstate"
    key                    = "terraform.tfstate"
    access_key             = "pDQILEz68lhfmVCrk3mL8k0YrBsPEE+nL7vWHkiz6UGRsaaCkyGEex/5hINHTNKWMVCg2mljNKWT+AStTAUJdA=="
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-resources"
  location = var.location
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-network"
  address_space       = ["10.0.0.0/22"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
  
  # snetwork_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_public_ip" "main" {
  name                = "${var.prefix}-public-ip"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  allocation_method   = "Dynamic"
}

resource "azurerm_network_security_group" "main" {
  name                = "${var.prefix}-nsg"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  security_rule {
    name                       = "SSHRule"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}


resource "azurerm_network_interface" "main" {
  name                = "${var.prefix}-nic"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.internal.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id = azurerm_public_ip.main.id
    # network_security_group_ids = [azurerm_network_security_group.main.id]
  }

  //snetwork_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_network_interface_application_security_group_association" "main" {
  network_interface_id          = azurerm_network_interface.main.id
  application_security_group_id = azurerm_network_security_group.main.id
}

resource "azurerm_linux_virtual_machine" "main" {
  name                            = "${var.prefix}-vm"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = azurerm_resource_group.main.location
  size                            = "Standard_D2s_v3"
  admin_username                  = var.username
  admin_password                  = var.password
  disable_password_authentication = false
  network_interface_ids = [
    azurerm_network_interface.main.id,
  ]

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  os_disk {
    storage_account_type = "Standard_LRS"
    caching              = "ReadWrite"
  }

    provisioner "remote-exec" {
    inline = [
      "echo 'Script execution start'",
      "sudo apt-get update",
      "sudo apt-get install -y python3",  # 安装 Python
      "sudo apt-get install -y python3-pip",  # 安装 pip
      "pip3 install fastapi uvicorn",  # 安装 FastAPI 和 Uvicorn
      "sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
      "echo \"deb [signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
      "sudo apt-get install -y docker-ce docker-ce-cli containerd.io",
      "sudo docker --version",
      "docker run -p 8000:8000 -d mly219blueheart/fastapi:latest",
      "echo 'Script execution end'",
    ]

    connection {
      type        = "ssh"
      user        = var.username
      password = var.password
      host        = azurerm_linux_virtual_machine.main.public_ip_address
    }

  }

  # custom_data = file("cloud-init-script.sh")

}