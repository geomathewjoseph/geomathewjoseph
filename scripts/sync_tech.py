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
}

def get_repos():
    headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
    url = f"https://api.github.com/users/{USERNAME}/repos"
    response = requests.get(url, headers=headers)
    return response.json()

def extract_tech(repos):
    techs = set()
    for repo in repos:
        if repo.get("language"):
            techs.add(repo["language"])
        topics = repo.get("topics", [])
        for topic in topics:
            normalized = topic.lower().replace("-", "").replace(".", "")
            for key in TECH_MAP.keys():
                if normalized == key.lower().replace("-", "").replace(".", ""):
                    techs.add(key)
    return sorted(list(techs))

def generate_markdown(techs):
    md = '\n<div align="center">\n'
    for tech in techs:
        if tech in TECH_MAP:
            md += f'![{tech}]({TECH_MAP[tech]})\n'
    md += '</div>\n'
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
