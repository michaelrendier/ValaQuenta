#!/usr/bin/env bash
#
# ValaQuenta — installer for Linux
#
#   bash install.sh              # install into a .venv here
#   bash install.sh --user       # install to the user site-packages instead
#   bash install.sh --system     # use the system python as-is (distro packages)
#   bash install.sh --no-jupyter # skip JupyterLab
#
# Invoke it with `bash install.sh` rather than `./install.sh`. Some filesystems
# (notably FAT/exFAT sdcards) cannot store the executable bit, so the shebang
# alone is not enough there.
#
# The script never sudo's and never touches anything outside this directory
# unless you ask for --user or --system.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

MODE="venv"
WANT_JUPYTER=1

for arg in "$@"; do
  case "$arg" in
    --user)       MODE="user" ;;
    --system)     MODE="system" ;;
    --no-jupyter) WANT_JUPYTER=0 ;;
    -h|--help)    sed -n '2,18p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

say()  { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[33m    %s\033[0m\n' "$*"; }
die()  { printf '\033[31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

# ── Python ───────────────────────────────────────────────────────────────────
say "Locating Python"
PY=""
for cand in python3.13 python3.12 python3.11 python3.10 python3; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c 'import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)' 2>/dev/null; then
      PY="$cand"; break
    fi
  fi
done
[ -n "$PY" ] || die "no Python 3.10+ found. Install one, e.g.:
    Debian/Ubuntu:  sudo apt install python3 python3-venv python3-pip
    Fedora:         sudo dnf install python3 python3-pip
    Arch:           sudo pacman -S python python-pip"
echo "    $PY -> $("$PY" --version 2>&1)"

# ── Environment ──────────────────────────────────────────────────────────────
PIP_TARGET=()
case "$MODE" in
  venv)
    say "Creating virtual environment (.venv)"
    if [ ! -d .venv ]; then
      "$PY" -m venv .venv 2>/dev/null || die "could not create a venv.
On Debian/Ubuntu the venv module is a separate package:
    sudo apt install python3-venv
Or re-run with:  bash install.sh --user"
    else
      echo "    .venv already exists, reusing it"
    fi
    # shellcheck disable=SC1091
    source .venv/bin/activate
    PY="python"
    ;;
  user)
    say "Installing into the user site-packages"
    PIP_TARGET=(--user)
    ;;
  system)
    say "Using the system Python as-is"
    ;;
esac

# ── Dependencies ─────────────────────────────────────────────────────────────
if [ "$MODE" = "system" ]; then
  warn "skipping pip install; assuming distro packages provide numpy/scipy/matplotlib"
else
  say "Installing dependencies"
  "$PY" -m pip install --upgrade pip >/dev/null 2>&1 || warn "could not upgrade pip; continuing"

  REQ="requirements.txt"
  if [ "$WANT_JUPYTER" -eq 0 ]; then
    REQ="$(mktemp)"
    grep -v -E '^(jupyterlab|ipykernel)' requirements.txt > "$REQ"
    echo "    (skipping JupyterLab)"
  fi

  if ! "$PY" -m pip install "${PIP_TARGET[@]}" -r "$REQ"; then
    warn "pip install failed."
    warn "If this is a distro-managed Python it may refuse to install"
    warn "system-wide (PEP 668). Re-run as:  bash install.sh   (uses a venv)"
    die "dependency installation failed"
  fi
fi

# ── Verify ───────────────────────────────────────────────────────────────────
say "Verifying"
"$PY" verify_install.py || die "verification failed — see output above"

# ── Done ─────────────────────────────────────────────────────────────────────
say "Installed"
if [ "$MODE" = "venv" ]; then
  cat <<EOF
    Activate the environment in each new shell:

        source "$REPO_DIR/.venv/bin/activate"

EOF
fi
cat <<'EOF'
    Try:
        python3 -m ValaQuenta --info
        jupyter lab notebooks/

    Start at notebooks/engines/ or wiki/00_index.md.
EOF
