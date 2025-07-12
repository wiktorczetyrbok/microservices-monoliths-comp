provider "google" {
  region      = var.zone
  project     = var.project_id
}

terraform {
  backend "gcs" {
    bucket = "terraform-state-cicd-pkraciuk"
    prefix = "state"
  }
}