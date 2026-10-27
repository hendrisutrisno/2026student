# CSDI Lab graduate research journey

A GitHub Pages template for graduate students at CSDI Lab, National Taipei University of Technology. It shows a public profile, semester timeline, research projects, and a list of encrypted meeting notes.

Edit your profile in YAML and your research content in Markdown or reStructuredText. Daily updates do not require HTML, CSS, or JavaScript.

## 1. Choose the right repository visibility

**Use a private source repository for confidential meeting notes.** Encryption protects the published meeting pages. It does not hide files or Git history in a public GitHub repository.

- GitHub Pages is available in public repositories on GitHub Free. Pages from a private repository requires a supported paid plan, such as GitHub Pro or Team. Check [GitHub Pages availability](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages).
- A private source repository normally publishes a **public website**. Private website access is a separate feature for eligible organizations. Do not assume visitors need a GitHub login.
- The template contains fictional examples. Replace them before presenting the site as your own work.
- Profile details, public images, project pages, meeting dates, and encrypted meeting files are public. Keep confidential material outside `docs/`.
- Use a public source repository only for fictional or approved public notes. The workflow stops for public sources unless you explicitly set the Actions repository variable `ALLOW_PUBLIC_MEETING_SOURCES` to `true`. This setting does not make source notes private.

## 2. Create your student repository

1. Sign in to GitHub.
2. Open the lab template and select **Use this template > Create a new repository**.
3. Choose your account and a short repository name, such as `2026yourname`.
4. Choose **Private** if you will keep real meeting notes in this repository.
5. Create the repository.

If **Use this template** is missing, ask the lab maintainer to enable **Settings > General > Template repository** on the source. You can also download its ZIP, create an empty repository, and upload all project files, including `.github/workflows/publish.yml`. Check that the workflow file is present after uploading.

## 3. Set up your public profile

Open `docs/_config.yml`, select **Edit**, and update the `student` fields. Save with **Commit changes** on your repository's default branch. A commit records a saved version of a file.

```yaml
title: Graduate Research Journey
url: "https://yourusername.github.io"
baseurl: "/2026yourname"

student:
  name: "Your Full Name"
  email: "your.email@example.com" # Leave empty to hide the email link.
  degree: "Master's Student"
  lab: "CSDI Lab"
  university: "National Taipei University of Technology"
  joined: "2026"
  interests: "Your research interests"
  summary: "Describe your research direction in one or two sentences."
  # photo: /assets/photos/profile.jpg
```

Use spaces for indentation, not tabs. Keep quotation marks around text containing a colon. `degree` is your current student status; use, for example, `Master's Student` or `PhD Student`.

`docs/_config.yml` is the only site configuration file. The publishing workflow gets the correct website address from GitHub Pages, so a copied repository can use a different owner or name without editing code. Set `url` and `baseurl` in this file for local preview. For a user site named `yourusername.github.io`, use `baseurl: ""`. For a project site, use `/repository-name` without a final slash.

Set `student.email` to the contact address you want to publish. It appears as a clickable contact link in your profile. Replace the example address with your own. Leave it empty (`email: ""`) or remove the field to hide it. This address is public.

To add a profile photo, upload it to `docs/assets/photos/` and set `student.photo` to `/assets/photos/profile.jpg`. Remove or comment out `photo` to use your initial instead. Images here are public.

## 4. Set the meeting password

1. Open **Settings > Secrets and variables > Actions**.
2. Under **Secrets**, select **New repository secret**.
3. Name it `MEETING_PASSWORD`.
4. Use a long, unique password. Share it privately with your supervisor.
5. Save the secret.

Do not put the password in a file, commit message, public issue, or workflow command. GitHub does not let you read a saved secret back. Keep a separate private copy.

For a public demonstration repository only, open the **Variables** tab and set `ALLOW_PUBLIC_MEETING_SOURCES` to `true`. In a public repository, source files and their history are already public, regardless of the meeting password.

## 5. Publish with GitHub Pages

