# RefBuddy Hoops — Deployment Guide (v1.1)

Target stack: **GitHub → Render → Cloudflare DNS → hoops.refbuddy.ai**

This is a *second, independent* app alongside RefBuddy Football. Separate repo,
separate Render service, separate password, shared domain via a subdomain.

---

## Why a subdomain, not a second domain

You already own `refbuddy.ai` and it already lives on Cloudflare. Adding
`hoops.refbuddy.ai` costs nothing, takes one DNS record, and inherits every
Cloudflare setting you already tuned for football.

The alternative — running both apps behind one Render service — would require a
reverse proxy in front of two Streamlit processes. That's real complexity for no
benefit, and it couples the two apps' uptime together.

| Approach | Cost | Setup | Isolation |
|----------|------|-------|-----------|
| **`hoops.refbuddy.ai` subdomain** | $0 | 1 CNAME | Full — separate service, env vars, spend |
| Second domain (`refbuddyhoops.ai`) | ~$15–60/yr | New Cloudflare zone + nameserver repoint | Full |
| Path routing (`refbuddy.ai/hoops`) | $0 | Reverse proxy, non-trivial | None — one crash takes both down |

Separate Render services also means tournament-season load on hoops can't
degrade football, and you can see each app's spend independently.

---

## Repo layout

```
refbuddy-hoops/
├── app.py                          ← the whole application (single file)
├── Claude.png                      ← sidebar logo (app falls back to text if absent)
├── requirements.txt                ← Python dependencies
├── .gitignore                      ← keeps secrets, PDFs, and film out of git
├── DEPLOYMENT.md                   ← this file
└── .streamlit/
    ├── config.toml                 ← COMMITTED. Pins light theme.
    ├── secrets.toml.template       ← COMMITTED. Placeholders only.
    └── secrets.toml                ← LOCAL ONLY, gitignored, never pushed
```

**Never commit:** `secrets.toml`, `.env`, any NFHS/MSHSL PDF, any game film.

`config.toml` **must** be committed. Without it Streamlit auto-detects the
visitor's system colour scheme, and a ref opening the app on a phone in dark
mode gets dark BaseWeb tokens underneath the custom CSS — invisible dropdown
values, black expander headers, a dark file-uploader dropzone.

---

## Step 1 — Run locally

```bash
mkdir refbuddy-hoops && cd refbuddy-hoops
# drop in app.py, Claude.png, requirements.txt, DEPLOYMENT.md
mkdir -p .streamlit
# drop config.toml and secrets.toml.template into .streamlit/

python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# edit .streamlit/secrets.toml with your real key and a hoops password

streamlit run app.py
```

Opens at http://localhost:8501

**Check before moving on:** password screen appears → sidebar shows the Claude
logo (not the words "Powered by Claude") → four tabs, not five → upload a photo
in Film & Grade and ask "Was there a foul?" and get a real answer.

If the logo renders as text, `Claude.png` isn't sitting next to `app.py`.

---

## Step 2 — Push to GitHub

Create a **new, separate repo** — do not add this to the football repo.

```bash
git init
git add app.py Claude.png requirements.txt .gitignore DEPLOYMENT.md \
        .streamlit/config.toml .streamlit/secrets.toml.template
git commit -m "RefBuddy Hoops v1.1 — initial deploy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/refbuddy-hoops.git
git push -u origin main
```

Before pushing, grep the actual tracked file contents — not filenames:

```bash
git ls-files | xargs grep -l "sk-ant-api03" 2>/dev/null || echo "clean"
```

`git status` alone is misleading here; it won't tell you a real key ended up
inside a committed `.template` file.

---

## Step 3 — Deploy on Render

1. **render.com → New → Web Service** → connect the `refbuddy-hoops` repo
2. Settings:

| Field | Value |
|-------|-------|
| Name | `refbuddy-hoops` |
| Environment | Python 3 |
| Build command | `pip install -r requirements.txt` |
| Start command | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |
| Instance type | Starter ($7/mo) |
| Health check path | `/_stcore/health` |

3. **Environment → Environment Variables**, add both:

```
ANTHROPIC_API_KEY = sk-ant-api03-your-real-key
APP_PASSWORD      = your-hoops-crew-password
```

