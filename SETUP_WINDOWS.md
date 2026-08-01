# Windows setup

Requirements: Git, Ruby 3.3.x, Bundler, Python 3.11+.

```powershell
git clone https://github.com/Tontonjeong/Tontonjeong.github.io.git D:\Codex\repos\active\Tontonjeong.github.io
Set-Location D:\Codex\repos\active\Tontonjeong.github.io
bundle install
bundle exec jekyll build --source src --destination _site --trace
```
