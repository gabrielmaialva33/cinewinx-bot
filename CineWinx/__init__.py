from CineWinx.core.bot import WinxBot
from CineWinx.core.dir import dirr
from CineWinx.core.git import git
from CineWinx.core.userbot import Userbot
from CineWinx.misc import dbb, heroku, sudo
from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()
# Bot Client
app = WinxBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()
AnimiZeY = AnimiZeYAPI()
ZenoFM = ZenoFMAPI()

HELPABLE = {}
