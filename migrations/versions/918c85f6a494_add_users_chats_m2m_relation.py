"""add users-chats m2m relation

Revision ID: 918c85f6a494
Revises: a689dc544470
Create Date: 2022-04-10 16:20:40.886908

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '918c85f6a494'
down_revision = 'a689dc544470'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users_in_chats',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column(
            'active',
            sa.Boolean(),
            server_default=sa.sql.expression.true(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(('chat_id',), ['chats.id'], ),
        sa.ForeignKeyConstraint(('user_id',), ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'chat_id'),
    )


def downgrade():
    op.drop_table('users_in_chats')
