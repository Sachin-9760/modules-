from click.testing import CliRunner

import main

runner = CliRunner()


def test_ingest_command():
    result = runner.invoke(main.cli, ["ingest", "--dry-run", "--source", "demo.csv", "--limit", "4"])
    assert result.exit_code == 0
    assert "Dry run" in result.output


def test_run_command():
    result = runner.invoke(main.cli, ["run", "--dataset", "demo.json", "--iterations", "2"])
    assert result.exit_code == 0
    assert "Run Summary" in result.output


def test_evaluate_command():
    result = runner.invoke(main.cli, ["evaluate", "--dataset", "demo.json", "--threshold", "0.75"])
    assert result.exit_code == 0
    assert "Evaluation report" in result.output


def test_report_command():
    result = runner.invoke(main.cli, ["report", "--format", "table"])
    assert result.exit_code == 0
    assert "Operational Report" in result.output
