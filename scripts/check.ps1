Write-Output "======================="
Write-Output "===== Check start ====="
Write-Output "======================="
Write-Output ""

Write-Output "----- black -----"
black . --exclude aac_env
Write-Output ""

Write-Output "----- flake8 -----"
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude aac_env
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude aac_env
Write-Output ""

Write-Output "----- pytest -----"
pytest -v -l
Write-Output ""

Write-Output "===== Done ====="