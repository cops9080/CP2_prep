# .github/workflows/update-stats.yml
name: Update Learning Stats

on:
  push:
    branches: [ main, master ]
  schedule:
    - cron: '0 0 * * *'  # 매일 자정에 실행

jobs:
  update-stats:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        fetch-depth: 0  # 전체 커밋 히스토리 가져오기
        
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        pip install PyGithub gitpython
        
    - name: Check file structure
      run: |
        echo "현재 디렉토리 구조:"
        find . -name "*.py" -o -name "*.yml"
        ls -la .github/ || echo ".github 폴더가 없습니다"
        ls -la .github/scripts/ || echo "scripts 폴더가 없습니다"
        
    - name: Update Statistics
      run: |
        if [ -f ".github/scripts/update_stats.py" ]; then
          python .github/scripts/update_stats.py
        else
          echo "update_stats.py 파일을 찾을 수 없습니다. 인라인 스크립트를 실행합니다."
          python -c "
import os
import re
import subprocess
from datetime import datetime
import glob

def count_java_files():
    java_files = glob.glob('**/*.java', recursive=True)
    java_files = [f for f in java_files if not f.startswith('.git')]
    return len(java_files)

def count_classes():
    class_count = 0
    for java_file in glob.glob('**/*.java', recursive=True):
        if java_file.startswith('.git'):
            continue
        try:
            with open(java_file, 'r', encoding='utf-8') as f:
                content = f.read()
                class_matches = re.findall(r'\b(?:public\s+)?(?:abstract\s+)?class\s+\w+', content)
                class_count += len(class_matches)
        except:
            continue
    return class_count

def count_projects():
    project_dirs = []
    for root, dirs, files in os.walk('.'):
        if root.startswith('./.git'):
            continue
        if any(f in files for f in ['Main.java', 'Application.java']) or any('App.java' in f for f in files):
            project_dirs.append(root)
    return len(project_dirs)

def get_git_stats():
    try:
        result = subprocess.run(['git', 'rev-list', '--all', '--count'], capture_output=True, text=True)
        total_commits = int(result.stdout.strip()) if result.returncode == 0 else 0
        
        result = subprocess.run(['git', 'log', '--reverse', '--format=%ct'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            first_commit_time = int(result.stdout.strip().split('\n')[0])
            learning_days = (datetime.now().timestamp() - first_commit_time) // 86400 + 1
        else:
            learning_days = 1
            
        return total_commits, int(learning_days)
    except:
        return 0, 1

def get_recent_activity():
    try:
        result = subprocess.run(['git', 'log', '--since=7 days ago', '--oneline'], capture_output=True, text=True)
        return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        return 0

# 통계 수집
java_files = count_java_files()
class_count = count_classes()
project_count = count_projects()
total_commits, learning_days = get_git_stats()
recent_commits = get_recent_activity()

# README.md 읽기 및 업데이트
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 새로운 통계 섹션
    current_time = datetime.now().strftime('%Y.%m.%d %H:%M')
    stats_section = f'''## 📊 학습 통계
- **총 학습 일수**: {learning_days}일
- **Java 파일 수**: {java_files}개
- **작성한 클래스**: {class_count}개
- **완성한 프로젝트**: {project_count}개
- **총 커밋 수**: {total_commits}개
- **최근 7일 커밋**: {recent_commits}개

**마지막 업데이트**: {current_time}

> 📈 이 통계는 매일 자동으로 업데이트됩니다 (GitHub Actions)'''

    # 기존 통계 섹션 교체
    pattern = r'## 📊 학습 통계.*?(?=##|\Z)'
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
    else:
        new_content = content + '\n\n' + stats_section
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'통계 업데이트 완료: {java_files}개 파일, {class_count}개 클래스, {total_commits}개 커밋')
    
except Exception as e:
    print(f'오류 발생: {e}')
"
        fi
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        
    - name: Commit and push if changed
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add README.md
        git diff --staged --quiet || git commit -m "📊 Auto-update learning statistics"
        git push
