"""Remove unused score column

Revision ID: 24ab58f281b
Revises: 4dfc0f037a6
Create Date: 2015-09-05 10:34:38.458332

"""

# revision identifiers, used by Alembic.
revision = '24ab58f281b'
down_revision = '4dfc0f037a6'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
	op.drop_column('quotes', 'score')


def downgrade():
	op.add_column('quotes', sa.Column('score', sa.INTEGER(), nullable=True))
