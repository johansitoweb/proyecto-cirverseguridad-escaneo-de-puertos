import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def detect_anomalies(data_path, contamination=0.1):
    # Cargar datos de tráfico de red
    try:
        data = pd.read_csv(data_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo {data_path} no se encontró.")
    except pd.errors.EmptyDataError:
        raise ValueError("El archivo está vacío.")
    except Exception as e:
        raise Exception(f"Ocurrió un error al cargar el archivo: {e}")

    # Verificar si las características necesarias están en el DataFrame
    required_features = ['feature1', 'feature2']  # Reemplaza con tus características
    for feature in required_features:
        if feature not in data.columns:
            raise ValueError(f"Falta la característica requerida: {feature}")

    # Seleccionar características
    X = data[required_features]

    # Escalar las características
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Dividir los datos
    X_train, X_test = train_test_split(X_scaled, test_size=0.2, random_state=42)

    # Entrenar el modelo
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(X_train)

    # Predecir anomalías
    predictions = model.predict(X_test)
    anomalies = X_test[predictions == -1]

    # Devolver las anomalías en un DataFrame original
    anomalies_df = pd.DataFrame(scaler.inverse_transform(anomalies), columns=required_features)

    # Visualizar resultados
    visualize_anomalies(X, anomalies_df)

    # Guardar anomalías en un archivo CSV
    anomalies_df.to_csv('anomalies_detected.csv', index=False)
    print(f"Anomalías guardadas en 'anomalies_detected.csv'.")

    return anomalies_df

def visualize_anomalies(original_data, anomalies):
    plt.figure(figsize=(10, 6))
    plt.scatter(original_data['feature1'], original_data['feature2'], label='Datos Normales', color='blue', alpha=0.5)
    plt.scatter(anomalies['feature1'], anomalies['feature2'], label='Anomalías', color='red', marker='x')
    plt.title('Detección de Anomalías')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Ruta al archivo CSV
    data_path = '../data/network_traffic.csv'  # Cambia esto a la ruta de tu archivo
    contamination_level = 0.1  # Ajusta este valor según sea necesario

    anomalies = detect_anomalies(data_path, contamination=contamination_level)
    print("Anomalías detectadas:")
    print(anomalies)