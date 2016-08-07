#!/usr/bin/env python2
# vim: set fileencoding=utf8

# windows 用户，需要安装下面的东西
# mutagen -- https://bitbucket.org/lazka/mutagen/downloads
#            https://bitbucket.org/lazka/mutagen/downloads/mutagen-1.22.tar.gz
# wget -- http://users.ugent.be/~bpuype/cgi-bin/fetch.pl?dl=wget/wget.exe 到C:\windows\system32

import re, sys, os, random, time, json, urllib2, logging, argparse
from mutagen.id3 import ID3,TRCK,TIT2,TALB,TPE1,APIC,TDRC,COMM,TPOS,USLT
from HTMLParser import HTMLParser
parser = HTMLParser()
# s = u'\x1b[1;%dm%s\x1b[0m'       # terminual color template


email = 'lyf021408@gmail.com'     # vip账号支持高品质音乐下载
password = 'lyf021408xiami'


#############################################################
# Xiami api for android
#{{{
# url_action_fav = "http://www.xiami.com/app/android/fav?id=%s&type=%s"
# url_action_unfav = "http://www.xiami.com/app/android/unfav?id=%s&type=%s"
# url_album = "http://www.xiami.com/app/android/album?id=%s&uid=%s"
# url_song = "http://www.xiami.com/app/android/song?id=%s&uid=%s"
# url_artist = "http://www.xiami.com/app/android/artist?id=%s"
# url_artist_albums = "http://www.xiami.com/app/android/artist-albums?id=%s&page=%s"
# url_artist_radio = "http://www.xiami.com/app/android/radio-artist?id=%s"
# url_artist_top_song = "http://www.xiami.com/app/android/artist-topsongs?id=%s"
# url_artsit_similars = "http://www.xiami.com/app/android/artist-similar?id=%s"
# url_collect = "http://www.xiami.com/app/android/collect?id=%s&uid=%s"
# url_grade = "http://www.xiami.com/app/android/grade?id=%s&grade=%s"
# url_lib_albums = "http://www.xiami.com/app/android/lib-albums?uid=%s&page=%s"
# url_lib_artists = "http://www.xiami.com/app/android/lib-artists?uid=%s&page=%s"
# url_lib_collects = "http://www.xiami.com/app/android/lib-collects?uid=%s&page=%s"
# url_lib_songs = "http://www.xiami.com/app/android/lib-songs?uid=%s&page=%s"
# url_myplaylist = "http://www.xiami.com/app/android/myplaylist?uid=%s"
# url_myradiosongs = "http://www.xiami.com/app/android/lib-rnd?uid=%s"
# url_playlog = "http://www.xiami.com/app/android/playlog?id=%s&uid=%s"
# url_push_songs = "http://www.xiami.com/app/android/push-songs?uid=%s&deviceid=%s"
# url_radio = "http://www.xiami.com/app/android/radio?id=%s&uid=%s"
# url_radio_categories = "http://www.xiami.com/app/android/radio-category"
# url_radio_similar = "http://www.xiami.com/app/android/radio-similar?id=%s&uid=%s"
# url_rndsongs = "http://www.xiami.com/app/android/rnd?uid=%s"
# url_search_all = "http://www.xiami.com/app/android/searchv1?key=%s"
# url_search_parts = "http://www.xiami.com/app/android/search-part?key=%s&type=%s&page=%s"
#}}}
#############################################################

############################################################
# Xiami api for android
# {{{
url_song = "http://www.xiami.com/app/android/song?id=%s"
url_album = "http://www.xiami.com/app/android/album?id=%s"
url_collect = "http://www.xiami.com/app/android/collect?id=%s"
url_artist_albums = "http://www.xiami.com/app/android/artist-albums?id=%s&page=%s"
url_artist_top_song = "http://www.xiami.com/app/android/artist-topsongs?id=%s"
url_lib_songs = "http://www.xiami.com/app/android/lib-songs?uid=%s&page=%s"
# }}}
############################################################

############################################################
# wget exit status
wget_es = {
    0:"No problems occurred.",
    2:"User interference.",
    1<<8:"Generic error code.",
    2<<8:"Parse error - for instance, when parsing command-line optio.wgetrc or .netrc...",
    3<<8:"File I/O error.",
    4<<8:"Network failure.",
    5<<8:"SSL verification failure.",
    6<<8:"Username/password authentication failure.",
    7<<8:"Protocol errors.",
    8<<8:"Server issued an error response."
}
############################################################

