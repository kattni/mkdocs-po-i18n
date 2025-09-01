import subprocess
from pathlib import Path

SOURCE_DIR = Path.cwd()


def generate_pot_files(input_dir: Path, output_dir: Path) -> None:
    subprocess.run(
        [
            "md2po",
            f"--input={input_dir}",
            f"--output={output_dir}",
            "--pot",
            "--duplicates=merge",
        ],
        check=True,
    )


def main():
    docs_en_directory = Path(__file__).parent / "docs"
    docs_en_directory.mkdir(parents=True, exist_ok=True)

    try:
        (Path(__file__).parent / "docs" / "en").symlink_to(
            SOURCE_DIR / "docs" / "en", target_is_directory=True
        )
    except FileExistsError:
        pass

    output_directory = SOURCE_DIR / "docs" / "locales" / "templates"

    output_directory.mkdir(parents=True, exist_ok=True)
    generate_pot_files(
        input_dir=Path("docs") / "en",
        output_dir=output_directory,
    )

    (Path(__file__).parent / "docs" / "en").unlink(missing_ok=True)
    (Path(__file__).parent / "docs").rmdir()


if __name__ == "__main__":
    main()
