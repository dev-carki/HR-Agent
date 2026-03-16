from langchain_core.tools import tool
import requests
from collections import Counter

@tool
def get_github_profile(github_url: str) -> dict:
    """GitHub 프로필에서 레포지토리 언어 통계와 주요 레포 목록을 조회합니다."""
    # 1. URL에서 username 추출
    parts = github_url.rstrip("/").split("/")
    if len(parts) > 4:
        return {"error": "프로필 URL이 아닙니다."}
    username = parts[-1]

    # 2. GitHub API 호출
    response = requests.get(f"https://api.github.com/users/{username}/repos")
    repos = response.json()
    
    if not response.ok or not isinstance(repos, list):
        return {"language_stats": {}, "repo_names": [], "total_stars": 0, "error": "GitHub API 호출 실패"}
    
    # 3. 필요한 정보만 추출해서 반환
    language_counter = Counter()
    repo_names = []
    total_stars = 0
    
    for repo in repos:
        if repo["language"]:
            language_counter[repo["language"]] += 1
        repo_names.append(repo["name"])
        total_stars += repo["stargazers_count"]
        
    total = sum(language_counter.values())
    language_stats = {lang: round(count / total * 100, 1) for lang, count in language_counter.items()}
    
    
    return {
      "language_stats": language_stats,  # 언어별 비율
      "repo_names": repo_names,
      "total_stars": total_stars
  }