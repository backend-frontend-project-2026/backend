resource "yandex_dns_zone" "this" {
  name   = "roomie-zone"
  zone   = "${trimsuffix(var.domain, ".")}."
  public = true
}

resource "yandex_iam_service_account" "dns_editor" {
  name = "dns-editor-sa"
}

resource "yandex_resourcemanager_folder_iam_member" "dns_editor" {
  folder_id = var.folder_id
  role      = "dns.editor"
  member    = "serviceAccount:${yandex_iam_service_account.dns_editor.id}"
}

resource "yandex_iam_service_account_key" "dns_editor" {
  service_account_id = yandex_iam_service_account.dns_editor.id
}

resource "local_sensitive_file" "dns_editor_key" {
  filename        = "${path.module}/dns-editor-key.json"
  file_permission = "0600"

  content = jsonencode({
    id                 = yandex_iam_service_account_key.dns_editor.id
    service_account_id = yandex_iam_service_account_key.dns_editor.service_account_id
    created_at         = yandex_iam_service_account_key.dns_editor.created_at
    key_algorithm      = yandex_iam_service_account_key.dns_editor.key_algorithm
    public_key         = yandex_iam_service_account_key.dns_editor.public_key
    private_key        = yandex_iam_service_account_key.dns_editor.private_key
  })
}

