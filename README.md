# Seattle-Area Field Day

This repo is behind the [Seattle-Area Field Day](https://seattleradiofieldday.org) website, aimed to inform members of the PSRG, WSARC, SeattleACS, amd Cascadia Radio, as well as members of the public, around our joint Field Day. The website is automatically rebuilt and deployed on any new merges into the `main` branch.

## Contributing

If you'd like to make changes to the website, please [see the contributing guide](./CONTRIBUTING.md).


## Quickstart

- Markdown files (`.md`) in the `site` directory are the source files for the website. Edit these, and then build the website to see your changes.
- Call `make` to see the available commands.


## Building the site locally

- Install the required packages with `pip install -r requirements.txt`. You'll need Python 3.10 or later.
- Build the site using `make build` and check your changes by opening the `site/_build/index.html` file in your browser.
- Use `make clean` to delete files from the `_build` directory; this is occasionally necessary to force a subtle refresh, for example when you change something like the CSS file.


## Satellite passes

The `generate_sat_passes.py` script generates a list of satellite passes for the Field Day weekend, and populates the `site/schedule_and_activities/satellite.md` page.

The script uses the N2YO API. In order for this script to work, you'll need an API key from the [N2YO](https://www.n2yo.com/api/) website. The API key should be stored in a file called `n2yo_api_key` in the root of the repository.

Satellite passes are typically only available about ten days before they happen, and they tend to get more accurate the closer you get to the event. We run this script manually, a few times over the ten days prior to Field Day. You can run it using `make satellites`.
