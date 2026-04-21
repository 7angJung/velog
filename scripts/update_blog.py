import feedparser
import git
import os

# 본인 벨로그 아이디로 수정
rss_url = 'https://api.velog.io/rss/@7angjung'

repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

# velog-posts 폴더 없으면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# 레포지토리 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

for entry in feed.entries:
    file_name = entry.title

    # 파일명에 사용할 수 없는 문자 치환
    file_name = file_name.replace('/', '-')
    file_name = file_name.replace('\\', '-')
    file_name = file_name.replace(':', '-')
    file_name = file_name.replace('*', '-')
    file_name = file_name.replace('?', '')
    file_name = file_name.replace('"', "'")
    file_name = file_name.replace('<', '(')
    file_name = file_name.replace('>', ')')
    file_name = file_name.replace('|', '-')

    file_name += '.md'
    file_path = os.path.join(posts_dir, file_name)

    # 아직 없는 파일만 생성
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# {entry.title}\n\n")
            file.write(f"링크: {entry.link}\n\n")
            file.write(entry.description)

        repo.git.add(file_path)
        repo.git.commit('-m', f'Add post: {entry.title}')
