.PHONY: version build clean prod-image

COUNT := $(shell git rev-list --all --count)
TAG := $(shell git describe --abbrev=0)
SHA1 := $(shell git log -1 --format=%h)
BRANCH := $(shell git branch --show-current | tr / _)
DATE := $(shell date)
DIFF := $(shell git rev-list --left-right --count  origin...main)

version:
	@echo """Version: $(TAG)""" >> version.txt
	@echo """--------------------------------""" >> version.txt
	@echo """Build date: $(DATE)""" >> version.txt
	@echo """SHA1: $(SHA1)""" >> version.txt
	@echo """Branch: $(BRANCH)""" >> version.txt
	@echo """Code diff: Behind-Ahead --> $(DIFF)""" >> version.txt
	@echo """--------------------------------""" >> version.txt

build:
	make clean
	make version

	@echo "=== building files ==="
	python setup.py bdist_egg --exclude-source-files -k -b build/dist

	cp -v requirements.txt build/dist/app
	cp -v ./app/prod.env build/dist/app
	cp -v ./app/logging.conf build/dist/app
	mv version.txt build/dist/app

clean:
	@echo "=== removing old build dir ===="
	# rm version.txt
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info


prod-image:
	make build
	docker build -t icanpe/short-url:$(BRANCH)-$(TAG) .
	docker push icanpe/short-url:$(BRANCH)-$(TAG)



