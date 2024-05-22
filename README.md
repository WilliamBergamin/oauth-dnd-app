# OAuth DND App

This is a Bolt for Python app that uses custom functions in [Workflow Builder](https://api.slack.com/start#workflow-builder).

## Setup

Before getting started, first make sure you have a development workspace where
you have permission to install apps. **Please note that the features in this
project require that the workspace be part of
[a Slack paid plan](https://slack.com/pricing).**


## Running Your Project Locally

While building your app, you can see your changes appear in your workspace in
real-time with `slack run`. You'll know an app is the development version if the
name has the string `(local)` appended.

```zsh
# Run app locally
$ pip install -r requirements.txt
$ python app.py

⚡️ Bolt app is running! ⚡️
```

To stop running locally, press `<CTRL> + C` to end the process.

### Linting
Run flake8 and black for linting and code formatting:

```zsh
# Run flake8 from root directory (linting)
flake8 *.py

# Run black from root directory (code formatting)
black .
```

## Using Functions in Workflow Builder
With your server running, your function is now ready for use in [Workflow Builder](https://api.slack.com/start#workflow-builder)! Add it as a custom step in a new or existing workflow, then run the workflow while your app is running.

For more information on creating workflows and adding custom steps, read more [here](https://slack.com/help/articles/17542172840595-Create-a-new-workflow-in-Slack).

## Project Structure

### `.slack/`

Contains `apps.dev.json` and `config.json`, which include installation details for your project.

### `app.py`

`app.py` is the entry point for the application and is the file you'll run to start the server. This project aims to keep this file as thin as possible, primarily using it as a way to route inbound requests.
