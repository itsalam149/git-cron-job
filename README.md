# GitHub Contribution & Counter Automation

[![Scheduled Counter Update](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME/actions/workflows/update.yml/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME/actions/workflows/update.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A transparent, production-grade GitHub automation pipeline designed to demonstrate scheduled tasks, Git automation, Python scripting, and CI/CD workflows using **GitHub Actions**.

The system runs on a cron schedule (or via manual trigger), executes a robust Python script to increment a tracked counter, records execution timestamps in both UTC and Indian Standard Time (IST), and automatically commits and pushes the changes back to the repository using legitimate Git operations.

---

## Architecture Overview

```mermaid
flowchart TD
    A[Trigger: Cron Schedule / Manual Dispatch] --> B[GitHub Actions Runner: ubuntu-latest]
    B --> C[Checkout Repository: actions/checkout@v4]
    C --> D[Setup Python: actions/setup-python@v5]
    D --> E[Execute Script: python update.py]
    E --> F[Read & Increment counter.txt]
    F --> G[Write UTC + IST Execution Timestamps]
    G --> H{Changes Detected via git diff?}
    H -- No --> I[Log 'No Changes' and Skip Commit]
    H -- Yes --> J[Configure Git Author Identity]
    J --> K[git commit -m 'chore: increment counter' [skip ci]]
    K --> L[git push origin main]
    L --> M[GitHub Contributions Indexer]
```

---

## Repository Structure

```text
git-cron-job/
├── .github/
│   └── workflows/
│       └── update.yml      # GitHub Actions workflow (Cron + Manual dispatch + Push)
├── .gitignore              # Standard Python and OS ignores
├── counter.txt             # Tracked data file storing counter and timestamps
├── update.py               # Robust Python script for reading, incrementing, and updating
└── README.md               # Documentation, setup guide, and troubleshooting
```

---

## How GitHub Contributions Actually Work

To have your automated commits count towards your personal **GitHub Contribution Graph**, your commits must adhere strictly to GitHub's official contribution rules:

### 1. Commit Author Email Association
* Commits **MUST** be authored with an email address that is registered and verified on your GitHub account (`GitHub Settings -> Emails`).
* If you use the default `github-actions[bot]` email (`41898282+github-actions[bot]@users.noreply.github.com`), GitHub will attribute the commit to the bot, **not** your personal profile.
* This repository defaults to using `${{ github.actor }}@users.noreply.github.com` (or custom repository variables `GIT_AUTHOR_NAME` and `GIT_AUTHOR_EMAIL`), ensuring commits are accurately mapped to your GitHub account.

### 2. Default Branch Requirement
* Commits must be made directly to the repository's **default branch** (typically `main` or `master`) or merged into the default branch via a pull request. Commits on orphan or unmerged feature branches are not counted.

### 3. Public vs. Private Repositories
* **Public Repositories**: Contributions are visible to anyone visiting your GitHub profile.
* **Private Repositories**: By default, private contributions are hidden on your profile. To show them:
  1. Go to your GitHub profile (`https://github.com/<YOUR_USERNAME>`).
  2. Click **Contribution settings** (dropdown above the contribution calendar).
  3. Check **Private contributions**.

### 4. Indexing and Caching Delays
* GitHub updates the contribution graph asynchronously. It typically takes **5 to 15 minutes** (and occasionally up to 24 hours during peak service load) for new commits to reflect in the contribution heatmap.

---

## Cron Scheduling & Timezones (UTC vs IST)

GitHub Actions cron schedules are always evaluated in **Coordinated Universal Time (UTC)**.

### Timezone Conversion Reference

| Target Time in India (IST, UTC+5:30) | UTC Equivalent (Cron Input) | Cron Expression |
| :--- | :--- | :--- |
| **11:30 AM IST (Daily)** | 06:00 UTC | `0 6 * * *` *(Default)* |
| **09:00 AM IST (Daily)** | 03:30 UTC | `30 3 * * *` |
| **06:00 PM IST (Daily)** | 12:30 UTC | `30 12 * * *` |
| **09:30 AM & 09:30 PM IST (Twice Daily)** | 04:00 & 16:00 UTC | `0 4,16 * * *` |

> [!NOTE]
> **GitHub Actions Scheduling Precision**: GitHub Actions scheduled workflows may run with a few minutes of latency depending on global queue traffic. This is normal behavior for free-tier CI/CD runners.

---

## Step-by-Step Setup Guide

### Step 1: Create a Remote Repository on GitHub
1. Open your browser and navigate to [github.com/new](https://github.com/new).
2. Set the **Repository name** (e.g., `git-cron-job`).
3. Choose **Public** (or **Private** with private contributions enabled).
4. **Do NOT** initialize with a README, .gitignore, or license (we already have them locally).
5. Click **Create repository**.

### Step 2: Initialize Git and Push Local Code
Open your macOS Terminal in the project directory (`/Users/faqrealam149/Desktop/git-cron-job`) and run:

```bash
# 1. Initialize local git repository
git init -b main

# 2. Add all project files to staging
git add .

# 3. Commit the initial baseline version
git commit -m "feat: initialize automated counter project"

# 4. Add your GitHub remote repository (replace YOUR_GITHUB_USERNAME and YOUR_REPOSITORY_NAME)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git

# 5. Push local main branch to GitHub
git push -u origin main
```

### Step 3: Enable GitHub Actions Workflow Write Permissions
By default, GitHub Actions workflows have read-only access. You must grant write permissions so the workflow can push commits:

1. Navigate to your repository on GitHub.
2. Go to **Settings** (tab at the top) -> **Actions** (left sidebar) -> **General**.
3. Scroll down to **Workflow permissions**.
4. Select **Read and write permissions**.
5. Check **Allow GitHub Actions to create and approve pull requests** (optional, recommended).
6. Click **Save**.

### Step 4 (Optional): Configure Custom Author Identity
If you want to explicitly define your author name and email:
1. In your repository, go to **Settings** -> **Secrets and variables** -> **Actions** -> **Variables** tab.
2. Add variable `GIT_AUTHOR_NAME` = `Your Full Name`.
3. Add variable `GIT_AUTHOR_EMAIL` = `your_email@example.com` (must match your verified GitHub email).

---

## Testing & Manual Verification

You don't have to wait for the cron schedule to verify that the pipeline works:

1. Go to the **Actions** tab in your GitHub repository.
2. Select **Scheduled Counter Update** from the left workflow list.
3. Click the **Run workflow** dropdown on the right side and click the green **Run workflow** button.
4. Watch the workflow execution run. Click on the job to inspect the real-time logs:
   - Verify Python setup
   - Check `update.py` output with UTC and IST timestamps
   - Confirm Git commit and push execution
5. Return to the **Code** tab:
   - Check `counter.txt` to see the incremented count and timestamps.
   - Click on the commit history to see the new automated commit.

---

## Troubleshooting Guide

### 1. Error: `Permission to <repo> denied to github-actions[bot]` (HTTP 403)
* **Cause**: GitHub Actions permissions are set to read-only.
* **Fix**: Follow **Step 3** above to enable **Read and write permissions** in `Settings -> Actions -> General -> Workflow permissions`.

### 2. Workflow runs but no commit is pushed
* **Cause**: `counter.txt` was not modified, or changes were already committed.
* **Fix**: The workflow includes `git diff --staged --quiet` to prevent empty commits. If the script modifies `counter.txt`, it will commit. Check `python update.py` execution logs in Actions.

### 3. Commits appear in repository, but no green square on profile
* **Cause 1**: The commit email does not match any email in your GitHub account. Check your local Git email with `git config user.email` and verify it exists under GitHub Settings -> Emails.
* **Cause 2**: The repository is Private and "Private contributions" is disabled. Enable it under your GitHub Profile -> Contribution settings -> Private contributions.
* **Cause 3**: Commits were pushed to a branch other than the default branch (`main`).
* **Cause 4**: Cache indexing delay. Wait 10–15 minutes and refresh your profile.

### 4. Cron job is not running at the exact expected minute
* **Cause**: GitHub Actions cron runners can have scheduling delays during peak hours.
* **Fix**: Normal behavior. Ensure the repository has had activity within the last 60 days (GitHub pauses cron jobs on inactive repositories).

---

## Safe Automation & Ethics Notice

This project is built for **educational and operational CI/CD demonstration purposes**. 

* It does not spoof commit dates, fake commit histories, manipulate git author timestamps fraudulently, or falsify professional contributions.
* It demonstrates how automated systems, data pipelines, and maintenance bots legitimately record telemetry and maintain repository state over time.

---

## License

This project is open-source and available under the [MIT License](LICENSE).
