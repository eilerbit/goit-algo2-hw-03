import csv
import random
from timeit import timeit
from BTrees.OOBTree import OOBTree


def load_items_from_csv(filename):
    items = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"]),
            }
            items.append(item)
    return items


def add_item_to_tree(tree, item):
    price = item["Price"]
    if price in tree:
        tree[price].append(item)
    else:
        tree[price] = [item]

def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = item


def range_query_tree(tree, min_price, max_price):
    result = []
    for price, items in tree.items(min_price, max_price):
        result.extend(items)
    return result

def range_query_dict(dictionary, min_price, max_price):
    return [item for item in dictionary.values() if min_price <= item["Price"] <= max_price]


def main():
    items = load_items_from_csv("generated_items_data.csv")

    tree = OOBTree()
    dct = {}

    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dct, item)

    price_ranges = [(random.uniform(10, 100), random.uniform(100, 1000)) for _ in range(100)]

    def run_tree_queries():
        for min_price, max_price in price_ranges:
            range_query_tree(tree, min(min_price, max_price), max(min_price, max_price))

    tree_time = timeit(run_tree_queries, number=1)

    def run_dict_queries():
        for min_price, max_price in price_ranges:
            range_query_dict(dct, min(min_price, max_price), max(min_price, max_price))

    dict_time = timeit(run_dict_queries, number=1)

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")

if __name__ == "__main__":
    main()
