# Terraform Settings Block
terraform {
  required_version = ">= 1.9"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.42.0"
    }
    local = {
      source  = "hashicorp/local"
      version = ">= 2.5.0"
    }
  }
  backend "gcs" {
    bucket = "terraform-on-gcp-gke-129test"
    prefix = "dev/gke-cluster-public"
  }
}

# Terraform Provider Block
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region1
}

# Criação do kubeconfig dentro de .kube
resource "local_file" "k8s_config" {
  # Opção 1: Salva na subpasta .kube do próprio módulo/diretório local
  filename = "${path.module}/.kube/config"

  # Opção 2: Se quiser apontar direto para a home do usuário (~/.kube/config):
  # filename = pathexpand("~/.kube/config")

  file_permission = "0600"

  content = <<-EOT
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: ${google_container_cluster.example.master_auth[0].cluster_ca_certificate}
    server: https://${google_container_cluster.example.endpoint}
  name: ${google_container_cluster.example.name}
contexts:
- context:
    cluster: ${google_container_cluster.example.name}
    user: ${google_container_cluster.example.name}
  name: ${google_container_cluster.example.name}
current-context: ${google_container_cluster.example.name}
kind: Config
preferences: {}
users:
- name: ${google_container_cluster.example.name}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: gcloud
      args:
      - config
      - config-helper
      - --format=json
  EOT
}