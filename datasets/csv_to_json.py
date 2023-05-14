import csv
import json


def csv_to_json(csv_path, json_path, model):
    json_data = []
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if 'id' in row:
                pk = int(row['id'])
                del row['id']

                if 'is_published' in row:
                    row['is_published'] = True if row['is_published'].lower() == 'true' else False
                if 'location_id' in row:
                    row['location'] = [row['location_id']]
                    del row['location_id']

                json_data.append({
                    'model': model,
                    'pk': pk,
                    'fields': row,
                })

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(json_data, ensure_ascii=False))


csv_to_json('ads.csv', 'ads.json', 'api.ads')
csv_to_json('category.csv', 'category.json', 'api.category')
csv_to_json('location.csv', 'location.json', 'users.location')
csv_to_json('user.csv', 'user.json', 'users.user')
