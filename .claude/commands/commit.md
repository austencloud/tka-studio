---
description: Write and commit git changes with AI-generated message
allowed-tools: Bash(git *)
---

Current git status:
!`git status`

Staged changes:
!`git diff --cached`

Recent commit messages for style reference:
!`git log -5 --oneline`

Please write a concise, descriptive git commit message for my staged changes.

Follow these guidelines:

- First line: Brief summary (use imperative mood: "Add", "Fix", "Update", not "Added", "Fixed", "Updated")
- Keep the first line under 50 characters if possible
- Add a blank line after the summary
- Provide a detailed explanation if the changes are non-trivial
- Explain what changed and why (not just how)
- Reference file names or modules when relevant
- Use present tense

After analyzing my changes and drafting the message, show me the proposed commit message and ask if I want to proceed with committing it.
