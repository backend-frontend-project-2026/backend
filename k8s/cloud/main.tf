terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
    local = {
      source = "hashicorp/local"
    }
  }
}

provider "yandex" {
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = "ru-central1-a"
}

resource "yandex_vpc_network" "this" {
  name = "roomie-network"
}

resource "yandex_vpc_subnet" "this" {
  name           = "roomie-subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.this.id
  v4_cidr_blocks = ["10.10.0.0/24"]
}

resource "yandex_vpc_security_group" "this" {
  name       = "roomie-sg"
  network_id = yandex_vpc_network.this.id

  ingress {
    protocol          = "TCP"
    predefined_target = "loadbalancer_healthchecks"
    from_port         = 0
    to_port           = 65535
  }

  ingress {
    protocol          = "ANY"
    predefined_target = "self_security_group"
    from_port         = 0
    to_port           = 65535
  }

  egress {
    protocol          = "ANY"
    predefined_target = "self_security_group"
    from_port         = 0
    to_port           = 65535
  }

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 6443
  }

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 443
  }

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = yandex_vpc_subnet.this.v4_cidr_blocks
    from_port      = 30000
    to_port        = 32767
  }

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = yandex_vpc_subnet.this.v4_cidr_blocks
    port           = 10501
  }

  egress {
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 0
    to_port        = 65535
  }
}

resource "yandex_iam_service_account" "cluster" {
  name = "k8s-resources-sa"
}

resource "yandex_iam_service_account" "nodes" {
  name = "k8s-nodes-sa"
}

resource "yandex_resourcemanager_folder_iam_member" "cluster_agent" {
  folder_id = var.folder_id
  role      = "k8s.clusters.agent"
  member    = "serviceAccount:${yandex_iam_service_account.cluster.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "cluster_public_ip" {
  folder_id = var.folder_id
  role      = "vpc.publicAdmin"
  member    = "serviceAccount:${yandex_iam_service_account.cluster.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "nodes_puller" {
  folder_id = var.folder_id
  role      = "container-registry.images.puller"
  member    = "serviceAccount:${yandex_iam_service_account.nodes.id}"
}

resource "yandex_kubernetes_cluster" "this" {
  name       = "roomie-cluster"
  network_id = yandex_vpc_network.this.id

  master {
    zonal {
      zone      = "ru-central1-a"
      subnet_id = yandex_vpc_subnet.this.id
    }
    public_ip          = true
    security_group_ids = [yandex_vpc_security_group.this.id]
  }

  service_account_id      = yandex_iam_service_account.cluster.id
  node_service_account_id = yandex_iam_service_account.nodes.id
  release_channel         = "REGULAR"

  depends_on = [
    yandex_resourcemanager_folder_iam_member.cluster_agent,
    yandex_resourcemanager_folder_iam_member.cluster_public_ip,
  ]
}

resource "yandex_kubernetes_node_group" "this" {
  cluster_id = yandex_kubernetes_cluster.this.id
  name       = "roomie-nodes"

  instance_template {
    platform_id = "standard-v3"
    resources {
      cores         = 2
      core_fraction = 20
      memory        = 2
    }
    boot_disk {
      type = "network-hdd"
      size = 30
    }
    network_interface {
      subnet_ids         = [yandex_vpc_subnet.this.id]
      nat                = true
      security_group_ids = [yandex_vpc_security_group.this.id]
    }
    scheduling_policy {
      preemptible = true
    }
  }

  scale_policy {
    fixed_scale {
      size = 1
    }
  }

  depends_on = [
    yandex_resourcemanager_folder_iam_member.nodes_puller,
  ]
}

