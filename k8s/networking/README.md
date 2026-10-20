# ДЗ 3: локальные домены, Ingress и HTTPS

Задание: установить ingress controller, создать Ingress для сервисов, настроить
локальные домены, установить cert-manager и выдать self-signed сертификаты.
Tailscale — необязательная часть, в этой работе не устанавливается.

## Как проходит запрос

```text
Браузер → hosts: 127.0.0.1 → kubectl port-forward :80/:443
        → Traefik → Ingress → Service → Pod
                  ↑
     TLS Secret ← Certificate ← self-signed Issuer (cert-manager)
```

| Адрес | Назначение |
|---|---|
| https://roomie.test | Frontend |
| https://roomie.test/api/v1/cities | API через домен frontend |
| https://api.roomie.test/docs | Swagger UI backend |
| https://api.roomie.test/openapi.json | Спецификация API |

Префикс `/api` сохраняется: backend уже обслуживает `/api/v1`.
Ingress `frontend` направляет `/api` в backend, остальные пути — во frontend.
Ingress `backend` направляет запросы отдельного API-домена в backend.
В закреплённом frontend-образе активная настройка API использует относительный
путь `/api/v1`, поэтому API доступно через тот же HTTPS-домен без mixed content.
Загруженные backend файлы сохраняются в PVC `backend-media`; frontend nginx
монтирует его только для чтения и отдаёт `/media/` по HTTPS. Это локальный
одноузловой minikube: ReadWriteOnce-том доступен обоим Pods на одном узле.
HTTP перенаправляется на HTTPS средствами Traefik. PostgreSQL доступен только
внутри кластера; сервисы приложения имеют тип ClusterIP.

На Windows с Docker driver адрес узла minikube может быть недоступен напрямую.
Поэтому пробрасываются именно порты ingress controller, а маршрутизацию и TLS
всё равно выполняет Traefik в Kubernetes.

## 1. Инструменты и отдельный кластер

Команды выполняются из корня backend в PowerShell. Нужны работающий Docker
Desktop с Linux containers, minikube, kubectl и Helm в PATH.
Используемые версии: minikube 1.39.0, Kubernetes/kubectl 1.34.11, Helm 4.3.1,
Traefik chart 42.1.0, cert-manager 1.21.2.

Если инструменты скачаны в `.local-k8s`, добавьте их в PATH текущего терминала:

```powershell
$env:Path = "$PWD\.local-k8s;$PWD\.local-k8s\windows-amd64;$env:Path"
docker info
minikube version
kubectl version --client
helm version
minikube start -p roomie-devops --driver=docker --cpus=4 --memory=4096 --kubernetes-version=v1.34.11 --base-image=gcr.io/k8s-minikube/kicbase:v0.0.51 --keep-context
kubectl --context=roomie-devops get nodes
```

Если кэш minikube хранится на другом диске, перед командами запуска задайте
`$env:MINIKUBE_HOME` в текущем терминале. Например:

```powershell
$env:MINIKUBE_HOME = 'D:\Minikube\.minikube'
```

На компьютере эта переменная также сохранена в настройках пользователя
Windows. Уже открытые терминалы и IDE могут требовать перезапуска для её загрузки.
Расположение диска Docker меняется отдельно через Docker Desktop.

Профиль `roomie-devops` отделяет домашку от других кластеров. Все команды ниже
явно указывают контекст; переключать глобальный kubectl context не нужно.

## 2. cert-manager и ingress controller

```powershell
kubectl --context=roomie-devops apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.21.2/cert-manager.yaml
kubectl --context=roomie-devops -n cert-manager rollout status deployment/cert-manager --timeout=300s
kubectl --context=roomie-devops -n cert-manager rollout status deployment/cert-manager-cainjector --timeout=300s
kubectl --context=roomie-devops -n cert-manager rollout status deployment/cert-manager-webhook --timeout=300s
helm upgrade --install traefik https://traefik.github.io/charts/traefik/traefik-42.1.0.tgz --kube-context roomie-devops --namespace ingress-system --create-namespace --values .\k8s\networking\traefik-values.yaml --wait --timeout 5m
```

