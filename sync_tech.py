import os
import re
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "geomathewjoseph"
README_PATH = "README.md"

# Mapping of tech keywords to Shields.io badges
TECH_MAP = {
    "Rust": "https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white",
    "Python": "https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white",
    "Java": "https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white",
    "TypeScript": "https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white",
    "JavaScript": "https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black",
    "C++": "https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white",
    "Next.js": "https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white",
    "React": "https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB",
    "Node.js": "https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=node.js&logoColor=white",
    "PyTorch": "https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white",
    "OpenCV": "https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white",
    "Redis": "https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white",
    "Kafka": "https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white",
    "Flink": "https://img.shields.io/badge/Apache_Flink-E6526F?style=for-the-badge&logo=apache-flink&logoColor=white",
    "Docker": "https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white",
    "Kubernetes": "https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white",
    "GCP": "https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white",
    "PostGIS": "https://img.shields.io/badge/PostGIS-336791?style=for-the-badge&logo=postgresql&logoColor=white",
    "MONAI": "https://img.shields.io/badge/MONAI-76B900?style=for-the-badge&logo=nvidia&logoColor=white",
    "MediaPipe": "https://img.shields.io/badge/MediaPipe-00C0FF?style=for-the-badge&logo=google&logoColor=white",
    "Socket.io": "https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white",
    "TailwindCSS": "https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white",
    "FastAPI": "https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white",
    "Flask": "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white",
    "Pandas": "https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white",
    "NumPy": "https://img.shields.io/badge/numpy-013243?style=for-the-badge&logo=numpy&logoColor=white",
    "Scikit-Learn": "https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white",
    "YOLOv8": "https://img.shields.io/badge/YOLOv8-FF3838?style=for-the-badge&logo=yolo&logoColor=white",
    "YOLO": "https://img.shields.io/badge/YOLOv8-FF3838?style=for-the-badge&logo=yolo&logoColor=white",  # Map generic YOLO topic to badge
    "TensorFlow": "https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white",
    "Keras": "https://img.shields.io/badge/Keras-D00000?style=for-the-badge&logo=keras&logoColor=white",
    "Android": "https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white",
    "Kotlin": "https://img.shields.io/badge/Kotlin-0095D5?style=for-the-badge&logo=kotlin&logoColor=white",
    "Swift": "https://img.shields.io/badge/Swift-F05138?style=for-the-badge&logo=swift&logoColor=white",
    "Flutter": "https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white",
    "Dart": "https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white",
    "Go": "https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white",
    "C": "https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white",
    "Shell": "https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white",
    "Bash": "https://img.shields.io/badge/Shell_Script-121011?style=for-the-badge&logo=gnu-bash&logoColor=white",
    "PowerShell": "https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white",
    "Linux": "https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black",
    "Git": "https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white",
    "GitHub Actions": "https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white",
    "Vercel": "https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white",
    "Netlify": "https://img.shields.io/badge/Netlify-00C7B7?style=for-the-badge&logo=netlify&logoColor=white",
    "Heroku": "https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white",
    "AWS": "https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white",
    "Azure": "https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white",
    "MongoDB": "https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white",
    "MySQL": "https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white",
    "SQLite": "https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white",
    "GraphQL": "https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white",
    "Android Studio": "https://img.shields.io/badge/Android%20Studio-3DDC84?style=for-the-badge&logo=android-studio&logoColor=white",
}

# Categorization of technologies
CATEGORIES = {
    "Languages": ["Rust", "Python", "Java", "TypeScript", "JavaScript", "C++", "C", "Go", "Kotlin", "Swift", "Dart", "Shell", "Bash", "PowerShell"],
    "Artificial Intelligence & Machine Learning": ["PyTorch", "TensorFlow", "Keras", "YOLOv8", "YOLO", "OpenCV", "MediaPipe", "MONAI", "Scikit-Learn", "Pandas", "NumPy"],
    "Systems & Data Engineering": ["Apache Kafka", "Apache Flink", "Redis", "PostGIS", "Docker", "Kubernetes", "Google Cloud", "AWS", "Azure", "Linux", "Git", "GitHub Actions"],
    "Web & App Development": ["Next.js", "React", "Node.js", "Socket.io", "Tailwind CSS", "FastAPI", "Flask", "Android", "Android Studio", "Flutter", "Vercel", "Netlify", "Heroku", "GraphQL"],
}

# Explicit overrides to ensure "Hidden Gems" are always captured from specific repos
REPO_OVERRIDES = {
    "SentinelStream": ["Java", "Flink", "Kafka", "Kubernetes", "Docker", "Redis", "Linux"],
    "synapse": ["TypeScript", "Next.js", "React", "Redis", "Socket.io", "Vercel"],
    "Health-AI-Sync": ["Python", "MONAI", "PyTorch", "NumPy", "Pandas"],
    "gesture-assistant": ["Python", "OpenCV", "MediaPipe", "TensorFlow"],
    "Intent-OS": ["Rust", "C", "Linux", "Bash"],
    "Drone-Detection": ["Python", "YOLOv8", "OpenCV", "Raspberry Pi", "Linux"],
    "aiml-roadmap": ["Scikit-Learn", "Pandas", "NumPy", "Git", "GitHub Actions"],
    "geomathewjoseph": ["Google Cloud", "Git", "GitHub Actions", "Android Studio", "Flutter", "Dart"] # Add profile-level skills
}

def get_repos():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    response = requests.get(url, headers=headers)
    return response.json()

def extract_tech(repos):
    techs = set()
    
    # 1. Scan Repositories
    for repo in repos:
        repo_name = repo["name"]
        
        # Add Language
        if repo.get("language"):
            techs.add(repo["language"])
            
        # Add Topics
        topics = repo.get("topics", [])
        for topic in topics:
            normalized = topic.lower().replace("-", "").replace(".", "")
            for key in TECH_MAP.keys():
                if normalized == key.lower().replace("-", "").replace(".", ""):
                    techs.add(key)
        
        # 2. Apply Overrides
        for override_name, override_techs in REPO_OVERRIDES.items():
            if repo_name.lower() == override_name.lower():
                for t in override_techs:
                    if t in TECH_MAP:
                        techs.add(t)

    return list(techs) # Return list, sorting happens in generation

def generate_markdown(techs_list):
    md = ""
    
    # Generate sections based on CATEGORIES order
    for category, allowed_techs in CATEGORIES.items():
        # Filter techs that belong to this category AND are present in the user's stack
        category_techs = [t for t in allowed_techs if t in techs_list]
        
        if category_techs:
            md += f'\n### {category}\n<div align="center">\n\n'
            for tech in category_techs:
                if tech in TECH_MAP:
                    md += f'![{tech}]({TECH_MAP[tech]})\n'
            md += '\n</div>\n'
            
    return md

def update_readme(new_content):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = r"<!-- TECH_STACK_START -->.*?<!-- TECH_STACK_END -->"
    replacement = f"<!-- TECH_STACK_START -->{new_content}<!-- TECH_STACK_END -->"
    
    new_readme = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    repos = get_repos()
    techs = extract_tech(repos)
    markdown = generate_markdown(techs)
    update_readme(markdown)
    print("README tech stack updated successfully!")
