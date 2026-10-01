import hashlib

def create_products_cache_key(
    page,
    limit,
    category,
    min_price,
    max_price,
    sort_by,
    order
):
    raw_key = (
        f"page={page}|"
        f"limit={limit}|"
        f"category={category}|"
        f"min_price={min_price}|"
        f"max_price={max_price}|"
        f"sort_by={sort_by}|"
        f"order={order}"
    )

    hashed_key = hashlib.sha256(
        raw_key.encode()
    ).hexdigest()

    return f"products:{hashed_key}"