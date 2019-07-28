test:
	example/build_deb.sh
	[ ! -f "/usr/local/bin/easydeb-hello" ]
	dpkg -i example/easydeb-hello_1.0.0_amd64.deb
	[ -f "/usr/local/bin/easydeb-hello" ]
	easydeb-hello world
	dpkg -r easydeb-hello
	[ ! -f "/usr/local/bin/easydeb-hello" ]