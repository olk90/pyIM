personQuery = """
select
    firstname as 'First Name',
    lastname as 'Last Name',
    email as 'E-Mail'
from Person
"""

inventoryQuery = """
select 
    i.name as 'Device',
    i.category as 'Category',
    i.available as 'Available',
    i.lending_date as 'Lending Date',
    p.firstname || ' ' || p.lastname as 'Lend to',
    i.next_mot as 'Next MOT'
from InventoryItem i
left outer join Person p on i.lender_id = p.id
"""