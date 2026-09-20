# Proyecto Clima — Laboratorio N3

Aplicación en Python que consulta el clima actual de varias ciudades de Panamá
usando la API pública de Open-Meteo y guarda cada consulta en una base de datos
SQLite local.

**Autor:** Bredy Guerra
**Diplomado de Programación en Python — Universidad Politécnica Internacional (UPI Panamá)**

## Estructura del proyecto

```
proyecto_clima/
├── src/
│   ├── api_client.py      # Consulta a la API y programa principal
│   └── db_manager.py      # CRUD sobre SQLite
├── data/                  # Aquí se crea clima.db (no se versiona)
├── tests/
│   └── test_db_manager.py # Pruebas del CRUD
├── .env.example           # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

## Instalación

1. Clonar el repositorio y entrar a la carpeta:

```bash
git clone https://github.com/0bredy/proyecto_clima.git
cd proyecto_clima
```

2. Crear y activar el entorno virtual:

```bash
python -m venv venv
```

- Windows (PowerShell): `venv\Scripts\Activate.ps1`
- Windows (CMD): `venv\Scripts\activate.bat`
- Linux / macOS: `source venv/bin/activate`

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` a partir de la plantilla:

- Windows: `copy .env.example .env`
- Linux / macOS: `cp .env.example .env`

## Uso

```bash
python src/api_client.py
```

El programa pide una ciudad, consulta el clima, guarda el reporte en
`data/clima.db` y muestra el historial completo.

Ciudades disponibles: david, panama, santiago, chitre, colon.

Para probar solo las operaciones CRUD con datos de ejemplo:

```bash
python src/db_manager.py
```

## Pruebas

```bash
python -m unittest discover tests
```

Las pruebas corren contra una base de datos temporal, así que no modifican
`data/clima.db`.

## Variables de entorno

| Variable             | Descripción                        | Valor por defecto                          |
|----------------------|------------------------------------|--------------------------------------------|
| `URL_API`            | Endpoint de la API de clima        | `https://api.open-meteo.com/v1/forecast`   |
| `CIUDAD_POR_DEFECTO` | Ciudad usada si no se escribe nada | `panama`                                   |
| `NOMBRE_BD`          | Nombre del archivo SQLite          | `clima.db`                                 |

## Dependencias

- `requests` — llamadas HTTP a la API
- `python-dotenv` — carga de variables desde `.env`
