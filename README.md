# CSDI Lab — Graduate Research Journey (Student Template)

A ready-to-use template for graduate students (Master's & PhD) at **CSDI Lab, National Taipei University of Technology (NTUT)**. It publishes your academic profile, semester timeline, research showcase, and password-protected meeting notes as a clean website hosted on **GitHub Pages** for free.

> **New to GitHub?** Don't worry. This guide walks you through every step from zero using the GitHub website — no command line or programming required for daily updates.

---

## What the website looks like

| Page | What's on it |
|---|---|
| **Home** | Your profile, academic milestones (Semester 1–4), and research showcase |
| **Regular meetings** | A public list of meeting dates; each opens a password-protected note |
| **Research showcase** | Featured projects, demos, publications, or thesis progress |

---

## Step 0 — What you need before starting

- A **GitHub account** (free) — sign up at [github.com](https://github.com) if you don't have one.
- A web browser with internet access.
- That's it. You can edit everything directly on the GitHub website.

---

## Step 1 — Create your own repository from this template

> A **repository** (or "repo") is like a folder on GitHub that stores your project files and tracks all changes.

1. On the GitHub page for this template repo, click the green **"Use this template"** button (near the top-right) → then **"Create a new repository"**.
2. **Owner**: Select your GitHub account (or supervisor's organization as instructed).
3. **Repository name**: Choose something short and lowercase, such as `2026yourname` (e.g. `2026verin` or `2026student`).
   - ⚠️ **Avoid spaces, uppercase letters, or special symbols.**
4. **Visibility**: Select **Private** — this keeps your raw meeting notes, draft writing, and research files private.
5. Click **"Create repository"**. GitHub copies all files into your new repo.

---

## Step 2 — Fill in your profile (`docs/_config.yml`)

This file configures your website name, link addresses, and profile details shown on the homepage.

1. In your new repo, click into the `docs/` folder → click on `_config.yml`.
2. Click the **pencil icon ✏️** (top-right of the file view) to edit.
3. Update the fields below:

```yaml
title: Graduate Research Journey
url: "https://yourusername.github.io"   # ← replace with your GitHub username
baseurl: "/2026yourname"                # ← MUST match your repository name exactly!

student:
  name: "Your Full Name"
  degree: "Master's Student"            # e.g. "Master's Student" or "PhD Student"
  lab: "CSDI Lab"
  university: "National Taipei University of Technology"
  joined: "2026"
  interests: "Computer Vision, Autonomous Systems, Deep Learning"
  summary: "A short 1–2 sentence introduction about your research direction."
```

> ⚠️ **CRITICAL**: `baseurl` must start with a slash `/` and match your exact repository name (e.g., `/2026verin`). If this does not match, the website CSS and styles will fail to load!

4. Scroll down and click **"Commit changes"** → **"Commit directly to the main branch"** → **"Commit changes"**.

> **Committing** is just GitHub's term for "saving". Every commit records what changed and when, so you can always go back.

---

## Step 3 — Set your meeting password (Secret)

Meeting notes are encrypted with AES-256-GCM. A password secret is required so only you and your supervisor can unlock them.

1. In your repository, click the **Settings** tab (top menu bar).
2. In the left sidebar, click **Secrets and variables** → **Actions**.
3. Click the green **"New repository secret"** button.
4. Set:
   - **Name**: `MEETING_PASSWORD`
   - **Secret**: Choose a strong, private password and share it with your advisor. (Do **not** use simple passwords like `hope` for real research).
5. Click **"Add secret"**.

> Repository secrets are securely hidden by GitHub. They are never published and cannot be viewed by visitors.

---

## Step 4 — Turn on the website (GitHub Pages)

1. In **Settings** → click **Pages** in the left sidebar.
2. Under **"Build and deployment"**:
   - Set **Source** to **GitHub Actions**.
3. Click the **Actions** tab (top menu bar).
4. Click **"Publish graduate journey"** in the left workflow list → click the **"Run workflow"** button → confirm **"Run workflow"**.
5. Wait 1–2 minutes. When you see a green checkmark ✅, your site is live!
6. Visit your website at:
   ```text
   https://yourusername.github.io/2026yourname/
   ```

---

## Step 5 — Prepare and add a regular meeting note ⭐

Before each supervision meeting, prepare a structured meeting note:

1. Click on `_templates/` → open `regular-meeting.rst` → copy all text.
2. Go to the `meetings/` folder (at the root of your repo, **not** inside `docs/`).
3. Click **"Add file"** → **"Create new file"**.
4. Name the file using the meeting date format: `YYYY-MM-DD.rst` (e.g. `2026-11-04.rst`).
5. Paste the template content and fill in:
   - **Sections 1–4**: Fill in at least 24 hours before your meeting (progress, learnings, questions).
   - **Section 5**: Complete after the meeting (agreed decisions and next steps).
6. Click **"Commit changes"**.

GitHub Actions will automatically encrypt the note, add the date to the meeting list, and deploy it securely!

### Adding private figures or photos to a meeting note

- Store images inside `meetings/assets/` (e.g. `meetings/assets/2026-11-04-results.png`).
- Reference them in your `.rst` file like this:

```rst
.. figure:: assets/2026-11-04-results.png
   :alt: Model convergence graph
   :width: 720px
   :align: center

   Training and validation loss curve over 100 epochs.
```

- Each image must be under 8 MB (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`).
- The build script converts the image into encrypted data inside the page ciphertext. **No unencrypted image file is ever published to the public website.**

### Adding math equations to a meeting note

You can write standard LaTeX math formulas directly in your `.rst` note:

- **Inline math formula**: `:math:`E = mc^2`` or `:math:`\mathbf{x} \in \mathbb{R}^n``
- **Block equation**:

```rst
.. math::

   \mathbf{x}_{t+1} = A \mathbf{x}_t + B \mathbf{u}_t
```

MathJax 3 automatically renders clean mathematical typography with scrollable support when unlocked.

---

## Step 6 — Add or edit semesters & research showcases (.md files) ⭐

Just like the highlights in the internship site, you **never need to edit HTML**. Every semester and research showcase is a simple Markdown (`.md`) file with front matter fields. The homepage updates automatically.

### 1. Change your profile image in the header

By default, the header shows an abstract monogram graphic. To use your own photo instead:

1. Upload your photo to `docs/assets/photos/` (e.g. `docs/assets/photos/profile.jpg`).
2. Open `docs/_config.yml`, add or uncomment `photo:` under `student:`:
   ```yaml
   student:
     name: "Jane Doe"
     degree: "Master's Student"
     photo: /assets/photos/profile.jpg   # ← path to your photo
     lab: "CSDI Lab"
   ```
3. Commit the changes. If you remove or comment out `photo`, it automatically reverts to the monogram graphic.

### 2. Manage semesters (`docs/_semesters/*.md`)

Each semester card on your homepage timeline is generated from a file in `docs/_semesters/`:

1. To edit an existing semester (e.g. Semester 1), open `docs/_semesters/01-semester.md` and click the **pencil icon ✏️**.
2. To add a new semester (e.g. Semester 5), copy `_templates/semester.md` and create `docs/_semesters/05-semester.md`.
3. Fill in the fields:
   ```yaml
   ---
   order: 1
   period: "Semester 1"
   title: "Building foundations"
   description: "Python, statistical learning, literature review, and baseline experiments."
   image: /assets/photos/semester-1-sample.png   # Optional: photo or chart
   caption: "Literature review & baseline experiment setup" # Optional caption
   ---
   ```
4. If you don't have a photo for that semester, simply delete or omit the `image:` and `caption:` lines.

### 3. Manage research showcases (`docs/_showcases/*.md`)

Each card in your **Research Showcase** is generated from a file in `docs/_showcases/`:

1. Open `_templates/showcase.md` and copy the content.
2. In `docs/_showcases/`, click **"Add file"** → **"Create new file"**.
3. Name it after your project (e.g. `robot-navigation.md` or `01-pose-estimation.md`).
4. Fill in the fields:
   ```yaml
   ---
   order: 1
   title: "Autonomous Mobile Robot Navigation"
   date: 2026-10-01
   tags:
     - "Robotics"
     - "ROS 2"
     - "Master's Thesis"
   image: /assets/photos/your-project.png   # Optional: cover image
   summary: "A 2–3 sentence overview of the research problem, methodology, and key results."
   links:
     - label: "Code Repository"
       url: "https://github.com/yourusername/repo"
     - label: "Read Paper"
       url: "https://arxiv.org/abs/..."
   ---
   ```
5. *(Optional)* You can write longer research notes, detailed results, equations, and figures below the `---` line. A **Read Details →** link will automatically appear on the showcase card so visitors can view the full project page!
6. Click **"Commit changes"**. The showcase card will appear immediately on the homepage.

---

## Repository layout

```text
2026yourname/
├── .github/workflows/publish.yml      # Auto-builds encrypted site — don't edit
├── .gitignore                         # Prevents accidental leak of local cache
├── docs/                              # ← Everything here is PUBLIC on your website
│   ├── _config.yml                    # Your profile settings & baseurl
│   ├── _layouts/default.html          # Page layout & dark/light theme toggle
│   ├── _data/meetings.json            # Auto-generated meeting date list
│   ├── _semesters/                    # ← Add/edit semester cards here (.md files)
│   │   ├── 01-semester.md
│   │   ├── 02-semester.md
│   │   ├── 03-semester.md
│   │   └── 04-semester.md
│   ├── _showcases/                    # ← Add research showcase cards here (.md files)
│   │   ├── 01-pose-estimation.md
│   │   └── 02-sensor-calibration.md
│   ├── _templates/                    # Templates for semesters & showcases
│   ├── assets/
│   │   ├── photos/                    # Public photos (profile, semester, showcase)
│   │   └── style.css                  # Website design stylesheet & fonts
│   ├── index.md                       # Public homepage (auto-reads collections)
│   └── meetings/index.html            # Public meeting list index
├── meetings/                          # ← PRIVATE raw meeting notes (.rst files)
│   ├── assets/                        # Private meeting images (never published directly)
│   └── 2026-10-21.rst                 # Example meeting note
├── research/                          # ← PRIVATE code, notebooks, datasets, drafts
├── scripts/build_protected_meetings.py# Encrypts notes with AES-256-GCM + MathJax
├── _templates/                        # Copyable templates for meetings, semesters, showcases
└── README.md
```

---

## Troubleshooting

| Problem | Cause | How to fix |
|---|---|---|
| **Website has no styling / broken layout** | `baseurl` in `docs/_config.yml` doesn't match repo name | Open `docs/_config.yml`, set `baseurl: "/your-repo-name"`, save, and re-run workflow. |
| **Meeting page password error** | Wrong password entered | Enter the exact secret string you set in `MEETING_PASSWORD`. |
| **Build fails (red ❌ in Actions)** | Missing secret | Go to **Settings > Secrets and variables > Actions** and ensure `MEETING_PASSWORD` is created. |
| **Dark / light mode icon not showing** | `_site/` folder was uploaded to GitHub | Never commit or upload `_site/` to GitHub. It is already excluded in `.gitignore`. |
| **Meeting note not appearing** | File has incorrect extension or location | File must be in `meetings/` (not `docs/`) and named `YYYY-MM-DD.rst`. |

---

## Privacy & Security Reminders

- **Everything in `docs/` is public**: Anyone with your website link can see files in `docs/`. Never put confidential data, private tokens, or unencrypted research notes in `docs/`.
- **`meetings/` and `research/` stay private**: In your private repository, your `.rst` sources and research notebooks remain accessible only to you and your advisor.
- **Meeting encryption**: Only the encrypted ciphertext is published to GitHub Pages. Visitors cannot read notes without the `MEETING_PASSWORD`.