############################################################
# Regular Expression Templates
re_disc_description = r'disc (\d+) \[(.+?)\]</'
############################################################

def decry(row, encryed_url):
    url = encryed_url
    urllen = len(url)
    rows = int(row)

    cols_base = urllen / rows  # basic column count
    rows_ex = urllen % rows    # count of rows that have 1 more column

    matrix = []
    for r in xrange(rows):
        length = cols_base + 1 if r < rows_ex else cols_base
        matrix.append(url[:length])
        url = url[length:]

    url = ''
    for i in xrange(urllen):
        url += matrix[i % rows][i / rows]

    return urllib.unquote(url).replace('^', '0')

def modificate_text(text):
    text = parser.unescape(text)
    text = re.sub(r'//*', '-', text)
    text = text.replace('/', '-')
    text = text.replace('\\', '-')
    text = re.sub(r'\s\s+', ' ', text)
    return text

def modificate_file_name_for_wget(file_name):
    file_name = re.sub(r'\s*:\s*', u' - ', file_name)    # for FAT file system
    file_name = file_name.replace('?', '')      # for FAT file system
    file_name = file_name.replace('"', '\'')    # for FAT file system
    return file_name

def z_index(song_infos):
    size = len(song_infos)
    if size <= 9:
        return 1
    elif size >= 10 and size <= 99:
        return 2
    elif size >= 100 and size <= 999:
        return 3
    else:
        return 1

#############################################################
# from https://gist.github.com/lepture/1014329
#############################################################
# {{{
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, lepture.com
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#    * Neither the name of the author nor the names of its contributors
#      may be used to endorse or promote products derived from this
#      software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urllib
import httplib
from contextlib import closing
from Cookie import SimpleCookie

ua = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36'
#ua = 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'

checkin_headers = {
    'User-Agent': ua,
    'Content-Length': '0',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'www.xiami.com',
    'Origin': 'http://www.xiami.com/',
    'Referer': 'http://www.xiami.com/',
    'Content-Length': '0',
}

