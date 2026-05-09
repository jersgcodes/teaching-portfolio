# ADR 0002 — Cloudflare Pages over Hetzner VPS for hosting

- Status: Accepted
- Date: 2026-05-07
- Conflicts with: original CLAUDE.md note ("auto-deploy via Coolify on the existing VPS")

## Context

Workspace `DEPLOYMENT.md` documents the existing Hetzner VPS at `46.225.51.40` (Ubuntu 24.04) running other projects via systemd + manual `git pull`. The original teaching-portfolio CLAUDE.md mentioned Coolify, but workspace policy says "no Coolify."

The teaching portfolio is **two static sites** with build-time data fetching. Long-term plans mention sprinkled interactivity (lens toggles, expandable diagrams, embedded sandboxes) and possibly a future runtime AI explainer (deferred to v1.5+).

## Options considered

### A. Existing Hetzner VPS, systemd + manual pull
Keep all Jerome's projects under one host for ops consistency.

- **Pros:** consistent with workspace pattern; full control
- **Cons:** VPS isn't a CDN; slower edge delivery; SSL/auth/DNS configuration required for two new subdomains; manual deploy adds friction; runs idle 24/7 to serve static content.

### B. GitHub Pages
Free, push-to-deploy.

- **Pros:** zero cost, zero ops
- **Cons:** no edge functions for the eventual AI explainer; clunky custom domain on apex; no built-in auth gate for labs (would need third-party).

### C. Cloudflare Pages on `jersgcodes.com` subdomains (chosen)
Push-to-deploy from each consumer repo. Free tier covers traffic. Cloudflare Workers available alongside Pages for any future server-side need (AI explainer endpoint, etc.). Cloudflare Access gates labs zone for free.

- **Pros:** edge CDN delivery; push-to-deploy; free; Workers ready when needed; Access auth comes free for labs; matches existing domain.
- **Cons:** new platform to learn (small surface); separate from VPS workflow.

### D. Vercel
Similar to Cloudflare Pages.

- **Pros:** great DX, Next.js-native
- **Cons:** auth gating for labs requires Vercel Pro ($$) or third-party; fewer free serverless allowances than Cloudflare's combined Pages+Workers.

## Decision

**Cloudflare Pages on `growth.jersgcodes.com` and `labs.jersgcodes.com`.**

Labs zone is gated by Cloudflare Access (free up to 50 seats; M365 SSO compatible).

VPS reserved for projects that genuinely need a server (FastAPI services, Telegram bots, scheduled jobs).

## Consequences

- Edge delivery (lower latency) for growth's public visitors.
- Auth gating on labs is a Cloudflare Access dashboard config, not application code — labs's Next.js doesn't need to know about auth.
- If runtime AI features become v1.5+ scope, they sit in Cloudflare Workers next to Pages — no migration.
- DNS for `jersgcodes.com` already lives on Cloudflare per workspace `DEPLOYMENT.md`, so no DNS provider change.
- Project CLAUDE.md was updated to remove the original Coolify mention.
