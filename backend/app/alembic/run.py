import asyncio
from alembic.config import Config
from alembic import command
from pathlib import Path
import argparse

ALEMBIC_INI = Path(__file__).parent.parent / "alembic.ini"

def main():
    """Интерактивный режим миграций"""
    print("Доступные команды:")
    print("  poetry run migrate-up      - Применить миграции")
    print("  poetry run migrate-down    - Откатить миграции")
    print("  poetry run migrate-create  - Создать новую миграцию")
    print("  poetry run alembic ...     - Прямой вызов alembic")

def upgrade():
    """Применить все миграции"""
    alembic_cfg = Config(ALEMBIC_INI)
    command.upgrade(alembic_cfg, "head")

def downgrade():
    """Откатить последнюю миграцию"""
    alembic_cfg = Config(ALEMBIC_INI)
    command.downgrade(alembic_cfg, "-1")

def create_migration():
    """Создать новую миграцию"""
    parser = argparse.ArgumentParser()
    parser.add_argument("message", help="Описание миграции")
    args = parser.parse_args()
    
    alembic_cfg = Config(ALEMBIC_INI)
    command.revision(
        alembic_cfg,
        message=args.message,
        autogenerate=True,
        head="head"
    )