"""Publish the generated report to the GitHub Pages results repo.

The rendered report does not live in this repo: it lives in the nested
``LLM_Game_Level_Generator_Benchmark_Results_Page`` checkout, which is its own
git repo served by GitHub Pages. Pushing its ``main`` branch is what triggers a
redeployment of the page, so every new iteration has to be written *into* that
checkout and then committed + pushed for the published page to stay current.

``report.py`` calls :func:`publish` at the end of a run (opt out with
``--no-publish``); ``runner.py --iteration N`` uses :func:`iteration_dir` so a
run's output lands in the right place to begin with.

Paths here are all derived from this file's location, so the tools keep working
regardless of the current working directory.
"""

import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

#: The GitHub Pages checkout (its own git repo, nested inside this one).
PAGES_REPO = os.path.normpath(
    os.path.join(HERE, "..", "LLM_Game_Level_Generator_Benchmark_Results_Page"))
#: Where iteration folders (``0``, ``1``, ... and ``nonreasoning/``) live.
ITERATIONS_DIR = os.path.join(PAGES_REPO, "Iterations")

DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "main"

# GitHub Pages serves the repo root, but the report's home page is one level
# down in Iterations/. A root redirect keeps the bare Pages URL working.
ROOT_REDIRECT = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=Iterations/index.html">
<link rel="canonical" href="Iterations/index.html">
<title>PCG Benchmark Report</title></head>
<body><p><a href="Iterations/index.html">PCG Benchmark Report</a></p></body></html>
"""


def iteration_dir(index) -> str:
    """Return the folder a given iteration's output belongs in."""
    return os.path.join(ITERATIONS_DIR, str(index))


def is_pages_repo() -> bool:
    """True if the Pages checkout exists and is a git repo."""
    return os.path.isdir(os.path.join(PAGES_REPO, ".git"))


def inside_pages_repo(path: str) -> bool:
    """True if ``path`` is the Pages checkout or something inside it."""
    repo = os.path.normcase(os.path.abspath(PAGES_REPO))
    target = os.path.normcase(os.path.abspath(path))
    return target == repo or target.startswith(repo + os.sep)


def ensure_pages_scaffolding() -> "list[str]":
    """Create the files GitHub Pages needs at the repo root, if missing.

    ``.nojekyll`` stops Pages from running the output through Jekyll (which
    would drop files/folders it considers special), and ``index.html``
    redirects the bare Pages URL to the report home page. Returns the paths
    that were created.
    """
    created = []
    nojekyll = os.path.join(PAGES_REPO, ".nojekyll")
    if not os.path.exists(nojekyll):
        with open(nojekyll, "w", encoding="utf-8") as f:
            f.write("")
        created.append(nojekyll)

    root_index = os.path.join(PAGES_REPO, "index.html")
    if not os.path.exists(root_index):
        with open(root_index, "w", encoding="utf-8") as f:
            f.write(ROOT_REDIRECT)
        created.append(root_index)
    return created


def _git(*args, check=True) -> subprocess.CompletedProcess:
    """Run a git command inside the Pages checkout."""
    return subprocess.run(["git", "-C", PAGES_REPO, *args],
                          capture_output=True, text=True, check=check)


def _current_branch() -> str:
    proc = _git("rev-parse", "--abbrev-ref", "HEAD", check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def publish(message: str, remote: str = DEFAULT_REMOTE, branch: str = DEFAULT_BRANCH) -> bool:
    """Commit everything in the Pages checkout and push it to ``branch``.

    The push always targets ``branch`` on ``remote`` (via a ``HEAD:branch``
    refspec) because that is the branch GitHub Pages deploys from, whatever
    the local branch happens to be called.

    Returns True on a successful push. Failures are reported but not raised --
    a report that is built but not yet pushed is still a usable result, and the
    caller (``report.py``) prints the recovery hint.
    """
    if not is_pages_repo():
        print(f"Publish skipped: {PAGES_REPO} is not a git checkout.")
        return False

    created = ensure_pages_scaffolding()
    for path in created:
        print(f"Created {os.path.relpath(path, PAGES_REPO)} for GitHub Pages")

    add = _git("add", "-A", check=False)
    if add.returncode != 0:
        print(f"Publish failed: git add -- {add.stderr.strip()}")
        return False

    # Nothing staged is fine: there may still be local commits to push.
    if _git("diff", "--cached", "--quiet", check=False).returncode == 0:
        print("Nothing new to commit in the results page repo.")
    else:
        commit = _git("commit", "-m", message, check=False)
        if commit.returncode != 0:
            print(f"Publish failed: git commit -- "
                  f"{(commit.stderr or commit.stdout).strip()}")
            return False
        print(f"Committed to {_current_branch() or branch}: {message}")

    push = _git("push", remote, f"HEAD:refs/heads/{branch}", check=False)
    if push.returncode != 0:
        print(f"Publish failed: git push -- {(push.stderr or push.stdout).strip()}")
        return False

    print(f"Pushed to {remote}/{branch} -- GitHub Pages will redeploy.")
    return True
