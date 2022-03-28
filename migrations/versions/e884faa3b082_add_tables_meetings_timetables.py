"""add tables meetings timetables

Revision ID: e884faa3b082
Revises: 56df5c6b0df6
Create Date: 2022-03-28 23:25:22.485959

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e884faa3b082'
down_revision = '56df5c6b0df6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'meetings',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('chat_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'timetables',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('time', sa.Time(), nullable=True),
        sa.Column('weekdays', sa.ARRAY(sa.Text()), nullable=True),
        sa.Column('meeting_id', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('timetables')
    op.drop_table('meetings')
