# Безопасность Roomie Match в Minikube

Выполняйте команды из корня backend. Соседний каталог frontend содержит клиент. Для изоляции используется профиль roomie-security с собственной сетью Calico. Существующие локальные backend-secret.yaml и postgres-secret.yaml должны находиться в k8s. При переносе на новый ПК создайте два Secret в namespace roomie-match. Ключи backend-secret — DB_USER, DB_PASSWORD, DB_NAME, JWT_SECRET_KEY; ключи postgres-secret — POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB. Реквизиты подключения к БД в обоих файлах должны совпадать.

```powershell
minikube start -p roomie-security --driver=docker --cni=calico --memory=4096 --cpus=2 --keep-context
docker build -t roomie-match-backend:local .
docker build --build-arg VITE_API_BASE_URL=/ -t roomie-match-frontend:security ../frontend
minikube -p roomie-security image load roomie-match-backend:local
minikube -p roomie-security image load roomie-match-frontend:security
./k8s/security/deploy.ps1
./k8s/security/viewer.ps1
kubectl --context=roomie-security -n kube-system get ds calico-node
kubectl --context=roomie-viewer-local get pods
kubectl --context=roomie-viewer-local auth can-i delete pods
kubectl --context=roomie-viewer-local auth can-i get secrets
```

Последние две команды должны вернуть no. Откройте Headlamp Desktop, выберите контекст **roomie-viewer-local**. В настройках кластера задайте доступный namespace **roomie-match**, затем откройте Workloads → Pods. Снимок этого экрана подходит для отчёта. Сертификат пользователя запрашивается на сутки. Перед следующей демонстрацией повторите viewer.ps1.

## Проверка сбоя

ntfy работает внутри учебного кластера. В отдельном терминале запустите:

```powershell
kubectl --context=roomie-security -n roomie-match port-forward svc/ntfy 8088:8080
```

Откройте страницу темы, затем создайте под с предсказуемым кодом завершения:

```powershell
$b64 = kubectl --context=roomie-security -n roomie-match get secret ntfy-topic -o jsonpath='{.data.topic}'
$topic = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64))
Start-Process "http://localhost:8088/$topic"
kubectl --context=roomie-security -n roomie-match run watcher-demo-2 --image=python:3.13-alpine --restart=Never --command -- python -c "raise SystemExit(42)"
kubectl --context=roomie-security -n roomie-match logs deploy/pod-watcher --tail=10
```

В теме появится сообщение с именем пода и exit=42. После показа удалите тестовый под по имени. Watcher опрашивает API каждые пять секунд, читает только поды своего namespace и повторяет отправку после сетевой ошибки. История уведомлений в этом учебном ntfy временная.

## Проверка сети и UID

Браузер обращается к frontend, nginx проксирует /api/ на backend:8000, backend обращается к postgres:5432. Watcher имеет доступ к API и ntfy:8080. DNS разрешён через CoreDNS, остальные соединения ограничены политикой deny-by-default. SMTP отключён в учебном ConfigMap.

```powershell
kubectl --context=roomie-security -n roomie-match exec deploy/frontend -- id -u
kubectl --context=roomie-security -n roomie-match exec deploy/backend -- id -u
kubectl --context=roomie-security -n roomie-match exec postgres-0 -- id -u
kubectl --context=roomie-security -n roomie-match exec deploy/backend -- python -c "import socket; socket.create_connection(('postgres',5432),3).close()"
kubectl --context=roomie-security -n roomie-match exec deploy/pod-watcher -- python -c "import socket; socket.create_connection(('postgres',5432),3)"
kubectl --context=roomie-security -n roomie-match port-forward svc/frontend 13000:80
```

Ожидаемые UID соответственно 101, 1000, 999. Соединение от backend открывается, а от watcher завершается по тайм-ауту. После показа остановите профиль командой `minikube stop -p roomie-security`.

[Материалы преподавателя](https://docs.simple-env.site/Enterprise/First-semester/K8s-security/)
