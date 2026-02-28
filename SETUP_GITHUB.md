# GitHub Repository Setup Instructions

## Option 1: Create Repository on GitHub Website (Recommended)

1. Go to https://github.com/new
2. Repository name: `trading-web-app`
3. Description: `Trading for Dummies - Beginner-friendly eToro trading web interface`
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize with README", ".gitignore", or "license" (we already have these)
6. Click **"Create repository"**

## Option 2: Use GitHub CLI (if you install it)

```bash
# Install GitHub CLI (if not installed)
brew install gh

# Authenticate
gh auth login

# Create repo and push
gh repo create trading-web-app --public --description "Trading for Dummies - Beginner-friendly eToro trading web interface" --source=. --remote=origin --push
```

## After Creating the Repository

Once you've created the repository on GitHub, run:

```bash
cd /Users/orire/trading-web-app
git remote add origin https://github.com/orire-dev/trading-web-app.git
git branch -M main
git push -u origin main
```

Or if you prefer SSH:
```bash
git remote add origin git@github.com:orire-dev/trading-web-app.git
git branch -M main
git push -u origin main
```
