"""Add tables to store forecast areas

Revision ID: 05287732e7c0
Revises: 5e6c3c0a1831
Create Date: 2020-03-31 23:52:34.853863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05287732e7c0'
down_revision = '5e6c3c0a1831'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_region_name'), 'region', ['name'], unique=False)
    op.create_table('prefecture',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prefecture_name'), 'prefecture', ['name'], unique=False)
    op.create_table('city',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('pref_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['pref_id'], ['prefecture.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_city_name'), 'city', ['name'], unique=False)
    op.create_table('pinpoint_location',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pinpoint_location_name'), 'pinpoint_location', ['name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pinpoint_location_name'), table_name='pinpoint_location')
    op.drop_table('pinpoint_location')
    op.drop_index(op.f('ix_city_name'), table_name='city')
    op.drop_table('city')
    op.drop_index(op.f('ix_prefecture_name'), table_name='prefecture')
    op.drop_table('prefecture')
    op.drop_index(op.f('ix_region_name'), table_name='region')
    op.drop_table('region')
    # ### end Alembic commands ###