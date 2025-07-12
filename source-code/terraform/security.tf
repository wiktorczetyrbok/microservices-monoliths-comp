resource "google_compute_network" "vpc_network" {
  name                    = "terraform-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet_app" {
  name          = "terraform-subnet-app"
  region        = var.region
  network       = google_compute_network.vpc_network.id
  ip_cidr_range = "10.0.0.0/24"
}

resource "google_compute_subnetwork" "subnet_load" {
  name          = "terraform-subnet-load"
  region        = var.region
  network       = google_compute_network.vpc_network.id
  ip_cidr_range = "10.0.1.0/24"
}

resource "google_compute_firewall" "allow_all_inbound" {
  name    = "allow-all-inbound"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"] 
}

resource "google_compute_firewall" "allow_all_outbound" {
  name    = "allow-all-outbound"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "all"
  }

  direction = "EGRESS"
  destination_ranges = ["0.0.0.0/0"]
}
