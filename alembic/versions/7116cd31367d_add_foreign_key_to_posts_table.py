"""add foreign key to posts table

Revision ID: 7116cd31367d
Revises: 5ca5ee71b25b
Create Date: 2022-07-14 11:07:34.879766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7116cd31367d'
down_revision = '5ca5ee71b25b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fkey', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
