from logger_utils import LoggerFactory
from mega import Mega

LOGGER = LoggerFactory.get_logger(__name__)


class MegaWrapper:

    def __init__(self, email=None, password=None):
        self._mega_client = Mega({'verbose': True})
        self._logged_usr = None
        self._logged_usr = self._login(
            email=email,
            password=password
        )

    def _login(self, email, password) -> Mega:
        return self._mega_client.login(email=email, password=password)

    def create_folder(self, folder_name, root_folder=None):
        if root_folder:
            folder = self._logged_usr.create_folder(folder_name, root_folder)
            LOGGER.debug(f'pasta criada {folder} (subpasta de {root_folder})')
        else:
            folder = self._logged_usr.create_folder(folder_name)
            LOGGER.debug(f'pasta criada {folder}')
        return folder

    def _folder_exists(self, folder_name):
        count = 0
        last_folder = None
        for node in folder_name.split('/'):
            folder = self._logged_usr.find(node, exclude_deleted=True)
            if not folder and count == 0:
                return False
            elif folder:
                count += 1
                last_folder = folder
            elif not folder:
                return {'lastLevelFounded': last_folder}
        return last_folder

    def upload(self, file_path, folder_name):
        if folder := self._folder_exists(folder_name=folder_name):
            try:
                folder_id = folder.get('lastLevelFounded')[0]
            except:
                folder_id = folder[0]
            else:
                actual_name = folder_name.split('/')[-1]
                folder_created = self.create_folder(actual_name, folder_id)
                key, value = [*folder_created.items()][0]
                folder_id = value
        else:
            folder_id = None
            for curr_folder in folder_name.split('/'):
                folder = self.create_folder(folder_name=curr_folder, root_folder=folder_id)
                folder_id = folder.get(curr_folder)
        self._mega_client.upload(filename=file_path, dest=folder_id)
