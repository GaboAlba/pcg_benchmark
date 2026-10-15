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
#: Where iteration folders (``0``, ``1``, ... ) for the reasoning-model
#: report live.
ITERATIONS_DIR = os.path.join(PAGES_REPO, "Iterations")
#: Where the non-reasoning-model (gpt-4.1) report's iterations live -- its
#: own numbered folders, nested under the reasoning report's.
NONREASONING_ITERATIONS_DIR = os.path.join(ITERATIONS_DIR, "nonreasoning")

#: The two independent reports published side by side, keyed by the name
#: passed to ``--track`` / ``iteration_dir``. Each maps to the folder its
#: iterations live in and the bare GitHub Pages URL points visitors to a
#: chooser (see ``LANDING_PAGE``) rather than either one directly.
TRACKS = {
    "reasoning": ITERATIONS_DIR,
    "nonreasoning": NONREASONING_ITERATIONS_DIR,
}
DEFAULT_TRACK = "reasoning"

DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "main"

# GitHub Pages serves the repo root, but the two reports' home pages are one
# (reasoning) or two (non-reasoning) levels down. Rather than redirect the
# bare Pages URL straight to one of them, land on a chooser so both are
# reachable from the published site -- the two reports cross-link each other
# from there (see report.py's --sibling-label/--sibling-href).
LANDING_PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PCG Benchmark Report</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
         margin: 0; color: #1f2933; background: #f5f7fa; }
  .container { max-width: 640px; margin: 0 auto; padding: 64px 24px; }
  h1 { font-size: 26px; margin: 0 0 8px; }
  p.subtitle { color: #616e7c; margin: 0 0 32px; }
  .cards { display: grid; gap: 16px; }
  a.card { display: block; background: #fff; border-radius: 10px; padding: 20px 22px;
           box-shadow: 0 1px 3px rgba(0,0,0,.08); color: inherit; text-decoration: none; }
  a.card:hover { box-shadow: 0 2px 6px rgba(0,0,0,.12); }
  a.card h2 { margin: 0 0 4px; font-size: 17px; color: #2563eb; }
  a.card p { margin: 0; color: #616e7c; font-size: 14px; }
</style></head>
<body><div class="container">
<h1>PCG Benchmark Report</h1>
<p class="subtitle">Comparing LLM-generated levels against non-LLM baselines.</p>
<div class="cards">
  <a class="card" href="Iterations/index.html">
    <h2>Reasoning-model report &rarr;</h2>
    <p>LLM-generated levels from a reasoning model vs. non-LLM baselines.</p>
  </a>
  <a class="card" href="Iterations/nonreasoning/index.html">
    <h2>Non-reasoning (gpt-4.1) report &rarr;</h2>
    <p>LLM-generated levels from gpt-4.1 (non-reasoning) vs. non-LLM baselines.</p>
  </a>
</div>
</div></body></html>
"""


def iteration_dir(index, track: str = DEFAULT_TRACK) -> str:
    """Return the folder a given iteration's output belongs in.

    ``track`` picks which of the two published reports (see ``TRACKS``) the
    iteration belongs to.
    """
    try:
        iterations_dir = TRACKS[track]
    except KeyError:
        raise ValueError(f"Unknown track {track!r}; choose one of {sorted(TRACKS)}")
    return os.path.join(iterations_dir, str(index))


def is_pages_repo() -> bool:
    """True if the Pages checkout exists and is a git repo."""
    return os.path.isdir(os.path.join(PAGES_REPO, ".git"))


def inside_pages_repo(path: str) -> bool:
    """True if ``path`` is the Pages checkout or something inside it."""
    repo = os.path.normcase(os.path.abspath(PAGES_REPO))
    target = os.path.normcase(os.path.abspath(path))
    return target == repo or target.startswith(repo + os.sep)


def ensure_pages_scaffolding() -> "list[str]":
    """Create/refresh the files GitHub Pages needs at the repo root.

    ``.nojekyll`` stops Pages from running the output through Jekyll (which
    would drop files/folders it considers special) and is only ever created
    once, empty. ``index.html`` is the chooser linking to both reports
    (``LANDING_PAGE``) -- rewritten every call (like the reports' own home
    pages) so it can't drift from the reports it links to. Returns the paths
    that were (re)written.
    """
    written = []
    nojekyll = os.path.join(PAGES_REPO, ".nojekyll")
    if not os.path.exists(nojekyll):
        with open(nojekyll, "w", encoding="utf-8") as f:
            f.write("")
        written.append(nojekyll)

    root_index = os.path.join(PAGES_REPO, "index.html")
    with open(root_index, "w", encoding="utf-8") as f:
        f.write(LANDING_PAGE)
    written.append(root_index)
    return written


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

    written = ensure_pages_scaffolding()
    for path in written:
        print(f"Wrote {os.path.relpath(path, PAGES_REPO)} for GitHub Pages")

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
