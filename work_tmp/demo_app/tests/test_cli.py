from typer.testing import CliRunner

from demo_app.cli import app

runner = CliRunner()


def test_cli_run_default_param():
    """Validate run command with default argument"""
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Hello" in result.output
