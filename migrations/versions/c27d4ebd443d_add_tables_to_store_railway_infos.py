"""Add tables to store railway infos

Revision ID: c27d4ebd443d
Revises: 05287732e7c0
Create Date: 2020-05-13 03:34:42.773040

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c27d4ebd443d'
down_revision = '05287732e7c0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('railway_category',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_railway_category_name'), 'railway_category', ['name'], unique=False)
    op.create_table('railway_company',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_railway_company_name'), 'railway_company', ['name'], unique=False)
    op.create_table('railway_region',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_railway_region_name'), 'railway_region', ['name'], unique=False)
    op.create_table('railway',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('status_page_url', sa.String(length=64), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['railway_category.id'], ),
    sa.ForeignKeyConstraint(['region_id'], ['railway_region.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_railway_name'), 'railway', ['name'], unique=False)
    op.create_index(op.f('ix_railway_status_page_url'), 'railway', ['status_page_url'], unique=False)
    op.create_table('railway_category_company',
    sa.Column('railway_category_id', sa.Integer(), nullable=True),
    sa.Column('railway_company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['railway_category_id'], ['railway_category.id'], ),
    sa.ForeignKeyConstraint(['railway_company_id'], ['railway_company.id'], )
    )
    op.create_table('railway_company_region',
    sa.Column('railway_company_id', sa.Integer(), nullable=True),
    sa.Column('railway_region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['railway_company_id'], ['railway_company.id'], ),
    sa.ForeignKeyConstraint(['railway_region_id'], ['railway_region.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('railway_company_region')
    op.drop_table('railway_category_company')
    op.drop_index(op.f('ix_railway_status_page_url'), table_name='railway')
    op.drop_index(op.f('ix_railway_name'), table_name='railway')
    op.drop_table('railway')
    op.drop_index(op.f('ix_railway_region_name'), table_name='railway_region')
    op.drop_table('railway_region')
    op.drop_index(op.f('ix_railway_company_name'), table_name='railway_company')
    op.drop_table('railway_company')
    op.drop_index(op.f('ix_railway_category_name'), table_name='railway_category')
    op.drop_table('railway_category')
    # ### end Alembic commands ###
