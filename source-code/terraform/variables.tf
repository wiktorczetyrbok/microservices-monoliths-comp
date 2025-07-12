variable "zone" {
  type        = string
  description = "GCP zone for vm"
}
variable "region" {
  type        = string
  description = "GCP region"
}
variable "vm_machine_type" {
  type        = string
  description = "machine type for vm"
  default = "c2d-standard-2"
}

variable "google_credentials" {
  type        = string
  description = "JSON credentials for Google Cloud"
  default     = ""
}

variable "project_id" {
  description = "The Google Cloud project ID"
  type        = string
}

variable "ssh_public_key" {
  description = "The public SSH key."
  type        = string
}

variable "swarm_workers_count" {
  description = "Number of swarm instances to create"
  default     = 0
}

variable "swarm_worker_token" {
  description = "Swarm token to join as worker"
  type = string
  default = ""
}