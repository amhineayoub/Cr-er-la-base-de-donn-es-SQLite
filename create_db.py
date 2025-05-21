import sqlite3

conn = sqlite3.connect("hotel.db")
cur = conn.cursor()

# Supprimer les tables si elles existent déjà
cur.executescript("""
DROP TABLE IF EXISTS Evaluation;
DROP TABLE IF EXISTS Reservation;
DROP TABLE IF EXISTS Chambre;
DROP TABLE IF EXISTS Type_Chambre;
DROP TABLE IF EXISTS Prestation;
DROP TABLE IF EXISTS Client;
DROP TABLE IF EXISTS Hotel;
""")

# Créer les tables
cur.executescript("""
CREATE TABLE Hotel (
    id_hotel INTEGER PRIMARY KEY,
    ville TEXT,
    pays TEXT,
    code_postal INTEGER
);

CREATE TABLE Client (
    id_client INTEGER PRIMARY KEY,
    adresse TEXT,
    ville TEXT,
    code_postal INTEGER,
    email TEXT,
    telephone TEXT,
    nom_complet TEXT
);

CREATE TABLE Prestation (
    id_prestation INTEGER PRIMARY KEY,
    prix NUMERIC,
    description TEXT
);

CREATE TABLE Type_Chambre (
    id_type INTEGER PRIMARY KEY,
    type TEXT,
    tarif NUMERIC
);

CREATE TABLE Chambre (
    id_chambre INTEGER PRIMARY KEY,
    etage INTEGER,
    numero INTEGER,
    id_type INTEGER,
    id_hotel INTEGER,
    FOREIGN KEY (id_type) REFERENCES Type_Chambre(id_type),
    FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel)
);

CREATE TABLE Reservation (
    id_reservation INTEGER PRIMARY KEY,
    date_arrivee DATE,
    date_depart DATE,
    id_client INTEGER,
    id_chambre INTEGER,
    FOREIGN KEY (id_client) REFERENCES Client(id_client),
    FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre)
);

CREATE TABLE Evaluation (
    id_evaluation INTEGER PRIMARY KEY,
    date_arrivee DATE,
    note NUMERIC,
    texte TEXT,
    id_client INTEGER,
    FOREIGN KEY (id_client) REFERENCES Client(id_client)
);
""")

# Insérer les données (selon l’annexe)
cur.executemany("INSERT INTO Hotel VALUES (?, ?, ?, ?)", [
    (1, 'Paris', 'France', 75001),
    (2, 'Lyon', 'France', 69002)
])

cur.executemany("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)", [
    (1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
    (2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
    (3, '8 Boulevard Saint-Michel', 'Marseille', 13085, 'paul.nouveau@email.fr', '0634567890', 'Paul Moreau'),
    (4, '27 Rue Nationale', 'Lille', 59000, 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
    (5, '18 Rue des Fleurs', 'Nice', 06000, 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
])

cur.executemany("INSERT INTO Prestation VALUES (?, ?, ?)", [
    (1, 15, 'Petit-déjeuner'),
    (2, 30, 'Navette aéroport'),
    (3, 0, 'Wi-Fi gratuit'),
    (4, 50, 'Spa et bien-être'),
    (5, 20, 'Parking sécurisé')
])

cur.executemany("INSERT INTO Type_Chambre VALUES (?, ?, ?)", [
    (1, 'Simple', 80),
    (2, 'Double', 120)
])

cur.executemany("INSERT INTO Chambre VALUES (?, ?, ?, ?, ?)", [
    (1, 2, 101, 1, 1),
    (2, 5, 201, 1, 1),
    (3, 6, 301, 2, 1),
    (4, 4, 108, 2, 2),
    (5, 3, 102, 1, 2),
    (6, 7, 307, 1, 1),
    (7, 3, 201, 2, 1),
    (8, 1, 101, 1, 2)
])

cur.executemany("INSERT INTO Reservation VALUES (?, ?, ?, ?, ?)", [
    (1, '2025-06-15', '2025-06-18', 1, 1),
    (2, '2025-07-01', '2025-07-05', 2, 2),
    (3, '2025-08-10', '2025-08-14', 3, 3),
    (4, '2025-09-05', '2025-09-07', 4, 4),
    (5, '2025-09-20', '2025-09-25', 5, 5),
    (6, '2025-11-12', '2025-11-14', 2, 6),
    (7, '2026-02-01', '2026-02-05', 2, 7),
    (8, '2026-01-15', '2026-01-18', 4, 8)
])

cur.executemany("INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)", [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
])

conn.commit()
conn.close()
