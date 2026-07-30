[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SiteRoot,

    [uri]$PublicUrl,

    [switch]$BuiltSite,

    [switch]$Online
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Net.Http
$resolvedRoot = (Resolve-Path -LiteralPath $SiteRoot).Path
$findings = [System.Collections.Generic.List[object]]::new()
$onlineSummary = [System.Collections.Generic.List[string]]::new()

function Add-Finding {
    param(
        [ValidateSet('Critical', 'High', 'Medium', 'Low')]
        [string]$Severity,
        [string]$Rule,
        [string]$File,
        [string]$Message
    )

    $findings.Add([pscustomobject]@{
        Severity = $Severity
        Rule     = $Rule
        File     = $File
        Message  = $Message
    })
}

function Get-RelativePath {
    param([string]$Path)

    $fullPath = [System.IO.Path]::GetFullPath($Path)
    if (-not $fullPath.StartsWith(
        $resolvedRoot,
        [System.StringComparison]::OrdinalIgnoreCase
    )) {
        throw "Path is outside the scan root: $fullPath"
    }

    return $fullPath.Substring($resolvedRoot.Length).TrimStart('\', '/')
}

function Get-HeadResult {
    param([uri]$Uri)

    $handler = [System.Net.Http.HttpClientHandler]::new()
    $handler.AllowAutoRedirect = $false
    $client = [System.Net.Http.HttpClient]::new($handler)
    $client.DefaultRequestHeaders.UserAgent.ParseAdd('portfolio-security-check/1.0')
    $request = [System.Net.Http.HttpRequestMessage]::new(
        [System.Net.Http.HttpMethod]::Head,
        $Uri
    )

    try {
        $response = $client.SendAsync($request).GetAwaiter().GetResult()
        return [pscustomobject]@{
            StatusCode = [int]$response.StatusCode
            Location   = $response.Headers.Location
        }
    }
    finally {
        $request.Dispose()
        $client.Dispose()
        $handler.Dispose()
    }
}

$allFiles = Get-ChildItem -LiteralPath $resolvedRoot -Recurse -File -Force
$textExtensions = @(
    '.html', '.htm', '.css', '.js', '.mjs', '.json', '.xml',
    '.md', '.liquid', '.yml', '.yaml', '.rb', '.txt'
)
$webExtensions = @('.html', '.htm', '.css', '.js', '.mjs', '.liquid')
$restrictedExtensions = @(
    '.dat', '.lic', '.key', '.pem', '.p12', '.pfx',
    '.sof', '.pof', '.jic', '.qar', '.qpf', '.qsf',
    '.zip', '.7z', '.rar'
)

foreach ($file in $allFiles) {
    $relative = Get-RelativePath -Path $file.FullName
    $extension = $file.Extension.ToLowerInvariant()

    if (
        $restrictedExtensions -contains $extension -or
        $file.Name -match '^(?i)(\.env(?:\..+)?|id_rsa|id_ed25519|credentials?|recovery[-_ ]?codes?)$'
    ) {
        Add-Finding -Severity Critical -Rule 'restricted-file' -File $relative `
            -Message 'Restricted credential, license, archive, or EDA file must not enter the repository or build.'
    }

    if ($extension -eq '.map') {
        Add-Finding -Severity High -Rule 'source-map' -File $relative `
            -Message 'Production source maps are not permitted in the public site.'
    }

    if (
        $BuiltSite -and
        $extension -in @('.ps1', '.psm1', '.bat', '.cmd', '.exe', '.dll', '.rb', '.lock', '.yml', '.yaml')
    ) {
        Add-Finding -Severity High -Rule 'build-artifact' -File $relative `
            -Message 'Development or executable artifact is present in the public build.'
    }

    if ($textExtensions -notcontains $extension) {
        continue
    }

    $content = Get-Content -Raw -LiteralPath $file.FullName

    $secretPatterns = [ordered]@{
        'private-key' = '-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
        'github-token' = '\bgh[pousr]_[A-Za-z0-9_]{20,}\b'
        'aws-access-key' = '\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'
        'generic-secret-assignment' = '(?im)^\s*(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*["''][^"'']{8,}["'']'
    }

    foreach ($entry in $secretPatterns.GetEnumerator()) {
        if ($content -match $entry.Value) {
            Add-Finding -Severity Critical -Rule $entry.Key -File $relative `
                -Message 'Possible secret detected. The matched value is intentionally not printed.'
        }
    }

    if ($webExtensions -contains $extension) {
        $webRules = @(
            @{
                Severity = 'High'
                Rule = 'mixed-content'
                Pattern = '(?i)(?:\b(?:src|href|action|poster|data)\s*=\s*["'']\s*http://|url\(\s*["'']?http://|fetch\(\s*["'']http://)'
                Message = 'HTTP resource reference can create Mixed Content.'
            },
            @{
                Severity = 'High'
                Rule = 'dom-html-sink'
                Pattern = '(?i)\b(?:innerHTML|outerHTML|insertAdjacentHTML|document\.write|document\.writeln)\b'
                Message = 'Unsafe DOM HTML sink requires removal or explicit security review.'
            },
            @{
                Severity = 'Critical'
                Rule = 'dynamic-code'
                Pattern = '(?i)(?:\beval\s*\(|\bnew\s+Function\s*\()'
                Message = 'Dynamic code execution is not permitted.'
            },
            @{
                Severity = 'High'
                Rule = 'javascript-url'
                Pattern = '(?i)(?:href|src)\s*=\s*["'']\s*javascript:'
                Message = 'javascript: URL is not permitted.'
            },
            @{
                Severity = 'Medium'
                Rule = 'inline-event-handler'
                Pattern = '(?i)\s+on(?:click|load|error|mouseover|focus|submit)\s*='
                Message = 'Inline event handlers weaken a strict CSP; use an external script.'
            },
            @{
                Severity = 'High'
                Rule = 'external-script'
                Pattern = '(?i)<script\b[^>]*\bsrc\s*=\s*["'']https?://'
                Message = 'External executable scripts are outside the approved minimal architecture.'
            },
            @{
                Severity = 'High'
                Rule = 'stateful-form'
                Pattern = '(?i)<form\b'
                Message = 'Forms require explicit approval and a revised threat model.'
            },
            @{
                Severity = 'High'
                Rule = 'unapproved-platform'
                Pattern = '(?i)\b(?:firebase|supabase|web3|ethereum|walletconnect|serviceWorker\.register)\b'
                Message = 'Unapproved dynamic platform, Web3 SDK, or Service Worker reference detected.'
            },
            @{
                Severity = 'Medium'
                Rule = 'local-absolute-path'
                Pattern = '(?i)(?:[A-Z]:\\Users\\|/Users/|/home/|/mnt/)'
                Message = 'Local absolute path can disclose account or workstation information.'
            }
        )

        foreach ($rule in $webRules) {
            if ($content -match $rule.Pattern) {
                Add-Finding -Severity $rule.Severity -Rule $rule.Rule -File $relative `
                    -Message $rule.Message
            }
        }
    }

    if ($extension -in @('.html', '.htm')) {
        if ($content -notmatch '(?i)<meta\b[^>]*http-equiv\s*=\s*["'']Content-Security-Policy["'']') {
            Add-Finding -Severity Medium -Rule 'csp-meta-missing' -File $relative `
                -Message 'No CSP meta policy found. GitHub Pages cannot provide arbitrary response headers.'
        }

        $blankTargets = [regex]::Matches(
            $content,
            '(?is)<a\b(?=[^>]*\btarget\s*=\s*["'']_blank["''])[^>]*>'
        )
        foreach ($target in $blankTargets) {
            if ($target.Value -notmatch '(?i)\brel\s*=\s*["''][^"'']*\bnoopener\b') {
                Add-Finding -Severity Medium -Rule 'noopener-missing' -File $relative `
                    -Message 'target="_blank" link is missing rel="noopener".'
                break
            }
        }
    }

    if ($relative -match '^(?i)\.github\\workflows\\.+\.ya?ml$') {
        if ($content -notmatch '(?m)^permissions\s*:') {
            Add-Finding -Severity High -Rule 'workflow-permissions' -File $relative `
                -Message 'Workflow must declare explicit minimum permissions.'
        }

        if ($content -match '(?m)^\s*pull_request_target\s*:') {
            Add-Finding -Severity Critical -Rule 'privileged-pr-trigger' -File $relative `
                -Message 'pull_request_target requires explicit security approval and is not allowed by default.'
        }

        foreach ($use in [regex]::Matches($content, '(?m)^\s*uses\s*:\s*[^@\s]+@([^\s#]+)')) {
            if ($use.Groups[1].Value -notmatch '^[0-9a-fA-F]{40}$') {
                Add-Finding -Severity High -Rule 'action-not-sha-pinned' -File $relative `
                    -Message 'Every Action must be pinned to a full 40-character commit SHA.'
                break
            }
        }
    }
}

if (
    (Test-Path -LiteralPath (Join-Path $resolvedRoot 'package.json')) -and
    -not (
        (Test-Path -LiteralPath (Join-Path $resolvedRoot 'package-lock.json')) -or
        (Test-Path -LiteralPath (Join-Path $resolvedRoot 'pnpm-lock.yaml')) -or
        (Test-Path -LiteralPath (Join-Path $resolvedRoot 'yarn.lock'))
    )
) {
    Add-Finding -Severity High -Rule 'node-lockfile-missing' -File 'package.json' `
        -Message 'Node dependency manifest exists without a lockfile.'
}

if (
    (Test-Path -LiteralPath (Join-Path $resolvedRoot 'Gemfile')) -and
    -not (Test-Path -LiteralPath (Join-Path $resolvedRoot 'Gemfile.lock'))
) {
    Add-Finding -Severity High -Rule 'bundler-lockfile-missing' -File 'Gemfile' `
        -Message 'Gemfile exists without Gemfile.lock.'
}

if ($Online) {
    if (-not $PublicUrl) {
        throw '-PublicUrl is required with -Online.'
    }

    $httpsBuilder = [System.UriBuilder]::new($PublicUrl)
    $httpsBuilder.Scheme = 'https'
    $httpsBuilder.Port = -1
    $httpsUrl = $httpsBuilder.Uri

    $httpBuilder = [System.UriBuilder]::new($httpsUrl)
    $httpBuilder.Scheme = 'http'
    $httpBuilder.Port = -1
    $httpUrl = $httpBuilder.Uri

    try {
        $httpResult = Get-HeadResult -Uri $httpUrl
        $locationText = if ($httpResult.Location) { $httpResult.Location.ToString() } else { '(none)' }
        $onlineSummary.Add("HTTP $($httpResult.StatusCode), Location=$locationText")
        $validRedirectCodes = @(301, 302, 307, 308)
        $validLocation = $false
        if ($httpResult.Location) {
            $absoluteLocation = [uri]::new($httpUrl, $httpResult.Location)
            $validLocation = (
                $absoluteLocation.Scheme -eq 'https' -and
                $absoluteLocation.Host -eq $httpsUrl.Host
            )
        }
        if (
            $validRedirectCodes -notcontains $httpResult.StatusCode -or
            -not $validLocation
        ) {
            Add-Finding -Severity High -Rule 'https-redirect' -File $httpUrl.AbsoluteUri `
                -Message 'HTTP must redirect to HTTPS on the same host.'
        }
    }
    catch {
        Add-Finding -Severity High -Rule 'http-check-failed' -File $httpUrl.AbsoluteUri `
            -Message "HTTP check failed: $($_.Exception.Message)"
    }

    try {
        $httpsResult = Get-HeadResult -Uri $httpsUrl
        $onlineSummary.Add("HTTPS $($httpsResult.StatusCode)")
        if ($httpsResult.StatusCode -lt 200 -or $httpsResult.StatusCode -ge 300) {
            Add-Finding -Severity High -Rule 'https-status' -File $httpsUrl.AbsoluteUri `
                -Message "Expected HTTPS 2xx, received $($httpsResult.StatusCode)."
        }
    }
    catch {
        Add-Finding -Severity Critical -Rule 'https-check-failed' -File $httpsUrl.AbsoluteUri `
            -Message "HTTPS check failed: $($_.Exception.Message)"
    }

    $tcpClient = $null
    $sslStream = $null
    try {
        $tcpClient = [System.Net.Sockets.TcpClient]::new($httpsUrl.Host, 443)
        $sslStream = [System.Net.Security.SslStream]::new($tcpClient.GetStream(), $false)
        $sslStream.AuthenticateAsClient($httpsUrl.Host)
        $certificate = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new(
            $sslStream.RemoteCertificate
        )
        $onlineSummary.Add(
            "TLS $($sslStream.SslProtocol), subject=$($certificate.Subject), expires=$($certificate.NotAfter.ToString('o'))"
        )
        if ((Get-Date) -lt $certificate.NotBefore -or (Get-Date) -gt $certificate.NotAfter) {
            Add-Finding -Severity Critical -Rule 'certificate-expired' -File $httpsUrl.Host `
                -Message 'TLS certificate is outside its validity period.'
        }
    }
    catch {
        Add-Finding -Severity Critical -Rule 'tls-validation' -File $httpsUrl.Host `
            -Message "TLS trust or hostname validation failed: $($_.Exception.Message)"
    }
    finally {
        if ($sslStream) { $sslStream.Dispose() }
        if ($tcpClient) { $tcpClient.Dispose() }
    }
}

if ($onlineSummary.Count -gt 0) {
    Write-Host 'Online checks:'
    $onlineSummary | ForEach-Object { Write-Host "  $_" }
}

if ($findings.Count -eq 0) {
    Write-Host "PASS: no findings in $resolvedRoot"
    exit 0
}

$severityOrder = @{ Critical = 0; High = 1; Medium = 2; Low = 3 }
$orderedFindings = $findings | Sort-Object @{ Expression = { $severityOrder[$_.Severity] } }, Rule, File
$orderedFindings | Format-Table Severity, Rule, File, Message -AutoSize -Wrap

$blockingCount = @(
    $findings | Where-Object { $_.Severity -in @('Critical', 'High') }
).Count

Write-Host "Findings: $($findings.Count); blocking: $blockingCount"
if ($blockingCount -gt 0) {
    exit 1
}
exit 0
