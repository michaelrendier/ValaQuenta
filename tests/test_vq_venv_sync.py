"""tools/vq_venv_sync.py: the command parser the PostToolUse hook feeds. It must find real pip invocations and nothing else."""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("vq_venv_sync", ROOT / "tools" / "vq_venv_sync.py")
vs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vs)
parse = vs.parse_packages


def test_plain_invocations_are_found():
    assert parse("pip install foo bar") == ["foo", "bar"]
    assert parse("pip3 install requests==2.31 numpy>=1.2") == ["requests==2.31", "numpy>=1.2"]
    assert parse(".venv/bin/pip install astropy") == ["astropy"]
    assert parse("python3 -m pip install --upgrade scipy") == ["scipy"]
    assert parse("source .venv/bin/activate && pip install pytest && echo done") == ["pytest"]
    assert parse("pip install 'uvicorn[standard]>=0.30'") == ["uvicorn[standard]>=0.30"]


def test_flags_files_and_comments_are_skipped():
    assert parse("pip install -r requirements.txt") == []
    assert parse("pip install --index-url https://example.org/simple foo") == ["foo"]
    assert parse("pip install foo   # only needed for the manifest builder") == ["foo"]
    assert parse("pip install ./local/dir some.whl foo") == ["foo"]


def test_text_that_only_mentions_pip_and_install_yields_nothing():
    """The 2026-11-27 incident: a primer written to a file by a heredoc, whose body mentions pip install, was parsed as a package list."""
    heredoc = """cat > CLAUDE.md <<'EOF'
## Step 1: set up
.venv/bin/pip install astroquery astropy requests   # only needed for build_mast_manifest.py
python3 test_nrao_fetch.py               # 14 checks against a local mock server
When the machine rebooted: just run the job again; many files resume.
EOF"""
    assert parse(heredoc) == []
    assert parse("echo 'you can pip install it later, the report says so'") == []
    assert parse("grep -n 'pip install' README.md") == []
    assert parse("git commit -m 'pip install notes for the install guide'") == []


def test_the_hook_still_sees_a_pip_line_after_other_commands():
    assert parse("cd /tmp\npip install foo\nls") == ["foo"]
    assert parse("python3 build.py; pip install bar | tail -1") == ["bar"]
