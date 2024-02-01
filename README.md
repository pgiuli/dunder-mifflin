# Gestor de ErP per a l'Empresa Dunder Mifflin

## Estructura
- Gestor de la Base de Dades **DB**.
- Gestor de Preus i verificador de dades.
- Gestor de l'interfície d'usuari **UI**.
- Servidor web WSGI.
- Gestor a temps real per a ajustaments.

## Característiques
- *Flask* com a base de la Webapp.
- Plantilles HTML indexades amb *Flask*.
- CSS uniforme amb *Bootstrap*.
- Base de dades *SQLite3*.


## Funcionalitats
- Base de dades escalable. 0 Modificacions al codi!
- Menús personalitzats per a les diferents classes d'usuaris.
- Comptabilització de capital per transacció.
- Apartat per a estadístiques, totes les transaccions (ítem, usuari i client són enregistrats).

## Instal·lació
1. Descarrega l'última *release* [des-de Github](https://github.com/pgiuli/dunder-mifflin/releases) o clona el repositori.
2. Un cop a la carpeta del gestor:
   1. Instal·la les llibreries necessàries `pip install -r requirements` o `pip3` alternativament.
   2. Modifica/Elimina les dades per defecte (per a usar com a DEMO, ometre aquest pas).
   3. Inicialitza la base de dades (`python3 db.py` o al gestor del projecte `config.py`).
4. Executa main.py per a inciar el servidor en mode Desenvolupament.
5. Accedeix a [http://127.0.0.1:5001](http://127.0.0.1:5001).
