all:

clean:
	find monu/ -name "*.pyc" -exec rm '{}' \;

clean_all:
	find monu/ -name ".DS_Store" -exec rm '{}' \;
	rm -rf build/ dist/ env/ *.egg-info

install:
	python monu/script/install_data.py

test:
	python -m unittest discover -s monu/test -p "*_test.py"

