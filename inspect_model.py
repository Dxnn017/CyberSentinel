import pickle
import sys
import joblib

# Intentar cargar el modelo de diferentes formas
model = None
try:
    # Método 1: pickle estándar
    with open('mejor_modelo.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Modelo cargado con pickle")
except Exception as e:
    print(f"✗ Error con pickle: {e}")
    try:
        # Método 2: joblib
        model = joblib.load('mejor_modelo.pkl')
        print("✓ Modelo cargado con joblib")
    except Exception as e2:
        print(f"✗ Error con joblib: {e2}")
        sys.exit(1)

if model is None:
    print("No se pudo cargar el modelo")
    sys.exit(1)

print("=" * 60)
print("INFORMACIÓN DEL MODELO")
print("=" * 60)
print(f"\nTipo de modelo: {type(model)}")
print(f"\nClase del modelo: {model.__class__.__name__}")

# Intentar obtener información sobre las características
if hasattr(model, 'feature_names_in_'):
    print(f"\nNúmero de características: {len(model.feature_names_in_)}")
    print(f"\nNombres de las características:")
    for i, feature in enumerate(model.feature_names_in_, 1):
        print(f"  {i}. {feature}")
elif hasattr(model, 'n_features_in_'):
    print(f"\nNúmero de características: {model.n_features_in_}")
    print("  (El modelo no tiene nombres de características guardados)")
else:
    print("\nNo se pudo determinar el número de características directamente")

# Información adicional del modelo
if hasattr(model, 'get_params'):
    print(f"\nParámetros del modelo:")
    params = model.get_params()
    for key, value in list(params.items())[:10]:  # Primeros 10 parámetros
        print(f"  - {key}: {value}")
    if len(params) > 10:
        print(f"  ... y {len(params) - 10} parámetros más")

# Si es un modelo de clasificación
if hasattr(model, 'classes_'):
    print(f"\nClases del modelo: {model.classes_}")

print("\n" + "=" * 60)
