# Sharing Repository Access

Guide to allow another GitHub account to clone/access this repository.

## Option 1: Add as Collaborator (Recommended)

**Best for**: Collaboration, full access, multiple people

### Steps:

1. **Go to Repository Settings**
   - Navigate to: https://github.com/orire-dev/trading-web-app
   - Click "Settings" tab
   - Click "Collaborators" in left sidebar
   - Click "Add people" button

2. **Add Collaborator**
   - Enter the GitHub username or email of the other account
   - Select permission level:
     - **Read**: Can clone and view
     - **Triage**: Can manage issues/PRs
     - **Write**: Can push changes
     - **Maintain**: Can manage settings
     - **Admin**: Full access

3. **Send Invitation**
   - Click "Add [username] to this repository"
   - They'll receive an email invitation
   - They need to accept the invitation

### Permission Levels:

- **Read** (Recommended for cloning only)
  - Can clone, pull, view code
  - Cannot push changes
  - Good for read-only access

- **Write** (For collaboration)
  - Can clone, pull, push, create branches
  - Can create issues and PRs
  - Good for active development

### Command for them to clone:
```bash
git clone https://github.com/orire-dev/trading-web-app.git
# or with SSH
git clone git@github.com:orire-dev/trading-web-app.git
```

---

## Option 2: Deploy Key (Read-Only Access)

**Best for**: CI/CD, automated systems, read-only access

### Steps:

1. **Generate SSH Key** (on their machine)
   ```bash
   ssh-keygen -t ed25519 -C "deploy-key" -f ~/.ssh/trading-app-deploy
   ```

2. **Get Public Key**
   ```bash
   cat ~/.ssh/trading-app-deploy.pub
   ```

3. **Add Deploy Key to Repository**
   - Go to: https://github.com/orire-dev/trading-web-app/settings/keys
   - Click "Add deploy key"
   - Title: "Deploy Key for [purpose]"
   - Key: Paste the public key
   - ✅ Check "Allow write access" if needed (usually leave unchecked)
   - Click "Add key"

4. **Configure SSH** (on their machine)
   ```bash
   # Add to ~/.ssh/config
   Host github-trading-app
       HostName github.com
       User git
       IdentityFile ~/.ssh/trading-app-deploy
   ```

5. **Clone with Deploy Key**
   ```bash
   git clone git@github-trading-app:orire-dev/trading-web-app.git
   ```

**Note**: Deploy keys are tied to one repository only.

---

## Option 3: Personal Access Token (PAT)

**Best for**: Temporary access, CI/CD, automation

### Steps:

1. **They Create a Personal Access Token**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: "Trading App Access"
   - Expiration: Choose duration
   - Scopes: Select `repo` (full control of private repositories)
   - Click "Generate token"
   - **Copy the token immediately** (won't be shown again)

2. **Clone Using Token**
   ```bash
   # HTTPS with token
   git clone https://[TOKEN]@github.com/orire-dev/trading-web-app.git
   
   # Or set as credential
   git clone https://github.com/orire-dev/trading-web-app.git
   # When prompted:
   # Username: [their-username]
   # Password: [paste-token-here]
   ```

3. **Store Token Securely** (optional)
   ```bash
   # Use Git credential helper
   git config --global credential.helper store
   # Or use GitHub CLI
   gh auth login
   ```

---

## Option 4: Organization Transfer

**Best for**: Long-term collaboration, team management

### Steps:

1. **Create Organization** (optional)
   - Go to: https://github.com/organizations/new
   - Create organization
   - Add the other account as member

2. **Transfer Repository**
   - Go to: https://github.com/orire-dev/trading-web-app/settings
   - Scroll to "Danger Zone"
   - Click "Transfer ownership"
   - Enter organization name
   - Confirm transfer

3. **Add Collaborators**
   - Now add people to the organization
   - They'll have access to all org repos

---

## Option 5: Fork (Public Repos Only)

**Best for**: Open source, public repositories

If you make the repo public:
- They can fork it
- They get their own copy
- Can submit pull requests

**Note**: Not recommended if you want to keep it private.

---

## Quick Comparison

| Method | Access Level | Best For | Setup Complexity |
|--------|-------------|----------|------------------|
| Collaborator | Full (configurable) | Team collaboration | ⭐ Easy |
| Deploy Key | Read-only (or write) | CI/CD, automation | ⭐⭐ Medium |
| PAT | Full (configurable) | Temporary access | ⭐⭐ Medium |
| Organization | Full team access | Long-term teams | ⭐⭐⭐ Complex |
| Fork | Own copy | Open source | ⭐ Easy (public only) |

---

## Recommended Approach

**For most cases**: Use **Option 1 (Add Collaborator)** with **Read** permission

### Quick Steps:
1. Go to: https://github.com/orire-dev/trading-web-app/settings/access
2. Click "Add people"
3. Enter their GitHub username
4. Select "Read" permission
5. Click "Add [username]"
6. They accept the invitation

### They clone with:
```bash
git clone https://github.com/orire-dev/trading-web-app.git
```

---

## Security Best Practices

1. **Use Least Privilege**: Give only necessary permissions
2. **Review Access Regularly**: Remove unused collaborators
3. **Use Deploy Keys for CI/CD**: Don't use personal accounts
4. **Rotate Tokens**: Change PATs periodically
5. **Monitor Activity**: Check repository insights

---

## Troubleshooting

### "Repository not found" error
- Check they accepted the invitation
- Verify they're logged into correct GitHub account
- Try cloning with HTTPS instead of SSH

### Permission denied
- Check their permission level
- Verify SSH key is added correctly
- Try using Personal Access Token

### Can't push changes
- They need "Write" or higher permission
- Check branch protection rules
- Verify they have write access

---

## Need Help?

- GitHub Docs: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/managing-teams-and-people-with-access-to-your-repository
- Repository: https://github.com/orire-dev/trading-web-app
