$ErrorActionPreference = 'Stop'
$admin = 'roomie-security'
$user = 'roomie-viewer'
$context = 'roomie-viewer-local'
$openssl = (Get-Command openssl -ErrorAction SilentlyContinue).Source
if (!$openssl) { $openssl = "$env:ProgramFiles/Git/usr/bin/openssl.exe" }
function Check { if ($LASTEXITCODE) { throw "Command failed ($LASTEXITCODE)" } }
$tempDir = New-Item -ItemType Directory -Path (Join-Path ([IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString('N')))
try {
    "[req]`ndistinguished_name=dn`n[dn]" | Set-Content -Encoding ascii "$tempDir/req.cnf"
    & $openssl req -config "$tempDir/req.cnf" -new -newkey rsa:2048 -nodes -subj "/CN=$user" -keyout "$tempDir/key.pem" -out "$tempDir/request.pem"
    Check
    $name = "$user-$([guid]::NewGuid().ToString('N'))"
    $request = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$tempDir/request.pem"))
    @{apiVersion='certificates.k8s.io/v1'; kind='CertificateSigningRequest'; metadata=@{name=$name};
      spec=@{request=$request; signerName='kubernetes.io/kube-apiserver-client'; expirationSeconds=86400; usages=@('client auth')}
    } | ConvertTo-Json -Depth 5 | kubectl --context=$admin create -f -
    Check
    kubectl --context=$admin certificate approve $name
    Check
    kubectl --context=$admin wait "--for=jsonpath={.status.certificate}" "csr/$name" --timeout=30s
    Check
    $cert = kubectl --context=$admin get csr $name -o jsonpath='{.status.certificate}'
    Check
    [IO.File]::WriteAllBytes("$tempDir/cert.pem",[Convert]::FromBase64String($cert))
    kubectl config set-credentials $user "--client-key=$tempDir/key.pem" "--client-certificate=$tempDir/cert.pem" --embed-certs=true
    Check
    kubectl config set-context $context --cluster=$admin --user=$user --namespace=roomie-match
    Check
} finally {
    foreach ($file in 'key.pem','cert.pem','request.pem','req.cnf') {
        $path = Join-Path $tempDir.FullName $file
        if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path -Force }
    }
    Remove-Item -LiteralPath $tempDir.FullName
}
