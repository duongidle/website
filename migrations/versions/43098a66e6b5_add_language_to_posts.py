"""add language to posts

Revision ID: 43098a66e6b5
Revises: 72ae2dd9479e
Create Date: 2019-10-29 09:57:00.871885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43098a66e6b5'
down_revision = '72ae2dd9479e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###
