"""empty message

Revision ID: ced5419238d3
Revises: 
Create Date: 2018-10-08 15:19:50.251729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ced5419238d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paper',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author_name', sa.String(length=64), nullable=True),
    sa.Column('paper_name', sa.Text(), nullable=True),
    sa.Column('author_email', sa.String(length=120), nullable=True),
    sa.Column('tool_name', sa.String(length=200), nullable=True),
    sa.Column('link_to_pdf', sa.String(length=250), nullable=True),
    sa.Column('link_to_archive', sa.String(length=250), nullable=True),
    sa.Column('link_to_readme', sa.String(length=250), nullable=True),
    sa.Column('link_to_demo', sa.String(length=250), nullable=True),
    sa.Column('bibtex', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paper')
    # ### end Alembic commands ###
