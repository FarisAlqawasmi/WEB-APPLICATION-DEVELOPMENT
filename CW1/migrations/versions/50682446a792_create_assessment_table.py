"""Create assessment table

Revision ID: 50682446a792
Revises: 
Create Date: 2024-10-14 16:20:20.351948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50682446a792'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assessment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('module_code', sa.String(length=10), nullable=False),
    sa.Column('deadline', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('is_completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assessment')
    # ### end Alembic commands ###