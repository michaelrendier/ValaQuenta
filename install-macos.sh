#!/usr/bin/env bash
#
# ValaQuenta — installer for macOS (Intel and Apple Silicon)
#
#   bash install-macos.sh              # install into a .venv here
#   bash install-macos.sh --user       # user site-packages instead
#   bash install-macos.sh --no-jupyter # skip JupyterLab
#
# Invoke with `bash install-macos.sh`, not `./install-macos.sh` -- the exec bit
# does not survive every filesystem or archive.
#
# Notes specific to macOS:
#   * The /usr/bin/python3 that ships with Xcode's command line tools works,
#     but it is minimal. Homebrew python is recommended and preferred here.
#   * matplotlib needs a GUI backend to show windows. Inside JupyterLab this
#     does not matter -- figures render inline.
#   * Nothing here requires sudo.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

MODE="venv"
WANT_JUPYTER=1

for arg in "$@"; do
  case "$arg" in
    --user)       MODE="user" ;;
    --no-jupyter) WANT_JUPYTER=0 ;;
    -h|--help)    sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

say()  { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
warn() { printf '\033[33m    %s\033[0m\n' "$*"; }
die()  { printf '\033[31mERROR: %s\033[0m\n' "$*" >&2; exit 1; }

[ "$(uname -s)" = "Darwin" ] || warn "this is the macOS installer but uname says $(uname -s)"

say "System"
echo "    macOS $(sw_vers -productVersion 2>/dev/null || echo '?')  arch $(uname -m)"

# ── Python ───────────────────────────────────────────────────────────────────
say "Locating Python"
PY=""
# Prefer Homebrew python over the Xcode one.
BREW_PREFIX="$(brew --prefix 2>/dev/null || true)"
CANDIDATES=()
if [ -n "$BREW_PREFIX" ]; then
  for v in 3.13 3.12 3.11 3.10; do
    CANDIDATES+=("$BREW_PREFIX/bin/python$v")
  done
fi
CANDIDATES+=(python3.13 python3.12 python3.11 python3.10 python3)

for cand in "${CANDIDATES[@]}"; do
  if command -v "$cand" >/dev/null 2>&1; then
    if "$cand" -c 'import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)' 2>/dev/null; then
      PY="$cand"; break
    fi
  fi
done

if [ -z "$PY" ]; then
  die "no Python 3.10+ found.

Install Homebrew, then Python:
    /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"
    brew install python

Or install Xcode command line tools:
    xcode-select --install"
fi
echo "    $PY -> $("$PY" --version 2>&1)"

if [ -z "$BREW_PREFIX" ]; then
  warn "Homebrew not found; using $PY."
  warn "If pip fails to build a wheel, 'brew install python' usually fixes it."
fi

# ── Environment ──────────────────────────────────────────────────────────────
PIP_TARGET=()
if [ "$MODE" = "venv" ]; then
  say "Creating virtual environment (.venv)"
  if [ ! -d .venv ]; then
    "$PY" -m venv .venv || die "could not create a venv with $PY"
  else
    echo "    .venv already exists, reusing it"
  fi
  # shellcheck disable=SC1091
  source .venv/bin/activate
  PY="python"
else
  say "Installing into the user site-packages"
  PIP_TARGET=(--user)
fi

# ── Dependencies ─────────────────────────────────────────────────────────────
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
  warn "On Apple Silicon a source build of scipy needs a Fortran compiler:"
  warn "    brew install gcc openblas"
  warn "Usually a prebuilt wheel exists and this is not needed -- check that"
  warn "pip is current and the Python is 3.10-3.13."
  die "dependency installation failed"
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
