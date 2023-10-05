from square.client import Client
import square as square
import csv
import sys

#Function to get invntory counts with pagination
def get_inventory_counts(resultDict = {}):
  
  # Create body of the request
  body = { "limit": 1000 }

  # Define cursor if applicable
  if ('cursor' in resultDict.keys()):
    body['cursor'] = resultDict['cursor']

  # Fetch next batch of inventory counts
  res_inventory_counts = client.inventory.batch_retrieve_inventory_counts(body = body)

  # Check for errors
  if res_inventory_counts.is_error():
    return []

  # Initialize empty list for inventory counts
  counts = []

  # Append inventory counts to list
  for inventory_object in res_inventory_counts.body['counts']:
    counts.append(inventory_object)

  # Concatenate previous results with new data
  if 'counts' in resultDict:
    counts = resultDict['counts'] + counts

  # Further process data if cursor is provided
  if ('cursor' in res_inventory_counts.body.keys()):
    return get_inventory_counts({ 'cursor': res_inventory_counts.body['cursor'], 'counts': counts })

  result_dict = {}

  for item in counts:
    id = item['catalog_object_id']
    if id in result_dict:
      result_dict[id] += int(item['quantity'])
    else:
      result_dict[id] = int(item['quantity'])

  # Processing finished; no cursor provided
  return result_dict

#Function to get catalog items with pagination 
def get_list_catalog(resultDict = {}):
  
  # Create body of the request
  cursor = resultDict['cursor'] if 'cursor' in resultDict.keys() else None

  # Fetch next batch of catalogs
  res_inventory = client.catalog.list_catalog(types = "ITEM", cursor = cursor)

  # Check for errors
  if res_inventory.is_error():
    return []

  # Initialize empty list for catalogs
  objects = []

  # Append catalogs to list
  for inventory_object in res_inventory.body['objects']:
    objects.append(inventory_object)

  # Concatenate previous results with new data
  if 'objects' in resultDict:
    objects = resultDict['objects'] + objects

  # Further process data if cursor is provided
  if ('cursor' in res_inventory.body.keys()):
    return get_list_catalog({ 'cursor': res_inventory.body['cursor'], 'objects': objects })

  # Processing finished; no cursor provided
  return objects


def get_combined_data(inventory_dict, catalog_list):

  result = {}

  # Loop through each item in the catolog
  for item in catalog_list:
    item_data = item['item_data']
    item_name = item_data['name']
    variations = item_data['variations']

    # Loop through each variation of this item
    for variation in variations:
      id = variation['id']
      item_variation = variation['item_variation_data']

      # Use $0 as price if the item uses variable pricing
      price = int(item_variation['price_money']['amount']) / 100 if item_variation['pricing_type'] == "FIXED_PRICING" else 0

      # Use 0 as quantity if item is out of stock/weird stocking case
      quantity = inventory_dict[id] if id in inventory_dict else 0

      # Write results to resulting dictionary
      result[id] = {
        "id": id,
        "name": f"{item_name} {item_variation['name']}",
        "quantity": quantity,
        "price": price,
        "price_on_hand": price * quantity
      }
  return result


def write_to_csv(combined_data):

  values = list(combined_data.values())

  with open('S:\IT\BI\SSIS Integration Files\Square Mckenneys Inventory\square_inventory.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=values[0].keys())
    writer.writeheader()
    for row in combined_data.values():
      writer.writerow(row)
  
  
#Error handling
try:
  
  key = sys.argv[1]

  #Setting up client connection
  client = Client(
    access_token=key,
    environment='production')
  
  # Get inventory counts in the form of a dictionary{}
  inventory_dict = get_inventory_counts()

  # Get the catolog items in the form of a list[]
  catalog_list = get_list_catalog()

  # Combines the data form catalog_list and inventory_dict
  combined_data = get_combined_data(inventory_dict, catalog_list)

  #writes all the data to a csv
  write_data = write_to_csv(combined_data)
  pass
except Exception as e:
  with open('C:\\Users\\automation\\Documents\\UiPath\\Square_API\\error.txt', 'w') as f:
    f.write(str(e))
