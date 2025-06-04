import os
import hashlib
from PIL import Image
import imagehash
import filetype

def get_file_hash(path):
    """Gibt einen MD5-Hash der Datei zurück (exakter Vergleich)"""
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def is_image(path):
    kind = filetype.guess(path)
    return kind is not None and kind.mime.startswith("image")

def is_video(path):
    kind = filetype.guess(path)
    return kind is not None and kind.mime.startswith("video")

def is_text(path):
    return path.lower().endswith(('.txt', '.md', '.csv'))

def is_pdf(path):
    return path.lower().endswith('.pdf')

def get_image_similarity_hash(path):
    """Erzeugt einen Bild-Hash zur Ähnlichkeitsprüfung"""
    try:
        img = Image.open(path).convert("RGB")
        return imagehash.average_hash(img)
    except:
        return None

def find_duplicates_and_similars(folder):
    """Durchsucht rekursiv einen Ordner und findet Duplikate & Ähnlichkeiten"""
    seen_hashes = {}
    results = []

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, folder)
            try:
                file_hash = get_file_hash(path)
                status = "Einzigartig"

                if file_hash in seen_hashes:
                    status = "Duplikat"
                else:
                    seen_hashes[file_hash] = path

                # Nur bei Bildern: ähnlicher Vergleich
                if is_image(path):
                    img_hash = get_image_similarity_hash(path)
                    if img_hash:
                        for other_path in seen_hashes.values():
                            if is_image(other_path):
                                other_img_hash = get_image_similarity_hash(other_path)
                                if other_img_hash and img_hash - other_img_hash <= 5:
                                    status = "Ähnlich"

                results.append({
                    "path": path,
                    "rel_path": rel_path,
                    "status": status
                })

            except Exception as e:
                results.append({
                    "path": path,
                    "rel_path": rel_path,
                    "status": f"Fehler: {e}"
                })

    return results

