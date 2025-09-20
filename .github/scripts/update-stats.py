#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions용 학습 통계 자동 업데이트 스크립트
파일 위치: .github/scripts/update_stats.py
"""

import os
import re
import subprocess
from datetime import datetime, timedelta
import glob
import sys

def run_git_command(command):
    """Git 명령어를 안전하게 실행"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Git 명령어 실행 실패: {command}")
            print(f"오류: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        print(f"Git 명령어 시간 초과: {command}")
        return None
    except Exception as e:
        print(f"Git 명령어 실행 중 오류: {e}")
        return None

def count_java_files():
    """Java 파일 개수 계산"""
    try:
        java_files = glob.glob("**/*.java", recursive=True)
        # .git 폴더와 target, build 폴더 제외
        java_files = [f for f in java_files if not any(
            excluded in f for excluded in ['.git', 'target', 'build', '.idea']
        )]
        print(f"발견된 Java 파일: {len(java_files)}개")
        for f in java_files[:5]:  # 처음 5개만 출력
            print(f"  - {f}")
        if len(java_files) > 5:
            print(f"  ... 외 {len(java_files) - 5}개")
        return len(java_files)
    except Exception as e:
        print(f"Java 파일 카운트 오류: {e}")
        return 0

def count_classes():
    """Java 클래스 개수 계산"""
    class_count = 0
    try:
        for java_file in glob.glob("**/*.java", recursive=True):
            if any(excluded in java_file for excluded in ['.git', 'target', 'build', '.idea']):
                continue
            
            try:
                with open(java_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # 다양한 클래스 선언 패턴 찾기
                patterns = [
                    r'\bpublic\s+class\s+\w+',
                    r'\bclass\s+\w+',
                    r'\babstract\s+class\s+\w+',
                    r'\bfinal\s+class\s+\w+',
                    r'\bpublic\s+abstract\s+class\s+\w+',
                    r'\bpublic\s+final\s+class\s+\w+'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, content, re.MULTILINE)
                    class_count += len(matches)
                    
            except Exception as e:
                print(f"파일 읽기 오류 ({java_file}): {e}")
                continue
                
        print(f"발견된 클래스: {class_count}개")
        return class_count
    except Exception as e:
        print(f"클래스 카운트 오류: {e}")
        return 0

def count_projects():
    """완성된 프로젝트 개수 계산"""
    project_dirs = set()
    try:
        # Main.java가 있는 디렉토리들
        main_files = glob.glob("**/Main.java", recursive=True)
        for main_file in main_files:
            if '.git' not in main_file:
                project_dir = os.path.dirname(main_file)
                project_dirs.add(project_dir if project_dir else '.')
        
        # *App.java가 있는 디렉토리들
        app_files = glob.glob("**/*App.java", recursive=True)
        for app_file in app_files:
            if '.git' not in app_file:
                project_dir = os.path.dirname(app_file)
                project_dirs.add(project_dir if project_dir else '.')
        
        # Application.java가 있는 디렉토리들
        application_files = glob.glob("**/Application.java", recursive=True)
        for app_file in application_files:
            if '.git' not in app_file:
                project_dir = os.path.dirname(app_file)
                project_dirs.add(project_dir if project_dir else '.')
        
        print(f"발견된 프로젝트 디렉토리: {len(project_dirs)}개")
        for proj_dir in sorted(project_dirs):
            print(f"  - {proj_dir}")
            
        return len(project_dirs)
    except Exception as e:
        print(f"프로젝트 카운트 오류: {e}")
        return 0

def get_git_stats():
    """Git 통계 정보 가져오기"""
    try:
        # 총 커밋 수
        total_commits_result = run_git_command('git rev-list --all --count')
        total_commits = int(total_commits_result) if total_commits_result and total_commits_result.isdigit() else 0
        
        # 첫 번째 커밋 날짜로 학습 시작일 계산
        first_commit_result = run_git_command('git log --reverse --format="%ct" | head -n1')
        
        if first_commit_result and first_commit_result.isdigit():
            first_commit_timestamp = int(first_commit_result)
            start_date = datetime.fromtimestamp(first_commit_timestamp).date()
            today = datetime.now().date()
            learning_days = (today - start_date).days + 1
        else:
            learning_days = 1
            
        print(f"Git 통계 - 총 커밋: {total_commits}개, 학습 일수: {learning_days}일")
        return total_commits, learning_days
        
    except Exception as e:
        print(f"Git 통계 오류: {e}")
        return 0, 1

def get_recent_activity():
    """최근 7일간 활동 계산"""
    try:
        recent_result = run_git_command('git log --since="7 days ago" --oneline')
        if recent_result:
            recent_commits = len([line for line in recent_result.split('\n') if line.strip()])
        else:
            recent_commits = 0
            
        print(f"최근 7일 커밋: {recent_commits}개")
        return recent_commits
    except Exception as e:
        print(f"최근 활동 계산 오류: {e}")
        return 0

def update_readme_stats():
    """README.md 파일의 통계 섹션 업데이트"""
    
    print("📊 학습 통계 수집 시작...")
    
    # 통계 수집
    java_files = count_java_files()
    class_count = count_classes()
    project_count = count_projects()
    total_commits, learning_days = get_git_stats()
    recent_commits = get_recent_activity()
    
    # README.md 읽기
    readme_path = 'README.md'
    if not os.path.exists(readme_path):
        print(f"❌ {readme_path} 파일을 찾을 수 없습니다.")
        return False
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ README.md 읽기 오류: {e}")
        return False
    
    # 현재 시간
    current_time = datetime.now().strftime('%Y.%m.%d %H:%M')
    
    # 새로운 통계 섹션 생성
    stats_section = f"""## 📊 학습 통계
- **총 학습 일수**: {learning_days}일
- **Java 파일 수**: {java_files}개
- **작성한 클래스**: {class_count}개
- **완성한 프로젝트**: {project_count}개
- **총 커밋 수**: {total_commits}개
- **최근 7일 커밋**: {recent_commits}개

**마지막 업데이트**: {current_time}

> 📈 이 통계는 매일 자동으로 업데이트됩니다 (GitHub Actions)"""

    # 기존 통계 섹션 찾기 및 교체
    pattern = r'## 📊 학습 통계.*?(?=##|\Z)'
    
    if re.search(pattern, content, re.DOTALL):
        # 기존 통계 섹션이 있으면 교체
        new_content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
        print("✅ 기존 통계 섹션을 업데이트했습니다.")
    else:
        # 통계 섹션이 없으면 맨 끝에 추가
        new_content = content.rstrip() + '\n\n' + stats_section + '\n'
        print("✅ 새로운 통계 섹션을 추가했습니다.")
    
    # 파일 저장
    try:
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    except Exception as e:
        print(f"❌ README.md 저장 오류: {e}")
        return False
    
    print("📈 통계 업데이트 완료:")
    print(f"   - 학습 일수: {learning_days}일")
    print(f"   - Java 파일: {java_files}개")
    print(f"   - 클래스: {class_count}개")
    print(f"   - 프로젝트: {project_count}개")
    print(f"   - 총 커밋: {total_commits}개")
    print(f"   - 최근 커밋: {recent_commits}개")
    
    return True

def main():
    """메인 실행 함수"""
    print("🚀 cops9080의 Java GUI 학습 통계 업데이트 시작")
    print("-" * 50)
    
    # 현재 작업 디렉토리 확인
    current_dir = os.getcwd()
    print(f"작업 디렉토리: {current_dir}")
    
    # Git 저장소인지 확인
    if not os.path.exists('.git'):
        print("❌ Git 저장소가 아닙니다.")
        sys.exit(1)
    
    # 통계 업데이트 실행
    success = update_readme_stats()
    
    if success:
        print("-" * 50)
        print("✅ 학습 통계 업데이트가 성공적으로 완료되었습니다!")
        sys.exit(0)
    else:
        print("-" * 50)
        print("❌ 학습 통계 업데이트 중 오류가 발생했습니다.")
        sys.exit(1)

if __name__ == "__main__":
    main()