class xiami_login(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self._auth = None

    def login(self):
        print('login ....')
        _form = {
            'email': self.email,
            'password': self.password,
            'LoginButton': '登录',
        }
        data = urllib.urlencode(_form)
        headers = {'User-Agent': ua}
        headers['Referer'] = 'http://www.xiami.com/web/login'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        with closing(httplib.HTTPConnection('www.xiami.com')) as conn:
            conn.request('POST', '/web/login', data, headers)
            res = conn.getresponse()
            cookie = res.getheader('Set-Cookie')
            self._auth = SimpleCookie(cookie)['member_auth'].value
            print('login success')
            return self._auth

    def checkin(self):
        if not self._auth:
            self.login()
        headers = checkin_headers
        headers['Cookie'] = 'member_auth=%s; t_sign_auth=1' % self._auth
        with closing(httplib.HTTPConnection('www.xiami.com')) as conn:
            conn.request('POST', '/task/signin', None, headers)
            res = conn.getresponse()
            return res.read()

# }}}
########################################################

class xiami(object):
    def __init__(self, url, email=email, password=password):
        self.url = url
        self.song_infos = []
        self.json_url = ''
        self.dir_ = os.getcwd().decode('utf8')
        self.template_wgets = 'wget -c -nv -U "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36" -O "%s" %s'
        self.template_song = 'http://www.xiami.com/song/gethqsong/sid/%s'

        self.showcollect_id = ''
        self.album_id = ''
        self.artist_id = ''
        self.song_id = ''
        self.user_id = ''
        self.cover_id = ''
        self.cover_data = ''

        self.html = ''
        self.disc_description_archives = {}

        home = os.path.expanduser('~')
        cookie_dir = os.path.join(home, '.Xiami.cookie')   # directory of login_time and member_auth cookie of xiami.com
        xm = xiami_login(email, password)
        if os.path.exists(cookie_dir):
            f = open(cookie_dir).read().split('\n')
            tm = str(int(time.time()))
            tm_s = (int(tm) - int(f[0])) > 18000           # 5 hours later, login after next loginning
            xm._auth = f[1]
            member_auth = xm._auth
            auth = xm.checkin()
            if auth != '0' or tm_s:
                member_auth = xm.login()
                if member_auth != f[1]: print('  --> member_auth is new one.')
                tm = str(int(time.time()))
                open(cookie_dir, 'w').write(tm + '\n' + member_auth)
                self.member_auth = member_auth
            else:
                self.member_auth = member_auth
        else:
            member_auth = xm.login()
            tm = str(int(time.time()))
            open(cookie_dir, 'w').write(tm + '\n' + member_auth)
            self.member_auth = member_auth

    def get_durl(self, id_):
        api_json = self.opener.open(self.template_song % id_).read()
        j = json.loads(api_json)
        t = j['location']
        row = t[0]
        encryed_url = t[1:]
        durl = decry(row, encryed_url)
        return durl

    def get_cover(self, info):
        if info['album_name'] == self.cover_id:
            return self.cover_data
        else:
            self.cover_id = info['album_name']
            i = 1
            while True:
                url = info['album_pic_url'].replace('.jpg', '_4.jpg')
                self.cover_data = os.popen('curl -s %s' % url).read()
                if self.cover_data[:5] != '<?xml':
                    return self.cover_data
                if i >= 10:
                    url = info['album_pic_url']
                    self.cover_data = os.popen('curl -s %s' % url).read()
                    return self.cover_data
                i += 1

    def get_lyric(self, lyric_url):
        if lyric_url:
            data = os.popen('curl -s %s' % lyric_url).read()
            return data.decode('utf8')
        else:
            return u''

    def get_disc_description(self, album_url, info):
        if not self.html:
            self.html = self.opener.open(album_url).read()
            t = re.findall(re_disc_description, self.html)
            t = dict([(a, modificate_text(parser.unescape(b))) for a, b in t])
            self.disc_description_archives = dict(t)
        if self.disc_description_archives.has_key(info['cd_serial']):
            disc_description = self.disc_description_archives[info['cd_serial']]
            return u'(%s)' % disc_description.decode('utf8')
        else:
            return u''

    def modified_id3(self, file_name, info):
        id3 = ID3()
        id3.add(TRCK(encoding=3, text=info['track']))
        id3.add(TDRC(encoding=3, text=info['year']))
        id3.add(TIT2(encoding=3, text=info['song_name']))
        id3.add(TALB(encoding=3, text=info['album_name']))
        id3.add(TPE1(encoding=3, text=info['artist_name']))
        id3.add(TPOS(encoding=3, text=info['cd_serial']))
        #id3.add(USLT(encoding=3, text=self.get_lyric(info['lyric_url'])))
        #id3.add(TCOM(encoding=3, text=info['composer']))
        #id3.add(WXXX(encoding=3, desc=u'xiami_song_url', text=info['song_url']))
        #id3.add(TCON(encoding=3, text=u'genres'))
        #id3.add(TSST(encoding=3, text=info['sub_title']))
        #id3.add(TSRC(encoding=3, text=info['disc_code']))
        id3.add(COMM(encoding=3, desc=u'Comment', text=u'\n\n'.join([info['song_url'], info['album_description']])))
        id3.add(APIC(encoding=3, mime=u'image/jpeg', type=3, desc=u'Cover', data=self.get_cover(info)))
        id3.save(file_name)

    def url_parser(self):
        if '/showcollect/' in self.url:
            self.showcollect_id = re.search(r'/showcollect/id/(\d+)', self.url).group(1)
            print u'\n  -- 正在分析精选集信息 ...'
            self.download_collect()
        elif '/album/' in self.url:
            self.album_id = re.search(r'/album/(\d+)', self.url).group(1)
            print u'\n  -- 正在分析专辑信息 ...'
            self.download_album()
        elif '/artist/' in self.url:
            self.artist_id = re.search(r'/artist/(\d+)', self.url).group(1)
            code = raw_input('输入 a 下载该艺术家所有专辑.\n输入 t 下载该艺术家top 20歌曲.\n>')
            if code == 'a':
                print u'\n  -- 正在分析艺术家专辑信息 ...'
                self.download_artist_albums()
            elif code == 't':
                print u'\n  -- 正在分析艺术家top20信息 ...'
                self.download_artist_top_20_songs()
            else:
                print u'  --> Over'
        elif '/song/' in self.url:
            self.song_id = re.search(r'/song/(\d+)', self.url).group(1)
            print u'\n  -- 正在分析歌曲信息 ...'
            self.download_song()
        elif '/u/' in self.url:
            self.user_id = re.search(r'/u/(\d+)', self.url).group(1)
            print u'\n  -- 正在分析用户歌曲库信息 ...'
            self.download_user_songs()
        else:
            print u'   请正确输入虾米网址.'

    def get_song_info(self, album_description, z, cd_serial_auth, i):
        song_info = {}
        song_info['song_id'] = i['song_id']
        song_info['song_url'] = u'http://www.xiami.com/song/' + i['song_id']
        song_info['track'] = i['track']
        song_info['album_description'] = album_description
        #song_info['lyric_url'] = i['lyric']
        #song_info['sub_title'] = i['sub_title']
        #song_info['composer'] = i['composer']
        #song_info['disc_code'] = i['disc_code']
        #if not song_info['sub_title']: song_info['sub_title'] = u''
        #if not song_info['composer']: song_info['composer'] = u''
        #if not song_info['disc_code']: song_info['disc_code'] = u''
        t = time.gmtime(int(i['gmt_publish']))
        song_info['year'] = unicode('-'.join([str(t.tm_year), str(t.tm_mon), str(t.tm_mday)]))
        song_info['song_name'] = modificate_text(i['name']).strip()
        song_info['artist_name'] = modificate_text(i['artist_name']).strip()
        song_info['album_pic_url'] = re.sub(r'_\d*', '', i['album_logo'])
        song_info['cd_serial'] = i['cd_serial']
        if cd_serial_auth:
            disc_description = self.get_disc_description('http://www.xiami.com/album/%s' % i['album_id'], song_info)
            if ''.join(self.disc_description_archives.values()) != u'':
                if disc_description:
                    song_info['album_name'] = modificate_text(i['title']).strip() + ' [Disc-' + song_info['cd_serial'] + '] ' + disc_description
                    file_name = '[Disc-' + song_info['cd_serial'] + '] ' + disc_description + ' ' + song_info['track'] + '.' + song_info['song_name'] + ' - ' + song_info['artist_name'] + '.mp3'
                    song_info['file_name'] = file_name
                    #song_info['cd_serial'] = u'1'
                else:
                    song_info['album_name'] = modificate_text(i['title']).strip() + ' [Disc-' + song_info['cd_serial'] + ']'
                    file_name = '[Disc-' + song_info['cd_serial'] + '] ' + song_info['track'] + '.' + song_info['song_name'] + ' - ' + song_info['artist_name'] + '.mp3'
                    song_info['file_name'] = file_name
                    #song_info['cd_serial'] = u'1'
            else:
                song_info['album_name'] = modificate_text(i['title']).strip()
                file_name = '[Disc-' + song_info['cd_serial'] + '] ' + song_info['track'] + '.' + song_info['song_name'] + ' - ' + song_info['artist_name'] + '.mp3'
                song_info['file_name'] = file_name
        else:
            song_info['album_name'] = modificate_text(i['title']).strip()
            file_name = song_info['track'].zfill(z) + '.' + song_info['song_name'] + ' - ' + song_info['artist_name'] + '.mp3'
            song_info['file_name'] = file_name
        # song_info['low_mp3'] = i['location']
        return song_info

    def get_song_infos(self, song_id):
        api_json = self.opener.open(url_song % song_id).read()
        j = json.loads(api_json)
        album_id = j['song']['album_id']
        api_json = self.opener.open(url_album % album_id).read()
        j = json.loads(api_json)
        t = j['album']['description']
        t = parser.unescape(t)
        t = parser.unescape(t)
        t = re.sub(r'<.+?(http://.+?)".+?>', r'\1', t)
        t = re.sub(r'<.+?>([^\n])', r'\1', t)
        t = re.sub(r'<.+?>(\r\n|)', u'\n', t)
        album_description = re.sub(r'\s\s+', u'\n', t).strip()
        cd_serial_auth = j['album']['songs'][-1]['cd_serial'] > u'1'
        z = 0
        if not cd_serial_auth:
            z = z_index(j['album']['songs'])
        for i in j['album']['songs']:
            if i['song_id'] == song_id:
                song_info = self.get_song_info(album_description, z, cd_serial_auth, i)
                return song_info

    def get_album_infos(self, album_id):
        api_json = self.opener.open(url_album % album_id).read()
        j = json.loads(api_json)
        t = j['album']['description']
        t = parser.unescape(t)
        t = parser.unescape(t)
        t = re.sub(r'<.+?(http://.+?)".+?>', r'\1', t)
        t = re.sub(r'<.+?>([^\n])', r'\1', t)
        t = re.sub(r'<.+?>(\r\n|)', u'\n', t)
        album_description = re.sub(r'\s\s+', u'\n', t).strip()
        d = modificate_text(j['album']['title'] + ' - ' + j['album']['artist_name'])
        dir_ = os.path.join(os.getcwd().decode('utf8'), d)
        self.dir_ = '\\'.join([dir_.split('\\', 1)[0], modificate_file_name_for_wget(dir_.split('\\', 1)[1])])
        cd_serial_auth = j['album']['songs'][-1]['cd_serial'] > u'1'
        z = 0
        if not cd_serial_auth:
            z = z_index(j['album']['songs'])
        song_infos = []
        for i in j['album']['songs']:
            song_info = self.get_song_info(album_description, z, cd_serial_auth, i)
            song_infos.append(song_info)
        return song_infos

    def download_song(self):
        logging.info('url -> http://www.xiami.com/song/%s' % self.song_id)
        song_info = self.get_song_infos(self.song_id)
        print u'\n  >> ' + u'1 首歌曲将要下载.'
        self.song_infos = [song_info]
        logging.info('directory: %s' % os.getcwd())
        logging.info('total songs: %d' % len(self.song_infos))
        self.download()

    def download_album(self):
        logging.info('url -> http://www.xiami.com/album/%s' % self.album_id)
        self.song_infos = self.get_album_infos(self.album_id)
        print u'\n  >> ' + unicode(len(self.song_infos)) + u' 首歌曲将要下载.'
        logging.info('directory: %s' % self.dir_)
        logging.info('total songs: %d' % len(self.song_infos))
        self.download()

    def download_collect(self):
        logging.info('url -> http://www.xiami.com/song/showcollect/id/%s' % self.showcollect_id)
        api_json = self.opener.open(url_collect % self.showcollect_id).read()
        j = json.loads(api_json)
        d = modificate_text(j['collect']['name'])
        dir_ = os.path.join(os.getcwd().decode('utf8'), d)
        self.dir_ = modificate_file_name_for_wget(dir_)
        print u'\n  >> ' + unicode(len(j['collect']['songs'])) + u' 首歌曲将要下载.'
        logging.info('directory: %s' % self.dir_)
        logging.info('total songs: %d' % len(j['collect']['songs']))
        n = 1
        for i in j['collect']['songs']:
            song_id = i['song_id']
            song_info = self.get_song_infos(song_id)
            self.song_infos = [song_info]
            self.download(n)
            self.html = ''
            self.disc_description_archives = {}
            n += 1

    def download_artist_albums(self):
        ii = 1
        while True:
            api_json = self.opener.open(url_artist_albums % (self.artist_id, str(ii))).read()
            j = json.loads(api_json)
            if j['albums']:
                for i in j['albums']:
                    album_id = i['album_id']
                    self.dir_ = ''
                    self.song_infos = self.get_album_infos(album_id)
                    print u'\n  >> ' + unicode(len(self.song_infos)) + u' 首歌曲将要下载.'
                    logging.info('url -> http://www.xiami.com/album/%s' % album_id)
                    logging.info('directory: %s' % self.dir_)
                    logging.info('total songs: %d' % len(self.song_infos))
                    self.download()
                    self.html = ''
                    self.disc_description_archives = {}
            else:
                break
            ii += 1

    def download_artist_top_20_songs(self):
        logging.info('url (top20) -> http://www.xiami.com/artist/%s' % self.artist_id)
        api_json = self.opener.open(url_artist_top_song % self.artist_id).read()
        j = json.loads(api_json)
        d = modificate_text(j['songs'][0]['artist_name'] + u' - top 20')
        dir_ = os.path.join(os.getcwd().decode('utf8'), d)
        self.dir_ = modificate_file_name_for_wget(dir_)
        print u'\n  >> ' + unicode(len(j['songs'])) + u' 首歌曲将要下载.'
        logging.info('directory: %s' % self.dir_)
        logging.info('total songs: %d' % len(j['songs']))
        n = 1
        for i in j['songs']:
            song_id = i['song_id']
            song_info = self.get_song_infos(song_id)
            self.song_infos = [song_info]
            self.download(n)
            self.html = ''
            self.disc_description_archives = {}
            n += 1

    def download_user_songs(self):
        logging.info('url -> http://www.xiami.com/u/%s' % self.user_id)
        dir_ = os.path.join(os.getcwd().decode('utf8'), u'虾米用户 %s 收藏的歌曲' % self.user_id)
        self.dir_ = modificate_file_name_for_wget(dir_)
        logging.info('directory: %s' % self.dir_)
        ii = 1
        n = 1
        while True:
            api_json = self.opener.open(url_lib_songs % (self.user_id, str(ii))).read()
            j = json.loads(api_json)
            if j['songs']:
                for i in j['songs']:
                    song_id = i['song_id']
                    song_info = self.get_song_infos(song_id)
                    self.song_infos = [song_info]
                    self.download(n)
                    self.html = ''
                    self.disc_description_archives = {}
                    n += 1
            else:
                break
            ii += 1

    def get_mp3_quality(self, durl):
        if 'm3.file.xiami.com' in durl:
            return 'H'
        else:
            return 'L'

    def download(self, n=None):
        dir_ = self.dir_
        cwd = os.getcwd().decode('utf8')
        if dir_ != cwd:
            if not os.path.exists(dir_):
                os.mkdir(dir_)
        ii = 1
        for i in self.song_infos:
            num = random.randint(0,100) % 7
            print u'\n  ++ 正在下载: %s' % i['file_name']
            durl = self.get_durl(i['song_id'])
            mp3_quality = self.get_mp3_quality(durl)
            if n == None:
                logging.info('  #%d [%s] -> %s' % (ii, mp3_quality, i['file_name'].encode('utf8')))
            else:
                logging.info('  #%d [%s] -> %s' % (n, mp3_quality, i['file_name'].encode('utf8')))
            if mp3_quality == 'L':
                print ' ## Warning:', 'gaining LOW quality mp3 link.'
            t = modificate_file_name_for_wget(i['file_name'])
            file_name = os.path.join(dir_, t)
            file_name_for_wget = file_name.replace('`', '\`')
            wget = self.template_wgets % (file_name_for_wget, durl)
            wget = wget.encode('gbk')
            status = os.system(wget)
            if status == 1024:
                iii = 0
                while iii < 3:
                    print u'    # Error 4 (Network failure), 10秒后从新尝试下载.'
                    os.remove(file_name)
                    time.sleep(10)
                    status = os.system(wget)
                    if status == 0:
                        break
                    else:
                        iii += 1
            if status != 0:     # other http-errors, such as 302.
                wget_exit_status_info = wget_es[status]
                logging.info('   \\\n                            \\->WARN: status: %d (%s), command: %s' % (status, wget_exit_status_info, wget))
                print '\n\n ----### ERROR ==> %d (%s) ###--- \n\n' % (status, wget_exit_status_info)
                print '  ===> ' + wget
                break

            self.modified_id3(file_name, i)
            ii += 1
            time.sleep(10)

def main(url):
    x = xiami(url)
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), ('User-Agent', ua), ('Cookie', 'member_auth=%s' % x.member_auth)]
    x.opener = opener
    x.url_parser()
    logging.info('  ########### work is over ###########\n')

if __name__ == '__main__':
    log_file = os.path.join(os.path.expanduser('~'), '.Xiami.log')
    logging.basicConfig(filename=log_file, level=10, format='%(asctime)s %(message)s')
    print u'程序运行日志在 %s' % log_file
    p = argparse.ArgumentParser(description='downloading any xiami.com')
    p.add_argument('url', help='any url of xiami.com')
    args = p.parse_args()
    main(args.url)
