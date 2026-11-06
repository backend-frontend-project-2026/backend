# Облачный стенд к 11 ноября

Конфигурация адаптирована из [практикума OpenTofu](https://docs.simple-env.site/Enterprise/First-semester/K8s-opentofu/). Создаются отдельная VPC, подсеть, группы безопасности, зональный мастер, одна прерываемая рабочая нода с HDD 30 ГБ, публичная DNS-зона и сервисные аккаунты. В примере из [занятия по Ingress](https://docs.simple-env.site/Enterprise/First-semester/K8s-cloud-ingress/) роль приложения выполняет nginx.

1. Откройте Billing → платёжный аккаунт → Аккаунт → Гранты → Показать все. Проверьте остаток и дату окончания. Условия получения для нового личного аккаунта описаны в [документации Billing](https://yandex.cloud/ru/docs/billing/concepts/bonus-account). Выберите существующий каталог или создайте отдельный учебный. В Quota Manager запросите квоту Compute Cloud «Общий объем HDD-дисков в зоне ru-central1-a» с учётом уже занятых дисков и ещё 30 ГБ. Дождитесь одобрения.
2. Зарегистрируйте домен. Подготовьте OpenTofu и Yandex Cloud CLI, выполните `yc init` с нужным облаком и каталогом. В этой директории создайте `terraform.tfvars` по образцу ниже. Поле domain содержит купленный домен без точки на конце.

```hcl
cloud_id  = "ID_ОБЛАКА"
folder_id = "ID_КАТАЛОГА"
domain    = "example.org"
```

3. В PowerShell из этой директории выполните команды ниже. После plan проверьте каталог, зону и размеры ресурсов. С apply начинается расход гранта. State и файлы ключей доступны локально и исключены из Git.

```powershell
$env:YC_TOKEN = yc iam create-token
tofu init
tofu validate
tofu plan
tofu apply
yc managed-kubernetes cluster get-credentials roomie-cluster --external
kubectl config current-context
kubectl --context=yc-roomie-cluster get nodes
```

4. У регистратора укажите серверы делегирования `ns1.yandexcloud.net` и `ns2.yandexcloud.net`. Проверьте `Resolve-DnsName example.org -Type NS` через публичный резолвер.
5. В созданном кластере откройте Marketplace и установите три приложения. Для **cert-manager с плагином Yandex Cloud DNS ACME** укажите email для Let's Encrypt, ID каталога зоны и содержимое dns-editor-key.json. Проверьте `kubectl --context=yc-roomie-cluster get clusterissuer yc-clusterissuer` (Ready). Для **ExternalDNS** выберите Yandex Cloud DNS, тот же каталог и DNS-ключ, источник Ingress, если он настраивается. Для **Gwin** используйте gwin-sa-key.json. Дождитесь Running у контроллеров и проверьте `kubectl --context=yc-roomie-cluster get ingressclass gwin-default`. Параметры установки показаны в [статье курса](https://docs.simple-env.site/Enterprise/First-semester/K8s-cloud-ingress/).
6. Выполните из этой директории, подставив свой домен. Gwin публикует адрес ALB в статусе Ingress, ExternalDNS создаёт A-запись, cert-manager получает сертификат через DNS-01 и сохраняет в Secret. Gwin импортирует его в Certificate Manager.

```powershell
$domain = 'example.org'
$sg = tofu output -raw alb_security_group_id
$manifest = (Get-Content ingress.yaml.in -Raw).Replace('DOMAIN',$domain).Replace('ALB_SECURITY_GROUP',$sg)
$manifest | kubectl --context=yc-roomie-cluster apply -f -
kubectl --context=yc-roomie-cluster -n nginx-test get ingress,certificate
kubectl --context=yc-roomie-cluster -n nginx-test wait --for=condition=Ready certificate/example-com-tls --timeout=10m
yc dns zone list-records --name roomie-zone
yc certificate-manager certificate list
Resolve-DnsName "app.$domain" -Type A
curl.exe --fail --head "https://app.$domain/"
```

Для сдачи сохраните адрес Ingress, A-запись с тем же IP, Certificate Ready, запись в Certificate Manager и ответ HTTPS 200.

7. После демонстрации удалите учебный Ingress, пока Gwin ещё работает. Дождитесь исчезновения его ALB, затем удалите учебный namespace, приложения Marketplace и ресурсы OpenTofu. Проверьте остатки балансировщиков, сертификатов, дисков и публичных адресов в каталоге. Если нужно сохранить делегирование, учитывайте, что destroy удаляет и зону.

```powershell
kubectl --context=yc-roomie-cluster -n nginx-test delete ingress nginx
yc alb load-balancer list
kubectl --context=yc-roomie-cluster delete namespace nginx-test
# После удаления приложений Marketplace и проверки ALB
tofu plan -destroy
tofu destroy
yc load-balancer network-load-balancer list
yc alb load-balancer list
```
