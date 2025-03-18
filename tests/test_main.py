import pytest
import pathlib
import io

from src.head.main import main


@pytest.mark.parametrize(
    "content, expected",
    [
        ("line1\nline2\nline3\n", "line1\nline2\nline3\n"),
        (
            "\n".join(f"line{i}" for i in range(1, 15)),
            "\n".join(f"line{i}" for i in range(1, 11)) + "\n",
        ),
        ("\n", "\n"),
    ],
)
def test_main_file(tmp_path: pathlib.Path, content, expected):
    file_path = tmp_path / "test.txt"
    file_path.write_text(content)

    out = io.StringIO()
    main(files=[file_path], output=out, lines=None, bytes=None)

    assert out.getvalue() == expected


@pytest.mark.parametrize(
    "stdin_content, expected",
    [
        ("line1\nline2\nline3\n", "line1\nline2\nline3\n"),
        ("single\n", "single\n"),
        ("\n", "\n"),
    ],
)
def test_main_stdin(stdin_content, expected):
    stdin_mock = io.StringIO(stdin_content)

    out = io.StringIO()
    main(files=[stdin_mock], output=out, lines=None, bytes=None)

    assert out.getvalue() == expected


@pytest.mark.parametrize(
    "content, num_lines, expected",
    [
        ("line1\nline2\nline3\n", 3, "line1\nline2\nline3\n"),
        ("single\n", 1, "single\n"),
        ("\n", 1, "\n"),
        (
            "\n".join(f"line{i}" for i in range(1, 11)),
            5,
            "\n".join(f"line{i}" for i in range(1, 6)) + "\n",
        ),
        ("lonely_line\n", 5, "lonely_line\n"),
    ],
)
def test_main_number_lines(tmp_path: pathlib.Path, content, num_lines, expected):
    file_path = tmp_path / "test.txt"
    file_path.write_text(content)

    out = io.StringIO()
    main(files=[file_path], output=out, lines=num_lines, bytes=None)

    assert out.getvalue() == expected


@pytest.mark.parametrize(
    "content, num_bytes, expected",
    [
        ("Hello, World!\nThis is a test.\n", 5, "Hello"),
        ("1234567890\nabcdefghij\n", 10, "1234567890"),
        ("Short\n", 10, "Short\n"),
        ("", 5, ""),
    ],
)
def test_main_number_bytes(tmp_path: pathlib.Path, content, num_bytes, expected):
    file_path = tmp_path / "test_bytes.txt"
    file_path.write_text(content)

    out = io.StringIO()
    main(files=[file_path], output=out, lines=None, bytes=num_bytes)

    assert out.getvalue() == expected


@pytest.mark.parametrize(
    "contents, expected",
    [
        (
            {
                "file1.txt": "line1\nline2\nline3\n",
                "file2.txt": "hello\nworld\n",
            },
            "==> file1.txt <==\nline1\nline2\nline3\n\n==> file2.txt <==\nhello\nworld\n",
        ),
        (
            {
                "testA.txt": "A1\nA2\nA3\nA4\n",
                "testB.txt": "B1\nB2\n",
                "testC.txt": "C1\n",
            },
            "==> testA.txt <==\nA1\nA2\nA3\nA4\n\n==> testB.txt <==\nB1\nB2\n\n==> testC.txt <==\nC1\n",
        ),
    ],
)
def test_main_multiple_files(tmp_path: pathlib.Path, contents, expected):
    file_paths = []
    for filename, content in contents.items():
        file_path = tmp_path / filename
        file_path.write_text(content)
        file_paths.append(file_path)

    out = io.StringIO()
    main(files=file_paths, output=out, lines=None, bytes=None)

    assert out.getvalue() == expected
