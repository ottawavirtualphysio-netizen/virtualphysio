$root = 'd:\Downloads\virtualphysio-main'
$replacements = @(
  @{ pattern = 'Virtual Physio\.ca'; replacement = 'Virtual Physio' },
  @{ pattern = '\+1 343 204 0699'; replacement = '+1 (343) 202-4226' },
  @{ pattern = '\+13432040699'; replacement = '+13432024226' },
  @{ pattern = 'https://wa\.me/13432040699'; replacement = 'https://wa.me/13432024226' }
)
Get-ChildItem $root -Recurse -File | Where-Object { $_.Extension -in '.html','.js','.css','.gs','.xml','.toml','.md' } | ForEach-Object {
  $path = $_.FullName
  $text = [System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))
  $original = $text
  foreach ($r in $replacements) {
    $text = [regex]::Replace($text, $r.pattern, $r.replacement)
  }
  if ($text -ne $original) {
    [System.IO.File]::WriteAllText($path, $text, [System.Text.UTF8Encoding]::new($false))
    Write-Output $path
  }
}
