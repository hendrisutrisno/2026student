# CSDI Lab — Graduate Research Journey (student template)

A public **student journey** site, with a public **regular meeting date list** and password-protected meeting pages generated from editable reStructuredText (`.rst`) files. Each student's **research code, notebooks, and source meeting notes** belong in their **private copy** of this repository.

## How this is secured

- Only `docs/` is compiled into the public website using GitHub Actions.
- Original meeting files live at the repository root in `meetings/YYYY-MM-DD.rst`, **outside `docs/`**.
- Private meeting figures and photos are stored in `meetings/assets/` (**outside `docs/`**). They are automatically base64-embedded and encrypted directly within the note's ciphertext. No unencrypted image files are ever published to GitHub Pages.
- Each `.rst` source is converted to HTML and encrypted using AES-256-GCM. The key is derived with PBKDF2-HMAC-SHA256 using a fresh random salt. The public page contains only encrypted content and a password form.
- The public `/meetings/` page lists dates and links to encrypted meeting pages.
- The Actions secret `MEETING_PASSWORD` is required; a missing secret causes the build to **fail rather than publish plaintext**.
- Research source and results should live in `research/`, outside `docs/`. The site does not link to them.

**The public template itself is for demonstration:** the example `.rst` is visible to anyone browsing this public repository. A password does not hide repository source. For real research notes and code, create a **private** student repository.

**Use a long, unique password for each real student repository.** `hope` is the requested **demonstration password only**, and is not suitable for protecting confidential research.

## 1. First-time setup of this public `2026student` template

1. In **Settings > Secrets and variables > Actions > New repository secret**, set:
   - Name: `MEETING_PASSWORD`
   - Value: `hope` (demo only)
2. In **Settings > Pages > Build and deployment**, change **Source** from *Deploy from a branch* to **GitHub Actions**.
3. Open **Actions > Publish graduate journey > Run workflow** (or push a commit).
4. Confirm the Pages deployment is successful.
5. Open `https://hendrisutrisno.github.io/2026student/` and click **Regular meetings > 2026-10-21**. Enter `hope`.

The password is **not stored in** `_config.yml`, `.rst`, JavaScript, or the public workflow file. GitHub injects it securely during the build.

## 2. Creating a student's private repository

1. Mark `2026student` as a **Template repository** in **Settings > General**.
2. Click **Use this template** and create a new **private** repository such as `2026verin`, owned by `hendrisutrisno`.
3. Invite the student as a collaborator. Keep administrative access for the supervisor.
4. Update **`docs/_config.yml`**, especially:

   ```yaml
   baseurl: "/2026verin"
   student:
     name: "Verin"
     degree: "Master's Student"
     lab: "CSDI Lab"
     university: "National Taipei University of Technology"
     joined: "2026"
     interests: "To be updated"
   ```
5. In the new repository, set **its own** `MEETING_PASSWORD` Actions secret to a strong password (template repositories **do not copy** secrets).
6. Under **Settings > Pages**, choose **GitHub Actions**.
7. Run **Publish graduate journey** in Actions.
8. Remove/replace the sample `meetings/2026-10-21.rst` with the student's own record.

With GitHub Pro, a private personal repository can publish a public GitHub Pages website. The **published website is not private**; its meeting pages use encryption to protect their content.

## 3. Adding a regular meeting

1. Copy `_templates/regular-meeting.rst` into `meetings/YYYY-MM-DD.rst` (e.g. `meetings/2026-10-28.rst`).
2. Complete sections 1–4 at least 24 hours before the meeting. Complete section 5 afterwards.
3. Commit to the private student's `main` branch.
4. GitHub Actions automatically regenerates the public date index and encrypts each note at an address such as `https://hendrisutrisno.github.io/2026verin/meetings/2026-10-28.html`.

### Meeting rules & security

- **Never move `.rst` files into `docs/`**: Source meeting notes must stay in `meetings/` (outside `docs/`). Only encrypted HTML is published.
- **Private meeting photos**: Store photos in `meetings/assets/` (not in `docs/`). Reference them in `.rst` via `.. figure:: assets/photo.jpg`. The build automatically embeds them as encrypted base64 data URIs directly inside the ciphertext. Max 8 MB per image (`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`).
- **Math equations**: You can write LaTeX equations natively:
  - Inline: `:math:`E = mc^2``
  - Block equation:
    ```rst
    .. math::

       \mathbf{x}_{t+1} = A \mathbf{x}_t + B \mathbf{u}_t
    ```
  MathJax 3 renders them with LaTeX typography once unlocked.
- **Do not commit generated files**: Never commit `_site/`, `.jekyll-cache/`, or generated `docs/meetings/*.html` to GitHub. GitHub Actions generates them securely during build.

## 4. Folder layout

```text
2026student/
├── .github/workflows/publish.yml      # build/deploy encrypted meeting pages
├── docs/                              # only folder released to the public website
│   ├── _config.yml
│   ├── _layouts/default.html
│   ├── _data/meetings.json             # overwritten by workflow
│   ├── assets/style.css
│   ├── index.md                        # public student homepage
│   └── meetings/index.html             # public date list
├── meetings/                          # .rst sources; private in student repo
│   └── 2026-10-21.rst                  # harmless sample in public template
├── research/                           # private experiments/code (add in student repos)
├── scripts/build_protected_meetings.py
├── _templates/regular-meeting.rst
└── README.md
```

Encrypted HTML pages are **created in the GitHub Actions runner** during publication and do not need to be committed to GitHub.

## 5. If the page does not publish

- Go to **Actions** and open the failed **Publish graduate journey** workflow.
- If it reports `Missing MEETING_PASSWORD`, create the Actions repository secret.
- Confirm **Settings > Pages > Source** is **GitHub Actions**, not *Deploy from a branch*.
- Confirm that the student's `docs/_config.yml` `baseurl` exactly matches the repository name.

## 6. Security limitations

- `hope` is only a demonstration password: a short common word is vulnerable to offline guessing of encrypted static content. Use a strong, unique secret for real records.
- Anyone with access to the private source repository can read the original `.rst` files without entering the site password; this is expected.
- Password-protected static HTML does not offer account-based access control, individual revocation, or protection against a person who has already decrypted or downloaded the page.
- Treat confidential industrial data, human-subject data, and unpublished manuscripts according to applicable access and publication rules. Encryption of a public page does not override those obligations.
