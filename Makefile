venv:
	. .venv/bin/activate

setup: requirements.txt
	pip install -r requirements.txt
	python db/db_connector.py

clean:
	rm -rf __pycache__
	rm -r .venv

create-venv:
	test -d .venv || python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt
	deactivate
	echo "Virtual environment set up successfully"

test:
	pytest
