"""empty message

Revision ID: ce8936c05ea1
Revises: e9f031d6a549
Create Date: 2019-06-24 06:22:44.298539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce8936c05ea1'
down_revision = 'e9f031d6a549'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('papers', sa.Column('category', sa.String(length=150), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('papers', 'category')
    # ### end Alembic commands ###
