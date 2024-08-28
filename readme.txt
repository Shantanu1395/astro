python3 -m venv venv
autopep8 data.py --in-place

git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/Shantanu1395/astro
git push origin main
docker build -t mega_project_map .
docker run --rm -v "$(pwd)/output:/app/output" mega_project_map

Resources
Astrolibrary.org


