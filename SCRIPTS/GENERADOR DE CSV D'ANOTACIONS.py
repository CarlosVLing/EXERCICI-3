#GENERADOR DE CSV D'EVALUACIÓ DES DEL JSON
import json
import pandas as pd

def extract_text(val):
    """
    Extract text and make it a string
    """
    t = val.get("text", "")
    if isinstance(t, list):
        return " ".join(t).strip()
    return str(t).strip()

# Ruta JSON
json_path = "project-8-at-2025-03-18-19-01-665d62c3.json"

# Carregar JSON
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Llista final per emmagatzemar les fileres
rows = []

# Processar anotacions
for entry in data:
    for annotation in entry["annotations"]:
        results = annotation["result"]
        group = None  # diccionari pel grup actual
        for item in results:
            from_name = item.get("from_name", "")
            value = item.get("value", {})
            # Si es un error, iniciem nou grup
            if from_name == "errors_auto":
                # Si el grupo anterior estava en curs, processar-lo abans de reiniciar
                if group is not None:
                    # Processem el grup: si existix almenys una correcció manual, la usem; sinó, la selecció
                    if group["manual_corrections"]:
                        chosen_corr = group["manual_corrections"][-1]
                        method = "Escriure manualment"
                    elif group["selection_corrections"]:
                        chosen_corr = group["selection_corrections"][-1]
                        method = "Seleccionar del original"
                    else:
                        chosen_corr = ""
                        method = ""
                    # Sols afegim el grup si l'error no està marcat como Exempt
                    if "Exempt" not in group["error_labels"]:
                        rows.append({
                            "Error": group["error_text"],
                            "Tipo de Error": group["error_type"],
                            "Corrección": chosen_corr,
                            "Método de Corrección": method
                        })
                # Iniciar un nou grupo
                group = {
                    "error_text": extract_text(value),
                    "error_labels": value.get("labels", []),
                    "error_type": "",
                    "manual_corrections": [],
                    "selection_corrections": []
                }
            # Si l'element és del tipus error i estem en un grup
            elif group is not None and from_name == "error_type_auto":
                # Extraure tipus, pot vindre de "labels" o "choices"
                if "labels" in value and value["labels"]:
                    group["error_type"] = value["labels"][0]
                elif "choices" in value and value["choices"]:
                    group["error_type"] = value["choices"][0]
            # Si és correcció i estem en grup
            elif group is not None and from_name in ["manual_correction_auto", "selected_correction", "correct_version_auto"]:
                corr_text = extract_text(value)
                if from_name == "manual_correction_auto":
                    group["manual_corrections"].append(corr_text)
                else:
                    group["selection_corrections"].append(corr_text)
        # En finalitzar el grup de results, processem el grup si existeix
        if group is not None:
            if group["manual_corrections"]:
                chosen_corr = group["manual_corrections"][-1]
                method = "Escriure manualment"
            elif group["selection_corrections"]:
                chosen_corr = group["selection_corrections"][-1]
                method = "Seleccionar del original"
            else:
                chosen_corr = ""
                method = ""
            if "Exempt" not in group["error_labels"]:
                rows.append({
                    "Error": group["error_text"],
                    "Tipo de Error": group["error_type"],
                    "Corrección": chosen_corr,
                    "Método de Corrección": method
                })

# Convertir a DataFrame i guardar en CSV
df = pd.DataFrame(rows)
output_csv = "errors_corrections.csv"
df.to_csv(output_csv, index=False)
print(f"Archivo de errores y correcciones guardado en {output_csv}")