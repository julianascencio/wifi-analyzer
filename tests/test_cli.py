import json
import os
import subprocess


def test_demo_and_import_pipeline(tmp_path):
    env = {**os.environ, "MPLBACKEND": "Agg"}
    subprocess.run(
        ["wifi-analyzer", "demo", "--output", str(tmp_path / "demo")],
        check=True,
        env=env,
        capture_output=True,
    )
    report = json.loads((tmp_path / "demo/summary.json").read_text())
    assert len(report["groups"]) == 4
    assert all(g["evidence"] == "synthetic" for g in report["groups"])
    for group in report["groups"]:
        assert (tmp_path / "demo" / group["map"]).read_bytes().startswith(b"\x89PNG")
    subprocess.run(
        [
            "wifi-analyzer",
            "report",
            str(tmp_path / "demo/survey.csv"),
            "--output",
            str(tmp_path / "imported"),
        ],
        check=True,
        env=env,
        capture_output=True,
    )
    assert json.loads((tmp_path / "imported/summary.json").read_text()) == report


def test_invalid_cli_input_has_no_traceback(tmp_path):
    result = subprocess.run(
        ["wifi-analyzer", "report", str(tmp_path / "missing.csv")], capture_output=True, text=True
    )
    assert result.returncode == 2
    assert "Traceback" not in result.stderr
