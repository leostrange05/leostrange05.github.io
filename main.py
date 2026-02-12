import subprocess
import os
import re

def define_env(env):
    @env.macro
    def recent_updates(count=5):
        # 1. Get the list of recently modified .md files from Git
        cmd = ["git", "log", "--name-only", "--pretty=format:%as", "--", "docs/*.md"]
        try:
            output = subprocess.check_output(cmd).decode("utf-8").split("\n")
        except Exception:
            return "*(Update history currently unavailable - Ensure Git is installed and this is a repository)*"

        updates = []
        seen_files = set()
        current_date = ""

        # Start the timeline container
        html = ['<div class="update-timeline">']

        for line in output:
            line = line.strip()
            if not line: continue

            # If the line looks like a date (YYYY-MM-DD), store it
            if re.match(r"\d{4}-\d{2}-\d{2}", line):
                current_date = line
                continue
            
            # If the line is a markdown file and we haven't processed it yet
            if line.endswith(".md") and line not in seen_files:
                # Avoid showing the home page itself in the updates
                if "index.md" in line: continue 
                
                # Check if file actually exists (prevents errors on deleted files in git history)
                if not os.path.exists(line): continue

                title = extract_title(line)
                
                # Create the URL relative to the site root
                # Removes 'docs/' and changes '.md' to '/'
                url_path = line.replace("docs/", "", 1).replace(".md", "/")
                site_url = env.conf.get('site_url', '/')
                if not site_url.endswith('/'): site_url += '/'
                full_url = f"{site_url}{url_path}"

                # Append the Timeline Item HTML
                item_html = f"""
                <div class="update-item">
                    <span class="update-date">{current_date}</span>
                    <a class="update-link" href="{full_url}">{title}</a>
                </div>
                """
                html.append(item_html)
                
                seen_files.add(line)
                
                if len(seen_files) >= count:
                    break

        html.append('</div>') # Close container
        
        # If no updates were found
        if len(seen_files) == 0:
            return "*(No recent updates found)*"

        return "\n".join(html)

def extract_title(filepath):
    """Attempts to find the best title for a markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            # 1. Check for YAML front matter title (title: My Page)
            in_yaml = False
            for line in lines:
                if line.strip() == "---":
                    in_yaml = not in_yaml
                    continue
                if in_yaml and line.strip().startswith("title:"):
                    return line.replace("title:", "").strip().strip('"').strip("'")
                if not in_yaml and line.strip() != "" and not line.startswith("---"):
                    break

            # 2. Check for the first H1 tag (# Title)
            for line in lines:
                if line.strip().startswith("# "):
                    return line.replace("# ", "").strip()
                    
    except Exception:
        pass
    
    # Fallback: Clean up the filename if no title is found
    return os.path.basename(filepath).replace(".md", "").replace("-", " ").title()