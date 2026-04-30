import geopandas as gpd
import tempfile
import zipfile
import os


def load_file(file):
    name = file.name.lower()

    # ---------------- GEOJSON ----------------
    if name.endswith(".geojson"):
        return gpd.read_file(file)

    # ---------------- KML ----------------
    elif name.endswith(".kml"):
        return gpd.read_file(file, driver="KML")

    # ---------------- SHAPEFILE (ZIP) ----------------
    elif name.endswith(".zip"):
        with tempfile.TemporaryDirectory() as tmp:

            # Save uploaded zip
            zip_path = os.path.join(tmp, "data.zip")
            with open(zip_path, "wb") as f:
                f.write(file.read())

            # Extract zip
            with zipfile.ZipFile(zip_path, 'r') as z:
                z.extractall(tmp)

            # 🔥 Find .shp file inside extracted folder
            shp_file = None
            for root, dirs, files in os.walk(tmp):
                for f in files:
                    if f.lower().endswith(".shp"):
                        shp_file = os.path.join(root, f)
                        break

            if shp_file is None:
                raise Exception("No .shp file found in ZIP")

            # Read shapefile
            return gpd.read_file(shp_file)

    # ---------------- UNSUPPORTED ----------------
    else:
        raise ValueError("Unsupported file format. Use GeoJSON, KML, or zipped Shapefile.")