Команды устанавливают официальный release cert-manager, ожидают готовности
его трёх Deployment, затем устанавливают Traefik через Helm с параметрами
из `traefik-values.yaml`. Если команда завершилась ошибкой, устраните её
перед выполнением следующей команды.

Проверка:

```powershell
kubectl --context=roomie-devops -n cert-manager get pods
kubectl --context=roomie-devops -n ingress-system get pods,services
kubectl --context=roomie-devops get ingressclass
```

Ожидается готовый `IngressClass` с именем `traefik`, а Pods контроллеров — Running.
Используется стандартный Kubernetes Ingress, Traefik CRD для маршрутов не нужны.

## 3. Учётные данные и приложение

```powershell
if (-not (Test-Path .\k8s\local.secret.env)) { Copy-Item .\k8s\secrets.env.example .\k8s\local.secret.env }
notepad .\k8s\local.secret.env
```

Замените `DB_PASSWORD` и `JWT_SECRET_KEY` своими локальными значениями;
JWT-ключ должен содержать не менее 32 символов. Файл исключён из Git.
При повторном запуске используйте прежний пароль: PostgreSQL хранит данные
в PVC, изменение Secret не меняет пароль в уже созданной базе.

```powershell
docker build -t roomie-match-backend:local .
docker pull annittabonita/roomie-match-frontend@sha256:48f9b7ae4d0df77314a8d87b9f9f9083cbedc35247f5e83e5103e7dc8d9fb182
docker tag annittabonita/roomie-match-frontend@sha256:48f9b7ae4d0df77314a8d87b9f9f9083cbedc35247f5e83e5103e7dc8d9fb182 roomie-match-frontend:local
minikube -p roomie-devops image load roomie-match-backend:local roomie-match-frontend:local
kubectl --context=roomie-devops apply -f .\k8s\namespace.yaml
kubectl --context=roomie-devops -n roomie-match create secret generic backend-secret --from-env-file=.\k8s\local.secret.env --dry-run=client -o yaml | kubectl --context=roomie-devops apply -f -

# PostgreSQL использует те же значения под именами POSTGRES_*.
$dbSettings = @{}
Get-Content .\k8s\local.secret.env | ForEach-Object {
    if ($_ -match '^DB_(USER|PASSWORD|NAME)=(.*)$') {
        $key = if ($Matches[1] -eq 'NAME') { 'POSTGRES_DB' } else { 'POSTGRES_' + $Matches[1] }
        $dbSettings[$key] = $Matches[2]
    }
}
$postgresSecret = @{
    apiVersion = 'v1'
    kind = 'Secret'
    metadata = @{ name = 'postgres-secret'; namespace = 'roomie-match' }
    type = 'Opaque'
    stringData = $dbSettings
}
$postgresSecret | ConvertTo-Json -Depth 4 | kubectl --context=roomie-devops apply -f -
Remove-Variable dbSettings,postgresSecret

kubectl --context=roomie-devops apply -k .\k8s
kubectl --context=roomie-devops -n roomie-match rollout status statefulset/postgres --timeout=300s
kubectl --context=roomie-devops -n roomie-match rollout status deployment/backend --timeout=300s
kubectl --context=roomie-devops -n roomie-match rollout status deployment/frontend --timeout=300s
kubectl --context=roomie-devops -n roomie-match wait --for=condition=Ready certificate/frontend-tls certificate/backend-tls --timeout=300s
```

Команды собирают backend из текущей ветки, скачивают закреплённый по digest образ
frontend команды, загружают оба образа в minikube, создают два Secret и применяют
манифесты. Значения в env-файле указываются без кавычек и без пробелов вокруг `=`.
Не выводите содержимое Secret в терминал и не добавляйте его в Git.
Если образы с тегом `local` пересобраны или изменились Secret, после применения
манифестов выполните `kubectl --context=roomie-devops -n roomie-match rollout restart deployment/backend deployment/frontend`
и повторите команды `rollout status` для обоих Deployment.
Backend ожидает PostgreSQL, применяет миграции и запускает bootstrap перед gunicorn.

