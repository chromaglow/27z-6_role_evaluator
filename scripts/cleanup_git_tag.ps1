# Git Tag Cleanup Script
# ======================
# This script helps clean up the accidental Git tag mentioned in the handoff.

Write-Host "Git Tag Cleanup Utility" -ForegroundColor Cyan
Write-Host "=======================" -ForegroundColor Cyan
Write-Host ""

# List all tags
Write-Host "Current Git tags:" -ForegroundColor Yellow
git tag -l

Write-Host ""
Write-Host "Looking for problematic tags..." -ForegroundColor Yellow

# The accidental tag name from the handoff
$accidentalTag = "git-tag--a-v1.0-internal--m-First-viable-internal-release-map-+-CLI-workflow-"

# Check if the accidental tag exists
$tagExists = git tag -l $accidentalTag

if ($tagExists) {
    Write-Host ""
    Write-Host "Found accidental tag: $accidentalTag" -ForegroundColor Red
    Write-Host ""
    
    $confirm = Read-Host "Do you want to delete this tag locally and remotely? (yes/no)"
    
    if ($confirm -eq "yes") {
        Write-Host ""
        Write-Host "Deleting local tag..." -ForegroundColor Yellow
        git tag -d $accidentalTag
        
        Write-Host "Deleting remote tag..." -ForegroundColor Yellow
        git push origin ":refs/tags/$accidentalTag"
        
        Write-Host ""
        Write-Host "Tag cleanup complete!" -ForegroundColor Green
    } else {
        Write-Host "Cleanup cancelled." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Accidental tag not found. Your tags look clean!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Final tag list:" -ForegroundColor Yellow
git tag -l

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
