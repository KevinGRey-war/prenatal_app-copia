$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $PSScriptRoot

$pythonCandidates = @('.venv-current\Scripts\python.exe', 'venv\Scripts\python.exe', '.venv\Scripts\python.exe')
$appPython = $null
foreach ($candidate in $pythonCandidates) {
    $candidatePath = Join-Path $PSScriptRoot $candidate
    if (Test-Path -LiteralPath $candidatePath) {
        & $candidatePath -c 'import streamlit' 2>$null
        if ($LASTEXITCODE -eq 0) { $appPython = $candidatePath; break }
    }
}
if (-not $appPython) { throw 'No hay un entorno de Python con Streamlit. Instala requirements.txt en un entorno virtual de esta carpeta.' }
$savedNode = $env:NODE_EXE
$savedPdfPython = $env:PDF_PYTHON_EXE
$nodeCommand = Get-Command node -ErrorAction SilentlyContinue
if ($nodeCommand) { $env:NODE_EXE = $nodeCommand.Source }
$env:PDF_PYTHON_EXE = $appPython

try {
    & $appPython -m streamlit run "$PSScriptRoot\app.py" --server.address 127.0.0.1 --server.port 8501 --server.headless false --browser.gatherUsageStats false
}
finally {
    $env:NODE_EXE = $savedNode
    $env:PDF_PYTHON_EXE = $savedPdfPython
}
