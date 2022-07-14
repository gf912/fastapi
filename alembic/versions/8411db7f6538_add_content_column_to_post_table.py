"""add content column to post table

Revision ID: 8411db7f6538
Revises: 287e9af639f7
Create Date: 2022-07-14 11:00:20.351462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8411db7f6538'
down_revision = '287e9af639f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
