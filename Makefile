all:

clean:
	find monu/ -name "*.pyc" -exec rm '{}' \;
	find monu/ -name ".DS_Store" -exec rm '{}' \;
	rm -rf build/ dist/ env/ *.egg-info
