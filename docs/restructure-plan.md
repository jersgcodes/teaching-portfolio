# Restructure plan: `teaching-portfolio/` -> `content-core/` + new `growth/` and `labs/`

This document describes the one-time migration from the current single directory `~/claude/teaching-portfolio/` to the locked three-repo architecture (see `CLAUDE.md` and ADR 0001).

**Status:** PENDING execution. Do not start until current `feat/design-lock` work is reviewed and committed.

---

## Decision: rename in place vs. fresh directory

**Chosen: rename `teaching-portfolio/` -> `content-core/` in place.**

- The directory has no commits yet (`git status` shows untracked files only). A rename is just `mv` — git history is empty so nothing is lost.
- All current files (CLAUDE.md, TASKS.md, USER_ACTIONS.md, docs/adr, schema, taxonomy, AGENTS.md, projects.yaml) belong in `content-core` per the locked design. No file needs to move out.
- New repos (`growth`, `labs`) are created as fresh sibling directories.

If the directory had commits, the alternative (fresh directory + `git mv` history-preserving migration) would be needed. Skip that complexity.

---

## Steps (execute in a build session)

### 1. Commit the design-lock work first

On `feat/design-lock` branch in `~/claude/teaching-portfolio/`:

```
git add .gitignore CLAUDE.md TASKS.md USER_ACTIONS.md docs/ schema/ taxonomy/ AGENTS.md projects.yaml
git commit -m "feat: design lock — architecture, taxonomy, schemas, ADRs"
```

**Do not push yet** — the directory is about to be renamed and the GitHub repo it'll back to doesn't exist yet.

### 2. Rename the directory

```
cd ~/claude
mv teaching-portfolio content-core
```

### 3. Create the GitHub repo for `content-core`

Public repo (per locked decision; flip to private only if team objects):

```
cd ~/claude/content-core
gh repo create jersgcodes/content-core --public --source=. --remote=origin
git push -u origin feat/design-lock
gh pr create --title "Initial design lock" --body "See CLAUDE.md and docs/adr/."
```

(Or merge `feat/design-lock` into a fresh `main` directly if no PR review is needed.)

### 4. Bootstrap `growth/`

```
cd ~/claude
bash ~/claude/scripts/new-project.sh growth   # uses workspace project template
cd growth
gh repo create jersgcodes/growth --private --source=. --remote=origin
git submodule add https://github.com/jersgcodes/content-core.git core
git commit -m "chore: add content-core as submodule"
```

### 5. Bootstrap `labs/`

Same as step 4 with `labs` instead of `growth`.

### 6. Scaffold Next.js in each consumer site

In each of `growth/` and `labs/`:

```
pnpm create next-app@latest . --typescript --app --tailwind --no-src-dir --import-alias "@/*"
```

Configure for static export (`next.config.js` -> `output: 'export'`).

### 7. Wire shared components from `content-core`

Each site's `next.config.js` and tsconfig point to `core/components/` for shared UI.

### 8. Set up Cloudflare Pages

For each consumer repo:

- Connect repo via Cloudflare dashboard
- Build command: `pnpm build`
- Output dir: `out` (Next.js static export)
- Custom domain: `growth.jersgcodes.com` / `labs.jersgcodes.com`

### 9. Cloudflare Access on labs

In Cloudflare dashboard for `labs.jersgcodes.com`:

- Create Access Application covering the whole zone
- Add policy: email allowlist or M365 SSO
- Test: unauthenticated -> challenge; authenticated -> through

### 10. Verify deploys

- `growth.jersgcodes.com` loads publicly
- `labs.jersgcodes.com` requires login
- Both render placeholder content

---

## Open execution risks

- **Submodule path conflicts** — if Next.js `app/` and submodule `core/components/` resolve oddly, may need a `tsconfig.paths` adjustment.
- **First Cloudflare Pages build for static-export Next.js** — sometimes needs `experimental.images.unoptimized: true` or matching adapter.
- **Cloudflare Access M365 SSO** — depends on whether Jerome's M365 tenant allows third-party OIDC. Fallback: email OTP allowlist.
- **GitHub repo rename later** — if `jersgcodes/content-core` is the wrong final name, repo rename is supported by GitHub but requires updating the submodule URL in each consumer.

---

## Rollback

If migration goes sideways before pushing:

```
cd ~/claude
mv content-core teaching-portfolio
```

After pushing, GitHub repos can be deleted via `gh repo delete`. Submodules in unpushed consumer repos can be removed with `git submodule deinit` + `git rm`.

---

## Post-migration TASKS.md updates

- Mark Task 2 DONE
- Move to Phase 1 (aggregator + validators)
