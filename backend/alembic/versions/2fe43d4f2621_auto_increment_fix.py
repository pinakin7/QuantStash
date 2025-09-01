"""auto_increment_fix

Revision ID: 2fe43d4f2621
Revises: 4d2862844f58
Create Date: 2025-09-01 17:25:24.460865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fe43d4f2621'
down_revision: Union[str, Sequence[str], None] = '4d2862844f58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # For SQLite compatibility, we need to recreate tables to change column types
    # Create new tables with correct schema
    op.create_table('dividend_history_new',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('dividend', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['ticker'], ['assets.ticker'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'date', name='uq_ticker_date_dividend')
    )
    
    op.create_table('price_history_new',
        sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Float(), nullable=True),
        sa.Column('high', sa.Float(), nullable=True),
        sa.Column('low', sa.Float(), nullable=True),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['ticker'], ['assets.ticker'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'date', name='uq_ticker_date_price')
    )
    
    # Copy data from old tables to new tables
    op.execute('INSERT INTO dividend_history_new SELECT * FROM dividend_history')
    op.execute('INSERT INTO price_history_new SELECT * FROM price_history')
    
    # Drop old tables
    op.drop_table('dividend_history')
    op.drop_table('price_history')
    
    # Rename new tables to original names
    op.rename_table('dividend_history_new', 'dividend_history')
    op.rename_table('price_history_new', 'price_history')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate tables with BIGINT ids
    op.create_table('dividend_history_old',
        sa.Column('id', sa.BIGINT(), nullable=False, autoincrement=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('dividend', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['ticker'], ['assets.ticker'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'date', name='uq_ticker_date_dividend')
    )
    
    op.create_table('price_history_old',
        sa.Column('id', sa.BIGINT(), nullable=False, autoincrement=True),
        sa.Column('ticker', sa.String(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('open', sa.Float(), nullable=True),
        sa.Column('high', sa.Float(), nullable=True),
        sa.Column('low', sa.Float(), nullable=True),
        sa.Column('close', sa.Float(), nullable=False),
        sa.Column('volume', sa.BigInteger(), nullable=True),
        sa.ForeignKeyConstraint(['ticker'], ['assets.ticker'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ticker', 'date', name='uq_ticker_date_price')
    )
    
    # Copy data back
    op.execute('INSERT INTO dividend_history_old SELECT * FROM dividend_history')
    op.execute('INSERT INTO price_history_old SELECT * FROM price_history')
    
    # Drop new tables
    op.drop_table('dividend_history')
    op.drop_table('price_history')
    
    # Rename old tables back
    op.rename_table('dividend_history_old', 'dividend_history')
    op.rename_table('price_history_old', 'price_history')
