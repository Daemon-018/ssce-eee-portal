# DEPLOY TO RENDER (one-time, ~4 mins)
# ====================================
# 1. Go to https://dashboard.render.com/new/web-service
# 2. Connect GitHub  -> select repo  Daemon-018/ssce-eee-portal
# 3. Render auto-detects:  Python  +  Procfile (web: gunicorn app:app)
# 4. Name: ssce-eee-portal
#    Runtime: Python 3
#    Build command: (empty — Render uses requirements.txt)
#    Start command: (empty — Render uses Procfile)
#    Instance type: Free
# 5. Advanced -> set env var:
#       SECRET_KEY = anything-random-long
# 6. Create Web Service. Render pulls the repo, pip installs, starts gunicorn.
#    app.py auto-builds the DB from seed_data.py on first boot (full dataset).
# 7. Your URL: https://ssce-eee-portal.onrender.com   (Redeploys on every push to main)

# UPDATING DATA LATER
# ===================
# After you change the DB locally (new results, faculty, notices):
#    cd ~/eee_site && .venv/bin/python export_seed.py
#    git add -A && git commit -m "update data" && git push
# Render auto-redeploys -> site updates. That's the "automatic" flow.

# KEEP TERMUX AS EDITOR, RENDER AS HOST
# =====================================
# Termux: edit + preview locally (live tunnel for demos)
# Render: permanent public host, auto-updates from GitHub