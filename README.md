# Rainbower

An experimental web app for exploring rainbow color profiles in photographs.

Rainbower helps investigate whether a suspected rainbow has the expected color structure. Select a line across the rainbow, inspect the image’s red, green, and blue (RGB) values along that line, and compare the measured profile with a theoretical rainbow profile.

## Goals

- Make rainbow color analysis accessible through an interactive web app.
- Explore rainbow features in photographs where their presence is not obvious.
- Compare measured color profiles with theoretical descriptions.
- Develop a quantitative, correlation-based approach to assessing rainbow presence.

The current prototype supports visual exploration. Automated rainbow detection is a development goal, not an established capability.

## How it works

1. **Upload a photograph.**
   Choose an image containing a suspected rainbow.

2. **Select a line across the rainbow.**
   Draw from the violet side toward the red side, crossing the rainbow’s color bands. Coordinate sliders provide another way to position the line, including on mobile devices.

3. **Sample the image colors.**
   The app extracts RGB values along the selected path.

4. **Inspect the measured profile.**
   A graph shows how the red, green, and blue intensities change along the line. The selected line’s coordinates and length help describe the sampled region.

5. **Compare with a theoretical profile.**
   Compare the measured curves with a simulated rainbow profile to explore similarities and differences.

## Measured and simulated profiles

The app distinguishes between two kinds of data:

- **Measured profile:** RGB values sampled from the selected photograph.
- **Simulated profile:** An analytical reference model combining a sky background with localized red, green, and blue rainbow peaks.

The simulated profile is a reference for comparison, not a measurement from the photograph. Visual similarity alone should not be treated as a validated detection result.

## Try the prototype

1. Clone the repo
2. Install the pixi dependency handler

```bash
pixi install                 # create environment
pixi run pip install -e .    # make src importable (one-time)
pixi run pytest              # verify 
```


### Local testing

The simplest way to try the app locally is the simple prototype:

```bash
pixi run run-test
```

This launches `simple_app.py`, a lightweight Streamlit prototype with a slider-based line input for quick iteration.

### Online testing

You can check the functioning over streamlit cloud or plotly cloud:

> Open the [Streamlit demo](https://rainbow-line-profiler-aoj4ojpzeh87ipgtmuhrks.streamlit.app), upload a photograph, and select a line across a suspected rainbow.

> A separate [Dash prototype](https://a0341eb1-03bc-48e3-b30b-a4a86de254fa.plotly.app) also explores an alternative interface.


Adjust the line and observe how its position changes the measured RGB curves. Compare those curves with the simulated reference profile.


## Current status and limitations

Rainbower is a working exploratory prototype built with Streamlit.

- Interactive line selection and RGB profile visualization are available.
- Coordinate sliders support line positioning on mobile devices.
- Mobile interaction remains buggy and needs usability improvements.
- Analysis currently centers on inspecting and comparing profiles, rather than producing an automatic rainbow/no-rainbow decision.
- Camera-response and background corrections are outside the initial prototype’s scope.


## Development direction

Future work includes improving usability, organizing the code into reusable modules, expanding usage documentation, and developing quantitative comparisons between measured and theoretical rainbow profiles.

## Commands

Rainbower uses [Pixi](https://pixi.sh) for environment management. All project tasks are run with `pixi run <task>`.

```bash
# Run the main Streamlit app
pixi run run-app

# Run the sandbox Streamlit app
pixi run run-sandbox

# Run the unit test suite
pixi run test

# Run linting
pixi run lint

# Format code
pixi run format

# Add a new dependency (updates pyproject.toml + pixi.lock, regenerates requirements.txt)
pixi run add-dep <package-name>
```
