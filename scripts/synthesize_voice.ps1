param([Parameter(Mandatory=$true)][string]$Manifest,
      [Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$speaker = New-Object -ComObject SAPI.SpVoice
$spanish = @($speaker.GetVoices() | Where-Object { $_.GetDescription() -match 'Spanish' })
if ($spanish.Count -eq 0) { throw 'Install a Spanish Windows speech voice before building assets.' }
$speaker.Voice = $spanish[0]
$speaker.Rate = 0
$entries = Get-Content -LiteralPath $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
$count = 0
foreach ($entry in $entries) {
    $destination = Join-Path $OutputDirectory ($entry.id + '.wav')
    if (-not (Test-Path -LiteralPath $destination)) {
        $stream = New-Object -ComObject SAPI.SpFileStream
        $stream.Format.Type = 22
        $stream.Open($destination, 3, $false)
        try {
            $speaker.AudioOutputStream = $stream
            [void]$speaker.Speak($entry.text, 0)
        } finally { $stream.Close() }
    }
    $count++
    if ($count % 50 -eq 0) { Write-Output "Narrated $count of $($entries.Count) clips" }
}
