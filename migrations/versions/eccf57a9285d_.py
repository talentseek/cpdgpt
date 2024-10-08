"""empty message

Revision ID: eccf57a9285d
Revises: b4ebdc7b450f
Create Date: 2024-09-21 19:18:44.339534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eccf57a9285d'
down_revision = 'b4ebdc7b450f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sdrs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('calendar_link', sa.String(length=255), nullable=True),
    sa.Column('rules', sa.Text(), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('demos')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('demos',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('start_time', sa.DATETIME(), nullable=False),
    sa.Column('end_time', sa.DATETIME(), nullable=False),
    sa.Column('status', sa.VARCHAR(length=50), nullable=False),
    sa.Column('location', sa.VARCHAR(length=255), nullable=True),
    sa.Column('duration', sa.INTEGER(), nullable=False),
    sa.Column('client_id', sa.INTEGER(), nullable=False),
    sa.Column('lead_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['lead_id'], ['leads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('sdrs')
    # ### end Alembic commands ###
