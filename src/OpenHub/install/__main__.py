import os
from subprocess import call
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
os.chmod(str(BASE_DIR) + '/install.sh', 755)
rc = call(str(BASE_DIR) + "/install.sh")