1. Open **Settings > Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.
3. Open **Actions > Publish graduate journey**.
4. Select **Run workflow** and choose your default branch.
5. Wait for both the build and deployment jobs to finish successfully.
6. Open the website URL shown by the deployment.

Future changes on the default branch publish automatically. A manual run on another branch builds for checking and does not deploy. No branch name is hardcoded. If GitHub asks to approve a deployment in the `github-pages` environment, review and approve it as the repository owner.

## 6. Update your research journey

The site uses files in `docs/` as its public source. Keep private notes in the root `meetings/` folder.

### Semester timeline

Edit files in `docs/_semesters/`. To add a semester, copy `_templates/semester.md` to a new file such as `docs/_semesters/05-semester.md`.

```yaml
---
order: 5
period: "Semester 5"
title: "Evaluating the method"
description: "Describe the experiments and the progress made this semester."
# image: /assets/photos/experiment.png
# caption: "Describe the public figure."
---
```

Use a different number in `order` for each card. Cards are sorted by this field. Edit the fields above the second `---`; the timeline does not display text written below them. Add as many semesters as you need for your program.

### Research showcase

Copy `_templates/showcase.md` to `docs/_showcases/your-project.md`. Set its title, order, date, tags, and summary. Use `links: []` until you have real, approved public links. You can then replace it with:

```yaml
links:
  - label: "Code"
    url: "https://github.com/yourusername/your-project"
```

Write longer project details below the second `---`. They appear on a separate project page linked from the showcase card. Describe planned work as planned work. Report only measured results, and do not claim a paper or software release before it exists.

Optional image paths start with `/assets/photos/`, not with the repository name. Upload each image before using its path. Leave unused image fields commented out to avoid broken images. Do not edit the generated HTML pages.

## 7. Keep a meeting record

1. Copy `_templates/regular-meeting.rst`.
2. Create `meetings/YYYY-MM-DD.rst` using the meeting date, such as `meetings/2026-11-04.rst`.
3. Set your name and date. Complete sections 1-4 before the meeting.
4. After the meeting, add decisions and agreed tasks to section 5.
5. Save the file on the default branch. The workflow builds and encrypts it.

The filename must be a valid date followed by `.rst`. The filename supplies the public meeting date. The two included notes are fictional; remove or replace them when you set up your site. They do not create a recurring meeting schedule.

### Private meeting figures

Store private figures in `meetings/assets/`, outside `docs/`, in a **private repository**. Supported formats are `.png`, `.jpg`, `.jpeg`, `.webp`, and `.gif`; each file must be at most 8 MiB. Refer to an uploaded file using a relative path:

```rst
.. figure:: assets/2026-11-04-results.png
   :alt: Training and validation loss over 100 epochs
   :width: 720px
   :align: center

   Compare training and validation loss.
```

The builder includes the figure inside the encrypted note. It does not publish the original image separately. Remote images and paths outside `meetings/assets/` are not supported for private figures.

### Equations

Use inline math such as:

```rst
The error is :math:`E = mc^2`.
```

Use a separate directive for a displayed equation:

```rst
.. math::

   \mathbf{x}_{t+1} = A \mathbf{x}_t + B \mathbf{u}_t
```

MathJax renders equations after the note is unlocked. An internet connection is needed for the external MathJax script. This script runs inside the unlocked page. Use an access-controlled service for highly sensitive records.

## 8. Optional local preview

