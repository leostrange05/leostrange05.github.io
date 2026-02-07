import subprocess
from datetime import datetime

def define_env(env):
    @env.macro
    def recent_updates(count=5):
        # Runs a git command to get the last N changed markdown files
        cmd = ["git", "log", "-n", "20", "--pretty=format:%h|%as|%s", "--name-only", "--", "*.md"]
        result = subprocess.check_output(cmd).decode("utf-8").split("\n")

        updates = []
        seen_files = set()

        # Logic to parse git output and get unique recent pages
        for line in result:
            if line.endswith(".md") and line not in seen_files and "index.md" not in line:
                title = line.replace("Docs/", "").replace("docs/", "").replace(".md", "").replace("/", " > ").title()
                url = env.conf['site_url'] + line.replace("Docs/", "").replace("docs/", "").replace(".md", "/")
                updates.append(f"- [{title}]({url})")
                seen_files.add(line)
                if len(updates) >= count: break

        return "\n".join(updates)