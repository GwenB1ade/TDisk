"""Create models

Revision ID: a6782a6991c1
Revises: 
Create Date: 2024-08-23 21:35:06.951606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6782a6991c1'
down_revision: Union[str, None] = None
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
    op.create_table('Object',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('author_uuid', sa.UUID(), nullable=False),
    sa.Column('storage_uuid', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['author_uuid'], ['User.uuid'], ),
    sa.ForeignKeyConstraint(['storage_uuid'], ['Storage.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Object')
    op.drop_table('Storage')
    op.drop_table('User')
    # ### end Alembic commands ###