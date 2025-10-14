from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from settings import DATABASE_URL
from models import Game
from logger import LOGGER

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def init_db():
    import models

    # importujemy modele, żeby Base je zarejestrowało
    try:
        models.Base.metadata.create_all(bind=engine)
        load_data()
    except:
        LOGGER.error(
            "Database did not manage to connect. Endpoints besides liveness will not work"
        )


def check_database():
    try:
        session = SessionLocal()
        session.execute("SELECT 1")
        return True
    except Exception:
        return False


def load_data():
    session = SessionLocal()
    if session.query(Game).count() == 0:
        session.execute(
            text(
                """
        INSERT INTO games (title, players, playtime, short_description, description, image_url) VALUES
        ('Catan', '3-4', 90, 'Klasyczna gra o osadnictwie.', 'Gracze rywalizują o zasoby i rozwój osad na wyspie Catan.', 'https://upload.wikimedia.org/wikipedia/en/thumb/a/a3/Catan-2015-boxart.jpg/250px-Catan-2015-boxart.jpg'),
        ('Carcassonne', '2-5', 45, 'Gra kafelkowa.', 'Gracze budują średniowieczny krajobraz z kafelków, zdobywając punkty.', 'https://cdn.svc.asmodee.net/production-zman/uploads/image-converter/2024/08/ZM7810_box-right.webp'),
        ('Ticket to Ride', '2-5', 60, 'Gra o budowaniu tras kolejowych.', 'Celem jest ukończenie połączeń kolejowych między miastami i zdobycie punktów.', 'https://files.rebel.pl/products/100/606/_4576/ttr-1200x900-ffffff-jpg.webp'),
        ('Terraforming Mars', '1-5', 120, 'Gra o terraformowaniu Marsa.', 'Gracze rozwijają technologie, tworzą miasta i roślinność na Marsie.', 'https://files.rebel.pl/products/108/5438/_99856/box_3d_TerraformacjaMarsa_podstawka.jpg'),
        ('Splendor', '2-4', 30, 'Gra strategiczna o handlu klejnotami.', 'Gracze kupują karty i rozwijają swoje kolekcje klejnotów, zdobywając punkty.', 'https://files.rebel.pl/products/100/606/_2022998/rebel-gra-ekonomiczna-splendor-2024-box3d-1200x900-ffffff-png.webp');
        """
            )
        )
        session.commit()
        session.close()
        LOGGER.error("Preloaded database")
