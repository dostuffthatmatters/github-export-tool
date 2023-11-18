import subprocess
from typing import Optional


def run_shell_command(command: str, cwd: Optional[str] = None) -> str:
    process = subprocess.run(command.split(" "), capture_output=True, cwd=cwd)
    assert (
        process.returncode == 0
    ), f'command "{command}" failed: {process.stderr.decode()}'
    return process.stdout.decode().strip()
