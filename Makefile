SOURCE=cross-stitch.py

mac:
	py2applet --make-setup $(SOURCE)
	rm -rf build dist
	#python setup.py py2app -A
	python setup.py py2app
	zip -r dist/cross-stitch-osx.zip dist/cross-stitch.app
	scp dist/cross-stitch-osx.zip fh.cs.au.dk:~/public_html_cs/files/
