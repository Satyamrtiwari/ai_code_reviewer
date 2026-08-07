import sys
import streamlit.web.server.server as server

# Patch Streamlit's Tornado server health endpoint before startup
server.HEALTH_ENDPOINT = r"(?:health|healthz|_stcore/health)"

from streamlit.web.cli import main

if __name__ == "__main__":
    sys.argv = ["streamlit", "run", "app.py"] + sys.argv[1:]
    main()