Daily editing can use the GitHub website. Local preview requires Git, Python, Ruby, and Bundler. Use the [Jekyll installation instructions](https://jekyllrb.com/docs/installation/) for your operating system. On Windows, install the full **RubyInstaller with Devkit** and complete its MSYS2 development tool setup; a portable Ruby executable alone cannot install all required native gems. Follow the [Windows setup guide](https://jekyllrb.com/docs/installation/windows/). Clone **your own repository**, then open its folder in a terminal.

```text
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS or Linux: `source .venv/bin/activate`

If PowerShell blocks environment activation, use `.venv\Scripts\python.exe` in place of `python` for the Python commands below.

Install dependencies:

```text
python -m pip install -r requirements.txt
bundle install
```

Set the meeting password without writing it into shell history. In PowerShell:

```powershell
$meetingCredential = New-Object System.Management.Automation.PSCredential ('local', (Read-Host 'Meeting password' -AsSecureString))
$env:MEETING_PASSWORD = $meetingCredential.GetNetworkCredential().Password
python scripts/build_protected_meetings.py
Remove-Item Env:MEETING_PASSWORD
```

In Bash:

```bash
read -rs -p "Meeting password: " MEETING_PASSWORD; echo
export MEETING_PASSWORD
python scripts/build_protected_meetings.py
unset MEETING_PASSWORD
```

Then preview the public site:

```text
bundle exec jekyll serve --source docs --destination _site
```

Open `http://localhost:4000/2026yourname/`, using the `baseurl` you set in `docs/_config.yml`. Run the meeting builder again after changing a note; Jekyll alone does not encrypt notes. Restart Jekyll after changing the configuration. Keep `_site/`, `.venv/`, generated meeting HTML, and passwords out of Git.

Before sharing changes, stop the preview with `Ctrl+C` and run the checks:

```text
python -m unittest discover -s tests
bundle exec jekyll build --source docs --destination _site
python scripts/check_site.py _site --url "https://yourusername.github.io" --baseurl "/2026yourname"
```

Use your configured `url` and `baseurl` in the last command. Use `--baseurl ""` for a user site or a custom domain without a repository path. Build the meeting pages first, as shown above. The checks cover encryption, private-file boundaries, and local website links; they do not check whether external websites remain available.


## Files to edit

| File or folder | Purpose |
|---|---|
| `docs/_config.yml` | Public profile and local preview address |
| `docs/_semesters/*.md` | Semester timeline cards |
| `docs/_showcases/*.md` | Public project cards and detailed pages |
| `docs/assets/photos/` | Approved public photos and figures |
| `meetings/YYYY-MM-DD.rst` | Meeting sources; private only in a private repository |
| `meetings/assets/` | Private meeting figures in a private repository |
| `_templates/` | Copyable source templates |
| `scripts/build_protected_meetings.py` | Builds encrypted meeting pages |
| `.github/workflows/publish.yml` | Builds and publishes the website |

`docs/_data/meetings.json` and dated HTML files in `docs/meetings/` are generated. Do not edit or commit generated output. Keep any private code, drafts, or datasets outside `docs/`, for example in a root `research/` folder in your private repository.

## Troubleshooting and privacy limits

| Problem | Check |
|---|---|
| Pages setting is unavailable | Confirm repository visibility and GitHub plan. |
| Workflow reports a missing password | Create the `MEETING_PASSWORD` repository secret. |
| Public-source safety check fails | Keep real notes private; opt in only for public examples. |
| A note fails to build | Check its date, RST syntax, image format, size, and file path. |
| Site has no styling in local preview | Check `url`, `baseurl`, and the address opened in your browser. |
| A card or photo does not update | Check the edited file location, then check the latest Actions run. |
| An unlocked note does not show equations | Check your internet connection and external script blocking. |
| You changed only the password secret | Run the workflow again; changing a secret does not trigger a build. |

AES-256-GCM encrypts published notes. Anyone can download the ciphertext and try password guesses offline, so a strong password matters. Meeting dates and page addresses are public. Changing the password and rebuilding does not remove older downloaded ciphertext. Anyone with repository access can read the source notes. If private content was ever committed to a public repository, deleting the file in a later commit does not erase it from history; ask the maintainer to review the exposure.

## Maintain this template

Before sharing the template with students:

1. Enable **Settings > General > Template repository** so students can use **Use this template**.
2. Keep only fictional notes, example projects, and approved public images in the template. Check file history before making a repository public; deleting a file does not remove earlier copies.
3. For a public demonstration, set `ALLOW_PUBLIC_MEETING_SOURCES` to `true` in **Settings > Secrets and variables > Actions > Variables**. Keep confidential student work in separate private repositories.
4. Run the checks above after changing the layout, encryption script, or workflow. Review dependency updates and confirm that the example site still works.
