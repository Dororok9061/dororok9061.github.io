# Verification

```powershell
bundle exec jekyll build --source src --destination _site --trace
python scripts\check_site.py _site
powershell -ExecutionPolicy Bypass -File scripts\security\verify-site-security.ps1 -SiteRoot _site -BuiltSite
```

Migration fresh-clone build result: BLOCKED; `bundle` was not found on PATH. Git clone/fsck passed.
