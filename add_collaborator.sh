#!/bin/bash
# Script to help add a collaborator to the repository

REPO="orire-dev/trading-web-app"

echo "🔐 Add Collaborator to Trading App Repository"
echo "=============================================="
echo ""
echo "Repository: $REPO"
echo ""
echo "Option 1: Add via GitHub Web UI (Recommended)"
echo "  1. Go to: https://github.com/$REPO/settings/access"
echo "  2. Click 'Add people'"
echo "  3. Enter their GitHub username"
echo "  4. Select permission level (Read/Write/etc.)"
echo "  5. Send invitation"
echo ""
echo "Option 2: Use GitHub CLI"
read -p "Do you have GitHub CLI installed? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    read -p "Enter GitHub username to add: " username
    read -p "Permission level (pull/triage/push/maintain/admin) [default: pull]: " permission
    permission=${permission:-pull}
    
    echo ""
    echo "Adding $username with $permission permission..."
    gh api repos/$REPO/collaborators/$username -X PUT -f permission=$permission
    echo "✅ Invitation sent!"
else
    echo ""
    echo "Install GitHub CLI: brew install gh"
    echo "Or use the web UI method above"
fi
echo ""
echo "📝 See SHARE_REPO.md for more options"
