"""create vote table

Revision ID: 4fd6dd9f7fd6
Revises: c4bab5c2d467
Create Date: 2022-07-17 19:59:03.266320

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fd6dd9f7fd6'
down_revision = 'c4bab5c2d467'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('votes',
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.String(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('user_id', 'post_id')
                    )


def downgrade() -> None:
    op.drop_table('votes')
