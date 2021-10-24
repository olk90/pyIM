personQuery = """
select
    firstname,
    lastname,
    email
from Person
"""

inventoryQuery = """
select 
    i.name,
    i.category,
    i.available,
    i.lending_date,
    p.firstname || ' ' || p.lastname,
    i.next_mot MOT
from InventoryItem i
left outer join Person p on i.lender_id = p.id
"""
