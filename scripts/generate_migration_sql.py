"""
Migrate all remaining JSON data to Supabase using batch inserts.
This script reads JSON files and generates SQL INSERT statements in batches.
"""
import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

def load_json(filename):
    """Load JSON data from file."""
    filepath = project_root / 'data' / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def escape_sql_string(s):
    """Escape single quotes in SQL strings."""
    if s is None:
        return 'NULL'
    return str(s).replace("'", "''")

def generate_municipalities_sql():
    """Generate SQL for municipalities."""
    data = load_json('municipalities.json')
    
    values = []
    for item in data:
        area = item.get('area_km2', 'NULL')
        pop = item.get('populacao', 'NULL')
        values.append(
            f"({item['id']}, '{escape_sql_string(item['nome'])}', "
            f"{item['provincia_id']}, {area}, {pop})"
        )
    
    # Split into batches of 50
    batch_size = 50
    sqls = []
    for i in range(0, len(values), batch_size):
        batch = values[i:i+batch_size]
        sql = f"""INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao) VALUES
{',\n'.join(batch)};"""
        sqls.append(sql)
    
    return sqls

def generate_schools_sql():
    """Generate SQL for schools."""
    data = load_json('schools.json')
    
    values = []
    for item in data:
        municipio = f"'{escape_sql_string(item.get('municipio'))}'" if item.get('municipio') else 'NULL'
        tipo = f"'{escape_sql_string(item.get('tipo'))}'" if item.get('tipo') else 'NULL'
        nivel = f"'{escape_sql_string(item.get('nivel'))}'" if item.get('nivel') else 'NULL'
        
        values.append(
            f"({item['id']}, '{escape_sql_string(item['nome'])}', "
            f"{item['provincia_id']}, {municipio}, {tipo}, {nivel})"
        )
    
    # All in one batch since there are only ~17 schools
    sql = f"""INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel) VALUES
{',\n'.join(values)};"""
    
    return [sql]

def generate_markets_sql():
    """Generate SQL for markets."""
    data = load_json('markets.json')
    
    values = []
    for item in data:
        municipio = f"'{escape_sql_string(item.get('municipio'))}'" if item.get('municipio') else 'NULL'
        tipo = f"'{escape_sql_string(item.get('tipo'))}'" if item.get('tipo') else 'NULL'
        endereco = f"'{escape_sql_string(item.get('endereco'))}'" if item.get('endereco') else 'NULL'
        
        values.append(
            f"({item['id']}, '{escape_sql_string(item['nome'])}', "
            f"{item['provincia_id']}, {municipio}, {tipo}, {endereco})"
        )
    
    sql = f"""INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco) VALUES
{',\n'.join(values)};"""
    
    return [sql]

def generate_hospitals_sql():
    """Generate SQL for hospitals."""
    data = load_json('hospitals.json')
    
    values = []
    for item in data:
        municipio = f"'{escape_sql_string(item.get('municipio'))}'" if item.get('municipio') else 'NULL'
        tipo = f"'{escape_sql_string(item.get('tipo'))}'" if item.get('tipo') else 'NULL'
        endereco = f"'{escape_sql_string(item.get('endereco'))}'" if item.get('endereco') else 'NULL'
        especialidades = f"'{escape_sql_string(item.get('especialidades'))}'" if item.get('especialidades') else 'NULL'
        
        values.append(
            f"({item['id']}, '{escape_sql_string(item['nome'])}', "
            f"{item['provincia_id']}, {municipio}, {tipo}, {endereco}, {especialidades})"
        )
    
    sql = f"""INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades) VALUES
{',\n'.join(values)};"""
    
    return [sql]

def save_all_sql():
    """Generate all SQL files for migration."""
    output_dir = project_root / 'scripts' / 'migrations_sql'
    output_dir.mkdir(exist_ok=True)
    
    # Municipalities
    print("Generating municipalities SQL...")
    mun_sqls = generate_municipalities_sql()
    for i, sql in enumerate(mun_sqls):
        with open(output_dir / f'municipalities_batch_{i+1}.sql', 'w', encoding='utf-8') as f:
            f.write(sql)
    print(f"  ✅ {len(mun_sqls)} batches created")
    
    # Schools
    print("Generating schools SQL...")
    school_sqls = generate_schools_sql()
    with open(output_dir / 'schools.sql', 'w', encoding='utf-8') as f:
        f.write(school_sqls[0])
    print(f"  ✅ 1 file created")
    
    # Markets
    print("Generating markets SQL...")
    market_sqls = generate_markets_sql()
    with open(output_dir / 'markets.sql', 'w', encoding='utf-8') as f:
        f.write(market_sqls[0])
    print(f"  ✅ 1 file created")
    
    # Hospitals
    print("Generating hospitals SQL...")
    hospital_sqls = generate_hospitals_sql()
    with open(output_dir / 'hospitals.sql', 'w', encoding='utf-8') as f:
        f.write(hospital_sqls[0])
    print(f"  ✅ 1 file created")
    
    # Reset sequences
    reset_sql = """
-- Reset auto-increment sequences
SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1));
SELECT setval('provinces_id_seq', COALESCE((SELECT MAX(id) FROM provinces), 1));
SELECT setval('municipalities_id_seq', COALESCE((SELECT MAX(id) FROM municipalities), 1));
SELECT setval('schools_id_seq', COALESCE((SELECT MAX(id) FROM schools), 1));
SELECT setval('markets_id_seq', COALESCE((SELECT MAX(id) FROM markets), 1));
SELECT setval('hospitals_id_seq', COALESCE((SELECT MAX(id) FROM hospitals), 1));
"""
    with open(output_dir / 'reset_sequences.sql', 'w', encoding='utf-8') as f:
        f.write(reset_sql)
    
    print(f"\n✅ All SQL files saved to: {output_dir}")
    return mun_sqls, school_sqls, market_sqls, hospital_sqls

if __name__ == '__main__':
    save_all_sql()
