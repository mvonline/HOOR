[CmdletBinding()]
param(
    [string]$CommitMessage = 'Publish Rad-e Hoor site update'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$SiteRoot = Join-Path $RepoRoot 'sites/hoor-github-pages-20261121'
$EncryptedContent = Join-Path $SiteRoot 'public/content.hoor'

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$CommandArgs,
        [Parameter(Mandatory = $true)][string]$AtPath
    )

    Push-Location -LiteralPath $AtPath
    try {
        & $FilePath @CommandArgs
        if ($LASTEXITCODE -ne 0) {
            throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($CommandArgs -join ' ')"
        }
    }
    finally {
        Pop-Location
    }
}

Write-Host '1/8  Syncing screenplay dialogue data...'
Invoke-CheckedCommand -FilePath 'python' -CommandArgs @('-I', 'tools/sync_dialogues.py') -AtPath $RepoRoot

Write-Host '2/8  Rebuilding the compiled novel...'
Invoke-CheckedCommand -FilePath 'python' -CommandArgs @('novel/build_book.py') -AtPath $RepoRoot

Write-Host '3/8  Checking story continuity...'
Push-Location -LiteralPath $RepoRoot
try {
    $ContinuityOutput = & python -I tools/check_continuity.py 2>&1
    $ContinuityExitCode = $LASTEXITCODE
    $ContinuityOutput | ForEach-Object { Write-Host $_ }
    if ($ContinuityExitCode -ne 0) {
        throw "Continuity checker failed with exit code $ContinuityExitCode."
    }
    if (($ContinuityOutput -join "`n") -notmatch 'TOTAL findings:\s*0') {
        throw 'Continuity findings must be resolved before publishing.'
    }
}
finally {
    Pop-Location
}

Write-Host '4/8  Building the encrypted-content source snapshot...'
Invoke-CheckedCommand -FilePath 'python' -CommandArgs @('tools/build_snapshot.py') -AtPath $RepoRoot

Write-Host '5/8  Checking and building the website...'
Invoke-CheckedCommand -FilePath 'npm.cmd' -CommandArgs @('run', 'check') -AtPath $SiteRoot
Invoke-CheckedCommand -FilePath 'npm.cmd' -CommandArgs @('run', 'build') -AtPath $SiteRoot

$BeforeHash = (Get-FileHash -LiteralPath $EncryptedContent -Algorithm SHA256).Hash
Write-Host '6/8  Encrypting the new website content.'
Write-Host 'Enter the current site password at the hidden prompt. It will not be echoed or saved in this script.'
Invoke-CheckedCommand -FilePath 'node' -CommandArgs @('scripts/encrypt-content.mjs') -AtPath $SiteRoot
$AfterHash = (Get-FileHash -LiteralPath $EncryptedContent -Algorithm SHA256).Hash
if ($BeforeHash -eq $AfterHash) {
    throw 'The encrypted content did not change; stopping before commit and push.'
}

$Branch = (& git -C $RepoRoot branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Branch -ne 'main') {
    throw "Publishing is restricted to branch 'main'; current branch is '$Branch'."
}
$Remote = (& git -C $RepoRoot remote get-url origin).Trim()
if ($LASTEXITCODE -ne 0 -or $Remote -notmatch 'github\.com[:/]mvonline/HOOR(?:\.git)?$') {
    throw "Unexpected origin remote '$Remote'; stopping before commit and push."
}
$StagedChanges = & git -C $RepoRoot diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    throw 'There are already staged changes. Unstage or review them before running this publisher.'
}

Write-Host '7/8  Staging tracked changes and the two new canonical design documents...'
& git -C $RepoRoot add -u
if ($LASTEXITCODE -ne 0) { throw 'Could not stage tracked project changes.' }
& git -C $RepoRoot add -- gameStory/redesign/v11-aaa/08_DIRECTOR_PRINCIPLES_FA.md gameStory/redesign/v11-aaa/09_PLACES_OF_LOT_FA.md tools/publish_hoor_site.ps1
if ($LASTEXITCODE -ne 0) { throw 'Could not stage the new canonical documents and publisher script.' }
& git -C $RepoRoot add -- sites/hoor-github-pages-20261121/public/media/gallery
if ($LASTEXITCODE -ne 0) { throw 'Could not stage the new gallery video and music files.' }
& git -C $RepoRoot diff --cached --check
if ($LASTEXITCODE -ne 0) { throw 'Staged changes failed git diff --check.' }
& git -C $RepoRoot diff --cached --stat

Write-Host '8/8  Committing and pushing to origin/main...'
& git -C $RepoRoot commit -m $CommitMessage
if ($LASTEXITCODE -ne 0) { throw 'Commit failed; changes remain staged for review.' }
& git -C $RepoRoot push origin main
if ($LASTEXITCODE -ne 0) { throw 'Push failed; the local commit is preserved.' }

Write-Host 'Publish complete. The new snapshot, encrypted content, and website changes are on origin/main.'
