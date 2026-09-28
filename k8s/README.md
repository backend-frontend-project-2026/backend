# Первый pod в Kubernetes

Манифест `nginx-pod.yaml` повторяет пример из [статьи курса](https://docs.simple-env.site/Enterprise/First-semester/K8s-intro/).

## Запуск в Windows PowerShell

Откройте Docker Desktop и дождитесь готовности движка. После установки minikube откройте новое окно PowerShell, чтобы обновился PATH.

Из корня репозитория:

```powershell
minikube start --driver=docker --cpus=4 --memory=4096 --kubernetes-version=v1.34.11
kubectl --context=minikube apply -f .\k8s\nginx-pod.yaml
kubectl --context=minikube wait --for=condition=Ready pod/nginx --timeout=180s
kubectl --context=minikube get nodes
kubectl --context=minikube get pods -o wide
kubectl --context=minikube logs nginx
```

Здесь используются 4 ГБ памяти вместо 8 ГБ из статьи: Docker на этой машине доступно около 7,6 ГБ. Kubernetes 1.34.11 совместим с установленным kubectl 1.34.1.

Ожидаемый результат: узел `minikube` имеет состояние `Ready`, pod `nginx` — `Running`, готовность `1/1`.

Проверено 8 сентября 2026 года: узел `Ready`, pod `nginx` — `1/1 Running`, 0 перезапусков; HTTP-запрос внутри контейнера вернул `200`.

## Посмотреть страницу nginx

```powershell
kubectl --context=minikube port-forward pod/nginx 8080:80
```

Не закрывая терминал, откройте http://localhost:8080. Завершить проброс порта можно нажатием Ctrl+C.

## Headlamp

Откройте Headlamp через меню «Пуск», выберите кластер `minikube`, затем раздел Pods и namespace `default`. Приложение читает подключение из `%USERPROFILE%\.kube\config`.

## После занятия

```powershell
minikube stop
```

Повторный запуск: `minikube start`. Удалить только учебный pod: `kubectl --context=minikube delete -f .\k8s\nginx-pod.yaml`.

## Расположение данных Docker

Виртуальный диск хранится в `D:\DockerDesktopWSL\disk\docker_data.vhdx`. Прежняя папка `C:\Users\Pc\AppData\Local\Docker\wsl\disk` указывает на неё через NTFS junction. Данные по обоим путям одни и те же. Не удаляйте содержимое этой папки для очистки места.

## Если Docker не запускается

На этой машине Docker Desktop 4.61.0 выдавал ошибку `The file cannot be accessed by the system` для `dockerInference` и `engine.sock`. Для восстановления были переименованы временные папки `%LOCALAPPDATA%\Docker\run` и `%LOCALAPPDATA%\docker-secrets-engine`, пока Docker был закрыт. Старые папки сохранены рядом с суффиксом `.before-k8s-<дата-время>`. Это обход ошибки: после следующего перезапуска она может повториться.

Не используйте `Reset to factory defaults` для этой ошибки: сброс может удалить данные Docker. Описание сходной ошибки: https://github.com/docker/desktop-feedback/issues/460.
