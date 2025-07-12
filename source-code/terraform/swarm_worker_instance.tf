resource "google_compute_instance" "swarm_worker_instance" {
  name         = "worker-instance-${count.index + 1}"
  machine_type = "c2d-standard-2"
  zone         = var.zone
  count        = var.swarm_workers_count

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.subnet_app.id
    access_config {
      // This block is intentionally left empty to assign a public IP
    }
  }

  metadata = {
    ssh-keys = "pkraciuk:${var.ssh_public_key}"
    startup-script = <<-EOT
      #!/bin/bash
      sudo apt-get update
      sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg2
      curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
      sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
      sudo apt-get update
      sudo apt-get install -y docker-ce docker-ce-cli containerd.io
      sudo apt install docker-compose -y
      sudo groupadd docker
      sudo usermod -aG docker pkraciuk
      sudo systemctl start docker
      sudo systemctl enable docker
      sleep 10
      echo ${var.swarm_worker_token} > /tmp/test.txt
      sudo docker swarm join --token ${var.swarm_worker_token} 10.0.0.2:2377
    EOT
  }
}
