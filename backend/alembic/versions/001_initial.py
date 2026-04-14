"""initial schema

Revision ID: 001
Revises:
Create Date: 2025-01-15 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('username', sa.String(100), unique=True, index=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'cars',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('external_id', sa.String(255), unique=True, index=True, nullable=False),
        sa.Column('brand', sa.String(100), index=True, nullable=False),
        sa.Column('brand_jp', sa.String(100), nullable=True),
        sa.Column('model', sa.String(200), index=True, nullable=False),
        sa.Column('model_jp', sa.String(200), nullable=True),
        sa.Column('grade', sa.String(500), nullable=True),
        sa.Column('year', sa.Integer, index=True, nullable=True),
        sa.Column('mileage_km', sa.Integer, nullable=True),
        sa.Column('price_jpy', sa.Integer, index=True, nullable=True),
        sa.Column('price_man', sa.Float, nullable=True),
        sa.Column('engine_cc', sa.Integer, nullable=True),
        sa.Column('transmission', sa.String(50), nullable=True),
        sa.Column('drive_type', sa.String(50), nullable=True),
        sa.Column('fuel_type', sa.String(50), nullable=True),
        sa.Column('color', sa.String(100), nullable=True),
        sa.Column('color_jp', sa.String(100), nullable=True),
        sa.Column('body_type', sa.String(100), nullable=True),
        sa.Column('doors', sa.Integer, nullable=True),
        sa.Column('seats', sa.Integer, nullable=True),
        sa.Column('inspection_date', sa.String(100), nullable=True),
        sa.Column('repair_history', sa.String(50), nullable=True),
        sa.Column('location', sa.String(200), nullable=True),
        sa.Column('dealer_name', sa.String(300), nullable=True),
        sa.Column('url', sa.String(500), nullable=False),
        sa.Column('thumbnail', sa.String(500), nullable=True),
        sa.Column('images', postgresql.ARRAY(sa.String), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('cars')
    op.drop_table('users')
