from pathlib import Path
import requests


class download_manager():
    def __init__(self):
        pass

    def download_file(self,
                      url,
                      file_name,
                      folder_name='data_to_parse',
                      format='csv'):
        '''

        :param url: set a url to download from
        :param file_name: file name
        :param folder_name: set a name to folder
        :param format: set a format to download
        :return:
        '''
        out_dir = Path(folder_name)
        out_dir.mkdir(parents=True, exist_ok=True)

        resp = requests.get(url, timeout=30)
        resp.raise_for_status()

        (out_dir / f"{file_name}.{format}").write_bytes(resp.content)
