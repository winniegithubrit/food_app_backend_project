"""Create tables

Revision ID: 28c23b7e339b
Revises: 
Create Date: 2023-08-02 15:33:32.775639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28c23b7e339b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('driver',
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('current_location', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('driver_id')
    )
    op.create_table('owner',
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('owner_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('type', sa.Boolean(), nullable=True),
    sa.Column('blocked', sa.String(), nullable=True),
    sa.Column('activity', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('customer_id')
    )
    op.create_table('restaurant',
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('restaurant_name', sa.String(), nullable=True),
    sa.Column('contact_number', sa.String(), nullable=True),
    sa.Column('opening_hours', sa.Time(), nullable=True),
    sa.Column('closing_hours', sa.Time(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.Column('payment_method', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.owner_id'], ),
    sa.PrimaryKeyConstraint('restaurant_id')
    )
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.owner_id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('customerReviews',
    sa.Column('customerReview_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('review_comment', sa.String(), nullable=True),
    sa.Column('review_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.PrimaryKeyConstraint('customerReview_id')
    )
    op.create_table('location',
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('delivery_fee', sa.Integer(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.owner_id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('menu',
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('menu_name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('prices', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('menu_id')
    )
    op.create_table('payment',
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('payment_type', sa.String(), nullable=True),
    sa.Column('payment_amount', sa.Integer(), nullable=True),
    sa.Column('payment_date_and_time', sa.DateTime(), nullable=True),
    sa.Column('payment_status', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('payment_id')
    )
    op.create_table('restaurantReviews',
    sa.Column('restaurantReview_id', sa.Integer(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('review_comment', sa.String(), nullable=True),
    sa.Column('review_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('restaurantReview_id')
    )
    op.create_table('superadmin',
    sa.Column('superadmin_id_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('restaurant_id', sa.Integer(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['owner.owner_id'], ),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurant.restaurant_id'], ),
    sa.PrimaryKeyConstraint('superadmin_id_id')
    )
    op.create_table('favourite',
    sa.Column('favourite_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.menu_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('favourite_id')
    )
    op.create_table('menuReviews',
    sa.Column('restaurantReview_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('review_comment', sa.String(), nullable=True),
    sa.Column('review_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.menu_id'], ),
    sa.PrimaryKeyConstraint('restaurantReview_id')
    )
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=True),
    sa.Column('order_date_and_time', sa.DateTime(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('payment_method', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menu.menu_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('deliveries',
    sa.Column('delivery_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('driver_id', sa.Integer(), nullable=True),
    sa.Column('delivery_date_and_time', sa.DateTime(), nullable=True),
    sa.Column('dispatch', sa.Boolean(), nullable=True),
    sa.Column('delivered', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['driver_id'], ['driver.driver_id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('delivery_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('deliveries')
    op.drop_table('order')
    op.drop_table('menuReviews')
    op.drop_table('favourite')
    op.drop_table('superadmin')
    op.drop_table('restaurantReviews')
    op.drop_table('payment')
    op.drop_table('menu')
    op.drop_table('location')
    op.drop_table('customerReviews')
    op.drop_table('admin')
    op.drop_table('restaurant')
    op.drop_table('customers')
    op.drop_table('user')
    op.drop_table('owner')
    op.drop_table('driver')
    # ### end Alembic commands ###
