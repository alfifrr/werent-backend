# Git Workflow & Branching Strategy

## 🌳 Branch Structure

### Main Branches
- **`main`** 
  - Production-ready code only
  - Protected branch - no direct pushes allowed
  - Only PM can merge here
  - Represents stable releases

- **`development`**
  - Default active branch for all development
  - Integration branch for all features
  - All feature branches merge here first
  - Thoroughly tested before merging to main

### Feature Branches
- **`feature/<descriptive-name>`**
  - Created from `development` branch
  - One feature per branch
  - Short-lived (delete after merge)
  - Examples: `feature/gear-management`, `feature/user-reviews`

## ⚠️ Critical Rules

### ❌ NEVER DO
- Push directly to `main` branch
- Create feature branches from `main`
- Merge untested code to `development`
- Force push to shared branches

### ✅ ALWAYS DO
- Create feature branches from `development`
- Test your code before creating PR
- Target `development` branch in PRs
- Get code review before merging
- Use descriptive commit messages

## 🔄 Development Workflow

### 1. Starting New Work
```bash
# Switch to development and get latest changes
git checkout development
git pull origin development

# Create new feature branch
git checkout -b feature/your-feature-name

# Start working on your feature
```

### 2. During Development
```bash
# Make your changes
# Add tests for new functionality
# Update documentation if needed

# Stage and commit changes
git add .
git commit -m "feat: add gear listing endpoint"

# Push feature branch (first time)
git push -u origin feature/your-feature-name

# Push subsequent changes
git push
```

### 3. Creating Pull Request
1. **Navigate to GitHub/GitLab**
2. **Create Pull Request:**
   - Source: `feature/your-feature-name`
   - Target: `development`
   - Title: Clear, descriptive title
   - Description: What changes were made and why

3. **Ensure PR checklist:**
   - [ ] All tests pass
   - [ ] Documentation updated
   - [ ] Code follows style guidelines
   - [ ] No merge conflicts
   - [ ] Feature is complete

### 4. Code Review Process
1. **Team members review** the pull request
2. **Address feedback** if any changes requested
3. **Ensure CI/CD passes** (tests, linting, etc.)
4. **Approval required** before merge
5. **Merge to development** after approval

### 5. Clean Up
```bash
# After successful merge, clean up
git checkout development
git pull origin development
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```

## 🚀 Release Process

### Development → Main (PM Only)
1. **PM reviews** development branch
2. **Final testing** on development
3. **Create release PR** from `development` to `main`
4. **PM approval** and merge to main
5. **Tag release** with version number
6. **Deploy to production**

## 📝 Commit Message Guidelines

### Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, etc.)
- **refactor:** Code refactoring
- **test:** Adding or updating tests
- **chore:** Maintenance tasks

### Examples
```bash
feat(auth): add user profile update endpoint
fix(gear): resolve inventory count calculation
docs(api): update authentication examples
test(auth): add signup validation tests
refactor(models): improve user model methods
```

## 🛡️ Branch Protection Settings

### Main Branch Protection
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require branches to be up to date
- ✅ Restrict pushes that create files larger than 100MB
- ✅ Only PM can merge

### Development Branch Protection
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Allow force pushes by repository admins
- ✅ Team members can merge after review

## 🤝 Team Collaboration

### For Developers
1. **Always work in feature branches**
2. **Keep feature branches small and focused**
3. **Regularly sync with development**
4. **Write clear commit messages**
5. **Test your code before creating PR**

### For Reviewers
1. **Review code thoroughly**
2. **Test the changes locally if needed**
3. **Provide constructive feedback**
4. **Ensure documentation is updated**
5. **Check that tests are included**

### For Project Manager
1. **Review development branch regularly**
2. **Ensure quality before merging to main**
3. **Coordinate releases**
4. **Manage branch protection settings**
5. **Oversee overall code quality**

## 🆘 Common Scenarios

### Syncing Feature Branch with Development
```bash
# While on your feature branch
git checkout development
git pull origin development
git checkout feature/your-feature-name
git merge development

# Resolve any conflicts if they exist
# Push updated feature branch
git push
```

### Handling Merge Conflicts
```bash
# When conflicts occur during merge
git status  # See conflicted files
# Edit files to resolve conflicts
git add <resolved-files>
git commit -m "resolve merge conflicts"
git push
```

### Emergency Hotfix
```bash
# For critical production fixes
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix

# Make minimal changes to fix the issue
git add .
git commit -m "hotfix: resolve critical authentication bug"
git push -u origin hotfix/critical-bug-fix

# Create PR to main (emergency approval from PM)
# After merge to main, also merge to development
```

## 📊 Workflow Summary

```
main ←─────────── (PM only) ←─────────── development
                                            ↑
                                            │ (PR + Review)
                                            │
                               feature/gear-management
                               feature/user-reviews  
                               feature/payment-system
```

This workflow ensures:
- **Code quality** through reviews
- **Stable main branch** for production
- **Organized development** through feature branches
- **Clear collaboration** with defined roles
- **Easy rollback** if issues arise

---

*Follow this workflow for smooth collaboration and high-quality code delivery! 🚀*
