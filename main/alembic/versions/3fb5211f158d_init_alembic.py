"""Init Alembic

Revision ID: 3fb5211f158d
Revises: 
Create Date: 2024-05-23 14:11:22.698708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fb5211f158d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.execute('CREATE EXTENSION "uuid-ossp"')
    op.create_table('products',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('name_product', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('username', sa.String(length=255), nullable=False),
                    sa.Column('password', sa.String(length=255), nullable=False),
                    sa.Column('email', sa.String(length=255), nullable=False),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('carts',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('product_id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tokens',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('access_token', sa.UUID(as_uuid=False), server_default=sa.text('uuid_generate_v4()'), nullable=False),
                    sa.Column('datetime_create', sa.DateTime(), nullable=False),
                    sa.Column('expires', sa.DateTime(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_access_token'), 'tokens', ['access_token'], unique=True)
    op.create_table('orders',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('cart_id', sa.BigInteger(), nullable=False),
                    sa.Column('product_id', sa.BigInteger(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    op.drop_index(op.f('ix_tokens_access_token'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_table('carts')
    op.drop_table('users')
    op.drop_table('products')
    # ### end Alembic commands ###
