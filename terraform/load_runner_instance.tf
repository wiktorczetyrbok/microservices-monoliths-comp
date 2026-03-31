resource "google_compute_instance" "load_runner_instance" {
  name         = "load-runner-instance"
  machine_type = "c4-standard-8"
  zone         = var.zone

  metadata = {
    ssh-keys = "wczetyrbok:${var.ssh_public_key}"
  }
}

resource "google_compute_address" "load_runner_ip" {
  name         = "load-runner-ip"
  subnetwork   = google_compute_subnetwork.subnet_load.id
  address_type = "INTERNAL"
  address      = "10.0.1.2" 
  region       = var.region
}