"""Add submitter_ip column

Revision ID: 26d11118fd2
Revises: 24ab58f281b
Create Date: 2015-09-05 10:07:36.595273

"""

# revision identifiers, used by Alembic.
revision = '26d11118fd2'
down_revision = '24ab58f281b'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.add_column('quotes', sa.Column('submitter_ip', sa.Text(), nullable=True))


def downgrade():
	op.drop_column('quotes', 'submitter_ip')
