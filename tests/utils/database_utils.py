import alembic
import alembic.config
from alembic import command


def migrate_to_db(alembic_ini_path="alembic.ini", revision="head"):
    config = alembic.config.Config(alembic_ini_path)
    config.config_ini_section = "test_db"
    command.upgrade(config, revision)
