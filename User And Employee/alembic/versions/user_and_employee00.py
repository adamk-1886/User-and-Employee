"""create users and employees tables

Revision ID: user_and_employee00
Revises: 
Create Date: 2025-05-28 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'user_and_employee00'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('email', sa.String),
    )
    op.create_table(
        'employees',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('role', sa.String),
    )

def downgrade():
    op.drop_table('employees')
    op.drop_table('users')
