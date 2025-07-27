"""merge migrations

Revision ID: d5f569f04e37
Revises: d6c17013232c, ec79ec9fa124
Create Date: 2025-07-27 13:31:05.835889

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f569f04e37'
down_revision = ('d6c17013232c', 'ec79ec9fa124')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
