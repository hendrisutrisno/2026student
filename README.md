# CSDI Lab — Graduate Research Journey (2026student)

A minimal, reusable GitHub Pages/Jekyll template for one student's research journey.

- **Homepage:** student profile and four-semester graduate journey.
- **Regular Meetings:** a date-index page generated automatically from `.rst` files.
- **Meeting file:** clicking a date opens the corresponding `.rst` document in GitHub's rendered viewer.

## 1. Make this repository reusable (for the lab owner)

1. Create `hendrisutrisno/2026student` and upload these files to the repository root.
2. Under **Settings > General**, enable **Template repository**.
3. For each student, select **Use this template > Create a new repository** and name it, for example, `2026verin` (all lowercase is recommended).
4. Keep the **Owner** as `hendrisutrisno` if the public site should be at `hendrisutrisno.github.io/2026verin/`.
5. Add that student as a collaborator with permission to edit files; the lab owner retains repository administration.
6. Enable the site at **Settings > Pages > Build and deployment > Deploy from a branch > main > /(root)**.

**Important:** GitHub requires admin permissions to rename an existing repository. A student with ordinary write access can edit files but typically cannot rename a repository. Selecting the desired repository name at creation avoids that issue.

## 2. What a student must edit

Open `_config.yml` and change:

```yaml
baseurl: "/2026verin" # must equal the new repository name, including case
student:
  name: "Verin"
  degree: "Master's Student"
  lab: "CSDI Lab"
  university: "National Taipei University of Technology"
  joined: "2026"
  interests: "My research interests"
  summary: "One or two sentences about my graduate research journey."
```

`github_owner` and `url` remain unchanged when the repo is hosted under `hendrisutrisno`. All GitHub repository and `.rst` links are calculated from `github_owner` and `baseurl` automatically, so **you do not have to edit meeting URLs**. If you choose a different GitHub owner, update `github_owner` and `url` as well.

## 3. Add a regular meeting

1. Copy `_templates/regular-meeting.rst` to `meetings/YYYY-MM-DD.rst`, using the actual meeting date (e.g. `meetings/2026-10-28.rst`).
2. Fill in progress, observations, questions, and next steps **at least 24 hours before the meeting**.
3. Commit to `main`.
4. After the meeting, update the decisions and agreed actions in the same file.

Jekyll scans `meetings/*.rst` and lists dates in **newest-first order**. Empty repositories show a short message until the first meeting is added. The file names should be ISO formatted, `YYYY-MM-DD.rst`, so alphabetical order matches chronological order.

The live links will be:

- Student homepage: `https://hendrisutrisno.github.io/2026verin/`
- Meeting dates: `https://hendrisutrisno.github.io/2026verin/meetings/`
- GitHub-rendered record: `https://github.com/hendrisutrisno/2026verin/blob/main/meetings/2026-10-28.rst`

## 4. Link from the lab's website

Add a member link such as:

```html
<a href="https://hendrisutrisno.github.io/2026verin/">Verin — Research Journey</a>
```

## 5. Public visibility and confidentiality

**Only publish meeting notes approved for public disclosure.** In this setup, the `.rst` files are in the GitHub Pages source and may be copied into the published website, in addition to being visible on GitHub. Do not put confidential supervision feedback, unpublished manuscripts, personal information, proprietary data, or protected research results in this public repository. Keep confidential materials in a separately controlled, private location.

## Technical notes

- GitHub Pages supports the Jekyll/Liquid static-file listing used here; no script or database is required to update the meeting index.
- `.rst` files are linked directly to GitHub's rendered file viewer, rather than being converted by Jekyll into HTML pages.
- The `_templates` folder is excluded from the deployed site.
- GitHub does **not** automatically redirect old **project-site** URLs after repository renaming. Update links if the repository name changes later.
