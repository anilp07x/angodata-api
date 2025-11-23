import json

municipalities = json.load(open('data/municipalities.json'))
remaining = municipalities[49:]

values = []
for m in remaining:
    nome = m['nome'].replace("'", "''")
    values.append(f"({m['id']}, '{nome}', {m['provincia_id']}, NULL, NULL)")

sql = f"INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao) VALUES\n{',\n'.join(values)};"

with open('scripts/municipalities_remaining.sql', 'w') as f:
    f.write(sql)

print(f"Generated SQL for {len(remaining)} municipalities")
