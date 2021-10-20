#!/bash/sh
python3 nytimesGet.py
python3 zeitGet.py
git add .
git commit -m "checkout"
git push origin main
