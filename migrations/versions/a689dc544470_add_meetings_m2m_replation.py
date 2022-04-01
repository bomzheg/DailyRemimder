"""add meetings m2m replation

Revision ID: a689dc544470
Revises: e884faa3b082
Create Date: 2022-04-02 00:15:59.819453

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a689dc544470'
down_revision = 'e884faa3b082'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'meeting_participants',
        sa.Column('meeting_id', sa.BigInteger(), nullable=False),
        sa.Column('participants_id', sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.ForeignKeyConstraint(['participants_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('meeting_id', 'participants_id')
    )


def downgrade():
    op.drop_table('meeting_participants')
