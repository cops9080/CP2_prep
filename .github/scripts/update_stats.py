# .github/scripts/update_stats.py
import os
import re
import git
from datetime import datetime, timedelta
from github import Github
import glob

def count_java_files():
    """Java 파일 개수 계산"""
    java_files = glob.glob("**/*.java", recursive=True)
    # .git 폴더 제외
    java_files = [f for f in java_files if not f.startswith('.git')]
    return len(java_files)

def count_classes():
    """Java 클래스 개수 계산"""
    class_count = 0
    for java_file in glob.glob("**/*.java", recursive=True):
        if java_file.startswith('.git'):
            continue
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # class 선언 찾기 (public class, class, abstract class 등)
                class_matches = re.findall(r'\b(?:public\s+)?(?:abstract\s+)?class\s+\w+', content)
                class_count += len(class_matches)
        except:
            continue
    return class_count

def count_projects():
    """완성된 프로젝트 개수 계산"""
    project_dirs = []
    for root, dirs, files in os.walk("."):
        if root.startswith('./.git'):
            continue
        # Main.java 또는 Application.java가 있는 폴더를 프로젝트로 간주
        if any(f in files for f in ['Main.java', 'Application.java']) or \
           any('App.java' in f for f in files):
            project_dirs.append(root)
    return len(project_dirs)

def get_git_stats():
    """Git 통계 정보 가져오기"""
    try:
        repo = git.Repo('.')
        commits = list(repo.iter_commits())
        
        # 총 커밋 수
        total_commits = len(commits)
        
        # 첫 번째 커밋 날짜로 학습 시작일 계산
        if commits:
            first_commit = commits[-1]  # 가장 오래된 커밋
            start_date = first_commit.committed_datetime.date()
            today = datetime.now().date()
            learning_days = (today - start_date).days + 1
        else:
            learning_days = 1
            
        return total_commits, learning_days
        
    except Exception as e:
        print(f"Git 통계 오류: {e}")
        return 0, 1

def get_recent_activity():
    """최근 7일간 활동 계산"""
    try:
        repo = git.Repo('.')
        since_date = datetime.now() - timedelta(days=7)
        
        recent_commits = [
            commit for commit in repo.iter_commits()
            if commit.committed_datetime > since_date
        ]
        
        return len(recent_commits)
    except:
        return 0

def update_readme_stats():
    """README.md 파일의 통계 섹션 업데이트"""
    
    # 통계 수집
    java_files = count_java_files()
    class_count = count_classes()
    project_count = count_projects()
    total_commits, learning_days = get_git_stats()
    recent_commits = get_recent_activity()
    
    # README.md 읽기
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("README.md 파일을 찾을 수 없습니다.")
        return
    
    # 통계 섹션 업데이트
    stats_section = f"""## 📊 학습 통계
- **총 학습 일수**: {learning_days}일
- **Java 파일 수**: {java_files}개
- **작성한 클래스**: {class_count}개
- **완성한 프로젝트**: {project_count}개
- **총 커밋 수**: {total_commits}개
- **최근 7일 커밋**: {recent_commits}개

**마지막 업데이트**: {datetime.now().strftime('%Y.%m.%d %H:%M')}"""

    # 기존 통계 섹션 찾기 및 교체
    pattern = r'## 📊 학습 통계.*?(?=##|\Z)'
    
    if re.search(pattern, content, re.DOTALL):
        # 기존 통계 섹션이 있으면 교체
        new_content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
    else:
        # 통계 섹션이 없으면 맨 끝에 추가
        new_content = content + '\n\n' + stats_section
    
    # 파일 저장
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"통계 업데이트 완료:")
    print(f"- 학습 일수: {learning_days}일")
    print(f"- Java 파일: {java_files}개")
    print(f"- 클래스: {class_count}개")
    print(f"- 프로젝트: {project_count}개")
    print(f"- 총 커밋: {total_commits}개")

if __name__ == "__main__":
    update_readme_stats()
