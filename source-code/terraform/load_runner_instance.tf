resource "google_compute_instance" "load_runner_instance" {
  name         = "load-runner-instance"
  machine_type = "n2-standard-8"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      size = 60
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet_load.id
    network_ip = google_compute_address.load_runner_ip.address
    access_config {
    }
  }

  metadata = {
    ssh-keys = "pkraciuk:${var.ssh_public_key}"
  }
}

resource "google_compute_address" "load_runner_ip" {
  name         = "load-runner-ip"
  subnetwork   = google_compute_subnetwork.subnet_load.id
  address_type = "INTERNAL"
  address      = "10.0.1.2" 
  region       = var.region
}