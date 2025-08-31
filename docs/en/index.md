# MkDocs PO I18n

MkDocs PO I18n is a tool designed to build translations of MkDocs documentation. Generated PO template (POT) files, created from the primary language Markdown documentation files, are used to generate PO files for each specified langauge. The PO translation files are used to build the translated site for each language. This tool is compatible with using Weblate for the translation workflow, and Read the Docs for hosting the original and translated documentation.

## Installation

MkDocs PO I18n is currently installable directly from GitHub. The following can be added to a `requirements.txt` file or a `pyproject.toml` file, where `desiredhash` is the commit hash you wish to install:

```text
"mkdocs-po-i18n @ git+https://github.com/kattni/mkdocs-po-i18n#desiredhash"
```

/// caution | Always pin to a commit hash!

Always pin to a commit hash when installing a package directly from GitHub. Doing so serves the same purpose as pinning a package to a specific release; in the event that the API changes or a bug is introduced, you won't be caught by surprise when your workflow breaks.

///

## Required prerequisites

The following setup is required by MkDocs PO I18n.

### MkDocs configuration files

This tool is designed to work with a specific MkDocs configuration setup.

You will create an `mkdocs.language-code.yml` file for the primary language and each language for which you intend to provide translations; this configuration is required for Read the Docs to build successfully. The settings contained in this file should be only options that are language-specific.

You will also create a base configuration file called `config.yml` that contains all configuration shared by all languages; this allows you to apply further options to all builds without duplicating information.

The `mkdocs.en.yml` for this repo contains the following:

```yaml
INHERIT: config.yml
site_name: MkDocs PO I18n
site_url: https://mkdocs-po-i18n.readthedocs.io/en/latest/
docs_dir: en

theme:
  language: en
```

The demo translation in this repo is French. The associated `mkdocs.fr.yml` file contains:

```yaml
INHERIT: config.yml
site_name: MkDocs PO I18n
site_url: https://mkdocs-po-i18n.readthedocs.io/fr/latest/
docs_dir: fr

theme:
  language: fr
```

Additional content in the `config.yml` file is only necessary if you intend to add further configuration to your MkDocs setup. Any options added to it will apply to both. This tool expects `config.yml` to exist, so even if you don't intend to add any other options at this time, you need to generate an empty file.

The `config.yml` for this repo would minimally require the following, as the Material theme language is specified in the `mkdocs.language.yml` files:

```yaml
theme:
  name: material
```

### Documentation directory structure

MkDocs PO I18n expects the Markdown documentation to be maintained in a `/docs/language-code/` subdirectory, where `language-code` is the primary documentation langauge code. The primary langauge for this documentation is English, so this Markdown content is in `/docs/en/`.

### PO file, POT file, and locales directory structure

The `locales/` directory is expected to be in the `/docs/` directory.

The POT files should reside in the `/docs/locales/templates/` directory.

The PO files for each language should reside in a `/docs/locales/language-code/LC_MESSAGES/` directory. The demo translation language for this documentation is French. The French PO files are in `/docs/locales/fr/LC_MESSAGES/`.

/// warning | Create new language code directories in `locales` before attempting to create PO files!

To avoid unnecessary incorrect directories being created if an invalid language code is provided in error, the method MkDocs PO I18n uses to verify if the provided language code is an existing language checks for the existence of the language code directory in the `/docs/locales/` directory. If the language code directory doesn't exist, the tool will fail to run with an error. Therefore, you must create the desired language code directories manually before running the translation tools.

///

## Recommended prerequisites

It is highly recommended to use `tox` for managing usage of this tool. It is not required, however, it creates a consistent environment locally and on Read the Docs, which makes troubleshooting issues much more straightforward.

### `tox` configuration

The following is an example `tox.ini`, similar to the one found in this repo. It accounts for English as a primary language, and French as the only available translation. You will need to make changes to it for a different setup.

```ini {hl_lines="8 11-12 14 16-20" linenums="1"}
[tox]
envlist = docs-all

[docs]
docs_dir = {tox_root}{/}docs
templates_dir = {tox_root}{/}docs{/}locales{/}templates

[testenv:docs{,-translate,-all,-live,-en,-fr}]
base_python = py313
skip_install = true
deps =
    [dev]
commands:
    !all-!translate-!live-!en-!fr : build_md_translations {posargs} en
    translate : build_pot_translations
    translate : build_po_translations fr
    live : live_serve {posargs}
    all : build_md_translations {posargs} en fr
    en : build_md_translations {posargs} en
    fr : build_md_translations {posargs} fr
```

