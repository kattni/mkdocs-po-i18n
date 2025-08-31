import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from tempfile import TemporaryDirectory


SOURCE_DIR = Path.cwd()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("watch_directory", nargs="*")
    parser.add_argument("--build-with-errors", action="store_true")
    parser.add_argument("--source-code", action="append")
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

        (temp_md_directory / "mkdocs.en.yml").symlink_to(
            SOURCE_DIR / "docs" / "mkdocs.en.yml"
        )
        (temp_md_directory / "config.yml").symlink_to(
            SOURCE_DIR / "docs" / "config.yml"
        )
        (temp_md_directory / "en").symlink_to(
            SOURCE_DIR / "docs" / "en", target_is_directory=True
        )

        serve_docs(config_location=(temp_md_directory / "mkdocs.en.yml"))


if __name__ == "__main__":
    main()
