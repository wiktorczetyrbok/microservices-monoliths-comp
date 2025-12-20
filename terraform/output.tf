output "app_instance_public_ip" {
  value = google_compute_instance.app_instance.network_interface[0].access_config[0].nat_ip
  description = "The public IP address of the App instance."
}

output "load_runner_instance_public_ip" {
  value = google_compute_instance.load_runner_instance.network_interface[0].access_config[0].nat_ip
  description = "The public IP address of the Load runner instance."
}