The highlighted lines above are where a different configuration would require changes.

If you are not using `pyproject.toml` with a `dev` dependency group that contains at least `tox`, lines 11-12 will need to be updated to reflect your configuration.

If your primary and translated languages are not the same, the following changes will be needed. Line 17 requires a language code if your primary language is not English. Lines 8, 14, 16, and 18-20 are all language-specific; if you add a language, you will need to update 8, 14, and 16, and include an additional line at the end, similar to 19 and 20, with the new language code.

## Optional Prerequisites

The following is required if you intend to use Read the Docs to host your documentation site.

### Read the Docs configuration

Read the Docs requires [a `.readthedocs.yaml` configuration file](https://docs.readthedocs.com/platform/stable/config-file/v2.html) be present in your repo. If you are using `tox` and `pyproject.toml` with dependency groups, your `.readthedocs.yaml` file should contain the following:

```yaml {linenums="1"}
version: 2

build:
  os: ubuntu-24.04
  tools:
    python: "3.13"
  jobs:
    pre_install:
      - python -m pip install --upgrade pip
      - python -m pip install --group 'dev'
    build:
      html:
        - python -m tox -e docs-$READTHEDOCS_LANGUAGE -- --output=$READTHEDOCS_OUTPUT/html/
```

If you are using `requirements.txt`, you will need to update line 10 to `- python -m pip install -r requirements.txt`.

If you are not using `tox`, you will need to update line 13 to `- python -m build_md_translations $READTHEDOCS_LANGUAGE -- --output=$READTHEDOCS_OUTPUT/html/`.

### Read the Docs primary and translation project creation and set up

[Create the primary Read the Docs project](https://docs.readthedocs.com/platform/stable/intro/add-project.html) for your repo. If you have already added the `.readthedocs.yml`, connecting a RTD project can be done automatically. This will act as the "parent project".

To add a translation project, navigate back to the Projects dashboard and click "+ Add project". Search for the repo you added as the primary project, and choose it. RTD will tell you that it's already been configured, but click "Continue" and it will still take you to the configuration page. Update the "Name"; adding `-language-code` is the simplest way to handle it, i.e. for French, update `project-name` to `project-name-fr`. Below that, there is a dropdown for "Language"; choose the associated language from this menu. Clicking "Next" will create the project.

To associate the translation project with the parent project, click on the parent project in the dashboard, and navigate to Settings > Translations. Click "+ Add translation", choose the translation project from the dropdown, and click "Save".

## Recommended usage

The following commands assume you have set up your [`tox.ini` configuration](#tox-configuration) as shown above.

To do a local build of the site in English, run the following:

```console
$ tox -e docs
```

You can also run:

```console
$ tox -e docs-en
```

To live serve the build of your site in English, run the following:

```console
$ tox -e docs-live
```

If your primary language is not English, you need to add a language code. For example, to live serve the site with German as your primary langauge, run the following:

```console
$ tox -e docs-live de
```

The first step towards translating content is to generate the PO template files, followed by generating the desired language PO files. To invoke this process, run the following:

```console
$ tox -e docs-translate
```

To build the site in a language other than your primary language, you'll run the language-specific command, by including the language code. For example, to build in French, run the following:

```console
$ tox -e docs-fr
```

To build in all available languages, including your primary language, run the following:

```console
$ tox -e docs-all
```

## Direct Usage

To do a local build of the site in English, run the following:

```console
$ build_md_translations en
```

To live serve the build of your site in English, run the following:

```console
$ live_serve
```

If your primary language is not English, you need to add a language code. For example, to live serve the site with German as your primary langauge, run the following:

```console
$ live_serve de
```

The first step towards translating content is to generate the PO template files. To generate the POT files, run the following:

```console
$ build_pot_translations
```

The next step is generating the desired language PO files. You can run this command with one or more language codes. For example, to generate the PO files for French, run the following:

```console
$ build_po_translations fr
```

To build the site locally with translated content, you can run this command with one or more language codes. For example, to build in French, run the following:

```console
$ build_md_translations fr
```
