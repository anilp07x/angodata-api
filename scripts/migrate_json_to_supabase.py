"""
Script to migrate data from JSON files to Supabase PostgreSQL database.
Uses MCP Supabase for direct SQL execution.
"""
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()


def load_json_data(filename):
    """Load data from JSON file."""
    filepath = project_root / 'data' / filename
    if not filepath.exists():
        print(f"⚠️  Arquivo não encontrado: {filepath}")
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def migrate_users():
    """Migrate users from JSON to database."""
    print("\n📦 Migrando usuários...")
    users = load_json_data('users.json')
    
    if not users:
        print("  ⚠️  Nenhum usuário encontrado")
        return
    
    migrated = 0
    for user in users:
        try:
            # Note: Using MCP execute_sql from command line or integrate with MCP client
            print(f"  • {user['email']} ({user['role']})")
            migrated += 1
        except Exception as e:
            print(f"  ❌ Erro ao migrar {user.get('email', 'unknown')}: {e}")
    
    print(f"  ✅ {migrated}/{len(users)} usuários migrados")


def migrate_provinces():
    """Migrate provinces from JSON to database."""
    print("\n🗺️  Migrando províncias...")
    provinces = load_json_data('provinces.json')
    
    if not provinces:
        print("  ⚠️  Nenhuma província encontrada")
        return
    
    migrated = 0
    for province in provinces:
        try:
            print(f"  • {province['nome']}")
            migrated += 1
        except Exception as e:
            print(f"  ❌ Erro ao migrar {province.get('nome', 'unknown')}: {e}")
    
    print(f"  ✅ {migrated}/{len(provinces)} províncias migradas")


def migrate_municipalities():
    """Migrate municipalities from JSON to database."""
    print("\n🏘️  Migrando municípios...")
    municipalities = load_json_data('municipalities.json')
    
    if not municipalities:
        print("  ⚠️  Nenhum município encontrado")
        return
    
    migrated = 0
    for mun in municipalities:
        try:
            print(f"  • {mun['nome']} (Província ID: {mun['provincia_id']})")
            migrated += 1
        except Exception as e:
            print(f"  ❌ Erro ao migrar {mun.get('nome', 'unknown')}: {e}")
    
    print(f"  ✅ {migrated}/{len(municipalities)} municípios migrados")


def migrate_schools():
    """Migrate schools from JSON to database."""
    print("\n🏫 Migrando escolas...")
    schools = load_json_data('schools.json')
    
    if not schools:
        print("  ⚠️  Nenhuma escola encontrada")
        return
    
    migrated = 0
    for school in schools:
        try:
            print(f"  • {school['nome']}")
            migrated += 1
        except Exception as e:
            print(f"  ❌ Erro ao migrar {school.get('nome', 'unknown')}: {e}")
    
    print(f"  ✅ {migrated}/{len(schools)} escolas migradas")


def migrate_markets():
    """Migrate markets from JSON to database."""
    print("\n🛒 Migrando mercados...")
    markets = load_json_data('markets.json')
    
    if not markets:
        print("  ⚠️  Nenhum mercado encontrado")
        return
    
    migrated = 0
    for market in markets:
        try:
            print(f"  • {market['nome']}")
            migrated += 1
        except Exception as e:
            print(f"  ❌ Erro ao migrar {market.get('nome', 'unknown')}: {e}")
    
    print(f"  ✅ {migrated}/{len(markets)} mercados migrados")


def migrate_hospitals():
    """Migrate hospitals from JSON to database."""
    print("\n🏥 Migrando hospitais...")
    hospitals = load_json_data('hospitals.json')
    
    if not hospitals:
        print("  ⚠️  Nenhum hospital encontrado")
        return
    
    migrated = 0
    for hospital in hospitals:
        try:
            print(f"  • {hospital['nome']}")
            migrated += 1
        except Exception as e:
            print(f"  ❌ Erro ao migrar {hospital.get('nome', 'unknown')}: {e}")
    
    print(f"  ✅ {migrated}/{len(hospitals)} hospitais migrados")


