param([switch]$ForceRebuild = $false)

if ($ForceRebuild) {
    pdoc --html --output-dir docs nextcloud_notes_api --force
    Move-Item -Force .\docs\nextcloud_notes_api\* .\docs
    Remove-Item -Recurse -Force .\docs\nextcloud_notes_api
}
else {
    pdoc --html --output-dir docs nextcloud_notes_api
    Move-Item -Force .\docs\nextcloud_notes_api\* .\docs
    Remove-Item -Recurse -Force .\docs\nextcloud_notes_api
}