# Contributing

I'd love your input, whether it's to add new content or report a problem.

This website is built using [JupyterBook](https://jupyterbook.org/). You are welcome to suggest edits to the content, and to submit your own content, by opening a pull request. Once approved and merged by a maintainer, the changes will be automatically published to the site via CI/CD.

If you aren't comfortable opening a pull request, you can also [submit an issue](https://github.com/QCaudron/fieldday/issues/new) or send an email to [Quentin K7DRQ](mailto:quentincaudron@gmail.com).

## Pull request process

1. Clone the repo and install the required packages with `pip install -r requirements.txt`. You'll need Python 3.8 or later.
2. Make your changes to the Markdown files in the `site` directory; if you create a new page, you'll need to add it to the [table of contents](./site/_toc.yml).
3. Build the site using `make build` and check your changes by opening the `site/_build/index.html` file in your browser.
4. If everything looks good, remove the built static site files using `make clean` before committing changed files to your feature branch.
5. [Open a pull request](https://gist.github.com/vlandham/3b2b79c40bc7353ae95a).
