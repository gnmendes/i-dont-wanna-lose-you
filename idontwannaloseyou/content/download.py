import yt_dlp as youtube_dl
from logger_utils import LoggerFactory
import copy


class _Download(object):
        
    def __init__(self, builder):
        self._ytdl_opts = YtdlOptions(builder)
        self.__LOGGER = LoggerFactory.get_logger(__name__)

    async def download(self, url):
        video_info = await self.__get_video_information(url)

        file_name = self.__get_file_name(video_info)

        self._ytdl_opts.set_file_name(file_name)
        
        self.__LOGGER.debug("A midia será armazenado em {}".format(self._ytdl_opts.outtmpl))
        options = copy.deepcopy(self._ytdl_opts.__dict__)
        with youtube_dl.YoutubeDL(options) as ytdl:
            ytdl.download([url])

        return self._ytdl_opts.outtmpl, self._remove_extra_information(video_info)

    async def __get_video_information(self, url):
        with youtube_dl.YoutubeDL({}) as ytdl:
            return ytdl.extract_info(url, download=False)

    def __get_file_name(self, info) -> str:
        title = info.get('title')
        formats = info.get('formats') or info.get('entries')[0]['formats']
        extension = formats[-1]['ext']
        return '%s.%s' % (title, extension)

    def _remove_extra_information(self, video_info):
        if video_info.get('formats'):
            del video_info['formats']
            return video_info

        del video_info['entries']
        return video_info


class YoutubeDLClientBuilder(object):
    __DATA = {}
    def __init__(self, output_location):
        self.__DATA['output_location'] = output_location
        
    def format(self, fmt):
        self.__DATA['format'] = fmt
        return self
    
    def no_warnings(self, warnings):
        self.__DATA['no_warnings'] = warnings
        return self
    
    def no_overwrites(self, overwrites):
        self.__DATA['no_overwrites'] = overwrites
        return self
    
    def ignore_errors(self, ignore_errors):
        self.__DATA['ignore_errors'] = ignore_errors
        return self
    
    def build(self) -> _Download:
        return _Download(self.__DATA)

class YtdlOptions():
    def __init__(self, builder):
        self.format = builder.get('format', "bestvideo+bestaudio/best")
        self.nooverwrites = builder.get('no_overwrites')
        self.no_warnings = builder.get('no_warnings')
        self.ignoreerroes = builder.get('ignore_errors')
        self.outtmpl: str = builder.get('output_location')


    def set_file_name(self, file_name: str):
        assert(file_name is not None)
        
        if not self.outtmpl.endswith("/"):
            self.outtmpl += "/"
        
        self.outtmpl += file_name
