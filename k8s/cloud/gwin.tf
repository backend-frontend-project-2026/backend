locals {
  gwin_roles = [
    "alb.editor",
    "vpc.publicAdmin",
    "certificate-manager.certificates.downloader",
    "certificate-manager.editor",
    "compute.viewer",
    "k8s.viewer",
  ]
}

resource "yandex_iam_service_account" "gwin" {
  name = "gwin-sa"
}

resource "yandex_resourcemanager_folder_iam_member" "gwin" {
  for_each = toset(local.gwin_roles)

  folder_id = var.folder_id
  role      = each.value
  member    = "serviceAccount:${yandex_iam_service_account.gwin.id}"
}

resource "yandex_iam_service_account_key" "gwin" {
  service_account_id = yandex_iam_service_account.gwin.id
}

resource "local_sensitive_file" "gwin_key" {
  filename        = "${path.module}/gwin-sa-key.json"
  file_permission = "0600"

  content = jsonencode({
    id                 = yandex_iam_service_account_key.gwin.id
    service_account_id = yandex_iam_service_account_key.gwin.service_account_id
    created_at         = yandex_iam_service_account_key.gwin.created_at
    key_algorithm      = yandex_iam_service_account_key.gwin.key_algorithm
    public_key         = yandex_iam_service_account_key.gwin.public_key
    private_key        = yandex_iam_service_account_key.gwin.private_key
  })
}

resource "yandex_vpc_security_group" "alb" {
  name       = "alb-sg"
  network_id = yandex_vpc_network.this.id

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 80
  }

  ingress {
    protocol       = "TCP"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 443
  }

  ingress {
    protocol          = "TCP"
    predefined_target = "loadbalancer_healthchecks"
    port              = 30080
  }

  egress {
    protocol       = "TCP"
    v4_cidr_blocks = yandex_vpc_subnet.this.v4_cidr_blocks
    from_port      = 0
    to_port        = 65535
  }
}

output "alb_security_group_id" {
  value = yandex_vpc_security_group.alb.id
}
