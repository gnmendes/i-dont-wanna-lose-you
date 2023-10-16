from download import YoutubeDLClientBuilder
from logger_utils import LoggerFactory
from content_repository import ContentRepository, Content

class ContentService(object):
    
    def __init__(self):
        self.__LOGGER = LoggerFactory.get_logger(__name__)
        self.__repository =  ContentRepository()
    
    async def download_content(self, body):
        contents = []
        for data in body:
            try:
                folder_name = data.get("folder")
                download_client = YoutubeDLClientBuilder(folder_name) \
                                            .no_overwrites(True) \
                                            .ignore_errors(True) \
                                            .no_warnings(True) \
                                            .build()
                                                        
                location, info = await download_client.download(url=data.get('url'))
                
                content = Content(
                    name=info.get("title"),
                    category=",".join(info.get("categories") or []),
                    description=info.get("description"),
                    duration=info.get("duration"),
                    format=info.get("ext"),
                    stored_at=location,
                    local_y_n=self.__islocal(location)
                )
                
                contents.append(content)

                self.__LOGGER.debug("Download de {} itens concluido!".format(info.get("title")))       
            except Exception as error:
                self.__LOGGER.debug(str(error))
                self.__LOGGER.debug(
                    'Não foi possivel efetuar o download da url %s.' % data.get("url")
                )
        await self._save(contents)        
        
        
    async def _save(self, contents):
        await self.__repository.save(contents)
                
    def __islocal(self, location: str):
        import re
        if re.search("^([a-zA-Z]){1}(:\/\/)", location):
            return "Y"
        return "N"