Use a **different** `APP_PASSWORD` than football. Basketball and football crews
barely overlap, so separate passwords mean sharing one doesn't expose the other.

4. Deploy. You get `https://refbuddy-hoops-xxxx.onrender.com`. Confirm the
   password screen appears before doing anything else.

### How the app finds these values

`st.secrets` does **not** read arbitrary environment variables — it only reads a
`secrets.toml` file on disk. Since there is no such file on Render (it's
gitignored), the app uses a `get_secret()` helper that checks, in order:

1. `os.environ` — how Render, Docker, and most hosts supply config
2. `secrets.toml` — local development and Streamlit Community Cloud
3. a legacy nested `[anthropic]` table

Every `st.secrets` access is wrapped in a broad `except Exception`, because when
no `secrets.toml` exists anywhere, simply touching `st.secrets` raises
`StreamlitSecretNotFoundError` — which is not a `KeyError` and will crash the
app on boot if caught too narrowly.

**Fail-closed safety:** if `APP_PASSWORD` is missing *and* the app detects it's
running on Render (via Render's own `RENDER=true` variable), it refuses to start
and shows an error instead of serving an unprotected app.

### Free vs Starter

Free spins down after ~15 minutes idle, so the first visitor waits ~50s for a
cold start. A crew checking a rule between quarters won't wait. Starter stays warm.

---

## Step 4 — Point hoops.refbuddy.ai at it

Your nameservers are already on Cloudflare from the football setup, so skip
straight to the records. **No Namecheap changes needed.**

### 4a. Add the custom domain in Render

Render → `refbuddy-hoops` service → **Settings → Custom Domains** → add:

- `hoops.refbuddy.ai`

Render shows you a target hostname to point at (something like
`refbuddy-hoops-xxxx.onrender.com`).

### 4b. Create the DNS record in Cloudflare

Cloudflare → `refbuddy.ai` → DNS → Records → **Add record**:

| Type | Name | Target | Proxy |
|------|------|--------|-------|
| CNAME | `hoops` | `refbuddy-hoops-xxxx.onrender.com` | Proxied (orange) |

Name is just `hoops`, not the full domain — Cloudflare appends the zone.

Leave your existing football records (`@` and `www`) exactly as they are. This
is purely additive.

### 4c. Cloudflare settings

Everything you set for football is zone-wide and already applies:

- **SSL/TLS → Full (strict)** — "Flexible" causes an infinite redirect loop
- **Always Use HTTPS: On**
- **Network → WebSockets: On** — Streamlit won't load without it
- **Speed → Rocket Loader: Off** — it breaks Streamlit's frontend
- **Caching Level: Standard**

Nothing new to change. Wait a few minutes for Render to issue the TLS cert, then
load `https://hoops.refbuddy.ai`. You should see the password screen.

---

## Step 5 — Cost controls

Three layers:

1. **App-level password** — `APP_PASSWORD` env var, covered above.
2. **Per-session frame cap** — `MAX_FRAMES_PER_SESSION = 400` in `app.py`. Every
   photo or video frame sent for analysis charges against it; the sidebar shows
   what's left. Lower to 200 to be conservative.
3. **Anthropic account spend limit** — the real backstop.

### Anthropic spend limit

1. https://platform.claude.com/settings/billing
2. **Spend limits** → **Adjust limit**
3. Set a monthly ceiling — e.g. `$50`

This is shared across both apps since they use the same API key. If you want
separate accounting, generate a second API key for hoops — usage still rolls up
to the same account and the same limit, but per-key usage is visible at
https://platform.claude.com/usage

### Prompt caching is already on

`CORE_KNOWLEDGE` (~9,000 tokens) is byte-identical on every call, so it's sent
as a cached system block. Anthropic stores the tokenized prefix and bills repeat
hits at a fraction of the normal input rate. On most models cached reads also
don't count against your input-tokens-per-minute limit.

Order matters and is already correct in the code: the cached block comes first,
the task-specific instructions second, so the prefix matches across chat, quiz,
film analysis, and pre-game generation alike.

---

## Step 6 — Updating CORE_KNOWLEDGE

`CORE_KNOWLEDGE` is a Python string literal starting around **line 69 of app.py**.
It is baked into the deployed file. It is *not* connected to your Claude Project
knowledge base — uploading a PDF to the Project does not change the deployed app.
Editing that string and pushing is the only way to update what RefBuddy knows.

### Add a game note

Find `## 7. PERSONAL GAME NOTES` and add a line under the right season:

```
**Edina JV/V 12/19/26:** Secondary defender slid into the arc late on a drive —
grounded, both feet inside. Blocking foul, and point at the arc when signaling.
```

### Add a new season's rule changes

Find `## 0. 2023–2026 NFHS & MSHSL RULES CHANGES & UPDATES` and add a dated block
in the same format (rule number, year, old, new, why it matters), then add a row
to the Quick-Reference table at the bottom of that section.

### Update MSHSL modifications

Find `## 2. MSHSL MINNESOTA-SPECIFIC RULES & MODIFICATIONS`. MSHSL typically
posts new Minnesota Rules Modifications in the fall at
https://www.mshsl.org/sports-and-activities/basketball-boys and
https://www.mshsl.org/sports-and-activities/basketball-girls

### Deploy the update

```bash
git add app.py
git commit -m "Update CORE_KNOWLEDGE — 2026-27 MSHSL modifications"
git push
```

Render auto-deploys on push. Watch the deploy log; ~2 minutes.

---

## Troubleshooting

**Infinite redirect loop at hoops.refbuddy.ai**
Cloudflare SSL/TLS mode is Flexible. Change to **Full (strict)**. Zone-wide, so
this would break football too — check there first.

**Page loads but spins forever / "Please wait…"**
WebSockets off in Cloudflare, or Rocket Loader on.

**Sidebar shows "Powered by Claude" as text instead of the logo**
`Claude.png` didn't make it into the commit. `git ls-files | grep Claude.png`
should return it. The app is designed to degrade to text rather than show a
broken image icon, so this fails quietly.

**"ANTHROPIC_API_KEY not found"**
Env var isn't set on Render, or has a typo. Names are case-sensitive.

**`StreamlitSecretNotFoundError: No secrets found` on boot**
You're running an older `app.py` that read `st.secrets[...]` directly and caught
only `KeyError`. v1.1 fixed this — pull the latest.

**Password screen won't accept the password**
Check for a trailing space in the Render env var value — Render preserves
whitespace exactly.

**"Session analysis limit reached"**
Working as designed — 400 frames per session. Refresh for a new session, or
raise `MAX_FRAMES_PER_SESSION`.

**Dark/invisible dropdowns on a phone**
`.streamlit/config.toml` isn't committed. That file pins light mode.

**Render deploy fails on opencv**
`requirements.txt` must specify `opencv-python-headless`, not `opencv-python`.
The non-headless build needs GUI libraries Render doesn't have.

**Photo upload gives "Could not read image"**
HEIC from an iPhone isn't decodable by OpenCV. On iOS: Settings → Camera →
Formats → **Most Compatible** to shoot JPEG, or screenshot the photo (screenshots
are always PNG).

---

## Cost reference

`claude-sonnet-4-6`, billed per million tokens, input and output separately.
Current rates: https://platform.claude.com/settings/billing

| Operation | Approximate input tokens |
|-----------|--------------------------|
| System prompt (CORE_KNOWLEDGE) | ~9,000 per call — **cached after first hit** |
| Chat question | ~9,000 + conversation history |
| Quiz question | ~9,000 |
| Photo analysis, 4 stills | ~15,000 |
| Film analysis, 30 frames | ~55,000 |
| Crew Eval, 40 frames | ~70,000 |

Photos are dramatically cheaper than video, which is why the Film & Grade tab
leads with them. Three or four well-chosen stills — defender establishing
position, point of contact, the finish — usually answer the question better than
30 frames of a clip, and cost a quarter as much.

---

## Privacy & IP posture

- No conversations or uploads are persisted server-side; everything lives in
  session memory and is discarded when the session ends.
- Uploads are transmitted to the Anthropic API for processing. Don't upload
  anything containing sensitive personal information about students.
- The system prompt instructs the model never to reproduce verbatim NFHS/MSHSL
  text — it summarizes and cites rule numbers instead.
- Source rulebook PDFs are excluded by `.gitignore` and must never be committed
  or served.
- The Terms of Use expander in the footer states non-affiliation with NFHS and
  MSHSL, disclaims warranty, and tells users to own a current rulebook.
