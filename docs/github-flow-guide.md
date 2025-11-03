# 🧭 TopoVision — GitHub Flow Guide

> **Purpose:**  
> This guide explains how the TopoVision development team collaborates using **GitHub Flow**.  
> It ensures consistency, clean merges, and a reliable project history across all contributors.

---

## 🌿 What is GitHub Flow?

**GitHub Flow** is a lightweight and modern workflow based on short-lived branches.  
It is designed for continuous integration and fast collaboration.

Main idea:
1. Create a new branch for each feature or fix.
2. Commit your changes.
3. Push the branch to GitHub.
4. Open a Pull Request (PR).
5. Request review and run automated tests.
6. Merge into `develop` → later into `main`.

---

## 🏗️ Main Branches Overview

| Branch | Description | Permissions |
|---------|--------------|--------------|
| `main` | Stable production-ready version. Used for final releases and presentations. | ✅ Protected (no direct commits) |
| `develop` | Integration branch for merging completed features. | ✅ Protected |
| `feature/*` | Temporary branches for new features or fixes. | 🧩 Developer owned |
| `hotfix/*` | For urgent fixes after a release. | 🔧 Developer owned |
| `docs/*` | Documentation-only changes. | 📚 Developer owned |

---

## 🧩 Branch Naming Convention

Each branch name should be **short, lowercase**, and **descriptive**.  
Format:

```

<type>/<short-description>

```

**Examples:**
```

feature/capture-module
feature/gui-layout
fix/preprocessing-bug
docs/update-readme
chore/add-ci-config

```

---

## 💬 Commit Message Convention

TopoVision uses the **Conventional Commits** standard.  
Each commit message should follow this format:

```

<type>(<scope>): <description>

````

| Type | Purpose |
|------|----------|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, no logic changes |
| `refactor` | Code restructuring without behavior change |
| `test` | Adding or modifying tests |
| `chore` | Maintenance tasks (builds, configs, deps) |
| `ci` | Continuous Integration or workflow updates |

**Examples:**
```bash
feat(gui): add button for opening camera
fix(preprocessing): correct grayscale conversion function
docs(readme): update installation steps
chore(config): add pre-commit configuration
````

---

## 🔁 Typical GitHub Flow Cycle

### 1️⃣ Create a new branch

```bash
git checkout develop
git pull
git checkout -b feature/capture-module
```

### 2️⃣ Make your changes

Edit your files, write tests, and commit regularly:

```bash
git add .
git commit -m "feat(capture): add OpenCVCamera backend"
```

### 3️⃣ Push to GitHub

```bash
git push origin feature/capture-module
```

### 4️⃣ Open a Pull Request (PR)

* Go to **GitHub → Pull Requests → New PR**
* Choose:

  * Base branch: `develop`
  * Compare branch: `feature/capture-module`
* Add a clear title and description.
* Request a review from your teammates.

### 5️⃣ Wait for CI to pass

GitHub Actions will run automated tests (`pytest`).
The PR can only be merged once all checks are ✅ green.

### 6️⃣ Merge the Pull Request

After approval and passing tests:

* Merge into `develop`
* Delete the feature branch from GitHub

### 7️⃣ Final integration to `main`

After completing the current phase (week), the team lead will:

```bash
git checkout main
git merge develop
git tag v0.1 -m "Phase 1 complete - Base architecture setup"
git push origin main --tags
```

---

## ⚙️ Code Review Guidelines

Before approving a PR:
✅ Check for clear and descriptive commit messages
✅ Confirm there are no linter or test failures
✅ Verify the code follows the SOLID principles
✅ Ensure functions have type hints and docstrings
✅ Comment on unclear logic or potential optimizations

---

## 🧰 Pre-commit Hooks

Every contributor must install and use the **pre-commit** system:

```bash
pre-commit install
pre-commit run --all-files
```

This guarantees all code follows:

* Black (formatting)
* isort (imports order)
* Flake8 (linting)
* MyPy (type checking)

Commits will be rejected automatically if any check fails.

---

## 🧱 Example Workflow Diagram

```text
[ feature/gui-mock ] → PR → [ develop ] → merge → [ main ]
        ^                       ^                     ^
     Developer             Integration           Stable release
```

Or visually:

```
 main ────────────────┐───────────────▶ (production)
                      │
 develop ─────┬───────┘
              │
 feature/capture-module
              │
              └──▶ pull request → review → merge → develop
```

---

## 🧾 Pull Request Template (Recommended)

When creating a PR, use this format:

```markdown
### Summary
Explain the purpose of this PR and what changes were made.

### Changes
- Added/Modified/Removed ...
- Updated dependencies / tests / docs

### Testing
Describe how you tested the feature (manual or automated).

### Checklist
- [ ] Code passes `pytest`
- [ ] Code follows project style (Black + Flake8)
- [ ] Commits follow Conventional Commits
- [ ] Documentation updated if needed
```

*(Optional: you can save this as `.github/pull_request_template.md`)*

---

## 🧭 Best Practices Summary

| ✅ Do                              | 🚫 Don’t                               |
| --------------------------------- | -------------------------------------- |
| Use small, focused branches       | Work directly in `main`                |
| Write descriptive commit messages | Commit “temp” or “fix” without context |
| Run tests locally before pushing  | Push broken code                       |
| Ask for peer review               | Merge without CI check                 |
| Keep `develop` always stable      | Leave unmerged feature branches        |

---

## 🧠 Team Workflow Example (Phase 1)

| Member    | Branch                      | Task                           |
| --------- | --------------------------- | ------------------------------ |
| Alejandro | `feature/project-structure` | Repo setup and `app.py`        |
| Andreina  | `feature/core-interfaces`   | Core interfaces and models     |
| Jonathan  | `feature/gui-mock`          | Mock GUI (Tkinter placeholder) |
| Kiara     | `feature/env-setup`         | CI and dependency setup        |
| Víctor    | `feature/docs-base`         | Documentation and setup guides |

Each member works independently → pushes → opens PR → merges into `develop`.
At the end of the week, the team lead merges everything into `main` and tags a release.

---

## 🏁 Final Notes

* All commits must be in **English**.
* Always pull from `develop` before creating a new branch.
* Avoid committing generated files (`__pycache__`, `.venv/`, etc.).
* Never commit secrets or environment variables.

---

**TopoVision Development Team — 2025**

> *“Better branches, cleaner merges, faster progress.”*
