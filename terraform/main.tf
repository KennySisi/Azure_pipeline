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

    security_rule {
    name                       = "HTTPRule"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "8000"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}


resource "azurerm_network_interface" "main" {
  name                = "${var.prefix}-nic"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  # network_security_group_id = azurerm_network_security_group.main.id

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.internal.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id = azurerm_public_ip.main.id
    # network_security_group_ids = [azurerm_network_security_group.main.id]
  }

}

# resource "azurerm_network_interface_application_security_group_association" "main" {
#   network_interface_id          = azurerm_network_interface.main.id
#   application_security_group_id = azurerm_network_security_group.main.id
# }

resource "azurerm_network_interface_security_group_association" "example" {
  network_interface_id      = azurerm_network_interface.main.id
  network_security_group_id = azurerm_network_security_group.main.id
}

locals {
  # 本地脚本路径
  script_path = "${path.module}/../scripts/run_script.sh"
}

# resource "null_resource" "copy_script" {
#   # 本地执行器只有在 apply 时运行一次
#   triggers = {
#     always_run = timestamp()
#   }

#   # 将脚本文件复制到临时目录
#   # provisioner "local-exec" {
#   #   command = <<-EOT
#   #     cp ${local.script_path} ${path.module}/temp/run_script.sh
#   #   EOT
#   #   interpreter = [ "bash", "-c" ]
#   # }
  
#   # provisioner "local-exec" {
#   #   command = <<-EOT
#   #     Copy-Item -Path ${local.script_path} -Destination ${path.module}/scripts/temp/run_script.sh
#   #   EOT
#   #   interpreter = ["PowerShell", "-Command"]
#   # }

# }

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

  provisioner "local-exec" {
    command = "echo start debug"
  }

  provisioner "local-exec" {
    command = "echo ${path.module}"
  }  
  
  provisioner "local-exec" {
    command = "echo %cd%"
  }

  # provisioner "file" {
  #   source      = "F:/Learning/Code/fast_api/azure_pipeline/scripts/run_script.sh"  # 本地文件路径
  #   destination = "/home/azureuser/run_script.sh"  # 虚拟机上的目标路径

  #   connection {
  #     type        = "ssh"
  #     user        = var.username
  #     password    = var.password
  #     host        = azurerm_linux_virtual_machine.main.public_ip_address
  #   }
  # }

  #   provisioner "remote-exec" {
  #     inline = [
  #     "tr -d '\r' < /home/azureuser/run_script.sh > /home/azureuser/run_script_unix.sh",
  #     "sudo chmod 777 /home/azureuser/run_script_unix.sh",
  #     "sudo /home/azureuser/run_script_unix.sh",
  #   ]

  #   connection {
  #     type        = "ssh"
  #     user        = var.username
  #     password = var.password
  #     host        = azurerm_linux_virtual_machine.main.public_ip_address
  #   }

  # }


  # custom_data = file("cloud-init-script.sh")
}

resource "null_resource" "copy_and_execute_script" {
  # 在 apply 时运行一次
  triggers = {
    always_run = timestamp()
  }

  provisioner "file" {
    source      = "F:/Learning/Code/fast_api/azure_pipeline/scripts/run_script.sh"  # 本地文件路径
    destination = "/home/azureuser/run_script.sh"  # 虚拟机上的目标路径

    connection {
      type        = "ssh"
      user        = var.username
      password    = var.password
      host        = azurerm_linux_virtual_machine.main.public_ip_address
    }
  }

  provisioner "remote-exec" {
    inline = [
      "tr -d '\r' < /home/azureuser/run_script.sh > /home/azureuser/run_script_unix.sh",
      "sudo chmod 777 /home/azureuser/run_script_unix.sh",
      "sudo /home/azureuser/run_script_unix.sh ${var.docker_image}",
    ]

    connection {
      type        = "ssh"
      user        = var.username
      password    = var.password
      host        = azurerm_linux_virtual_machine.main.public_ip_address
    }
  }
}