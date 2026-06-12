output "external_ip" {
  description = "Public IP address of the virtual machine"
  value       = yandex_compute_instance.football_api_vm.network_interface[0].nat_ip_address
}

output "application_url" {
  description = "Application URL"
  value       = "http://${yandex_compute_instance.football_api_vm.network_interface[0].nat_ip_address}"
}
