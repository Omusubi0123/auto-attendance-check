echo "======================="
echo "===== Check start ====="
echo "======================="
echo ""

echo "----- black -----"
black . --exclude aac_env
echo ""

echo "----- flake8 -----"
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude aac_env
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude aac_env
echo ""

echo "----- pytest -----"
pytest
echo ""

echo "===== Done ====="