import strawberry
from strawberry.federation.schema_directives import Key


@strawberry.federation.type(keys=[Key(fields="id", resolvable=False)])
class User:
    id: strawberry.ID
    shipping_address: str | None = strawberry.federation.field(external=True)


@strawberry.federation.type(keys=[Key(fields="id", resolvable=False)])
class Product:
    id: strawberry.ID
    weight: float | None = strawberry.federation.field(external=True)


def calculate_shipping_cost(root: "Order") -> float:
    cost = 0.0

    if root.buyer.shipping_address is not None:
        cost += 10.0

    for item in root.items:
        if item.weight is not None:
            cost += item.weight * 0.5

    return cost


@strawberry.federation.type(keys=["id"])
class Order:
    id: strawberry.ID
    buyer: User = strawberry.federation.field(external=True)
    items: list[Product] = strawberry.federation.field(external=True)
    shipping_cost: float | None = strawberry.federation.field(
        requires=[
            "items { id weight }",
            "buyer { id shippingAddress }",
        ],
        resolver=calculate_shipping_cost,
    )


schema = strawberry.federation.Schema(
    enable_federation_2=True,
    types=[Order],
)
