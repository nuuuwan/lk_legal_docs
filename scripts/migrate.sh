DECADE_BASE="202"
DECADE="${DECADE_BASE}0s"
BRANCH="data_$DECADE"

echo "Creating branch $BRANCH for decade $DECADE"

git checkout -b $BRANCH
cd data

find . -type d -mindepth 2 -maxdepth 2 ! -name "${DECADE_BASE}*" 
find . -type d -mindepth 2 -maxdepth 2 ! -name "${DECADE_BASE}*" -exec rm -rf {} +

git add -A
git commit -m "Deleted non-${DECADE} files"

cd ..

git push origin $BRANCH
git checkout main