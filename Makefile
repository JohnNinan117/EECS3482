venv:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

client: venv
	. venv/bin/activate && python3 client.py
.PHONY: client			

server: venv
	. venv/bin/activate && python3 server.py
.PHONY: server

pwd_gen: venv
	. venv/bin/activate && python3 pwd_gen.py
.PHONY: pwd_gen

test:
	python3 client.py && python3 crypto.py && python3 codec.py
.PHONY: test

clean:
	-rm -r venv
.PHONY: clean

lab0-ag:
	ag0/ag0.py
.PHONY: lab0-ag
