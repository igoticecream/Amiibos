all:
	@python3 amiibo.py
	@mkdir "amiibo/Legend Of Zelda/Midna & Wolf Link/areas"
	@cp areas/0x1019C800.bin "amiibo/Legend Of Zelda/Midna & Wolf Link/areas"

count:
	@find amiibo -type f -name amiibo.json | wc -l
