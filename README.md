# MkDocs PO I18n

A translation tool for using PO file with MkDocs. Compatible with Read the Docs and Weblate.

## Installation

MkDocs PO I18n is currently installable directly from GitHub. The following can be added to a `requirements.txt` file or a `pyproject.toml` file, where `desiredhash` is the commit hash you wish to install:

```text
"mkdocs-po-i18n @ git+https://github.com/kattni/mkdocs-po-i18n#desiredhash"
```

Note: Always pin to a commit hash when installing a package directly from GitHub. Doing so serves the same purpose as pinning a package to a specific release; in the event that the API changes or a bug is introduced, you won't be caught by surprise when your workflow breaks.

## Required Prerequisites

Required prerequisites can be found [here](https://mkdocs-po-i18n.readthedocs.io/en/latest/#required-prerequisites).

## Optional Prerequisites

Optional Read the Docs set up can be found [here](https://mkdocs-po-i18n.readthedocs.io/en/latest/#required-prerequisites).

## Basic Usage

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

## Documentation

Docs can be found [here](https://mkdocs-po-i18n.readthedocs.io/en/latest/).
