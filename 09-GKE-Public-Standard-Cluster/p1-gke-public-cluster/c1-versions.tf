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

# Criação e preenchimento automático do ~/.kube/config para acesso ao cluster GKE
resource "local_file" "k8s_config" {
  filename        = pathexpand("~/.kube/config")
  file_permission = "0600"

  content = <<-EOT
apiVersion: v1
kind: Config
preferences: {}
clusters:
- name: ${google_container_cluster.gke_cluster.name}
  cluster:
    certificate-authority-data: ${google_container_cluster.gke_cluster.master_auth[0].cluster_ca_certificate}
    server: https://${google_container_cluster.gke_cluster.endpoint}
contexts:
- name: ${google_container_cluster.gke_cluster.name}
  context:
    cluster: ${google_container_cluster.gke_cluster.name}
    user: ${google_container_cluster.gke_cluster.name}
current-context: ${google_container_cluster.gke_cluster.name}
users:
- name: ${google_container_cluster.gke_cluster.name}
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      interactiveMode: Never
      command: bash
      args:
      - -c
      - |
        if command -v gke-gcloud-auth-plugin >/dev/null 2>&1; then
          exec gke-gcloud-auth-plugin
        else
          printf '{"apiVersion":"client.authentication.k8s.io/v1beta1","kind":"ExecCredential","status":{"token":"%s"}}\n' "$(gcloud auth print-access-token)"
        fi
  EOT
}