Секреты приложения не записываются в YAML репозитория. TLS Secret создаются
самим cert-manager из ресурсов Certificate. Первый учебный Pod nginx в
`k8s/nginx-pod.yaml` не входит в Kustomization этой работы.

## 4. Локальные домены

Откройте PowerShell **от имени администратора**:

```powershell
Copy-Item "$env:SystemRoot\System32\drivers\etc\hosts" "$env:TEMP\hosts-backup-$(Get-Date -Format yyyyMMdd-HHmmss)"
notepad "$env:SystemRoot\System32\drivers\etc\hosts"
```

Команды сохраняют резервную копию hosts и открывают файл. Добавьте строку,
если этих доменов ещё нет:

```text
127.0.0.1 roomie.test api.roomie.test
```

Если домен уже связан с другим IP, исправьте его запись; не добавляйте дубликаты.
Сохраните файл.
Файл Windows: `C:\Windows\System32\drivers\etc\hosts`.

## 5. Открыть доступ и проверить

В отдельном терминале с настроенным PATH:

```powershell
kubectl --context=roomie-devops -n ingress-system port-forward --address=127.0.0.1 service/traefik 80:80 443:443
```

Не закрывайте этот терминал: он соединяет localhost:80/443 с сервисом Traefik.
Оба порта должны быть свободны. Если они заняты другим проектом, сначала
определите, какое приложение их использует; не останавливайте чужие контейнеры
вслепую. Завершение port-forward: Ctrl+C.

В другом терминале:

```powershell
kubectl --context=roomie-devops -n roomie-match get pods,services,ingress
kubectl --context=roomie-devops -n roomie-match get issuer,certificate
kubectl --context=roomie-devops -n roomie-match wait --for=condition=Ready certificate/frontend-tls certificate/backend-tls --timeout=300s
curl.exe -I http://roomie.test
curl.exe -I http://api.roomie.test
```

Ожидается `1/1 Running` у Pods приложения и `Ready=True` у сертификатов.
HTTP-запросы должны вернуть перенаправление с `Location: https://...`.
Пустой столбец ADDRESS у Ingress допустим при ClusterIP и port-forward.

Откройте все четыре HTTPS-адреса из таблицы выше в браузере: должны появиться
frontend, JSON со списком городов, Swagger UI и OpenAPI JSON. В инструментах
разработчика браузера (Network) проверьте HTTP 200. Через просмотр сертификата
проверьте соответствие домена и срок действия.

Откройте https://roomie.test и https://api.roomie.test/docs.
Браузер предупреждает о недоверенном сертификате: это ожидаемо для self-signed.
Для локальной демонстрации разрешите переход в браузере. Публичный домен,
Let's Encrypt и доступ из интернета для задания не требуются.

Посмотреть сертификаты без вывода приватных ключей:

```powershell
kubectl --context=roomie-devops -n roomie-match get issuer,certificate
kubectl --context=roomie-devops -n roomie-match describe certificate frontend-tls
kubectl --context=roomie-devops -n roomie-match describe certificate backend-tls
kubectl --context=roomie-devops -n roomie-match get secret frontend-tls backend-tls
```

## Если что-то не запускается

```powershell
kubectl --context=roomie-devops -n roomie-match get pods,pvc,ingress,certificate
kubectl --context=roomie-devops -n roomie-match get events --sort-by=.lastTimestamp
kubectl --context=roomie-devops -n roomie-match logs deployment/backend --all-containers --tail=80
kubectl --context=roomie-devops -n ingress-system logs deployment/traefik --tail=80
```

`ImagePullBackOff` — проверить интернет и загрузку образа.
`CreateContainerConfigError` — проверить наличие `backend-secret` и `postgres-secret`.
`503` — проверить readiness Pods и EndpointSlice сервисов.
`404` от Traefik — проверить домен запроса и `ingressClassName`.
Ошибка соединения с localhost — проверить работающий port-forward.

