from idontwannaloseyou.controller import app, Verbs
from idontwannaloseyou.download import Download
from idontwannaloseyou.megawrapper import MegaWrapper
from idontwannaloseyou.logger_utils import LoggerFactory
from flask import request, jsonify
import json
import os

RESOURCE_NAME = '/video'
LOGGER = LoggerFactory.get_logger(__name__)
MEGA = None


def build_response_object(data):
    return {
        'original_url': data.get('url'),
        'person_folder': data.get('folder')
    }


def save_in_cloud(file_location, folder_name, mega_client):
    if not os.path.isfile(file_location):
        LOGGER.debug(
            'Caminho especificado não remete a um arquivo!'
            ' Por favor verificar novamente o seguinte caminho: %s' % file_location
        )
    else:
        if not mega_client:
            mega_client = MegaWrapper(email=os.getenv('EMAIL'), password=os.getenv('PASSWORD'))
        mega_client.upload(file_location, folder_name)


@app.route(RESOURCE_NAME, methods=[str(Verbs.POST)])
def download_and_store():
    if body := json.loads(request.get_data()):
        if not isinstance(body, list):
            body = [body]

        response = []
        for data in body:
            response_data = build_response_object(data)
            try:
                download_client = Download()
                metadata = download_client.download(url=data.get('url'))
                response_data['metadata'] = metadata
                folder_name = data.get("folder")
                save_in_cloud(file_location=metadata.get('file_location'),
                              folder_name=folder_name,
                              mega_client=MEGA)
                response_data['cloud_filepath'] = folder_name
            except Exception as error:
                LOGGER.debug(str(error))
                LOGGER.debug(
                    'Não foi possivel efetuar o download da url %s.' % data.get("url")
                )
                response_data['downloaded'] = False
            finally:
                response.append(response_data)

        return jsonify(response), 200
    return jsonify({'erro': 'Payload submetido é inválido'}), 400


@app.route(RESOURCE_NAME + '/previously-downloaded', methods=[str(Verbs.POST)])
def store_previously_download_video():
    if payload := json.loads(request.get_data()):
        path = payload.get('path')
        # TODO: ter uma validacao em que ele verifica se existe mais de um nível na string (/), do contrário retorna
        #  uma pasta base

        folder_name = payload.get('folder')
        save_in_cloud(file_location=path, folder_name=folder_name,
                      mega_client=MEGA)
        LOGGER.debug(
            'Upload do arquivo presente no caminho %s iniciado!' % path
        )
        return jsonify(
            {
                "message": "Upload do arquivo presente no caminho %s finalizado!" % path,
                "cloud_path": folder_name
            }
        ), 200
    return 'Payload não submetido', 400
