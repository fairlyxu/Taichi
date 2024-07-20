import os

from dotenv import load_dotenv
load_dotenv()


from pathlib import Path
current_file_path = Path(__file__).resolve()
project_root_path = current_file_path.parents[0]
while not (project_root_path / 'mmqload.conf').exists() and project_root_path != project_root_path.root:
    project_root_path = project_root_path.parent
os.environ.setdefault('INPUT_IMG_DIR', str(project_root_path) + '/input')
os.environ.setdefault('OUTPUT_IMG_DIR',str(project_root_path) + '/output')

print(os.environ)