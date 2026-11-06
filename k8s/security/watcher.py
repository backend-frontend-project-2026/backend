import json
import os
import ssl
import time
from pathlib import Path
from urllib.request import Request, urlopen

credentials = Path("/var/run/secrets/kubernetes.io/serviceaccount")
namespace = (credentials / "namespace").read_text().strip()
api = f"https://kubernetes.default.svc/api/v1/namespaces/{namespace}/pods"
tls = ssl.create_default_context(cafile=str(credentials / "ca.crt"))
topic = os.environ["NTFY_TOPIC"]
previous = {}

while True:
    try:
        request = Request(api, headers={"Authorization": "Bearer " + (credentials / "token").read_text().strip()})
        with urlopen(request, context=tls, timeout=10) as response:
            pods = json.load(response)["items"]
        present = set()
        for pod in pods:
            uid = pod["metadata"]["uid"]
            present.add(uid)
            status = pod.get("status", {})
            problems = []
            if status.get("phase") == "Failed":
                problems.append(status.get("reason") or "Failed")
            for container in status.get("initContainerStatuses", []) + status.get("containerStatuses", []):
                state = container["state"]
                waiting = state.get("waiting", {}).get("reason")
                if waiting and waiting not in {"ContainerCreating", "PodInitializing"}:
                    problems.append(waiting)
                termination = state.get("terminated") or container.get("lastState", {}).get("terminated", {})
                if termination.get("exitCode", 0) != 0:
                    problems.append(f"{container['name']} exit={termination['exitCode']} restarts={container['restartCount']}")
            current = tuple(problems)
            if current and previous.get(uid) != current:
                message = f"{namespace}/{pod['metadata']['name']}: {', '.join(current)}"
                with urlopen(f"http://ntfy:8080/{topic}", data=message.encode(), timeout=10) as response:
                    response.read()
                print(message, flush=True)
            previous[uid] = current
        previous = {uid: state for uid, state in previous.items() if uid in present}
    except (OSError, ValueError) as error:
        print(f"Watcher retry: {type(error).__name__}", flush=True)
    time.sleep(5)
