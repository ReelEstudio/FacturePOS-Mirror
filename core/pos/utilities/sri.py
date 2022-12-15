import requests


def search_ruc_in_sri(ruc):
    response = {'error': 'El número de ruc es inválido'}
    url = f'https://srienlinea.sri.gob.ec/movil-servicios/api/v1.0/estadoTributario/{ruc}'
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        response = r.json()
    else:
        response['error'] = r.json()['mensaje']
    return response
