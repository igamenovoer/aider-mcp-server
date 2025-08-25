# Aider Auto-Approval Guide

This guide explains how to configure Aider to automatically say "yes" to all permission requests and confirmation prompts.

## Quick Start

To start Aider with automatic approval for all prompts:

```bash
aider --yes-always
```

## Configuration Methods

### 1. Command Line Flag

The simplest way is to use the `--yes-always` flag when starting Aider:

```bash
# Basic usage
aider --yes-always

# With specific files
aider --yes-always file1.py file2.py

# With model specification
aider --yes-always --model claude-3-5-sonnet-20241022
```

### 2. Environment Variable

Set the environment variable to make this behavior persistent:

**PowerShell (Windows):**
```powershell
$env:AIDER_YES_ALWAYS = "true"
aider
```

**Bash/Zsh (Linux/macOS):**
```bash
export AIDER_YES_ALWAYS=true
aider
```

**Permanent setup in PowerShell profile:**
```powershell
# Add to your PowerShell profile
Add-Content $PROFILE '$env:AIDER_YES_ALWAYS = "true"'
```

### 3. Configuration File

Create or edit `.aider.conf.yml` in your project root:

```yaml
yes-always: true
```

### 4. .env File

Add to your `.env` file in the project root:

```
AIDER_YES_ALWAYS=true
```

## What Gets Auto-Approved

When `--yes-always` is enabled, Aider will automatically approve:

- ✅ File modification permissions
- ✅ Adding new files to the editing scope
- ✅ Reading additional files for context
- ✅ Git commits and changes
- ✅ Installing dependencies
- ✅ Running tests or linting
- ✅ Creating new directories
- ✅ Any other confirmation prompts

## Use Cases

### Automated Workflows
```bash
# CI/CD pipeline
aider --yes-always --message "Fix all linting errors" src/
```

### Batch Processing
```bash
# Process multiple files without interruption
aider --yes-always --file *.py --message "Add docstrings to all functions"
```

### Non-Interactive Sessions
```bash
# For scripts or automation
aider --yes-always --message-file instructions.txt
```

## Safety Considerations

⚠️ **Important Warnings:**

1. **Version Control**: Always use version control (git) when using `--yes-always`
2. **Review Changes**: Check the changes after Aider completes its work
3. **Backup**: Keep backups of important files
4. **Test Environment**: Consider using this in test environments first

## Combining with Other Options

### Auto-commit with approval
```bash
aider --yes-always --auto-commits
```

### With specific models
```bash
aider --yes-always --model gpt-4 --weak-model gpt-3.5-turbo
```

### With testing enabled
```bash
aider --yes-always --auto-test --test-cmd "pytest"
```

### With linting
```bash
aider --yes-always --auto-lint --lint-cmd "python: flake8"
```

## Architect Mode Auto-Approval

For architect mode, there's a separate flag:

```bash
aider --architect --auto-accept-architect
```

This automatically applies architect suggestions without prompting.

## Troubleshooting

### Check Current Configuration
```bash
aider --help | grep yes
```

### Verify Environment Variable
**PowerShell:**
```powershell
echo $env:AIDER_YES_ALWAYS
```

**Bash:**
```bash
echo $AIDER_YES_ALWAYS
```

### Override in Emergency
If you need to temporarily disable auto-approval:
```bash
aider --no-yes-always  # This doesn't exist, use normal aider instead
# or
AIDER_YES_ALWAYS=false aider
```

## Best Practices

1. **Start Small**: Test with small, non-critical files first
2. **Use Branches**: Work on feature branches when using auto-approval
3. **Monitor Output**: Watch the terminal output for any unexpected behavior
4. **Gradual Adoption**: Begin with specific file types before applying to entire projects
5. **Documentation**: Keep notes of what changes were made automatically

## Example Workflows

### Code Review Fixes
```bash
# Automatically fix all review comments
aider --yes-always --message "Address all code review comments from PR #123"
```

### Refactoring
```bash
# Large-scale refactoring
aider --yes-always --file src/ --message "Rename all instances of oldFunction to newFunction"
```

### Documentation Generation
```bash
# Add documentation to all functions
aider --yes-always *.py --message "Add comprehensive docstrings to all functions and classes"
```

## Related Configuration Options

- `--auto-commits`: Automatically commit changes
- `--auto-test`: Run tests after changes
- `--auto-lint`: Run linting after changes
- `--dry-run`: See what would happen without making changes

## Summary

The `--yes-always` flag is a powerful feature that makes Aider fully autonomous. Use it wisely with proper safeguards in place, and it can significantly speed up your development workflow.
