# Development <!-- omit in toc -->

> [!NOTE]
> All of the steps on this page should be run from the root of the [`analytics/`](../../analytics/) sub-directory

<details>
   <summary>Table of contents</summary>

- [Setting up the tool locally](#setting-up-the-tool-locally)
  - [Docker vs Native](#docker-vs-native)
    - [Running with Docker](#running-with-docker)
    - [Running natively](#running-natively)
  - [Configuring secrets](#configuring-secrets)
    - [Prerequisites](#prerequisites)
    - [Finding reporting channel ID](#finding-reporting-channel-id)
    - [Finding slackbot token](#finding-slackbot-token)
- [Running the tool locally](#running-the-tool-locally)
  - [Using the `make` commands](#using-the-make-commands)
  - [Using the CLI tool](#using-the-cli-tool)
- [Common development tasks](#common-development-tasks)
  - [Adding a new dataset](#adding-a-new-dataset)
  - [Adding a new metric](#adding-a-new-metric)
  - [Adding a new CLI entrypoint](#adding-a-new-cli-entrypoint)

</details>

## Setting up the tool locally

The following sections describe how to install and work with the analytics application on your own computer. If you don't need to run the application locally, view the [usage docs](usage.md) for other ways to monitor our operational metrics.

### Docker vs Native

This project run itself inside of docker by default. If you wish to run this natively, add PY_RUN_APPROACH=local to your environment variables. You can set this by either running `export PY_RUN_APPROACH=local` in your shell or add it to your ~/.zshrc file (and run `source ~/.zshrc`).

After choosing your approach, following the corresponding setup instructions:

- [Running with Docker](#running-with-docker)
- [Running natively](#running-natively)

#### Running with Docker

**Pre-requisites**

- Docker installed and running locally: `docker --version`
- Docker compose installed: `docker-compose --version`

**Steps**

1. Run `make build`
2. Retrieve GH_TOKEN from [AWS](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/%252Fanalytics%252Fgithub-token/description?region=us-east-1&tab=Table#list_parameter_filters=Name:Contains:analytics%2Fgithub-token)
  - Add `export GH_TOKEN=...` to your `zshrc` or similar
3. Set the slackbot token and the channel ID for Slack after following the instructions in [configuring secrets](#configuring-secrets). **Note:** replace the `...` with the value of these secrets:
   ```
   export ANALYTICS_SLACK_BOT_TOKEN=...
   export ANALYTICS_REPORTING_CHANNEL_ID=...
   ```
4. Run `make test-audit` to confirm the application is running correctly.

#### Running natively

**Pre-requisites**

- **Python version 3.12:** [pyenv](https://github.com/pyenv/pyenv#installation) is one popular option for installing Python,
   or [asdf](https://asdf-vm.com/).
- **Poetry:** After installing and activating the right version of Python, [install poetry with the official installer](https://python-poetry.org/docs/#installing-with-the-official-installer) or alternatively use [pipx to install](https://python-poetry.org/docs/#installing-with-pipx).
- **GitHub CLI:** [Install the GitHub CLI](https://github.com/cli/cli#installation)

**Steps**

1. Set up the project: `make setup` -- This will install the required packages and prompt you to authenticate with GitHub
2. Retrieve GH_TOKEN from [AWS](https://us-east-1.console.aws.amazon.com/systems-manager/parameters/%252Fanalytics%252Fgithub-token/description?region=us-east-1&tab=Table#list_parameter_filters=Name:Contains:analytics%2Fgithub-token)
  - Add `export GH_TOKEN=...` to your `zshrc` or similar
3. Set the slackbot token and the channel ID for Slack after following the instructions in [configuring secrets](#configuring-secrets). **Note:** replace the `...` with the value of these secrets:
   ```
   export ANALYTICS_SLACK_BOT_TOKEN=...
   export ANALYTICS_REPORTING_CHANNEL_ID=...
   ```
4. Run `make test-audit` to confirm the application is running correctly.

### Configuring secrets

#### Prerequisites

In order to correctly set the value of the `slack_bot_token` and `reporting_channel_id` you will need:

1. To be a member of the Simpler.Grants.gov slack workspace
2. To be a collaborator on the Sprint Reporting Bot slack app

If you need to be added to the slack workspace or to the list of collaborators for the app, contact a project maintainer.

#### Finding reporting channel ID

1. Go to the `#z_bot-sprint-reporting` channel but use the `#z_bot-analytics-ci-test` channel for testing in the Simpler.Grants.gov Slack workspace.
2. Click on the name of the channel in the top left part of the screen.
3. Scroll down to the bottom of the resulting dialog box until you see where it says `Channel ID` and copy.

<img alt="Screenshot of dialog box with channel ID" src="../../analytics/static/screenshot-channel-id.png" height=500>

#### Finding slackbot token

1. Go to [the dashboard](https://api.slack.com/apps) that displays the slack apps for which you have collaborator access
2. Click on `Sprint Reporting Bot` to go to the settings for our analytics slackbot
3. From the side menu, select `OAuth & Permissions` and scroll down to the "OAuth tokens for your workspace" section
4. Copy the "Bot user OAuth token" which should start with `xoxb`

<img alt="Screenshot of slack app settings page with bot user OAuth token" src="../../analytics/static/screenshot-slackbot-token.png" width=750>

## Running the tool locally

While the [usage guide](usage.md) describes all of the options for running the `analytics` package locally, the following sections highlight some helpful commands to interact with the tool during development.

### Using the `make` commands

In earlier steps, you'll notice that we've configured a set of `make` commands that help streamline common developer workflows related to the `analytics` package. You can view the [`Makefile`](../../analytics/Makefile) for the full list of commands, but some common ones are also described below:

- `make install` - Checks that you have the prereqs installed, installs new dependencies, and prompts you to authenticate with the GitHub CLI.
- `make unit-test` - Runs the unit tests and prints a coverage report
- `make e2e-test` - Runs integration and end-to-end tests and prints a coverage report
- `make lint` - Runs [linting and formatting checks](formatting-and-linting.md)
- `make sprint-reports-with-latest-data` Runs the full analytics pipeline which includes:
  - Exporting data from GitHub
  - Calculating the following metrics
  - Either printing those metrics to the command line or posting them to slack (if `ACTION=post-results` is passed)

### Using the CLI tool

The `analytics` package comes with a built-in CLI that you can use to discover the reporting features available. Start by simply typing `poetry run analytics --help` which will print out a list of available commands:

![Screenshot of passing the --help flag to CLI entry point](../../analytics/static/screenshot-cli-help.png)

Additional guidance on working with the CLI tool can be found in the [usage guide](usage.md#using-the-command-line-interface).

## Common development tasks

### Adding a new dataset

1. Create a new python file in `src/analytics/datasets/`.
2. In that file, create a new class that inherits from the `BaseDataset`.
3. Store the names of key columns as either class or instance attributes.
4. If you need to combine multiple source files (or other datasets) to produce this dataset, consider creating a class method that can be used to instantiate this dataset from those sources.
5. Create **at least** one unit test for each method that is implemented with the new class.

### Adding a new metric

1. Create a new python file in `src/analytics/metrics/`.
2. In that file, create a new class that inherits from the `BaseMetric`.
3. Determine which dataset class this metric requires as an input. **Note:** If the metric requires a dataset that doesn't exist, review the steps to [add a dataset](#adding-a-new-dataset).
4. Implement the following methods on that class.:
   - `__init__()` - Instantiates the metric class and accepts any inputs needed to calculate the metric (e.g. `sprint` for `SprintBurndown`)
   - `calculate()` - Calculates the metric and stores the output to a `self.results` attribute. **Tip:** It's often helpful to break the steps involved in calculating the metric into a series of private methods (i.e. methods that begin with an underscore, e.g. `_get_and_validate_sprint_name()`) that can be called from the main `calculate()` method.
   - `get_stats()` - Calculates and returns key stats about the metric or input dataset. **Note:** Stats are different from metrics in that they represent single values and aren't meant to be visualized in a chart.
   - `format_slack_message()` - Generate a string that will be included if the results are posted to Slack. This often includes a list of stats as well as the title of the metric.
5. Create *at least* one unit test for each of these methods to test them against a simplified input dataset to ensure the function has been implemented correctly. For more information review the [docs on testing](../../documentation/analytics/testing.md)
6. Follow the steps in [adding a new CLI entrypoint](#adding-a-new-cli-entrypoint) to expose this metric via the CLI.

### Adding a new CLI entrypoint

1. Add a new function to [`cli.py`](../../analytics/src/analytics/cli.py)
2. Wrap this function with a [sub-command `typer` decorator](https://typer.tiangolo.com/tutorial/subcommands/single-file/). For example if you want to calculate sprint burndown with the entrypoint `analytics calculate sprint_burndown`, you'd use the decorator: `metrics_app.command(name="sprint_burndown")`
3. If the function accepts parameters, [annotate those parameters](https://typer.tiangolo.com/tutorial/options/name/).
4. Add *at least* one unit test for the CLI entrypoint, optionally mocking potential side effects of calling the entrypoint.

### Copying table from grants-db

1. Add a new sql migration file in `src/analytics/integrations/etldb/migrations/versions` and prefix file name with the next iteration number (ex: `0007`).
2. Use your database management system(ex: `pg_admin`, `db_beaver`...) and right-click on the table you wish to copy and select `SQL scripts` then `request and copy original DDL` 
3. Paste the DDL in your new migration file. Fix any formating issues, see previous migration files for reference.
4. Remove all reference to schema, roles, triggers and the use of `default now()` for timestamp columns.

    Example: 
    ``` sql 
    create table if not exists opi.opportunity
    ( 
     ...,
     created_at              timestamp with time zone default now() not null,
     ...
    )
    ```
    should be
    ``` sql 
    CREATE TABLE IF NOT EXISTS opportunity;
    ( 
     ...,
     created_at              timestamp with time zone not null
     ...
    )
      ```

5. Run migration via `make db-migrate` command

