"""Update DB schema to reflect submodules changes

Revision ID: 9ab05df71cf8
Revises: 5c5459333ab9
Create Date: 2020-08-22 15:43:03.437133

"""
from alembic import op
import sqlalchemy as sa

NAMING_CONVENTION = {
    'fk':
    'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
}

# revision identifiers, used by Alembic.
revision = '9ab05df71cf8'
down_revision = '5c5459333ab9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'subprefecture',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(length=64), nullable=True),
        sa.Column('prefecture_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['prefecture_id'], ['prefecture.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    with op.batch_alter_table(
        'city',
        naming_convention=NAMING_CONVENTION
    ) as batch_op:
        batch_op.add_column(sa.Column('code', sa.Integer(), nullable=True))
        batch_op.add_column(
            sa.Column('subprefecture_id', sa.Integer(), nullable=True)
        )
        batch_op.drop_index('ix_city_name')
        batch_op.drop_constraint(
            'fk_city_pref_id_prefecture',
            type_='foreignkey')
        batch_op.create_foreign_key(
            'fk_city_subprefecture_id_subprefecture',
            'subprefecture',
            ['subprefecture_id'],
            ['id']
        )
        batch_op.drop_column('pref_id')

    with op.batch_alter_table('prefecture') as batch_op:
        batch_op.add_column(sa.Column('code', sa.Integer(), nullable=True))
        batch_op.drop_index('ix_prefecture_name')

    with op.batch_alter_table('region') as batch_op:
        batch_op.add_column(sa.Column('code', sa.Integer(), nullable=True))
        batch_op.drop_index('ix_region_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('region') as batch_op:
        batch_op.create_index(
            'ix_region_name',
            ['name'],
            unique=False
        )
        batch_op.drop_column('code')

    with op.batch_alter_table('prefecture') as batch_op:
        batch_op.create_index(
            'ix_prefecture_name',
            ['name'],
            unique=False
        )
        batch_op.drop_column('code')

    with op.batch_alter_table(
        'city',
        naming_convention=NAMING_CONVENTION
    ) as batch_op:
        batch_op.add_column(
            sa.Column('pref_id', sa.INTEGER(), nullable=True)
        )
        batch_op.drop_constraint(
            'fk_city_subprefecture_id_subprefecture',
            type_='foreignkey'
        )
        batch_op.create_foreign_key(
            'fk_city_pref_id_prefecture',
            'prefecture',
            ['pref_id'],
            ['id']
        )
        batch_op.create_index(
            'ix_city_name',
            ['name'],
            unique=False
        )
        batch_op.drop_column('subprefecture_id')
        batch_op.drop_column('code')

    op.drop_table('subprefecture')
    # ### end Alembic commands ###
