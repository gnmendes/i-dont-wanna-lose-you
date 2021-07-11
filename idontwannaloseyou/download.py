import youtube_dl
import os

TMP_DIR = 'tmp'


class Download(object):

    @staticmethod
    def __get_video_information(url):
        with youtube_dl.YoutubeDL({}) as ytdl:
            return ytdl.extract_info(url, download=False)

    @staticmethod
    def __get_file_location(info):
        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)
        title = info.get('title')
        formats = info.get('formats') or info.get('entries')[0]['formats']
        extension = formats[-1]['ext']
        filename = '%s.%s' % (title, extension)
        return os.path.join(TMP_DIR, filename)

    def download(self, url):
        video_info = self.__get_video_information(url=url)

        output_location = self.__get_file_location(info=video_info)
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_location,
            'nooverwrites': True,
            'no_warnings': False,
            'ignoreerrors': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ytdl:
            ytdl.download([url])

        return {'file_location': output_location,
                'video_information': self._remove_extra_information(video_info)}

    @staticmethod
    def _remove_extra_information(video_info):
        if video_info.get('formats'):
            del video_info['formats']
        else:
            del video_info['entries']
        return video_info
