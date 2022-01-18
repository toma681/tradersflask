# Berkeley Trading Competiton
## Tech Stack
- React
- Flask
- SQLite3
- AWS

## How to Use

Prerequisites: Conda installation. Use miniconda if installing conda for the first time.

https://docs.conda.io/en/latest/miniconda.html

1. Clone repository: https://github.com/Traders-at-Berkeley/berkeley-trading-comp.git

2. Create the conda environment to run the game. Use one of the two following options:
```
conda create --name btc_comp python=3.7.3 requests Flask flask_cors Flask-Caching numpy
```

3. Activate conda environment

```
conda activate btc_comp
```

4. Start server and moderator script, each in different tabs.
```
python main.py
python moderator_scripts/a_cl.py # for game a
python moderator_scripts/b_cl.py # for game b
```

If you get bumped out of the moderator script, you can just restart it by entering the same line again.

5. Visit localhost:8080 to open website.

You're good to go!

# Build process - You won't need this

## Client
In client/
```
yarn install
yarn build
```

## Server
Add dependencies to conda environment list (above) to avoid dependency issues.
Run python code as you normally would. Make sure debug mode is false.
