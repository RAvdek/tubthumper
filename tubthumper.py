import json
import os
import random
import time
import click
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


SONG_PATH = os.path.join(os.path.dirname('.'), 'songs')
FB_URL = 'http://www.facebook.com'
TEXTBOX_CLASS = '_1mf _1mj'
SCROLL_JS = "window.scrollTo(0,Math.max(document.documentElement.scrollHeight," \
            "document.body.scrollHeight,document.documentElement.clientHeight));"


class TubThumper(object):

    def __init__(self, song, email, password):
        self.chrome = webdriver.Chrome()
        try:
            with open(os.path.join(SONG_PATH, '{}.json'.format(song))) as f:
                song_dict = json.load(f)
        except IOError:
            raise IOError("Song not available!")
        self.youtube = song_dict['youtube']
        self.lyrics = song_dict['lyrics'].split('\n')
        self._login(email=email, password=password)

    def _login(self, email, password):
        self.chrome.get(FB_URL)
        self.chrome.find_element_by_id('email').send_keys(email)
        self.chrome.find_element_by_id('pass').send_keys(password)
        self.chrome.find_element_by_id('loginbutton').click()

    def find_next_textbox(self):
        return self.chrome.find_element_by_class_name(TEXTBOX_CLASS)

    def generate_post(self):
        return '\n\n'.join([random.choice(self.lyrics), self.youtube])

    def scroll_to_bottom(self):
        self.chrome.execute_script(SCROLL_JS)

    @staticmethod
    def random_wait(min_time=1, max_time=5):
        if max_time < min_time:
            max_time = min_time + 1
        sleep_time = min_time + (max_time - min_time)*random.random()
        time.sleep(sleep_time)

    def thump_once(self):
        text_box = self.find_next_textbox()
        text_box.send_keys(self.generate_post())
        text_box.send_keys(Keys.ENTER)

    def thump_n(self, n=None):
        thumps = 0
        while thumps < n:
            self.thump_once()
            self.scroll_to_bottom()
            self.random_wait()
            if n:
                thumps += 1

    def die(self):
        self.chrome.quit()


@click.option('--n_thumps', default=None, help="How many posts to post?")
@click.option('--song', default='tubthumping', help="Choose your song! (See songs/)")
@click.argument('password')
@click.argument('email')
@click.command()        
def main(email, password, song, n_thumps):

    tt = TubThumper(song, email, password)
    tt.thump_n(n_thumps)
    tt.die()

if __name__ == '__main__':
    main()
