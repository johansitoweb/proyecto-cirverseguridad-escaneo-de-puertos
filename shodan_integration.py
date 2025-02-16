import shodan
import json
import argparse

def get_shodan_info(api_key, target_ip, save_to_file=False):
    api = shodan.Shodan(api_key)
    try:
        ip_info = api.host(target_ip)
        print(f"Información de {target_ip}:")
        print(f"Organización: {ip_info.get('org', 'N/A')}")
        print(f"Ubicación: {ip_info.get('city', 'N/A')}, {ip_info.get('country_name', 'N/A')}")
        print(f"ISP: {ip_info.get('isp', 'N/A')}")
        print(f"Puerto(s) Abierto(s): {[service['port'] for service in ip_info['data']]}")
        
        # Mostrar información de servicios
        for service in ip_info['data']:
            print(f"\nServicio en el puerto {service['port']}:")
            print(f"  - Protocolo: {service['transport']}")
            print(f"  - Nombre: {service.get('product', 'N/A')}")
            print(f"  - Versión: {service.get('version', 'N/A')}")
            print(f"  - Banner: {service.get('data', 'N/A')}")

        # Guardar resultados en un archivo JSON
        if save_to_file:
            with open(f"{target_ip}_info.json", 'w') as json_file:
                json.dump(ip_info, json_file, indent=4)
            print(f"Información guardada en {target_ip}_info.json")

    except shodan.APIError as e:
        print(f"Error de API: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Obtener información de Shodan para una IP específica.')
    parser.add_argument('api_key', type=str, help='Tu API Key de Shodan.')
    parser.add_argument('target_ip', type=str, help='La IP objetivo para escanear.')
    parser.add_argument('--save', action='store_true', help='Guardar la información en un archivo JSON.')

    args = parser.parse_args()

    get_shodan_info(args.api_key, args.target_ip, save_to_file=args.save)