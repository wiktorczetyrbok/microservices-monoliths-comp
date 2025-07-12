resource "google_compute_instance" "app_instance" {
  name         = "app-instance"
  machine_type = var.vm_machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size = 30
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet_app.id
    network_ip = google_compute_address.benchmark_app_ip.address
    access_config {
    }
  }

  metadata = {
    ssh-keys = "pkraciuk:${var.ssh_public_key}"
  }
}

resource "google_compute_address" "benchmark_app_ip" {
  name         = "benchmark-app-ip"
  subnetwork   = google_compute_subnetwork.subnet_app.id
  address_type = "INTERNAL"
  address      = "10.0.0.2" 
  region       = var.region
}
