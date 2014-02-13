README.rst: generate-readme.sh cross-stitch.py fisker-pattern.png
	@bash $< $@

fisker-pattern.png: cross-stitch.py fiskeren.jpg
	@python $< -i fiskeren.jpg -o $@ -w 50

clean:
	$(RM) README.rst
	$(RM) fisker-pattern.png
