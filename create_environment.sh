#bash
conan profile update "settings.compiler=Visual Studio" default
conan profile update "settings.compiler.version=14" default


python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
