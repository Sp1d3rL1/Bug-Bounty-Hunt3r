#!/usr/bin/env bash
set -euo pipefail

# Read before running. This installs common bug bounty tooling from official-ish sources.
# Do not run on production servers. Prefer a fresh VPS.

mkdir -p "$HOME/tools" "$HOME/go/bin"
export PATH="$PATH:$HOME/go/bin"

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1"; return 1; }; }

if ! command -v go >/dev/null 2>&1; then
  echo "Go is required. Install Go from your distro or https://go.dev/dl/ first."
  exit 1
fi

# ProjectDiscovery core
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install -v github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Passive URL collection
go install -v github.com/lc/gau/v2/cmd/gau@latest
go install -v github.com/tomnomnom/waybackurls@latest

# Fuzzing/helper tools - keep manual and authorized-only
go install -v github.com/ffuf/ffuf/v2@latest
go install -v github.com/tomnomnom/anew@latest

# Secrets scanning
go install -v github.com/gitleaks/gitleaks/v8@latest

nuclei -update-templates

echo "Done. Add this to shell profile: export PATH=\$PATH:\$HOME/go/bin"
