# NUCLEAR OPTION: Disable all git hooks
# Run this if you want to completely eliminate all popups

# 1. Disable pre-commit hooks entirely
pre-commit uninstall

# 2. Move the hook files to disable them
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled 2>/dev/null || echo "No pre-commit hook found"

# 3. Set up git aliases for manual ruff checking
git config --local alias.check "!ruff check --fix . && ruff format ."
git config --local alias.commit-clean "!f() { git add .; ruff check --fix . --quiet; ruff format . --quiet; git add .; git commit -m \"$1\"; }; f"

echo "All git hooks disabled. Use 'git commit-clean \"message\"' for commits with ruff."
