"""Rename Dislike liked_at to diliked_at

Revision ID: 5c5c19f5a33e
Revises: bc519f04a43b
Create Date: 2022-05-14 05:55:38.365170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5c5c19f5a33e'
down_revision = 'bc519f04a43b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dislike', sa.Column('disliked_at', sa.DateTime(), nullable=True))
    op.drop_column('dislike', 'liked_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dislike', sa.Column('liked_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('dislike', 'disliked_at')
    # ### end Alembic commands ###