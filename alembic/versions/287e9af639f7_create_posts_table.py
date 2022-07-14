"""create posts table

Revision ID: 287e9af639f7
Revises: 
Create Date: 2022-07-14 10:12:53.808637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '287e9af639f7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
