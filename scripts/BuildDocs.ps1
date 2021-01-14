param([switch]$ForceRebuild = $false) 

if ($ForceRebuild) {
    pdoc --html --output-dir pdoc_build nextcloud_notes_api --force
}
else {
    pdoc --html --output-dir pdoc_build nextcloud_notes_api
}