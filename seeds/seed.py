from app import SessionLocal
from app import Category
from app import Store
from app import Product

def run():
    db = SessionLocal()
    try:
        # Categorías
        tecnologia = Category(name="Tecnología", slug="tecnologia")
        ropa       = Category(name="Ropa",       slug="ropa")
        db.add_all([tecnologia, ropa])
        db.flush()  # obtener IDs sin hacer commit

        db.add(Category(name="Portátiles",  slug="portatiles",  parent_id=tecnologia.id))
        db.add(Category(name="Smartphones", slug="smartphones",  parent_id=tecnologia.id))

        # Tiendas
        amazon = Store(name="Amazon ES",     base_url="https://www.amazon.es",       currency="EUR")
        pcc    = Store(name="PCComponentes", base_url="https://www.pccomponentes.com",currency="EUR")
        db.add_all([amazon, pcc])

        db.commit()
        print("✅ Seed completado")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run()