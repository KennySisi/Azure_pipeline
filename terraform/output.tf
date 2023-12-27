output "public_ip_address" {
  value = azurerm_public_ip.main.ip_address
}

output "virtyak_machine_public_ip_address" {
  value = azurerm_linux_virtual_machine.main.public_ip_address
}