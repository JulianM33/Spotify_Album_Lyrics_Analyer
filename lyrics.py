# function to scrape lyrics from genius
import requests
from bs4 import BeautifulSoup

# Scraping the lyrics off of the Genius.com website
def scrape_lyrics(artistname, songname):
    artistname2 = str(artistname.replace(' ', '-')) if ' ' in artistname else str(artistname)
    songname2 = str(songname.replace(' ', '-')) if ' ' in songname else str(songname)
    page = requests.get('https://genius.com/' + artistname2 + '-' + songname2 + '-' + 'lyrics')
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-6 YYrds")
    if lyrics1:
        lyrics = lyrics1.get_text()
    elif lyrics2:
        lyrics = lyrics2.get_text()
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics


# function to attach lyrics onto data frame
# artist_name should be inserted as a string
def lyrics_onto_frame(df1, artist_name):
    for i, x in enumerate(df1['track']):
        test = scrape_lyrics(artist_name, x)
        df1.loc[i, 'lyrics'] = test
    return df1




def get_lyrics(track_name, source, cache=True):
    ''' returns list of strings with lines of lyrics
        also reads/write to cache file | if cache=True
        track_name -> track name in format "artist - title"
        source -> source to fetch lyrics from ('google' or 'azlyrics')
        cache -> bool | whether to check lyrics from cache or not.
    '''
    # filepath = get_filename(track_name)
    #
    # if not os.path.isdir(CACHE_PATH):
    #     os.makedirs(CACHE_PATH)
    #
    # if os.path.isfile(filepath) and cache:
    #     # lyrics exist
    #     with open(filepath) as file:
    #         lyrics_lines = file.read().splitlines()
    # else:

    if source == 'google':
        lyrics_lines = fetch_lyrics(url + query(track_name))
    else:
        lyrics_lines = get_azlyrics(url + query(track_name))

    if isinstance(lyrics_lines, str):
        return ['lyrics not found! :(', 'Issue is:', lyrics_lines]

    text = map(lambda x: x.replace('&amp;', '&') + '\n', lyrics_lines)

    # with open(filepath, 'w') as file:
    #     file.writelines(text)

    return lyrics_lines


def fetch_lyrics(url):
    ''' fetches sources from google, then azlyrics
        checks if lyrics are valid

        returns list of strings
        if lyrics not found in both google & azlyrics
        returns string of error from get_azlyrics()
    '''
    html = get_html(url)
    if isinstance(html, tuple):
        return html[0]

    html_regex = re.compile(
        r'<div class="{}">([^>]*?)</div>'.format(CLASS_NAME), re.S)

    text_list = html_regex.findall(html)

    if len(text_list) < 2:
        # No google result found!
        lyrics_lines = get_azlyrics(url)
    else:
        ly = []
        for l in text_list[1:]:
            # lyrics must be multiline,
            # ignore the artist info below lyrics
            if l.count('\n') > 2:
                ly += l.split('\n')
        if len(ly) < 5:
            # too short match for lyrics
            lyrics_lines = get_azlyrics(url)
        else:
            # format lyrics
            lyrics_lines = ly

    return lyrics_lines





def get_azlyrics(url):
    ''' fetches lyrics from azlyrics
        returns list if strings of lyrics
        if lyrics not found returns error string
    '''
    az_html = get_az_html(url)
    if isinstance(az_html, tuple):
        return az_html[0]

    az_regex = re.compile(
        r'<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->(.*)<!-- MxM banner -->', re.S)

    ly = az_regex.search(az_html)
    if ly == None:
        # Az lyrics not found
        return 'Azlyrics missing...'

    rep = {'&quot;': '\"', '&amp;': '&', '\r': ''}

    ly = re.sub(r'<[/]?\w*?>', '', ly.group(1)).strip()
    # ly = ly.replace('&quot;', '\"').replace('&amp;', '&')
    # regex = re.compile('|'.join(substrings))
    ly = re.sub('|'.join(rep.keys()), lambda match: rep[match.group(0)], ly)
    lyrics_lines = ly.split('\n')

    return lyrics_lines












