from api.basket import router as router_basket
from api.images import router as router_images
from api.products import router as router_products
from api.styles import router as router_styles
from api.users import router as router_users

all_routers = [
    router_images,
    router_styles,
    router_basket,
    router_users,
    router_products,
]
