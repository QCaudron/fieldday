.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'


.PHONY: build
build:  ## Build the Jupyterbook
	jupyter-book build site/

.PHONY: clean
clean:  ## Remove build files
	jupyter-book clean site/