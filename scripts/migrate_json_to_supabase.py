"""
Script to migrate data from JSON files to the Supabase PostgreSQL database.

- Uses SQLAlchemy models (src.database.models).
- Idempotent: re-running does not duplicate data (checks IDs before insert).
- Preserves original IDs, password hashes, roles and created_at of users.
- Validates landfill/province relationships before inserting.
- Resets ID sequences at the end.
"""

import json
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv  # noqa: E402
from sqlalchemy import inspect, text  # noqa: E402

load_dotenv()

from sqlalchemy.orm import Session  # noqa: E402

from src.database import base as db_base  # noqa: E402
from src.database.models import Hospital, Market, Municipality, Province, School, User, UserRole  # noqa: E402

DATA_DIR = project_root / "data"
TABLES = ["users", "provinces", "municipalities", "schools", "markets", "hospitals"]


def load_json_data(filename):
    """Load data from JSON file."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"WARNING: arquivo não encontrado: {filepath}")
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def existing_ids(session, model):
    """Return the set of ids already present in the table."""
    return {row[0] for row in session.query(model.id).all()}


def insert_missing(session, model, records, build_row, label, report):
    """Insert only records whose id is not yet in the database."""
    ids = existing_ids(session, model)
    created = skipped = errors = 0
    for rec in records:
        rid = rec.get("id")
        if rid in ids:
            skipped += 1
            continue
        try:
            session.add(build_row(rec))
            ids.add(rid)
            created += 1
        except Exception as exc:  # noqa: BLE001
            errors += 1
            msg = f"id={rid}: {exc}"
            report.setdefault(label, []).append(msg)
            print(f"    ERRO {label} {msg}")
            session.rollback()
    total = created + skipped + errors
    print(f"  ✓ {label}: total={total} inseridos={created} ignorados={skipped} erros={errors}")
    return created, skipped, errors


def build_user(rec):
    return User(
        id=rec["id"],
        username=rec["username"],
        email=rec["email"],
        password_hash=rec["password_hash"],
        role=UserRole(rec["role"]),
        created_at=rec.get("created_at"),
    )


def build_province(rec):
    return Province(
        id=rec["id"],
        nome=rec["nome"],
        capital=rec.get("capital"),
        area_km2=rec.get("area_km2"),
        populacao=rec.get("populacao"),
    )


def build_municipality(rec):
    return Municipality(
        id=rec["id"],
        nome=rec["nome"],
        provincia_id=rec["provincia_id"],
        area_km2=rec.get("area_km2"),
        populacao=rec.get("populacao"),
    )


def make_builder(model_cls, municipio_key):
    """Build a factory for schools/markets/hospitals, validating the municipality."""

    column_names = set(inspect(model_cls).columns.keys())

    def build(rec):
        municipio_id = rec.get(municipio_key)
        municipio_nome = None
        if municipio_id is not None:
            mun = municipalities_by_id.get(municipio_id)
            if mun is None:
                raise ValueError(f"municipio_id={municipio_id} não existe")
            if rec.get("provincia_id") and mun["provincia_id"] != rec["provincia_id"]:
                print(
                    f"  AVISO: id={rec['id']} '{rec['nome']}' — municipio '{mun['nome']}' "
                    f"é da provincia_id={mun['provincia_id']}, registro diz "
                    f"provincia_id={rec['provincia_id']}"
                )
            municipio_nome = mun["nome"]
        else:
            municipio_nome = rec.get("municipio")
        values = {
            "id": rec["id"],
            "nome": rec["nome"],
            "tipo": rec.get("tipo"),
            "provincia_id": rec["provincia_id"],
            "municipio_id": municipio_id,
            "municipio": municipio_nome,
            "nivel": rec.get("nivel"),
            "endereco": rec.get("endereco"),
            "especialidade": rec.get("especialidade"),
            "categoria": rec.get("categoria"),
            "especialidades": rec.get("especialidades"),
        }
        return model_cls(**{k: v for k, v in values.items() if k in column_names})

    return build


def reset_sequences(session):
    """Reset auto-increment sequences to continue after max(id)."""
    for table in TABLES:
        sql = "SELECT setval(pg_get_serial_sequence(:t, 'id'), " "COALESCE((SELECT MAX(id) FROM %s), 1))" % table
        result = session.execute(text(sql), {"t": table}).scalar()
        print(f"  seq {table}_id_seq -> {result}")


def verify(session):
    """Final verification: counts in DB vs JSON."""
    counts = {
        "users": session.query(User).count(),
        "provinces": session.query(Province).count(),
        "municipalities": session.query(Municipality).count(),
        "schools": session.query(School).count(),
        "markets": session.query(Market).count(),
        "hospitals": session.query(Hospital).count(),
    }
    json_counts = {
        "users": len(load_json_data("users.json")),
        "provinces": len(load_json_data("provinces.json")),
        "municipalities": len(load_json_data("municipalities.json")),
        "schools": len(load_json_data("schools.json")),
        "markets": len(load_json_data("markets.json")),
        "hospitals": len(load_json_data("hospitals.json")),
    }
    print("\nRelatório final (DB vs JSON):")
    ok = True
    for table in TABLES:
        status = "OK" if counts[table] >= json_counts[table] else "MISMATCH"
        if status != "OK":
            ok = False
        print(f"  {table}: {counts[table]} / {json_counts[table]} [{status}]")
    return ok


def main():
    global municipalities_by_id
    print("Iniciando migração JSON -> Supabase...")
    db_base.init_database()
    engine = db_base.engine

    municipalities = load_json_data("municipalities.json")
    municipalities_by_id = {m["id"]: m for m in municipalities}

    with Session(bind=engine) as session:
        report = {}

        insert_missing(
            session,
            Province,
            load_json_data("provinces.json"),
            build_province,
            "provinces",
            report,
        )
        session.commit()

        insert_missing(
            session,
            Municipality,
            municipalities,
            build_municipality,
            "municipalities",
            report,
        )
        session.commit()

        users = load_json_data("users.json")
        users_by_email: dict = {}
        for u in users:
            if u["email"] in users_by_email:
                raise SystemExit(f"ERRO: email duplicado no JSON: {u['email']}")
            users_by_email[u["email"]] = u
        names = [u["username"] for u in users]
        if len(names) != len(set(names)):
            raise SystemExit("ERRO: usernames duplicados no JSON")
        insert_missing(session, User, users, build_user, "users", report)
        session.commit()

        insert_missing(
            session,
            School,
            load_json_data("schools.json"),
            make_builder(School, "municipio_id"),
            "schools",
            report,
        )
        session.commit()

        insert_missing(
            session,
            Market,
            load_json_data("markets.json"),
            make_builder(Market, "municipio_id"),
            "markets",
            report,
        )
        session.commit()

        insert_missing(
            session,
            Hospital,
            load_json_data("hospitals.json"),
            make_builder(Hospital, "municipio_id"),
            "hospitals",
            report,
        )
        session.commit()

        print("\nResetando sequences:")
        reset_sequences(session)

        ok = verify(session)

        if report:
            print("\nErros reportados:")
            for label, errs in report.items():
                for err in errs:
                    print(f"  [{label}] {err}")

        session.commit()
        if not ok:
            print("ATENÇÃO: contagens divergentes!")
            sys.exit(1)
        print("Migração concluída com sucesso.")
    return 0


if __name__ == "__main__":
    main()
