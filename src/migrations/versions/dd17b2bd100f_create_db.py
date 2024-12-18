"""Create DB

Revision ID: dd17b2bd100f
Revises: a6782a6991c1
Create Date: 2024-10-12 17:05:42.141873

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd17b2bd100f'
down_revision: Union[str, None] = 'a6782a6991c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('google_access_token', sa.String(), nullable=False),
    sa.Column('refresh_token_name', sa.String(), nullable=True),
    sa.Column('picture', sa.String(), nullable=False),
    sa.Column('storages', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('uuid'),
    sa.UniqueConstraint('email')
    )
    op.create_table('Storage',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('creator_uuid', sa.UUID(), nullable=False),
    sa.Column('private', sa.Boolean(), nullable=False),
    sa.Column('participants_uuids', sa.JSON(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['creator_uuid'], ['User.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Storage')
    op.drop_table('User')
    # ### end Alembic commands ###
