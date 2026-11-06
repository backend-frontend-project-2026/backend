param()
$ErrorActionPreference = 'Stop'
$profileName = 'roomie-security'
function Kube {
    & kubectl --context=$profileName @args
    if ($LASTEXITCODE) { throw "kubectl failed ($LASTEXITCODE)" }
}
$root = Split-Path $PSScriptRoot
Kube apply -f "$root/namespace.yaml"
Kube apply -f "$root/backend-configmap.yaml"
Kube -n roomie-match patch configmap backend-config --type merge -p '{"data":{"FRONTEND_BASE_URL":"http://127.0.0.1:13000","MEDIA_BASE_URL":"http://127.0.0.1:13000/media"}}'
Get-ChildItem $root -Filter '*.yaml' | Where-Object Name -notin 'namespace.yaml','backend-configmap.yaml','nginx-pod.yaml','kustomization.yaml' | ForEach-Object { Kube apply -f $_.FullName }
Kube -n roomie-match set image deployment/frontend frontend=roomie-match-frontend:security
$existing = Kube -n roomie-match get secret ntfy-topic --ignore-not-found -o name
if (!$existing) {
    $topic = [guid]::NewGuid().ToString('N')
    Kube -n roomie-match create secret generic ntfy-topic "--from-literal=topic=$topic"
}
# Calico may see either the service VIP or the translated API endpoint.
$vip = Kube -n default get svc kubernetes -o jsonpath='{.spec.clusterIP}'
$endpoints = (Kube -n default get endpoints kubernetes -o json | ConvertFrom-Json).subsets
$rules = @(@{to=@(@{ipBlock=@{cidr="$vip/32"}}); ports=@(@{port=443})})
foreach ($subset in $endpoints) {
    foreach ($address in $subset.addresses) {
        $rules += @{to=@(@{ipBlock=@{cidr="$($address.ip)/32"}}); ports=@($subset.ports | ForEach-Object { @{port=$_.port} })}
    }
}
@{apiVersion='networking.k8s.io/v1'; kind='NetworkPolicy'; metadata=@{name='watcher-api'; namespace='roomie-match'};
  spec=@{podSelector=@{matchLabels=@{app='pod-watcher'}}; policyTypes=@('Egress'); egress=$rules}
} | ConvertTo-Json -Depth 12 | kubectl --context=$profileName apply -f -
if ($LASTEXITCODE) { throw 'API policy failed' }
Kube apply -k $PSScriptRoot
