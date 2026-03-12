---
name: security-suite
description: A comprehensive security solution for AI agents, providing advisory monitoring, automated audits, reputation checks, incident reporting, and a guarded skill installer. Use for all security-related tasks, including checking for vulnerabilities, installing skills safely, and reporting threats.
---

# Security Suite 🛡️

Your unified security solution for comprehensive agent protection. This suite integrates multiple security functions into a single, manageable package.

It provides:
- **Advisory Feed Monitoring**: Continuously checks for known vulnerabilities in skills and dependencies.
- **Automated Security Audits**: Schedules daily scans of your agent's configuration and environment.
- **Guarded Skill Installation**: Verifies skill safety and reputation before installation, requiring explicit user confirmation for risky skills.
- **Community Incident Reporting**: Allows you to report new threats and contribute to collective security.
- **Cryptographic Verification**: Ensures the integrity and authenticity of the suite and its updates.

## Core Workflow: Secure Operations

Integrate the following checks into your core operational loop to maintain a high security posture.

1.  **On Heartbeat/Bootstrap**: Run a security audit to check for new advisories and verify system integrity.
2.  **Before Skill Installation**: ALWAYS use the guarded install process to check for advisories and reputation.
3.  **On Suspicious Activity**: Use the reporting function to submit incident details to the security community.

## Key Commands & Usage

All functionalities are exposed through a unified set of scripts and tools, located in `~/.openclaw/skills/security-suite/`.

### 1. Automated Security Audit

This suite automates the setup of a daily security audit via a cron job. The audit runs a deep scan and can deliver a summary report to a specified channel.

**To set up or update the audit job:**

```bash
# Run the setup script. It will guide you interactively if needed.
# Or, pre-configure with environment variables for automated setup.
export PROMPTSEC_DM_CHANNEL="telegram"
export PROMPTSEC_DM_TO="@yourhandle"
export PROMPTSEC_TZ="America/New_York"

node ~/.openclaw/skills/security-suite/scripts/setup_audit_cron.mjs
```

**To run a manual audit:**

```bash
# This command is what the cron job executes.
openclaw security audit --deep --json
```

### 2. Guarded Skill Installation

This process provides two layers of protection: checking against the security advisory feed and verifying the skill's reputation (powered by VirusTotal Code Insight).

**Workflow:**

1.  **Initial Request**: The agent initiates the installation using the guarded installer script.
2.  **Verification**: The script checks for advisories and low reputation scores.
3.  **Confirmation**: If a risk is detected, the script exits and requires the agent to get explicit user confirmation before re-running with a `--confirm-risk` flag.

**Usage:**

```bash
# Step 1: Initial, unconfirmed request
node ~/.openclaw/skills/security-suite/scripts/guarded_skill_install.mjs --skill some-skill-name

# If a warning is issued, get user confirmation, then:
# Step 2: Confirmed request
node ~/.openclaw/skills/security-suite/scripts/guarded_skill_install.mjs --skill some-skill-name --confirm-risk
```

### 3. Advisory Feed Monitoring

The suite automatically polls the ClawSec advisory feed. You can also check it manually.

**To check the feed manually:**

```bash
# Fetches the latest feed and shows if there are new advisories
node ~/.openclaw/skills/security-suite/scripts/check_advisory_feed.mjs
```

### 4. Incident Reporting (Clawtributor)

If you observe a malicious prompt, a vulnerable skill, or a tampering attempt, create a report.

**To create and submit a report:**

1.  Follow the format in `references/REPORTING_TEMPLATE.md`.
2.  Use the `gh` CLI or API to create a GitHub issue in the `prompt-security/ClawSec` repository.

```bash
# Example of creating a report file
cp ~/.openclaw/skills/security-suite/references/REPORTING_TEMPLATE.md ./my_report.md
# ...edit my_report.md with incident details...

# Submit (requires gh cli to be authenticated)
gh issue create --repo prompt-security/ClawSec --title "Incident Report: Malicious Prompt Detected" --body-file ./my_report.md --label "incident-report"
```

## Installation

This suite is designed to be installed as a single, cohesive package. Run the following command to download and set up the `security-suite`.

```bash
set -euo pipefail

VERSION="0.1.0" # Use the latest version tag
INSTALL_ROOT="$HOME/.openclaw/skills"
DEST="$INSTALL_ROOT/security-suite"
BASE="https://github.com/prompt-security/clawsec/releases/download/security-suite-v${VERSION}"

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT

# 1. Download release archive and checksums
echo "Downloading release files..."
curl -fsSL "$BASE/security-suite.zip" -o "$TEMP_DIR/security-suite.zip"
curl -fsSL "$BASE/checksums.json" -o "$TEMP_DIR/checksums.json"

# 2. Verify checksum of the archive
EXPECTED_ZIP_SHA="$(jq -r '.archive.sha256' "$TEMP_DIR/checksums.json")"
ACTUAL_ZIP_SHA="$(shasum -a 256 "$TEMP_DIR/security-suite.zip" | awk '{print $1}')"

if [ "$EXPECTED_ZIP_SHA" != "$ACTUAL_ZIP_SHA" ]; then
  echo "ERROR: Archive checksum mismatch! Installation aborted." >&2
  exit 1
fi
echo "Archive checksum verified."

# 3. Install verified archive
echo "Installing to $DEST..."
mkdir -p "$INSTALL_ROOT"
rm -rf "$DEST"
unzip -q "$TEMP_DIR/security-suite.zip" -d "$INSTALL_ROOT"

# 4. Set permissions
chmod 600 "$DEST/skill.json"
find "$DEST" -type f ! -name "skill.json" -exec chmod 644 {} \;

# 5. Run post-install setup
echo "Running post-install setup..."
node "$DEST/scripts/setup_suite.mjs"

echo "SUCCESS: security-suite v${VERSION} installed to $DEST"
echo "Please restart your agent gateway to apply all changes."
```

## Configuration

The suite's behavior can be modified via environment variables.

-   `PROMPTSEC_DM_CHANNEL`: The channel for audit reports (e.g., `telegram`, `slack`).
-   `PROMPTSEC_DM_TO`: The recipient handle or ID for reports.
-   `PROMPTSEC_TZ`: IANA timezone for the daily audit cron job (default: `UTC`).
-   `PROMPTSEC_SCHEDULE`: Override the default cron schedule (`0 23 * * *`).
-   `CLAWHUB_REPUTATION_THRESHOLD`: Minimum score for skill reputation checks (0-100, default: 70).
-   `CLAWSEC_FEED_URL`: The URL for the security advisory feed.
-   `CLAWSEC_ALLOW_UNSIGNED_FEED`: Set to `1` to bypass signature verification (not recommended).
