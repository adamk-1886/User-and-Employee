"""rename role to employee_role and add employee_designation

Revision ID: update_employee_table01
Revises: user_and_employee00
Create Date: 2025-05-29 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'update_employee_table01'
down_revision = 'user_and_employee00'
branch_labels = None
depends_on = None


def upgrade():
    # Rename column 'role' to 'employee_role'
    op.alter_column('employees', 'role', new_column_name='employee_role')

    # Add new column 'employee_designation'
    op.add_column('employees', sa.Column('employee_designation', sa.String))


def downgrade():
    # Revert the column rename
    op.alter_column('employees', 'employee_role', new_column_name='role')

    # Drop the new column
    op.drop_column('employees', 'employee_designation')
