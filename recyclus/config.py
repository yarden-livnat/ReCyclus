from pathlib import Path

config_path = Path.home()

config = dict(
    config_path=config_path,
    config_file=config_path / '.recyclus',
    auth_file=config_path / '.recyclus-credentials',
    server='http://localhost:5000/api'
)