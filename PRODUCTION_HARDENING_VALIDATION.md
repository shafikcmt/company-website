# Production hardening follow-up — 2026-10-03

## About-only release isolation — current status

- `hapl/views.py` now differs from HEAD only in About KPI, management/staff and FAQ ordering (three hunks). Home view changes were saved in ignored `tmp/excluded-home/home-view-changes.patch`, alongside the original full view file. All nine excluded Home files remain unchanged, verified by SHA-256 hashes.
- `tests/test_public_production.py` validates About/Products/Contact shared-shell rendering and only approved release assets. It no longer renders the unapproved Home template or requires Home CSS. Explicit About JavaScript and all three favicon checks supplement full manifest/CSS/font coverage.
- Created ignored `tmp/about-only-release/` from `git archive HEAD`, overlaid exactly the 23 approved release files, and excluded all Home redesign files. Its homepage and homepage tests match HEAD content. Local environment/media/dependency access is QA-only; none belongs in the release.
- Ran the existing public production build in that isolated copy and copied its compiled CSS to the working tree. The release stylesheet therefore includes baseline homepage utilities without depending on the unapproved redesign sources. About CSS remains unchanged and is served separately.
- Isolated validation: 15 relevant tests pass (About CMS, image retention, public production); system checks pass; no migrations; diff whitespace and About JavaScript syntax checks pass.
- Isolated browser validation passes at 360, 768, 1024, 1440 and 1920 px: About navigation/Escape focus, FAQ keyboard interaction, configured social URL schemes, favicon HTTP responses, Contact link, images/media, computed reduced-motion transitions, no horizontal overflow, no JavaScript runtime or console warnings/errors, and no-JavaScript content/FAQ. Baseline homepage returns 200, displays its existing hero, and loads no Home redesign assets. Social ownership and remote destinations still require company approval.
- No stage, commit, push or deployment performed. The approved 23-file code scope can be staged after review; content/security/hosting launch blockers below remain. Earlier 23-test/30-browser results describe the combined workspace and are historical; the isolated checks above supersede them for this release.

## Already present at the start

Inspected the existing diff, implementation notes and prior QA scripts before editing. The About design, CSS/JS, responsive/accessibility work, dynamic naming, deterministic KPI/team/FAQ selection, Admin guidance, social URL validation, 1920×1440 upload cap and favicon assets were already implemented. Home changes were also present and preserved.

Non-watch npm build scripts, the public Tailwind theme/content configuration, scoped legacy base rules and image-retention implementation were already present. Five image-retention tests had been drafted. The shared base still loaded the development CDN and hardcoded unverified contacts; successful validation of the retention tests was unfinished.

## Completed now

- Shared base loads compiled `css/public.styles.css`; removed the development CDN and inline runtime configuration. Added the existing stylesheet's `public-site` body marker to exclude legacy base overrides and preserve utility/page-specific styling.
- Regenerated public CSS. Repeat public build produced the same hash. Public and admin build commands passed; restored the unrelated admin generated asset byte-for-byte to its initially clean tracked version after build verification.
- Removed placeholder phone and unverified address/email from the shared footer; linked to the existing Contact route. Generated ContactData records were not published as approved company details. No schema or company-data changes.
- Validated the existing image-retention implementation: processed images survive replacement, clear, deletion, failed save and rollback, including shared references. Added clear-rollback and ordinary-save/no-reprocessing coverage. Original uploads are still not retained separately; orphan processed files can accumulate. Future pruning requires a backed-up retention policy accounting for shared references and database restores. Non-image cleanup behavior is unchanged.
- Added production regression tests for compiled CSS loading, contact omission, responsive/brand utilities, full static collection, manifest-hashed template assets and transitive CSS/font references.
- Fixed disposable test storage permissions and registered cleanup during setup. Python 3.14 TemporaryDirectory ACLs excluded the sandbox user, causing the initial failed runs; normal workspace directory creation resolved this without changing production storage.

## Checks run

- `npm.cmd run build:public`: passed; repeat hash identical.
- `npm.cmd run build`: both builds passed. Non-fatal Browserslist warning: caniuse-lite is outdated. Dependency files unchanged.
- With `DATABASE_URL=sqlite:///:memory:`, `venv/Scripts/python.exe -m pytest tests hapl/tests.py -o addopts='' -p no:cacheprovider --tb=short`: **23 passed**, using an isolated database and disposable media/static storage. No live records/media changed.
- Static regression: `DEBUG=False`, isolated ManifestStaticFilesStorage and full `collectstatic` post-processing. Public/About/Home CSS, page JavaScript, local icon font and favicon references resolve to collected hashed files.
- `manage.py check`: no issues. `makemigrations --check --dry-run`: no changes. `git diff --check`: passed. `node --check` for About/Home JavaScript: passed.
- Local Chromium/Edge: Home/About at 360, 390, 768, 1024, 1280, 1440 and 1920 px; eight other public routes at 360 and 1440 px (**30 page/viewport checks**). All returned 200 with no horizontal overflow. Configured images and local static assets loaded; no JavaScript runtime errors. About FAQ keyboard operation, mobile menu/Escape, reduced-motion and no-JavaScript content/FAQ passed. Script, results and screenshots are under ignored `tmp/`.
- Browser QA uses development asset serving. An initial DEBUG=False run lacked static/media serving because no production web server was configured; this was not a CSS layout regression. The gallery's intentionally empty hidden lightbox image is excluded from configured-image checks; final media issue list is empty.
- `manage.py check --deploy`: five current-environment warnings: W004 (HSTS), W008 (HTTPS redirect), W009 (secret-key strength), W012 (secure session cookie), W016 (secure CSRF cookie). No secrets or environment/security settings rewritten.

## Files changed by this follow-up

- `templates/www/base.html`
- `common/static/css/public.styles.css`
- `tests/test_image_retention.py`
- `tests/storage_helpers.py` (new)
- `tests/test_public_production.py` (new)
- `ABOUT_CMS_HARDENING.md`, `ABOUT_RELEASE_REVIEW.md` (current-status pointers)
- `PRODUCTION_HARDENING_VALIDATION.md` (new)

All other initial working-tree changes were preserved, including the About template/design and image-retention code.

## Remaining launch blockers

1. Company approval and replacement of documented demo story/KPIs/team/FAQs; approved legal naming, claims/core values, social ownership and image rights/quality. Verified contacts are not supplied; footer offers the Contact route.
2. Staging/production acceptance of actual static/media serving, caching, backups/restore and image codecs. Local collection and development browser QA do not prove remote hosting behavior. Django's DEBUG-only static/media URL helpers do not serve assets in production.
3. Resolve the five security warnings in the actual hosting environment, including reverse-proxy HTTPS configuration where applicable.

No commit, push or deployment performed.