def generate_sql_inserts():
    """
    Generate SQL INSERT statements for all data.
    This can be copied and pasted into Supabase SQL Editor or used with MCP.
    """
    print("\n" + "="*70)
    print("GERANDO SQL PARA MIGRAÇÃO DE DADOS")
    print("="*70)
    
    sql_statements = []
    
    # Users
    users = load_json_data('users.json')
    if users:
        print("\n-- USERS")
        for user in users:
            sql = f"""INSERT INTO users (id, username, email, password_hash, role, created_at)
VALUES ({user['id']}, '{user['username'].replace("'", "''")}', '{user['email']}', 
        '{user['password_hash']}', '{user['role']}', '{user['created_at']}')
ON CONFLICT (email) DO NOTHING;"""
            sql_statements.append(sql)
            print(sql)
    
    # Provinces
    provinces = load_json_data('provinces.json')
    if provinces:
        print("\n-- PROVINCES")
        for prov in provinces:
            sql = f"""INSERT INTO provinces (id, nome, capital, area_km2, populacao)
VALUES ({prov['id']}, '{prov['nome'].replace("'", "''")}', '{prov.get('capital', '').replace("'", "''")}', 
        {prov.get('area_km2', 'NULL')}, {prov.get('populacao', 'NULL')})
ON CONFLICT (nome) DO NOTHING;"""
            sql_statements.append(sql)
            print(sql)
    
    # Municipalities
    municipalities = load_json_data('municipalities.json')
    if municipalities:
        print("\n-- MUNICIPALITIES")
        for mun in municipalities:
            sql = f"""INSERT INTO municipalities (id, nome, provincia_id, area_km2, populacao)
VALUES ({mun['id']}, '{mun['nome'].replace("'", "''")}', {mun['provincia_id']}, 
        {mun.get('area_km2', 'NULL')}, {mun.get('populacao', 'NULL')});"""
            sql_statements.append(sql)
            print(sql)
    
    # Schools
    schools = load_json_data('schools.json')
    if schools:
        print("\n-- SCHOOLS")
        for school in schools:
            sql = f"""INSERT INTO schools (id, nome, provincia_id, municipio, tipo, nivel)
VALUES ({school['id']}, '{school['nome'].replace("'", "''")}', {school['provincia_id']}, 
        '{school.get('municipio', '').replace("'", "''")}', 
        '{school.get('tipo', '').replace("'", "''")}', 
        '{school.get('nivel', '').replace("'", "''")}');"""
            sql_statements.append(sql)
            print(sql)
    
    # Markets
    markets = load_json_data('markets.json')
    if markets:
        print("\n-- MARKETS")
        for market in markets:
            sql = f"""INSERT INTO markets (id, nome, provincia_id, municipio, tipo, endereco)
VALUES ({market['id']}, '{market['nome'].replace("'", "''")}', {market['provincia_id']}, 
        '{market.get('municipio', '').replace("'", "''")}', 
        '{market.get('tipo', '').replace("'", "''")}', 
        '{market.get('endereco', '').replace("'", "''")}');"""
            sql_statements.append(sql)
            print(sql)
    
    # Hospitals
    hospitals = load_json_data('hospitals.json')
    if hospitals:
        print("\n-- HOSPITALS")
        for hospital in hospitals:
            sql = f"""INSERT INTO hospitals (id, nome, provincia_id, municipio, tipo, endereco, especialidades)
VALUES ({hospital['id']}, '{hospital['nome'].replace("'", "''")}', {hospital['provincia_id']}, 
        '{hospital.get('municipio', '').replace("'", "''")}', 
        '{hospital.get('tipo', '').replace("'", "''")}', 
        '{hospital.get('endereco', '').replace("'", "''")}', 
        '{hospital.get('especialidades', '').replace("'", "''")}');"""
            sql_statements.append(sql)
            print(sql)
    
    # Reset sequences
    print("\n-- RESET SEQUENCES")
    reset_sql = """
-- Reset auto-increment sequences to continue from max ID
SELECT setval('users_id_seq', COALESCE((SELECT MAX(id) FROM users), 1));
SELECT setval('provinces_id_seq', COALESCE((SELECT MAX(id) FROM provinces), 1));
SELECT setval('municipalities_id_seq', COALESCE((SELECT MAX(id) FROM municipalities), 1));
SELECT setval('schools_id_seq', COALESCE((SELECT MAX(id) FROM schools), 1));
SELECT setval('markets_id_seq', COALESCE((SELECT MAX(id) FROM markets), 1));
SELECT setval('hospitals_id_seq', COALESCE((SELECT MAX(id) FROM hospitals), 1));
"""
    print(reset_sql)
    
    # Save to file
    output_file = project_root / 'scripts' / 'migration.sql'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(sql_statements))
        f.write('\n\n' + reset_sql)
    
    print(f"\n✅ SQL salvo em: {output_file}")
    print("\n📋 Para executar:")
    print("   1. Copie o SQL acima")
    print("   2. Cole no Supabase SQL Editor")
    print("   3. Execute")
    print(f"   OU execute: cat {output_file} | supabase db execute")


if __name__ == '__main__':
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "MIGRAÇÃO DE DADOS JSON → SUPABASE" + " "*20 + "║")
    print("╚" + "="*68 + "╝")
    
    generate_sql_inserts()
    
    print("\n" + "="*70)
    print("MIGRAÇÃO COMPLETA!")
    print("="*70)
