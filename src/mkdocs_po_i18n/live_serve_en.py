import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory


SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Live-serve MkDocs documentation in English.")
    parser.add_argument(
        "language_code",
        default="en",
        help="The primary documentation language code, if not English. Defaults to 'en'.",
    )
    parser.add_argument(
        "watch_directory",
        nargs="*",
        help="Directory or directories to watch for changes to serve live updates.",
    )
    parser.add_argument(
        "--build-with-errors",
        action="store_true",
        help="Allow the documentation to build with errors. Defaults to the build failing on errors.",
    )
    parser.add_argument(
        "--source-code",
        action="append",
        help="Source code directory to include in the build.",
    )
    args = parser.parse_args()

    return args


def serve_docs(config_location) -> None:
    args = parse_args()

    serve_command = [
        "python",
        "-m",
        "mkdocs",
        "serve",
        "--clean",
        "--config-file",
        f"{config_location}",
        "--watch",
        "docs",
    ]

    if not args.build_with_errors:
        serve_command.extend(["--strict"])

    if args.watch_directory:
        for directory in args.watch_directory:
            serve_command.extend(["--watch", directory])

    subprocess.run(
        serve_command,
        check=True,
    )


def main():
    args = parse_args()

    with TemporaryDirectory() as temp_md_directory:
        temp_md_directory = Path(temp_md_directory)

        if args.source_code:
            for directory in args.source_code:
                if "/" in directory:
                    Path(temp_md_directory / directory).parent.mkdir(
                        parents=True, exist_ok=True
                    )
                (temp_md_directory / directory).symlink_to(
                    SOURCE_DIR / directory, target_is_directory=True
                )

        for language_code in args.language_code:
            (temp_md_directory / f"mkdocs.{language_code}.yml").symlink_to(
                SOURCE_DIR / "docs" / f"mkdocs.{language_code}.yml"
            )
            (temp_md_directory / "config.yml").symlink_to(
                SOURCE_DIR / "docs" / "config.yml"
            )
            (temp_md_directory / f"{language_code}").symlink_to(
                SOURCE_DIR / "docs" / f"{language_code}", target_is_directory=True
            )

            serve_docs(
                config_location=(temp_md_directory / f"mkdocs.{language_code}.yml")
            )


if __name__ == "__main__":
    main()
