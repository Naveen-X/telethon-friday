from fridaybot.Configs import Config
from fridaybot.utils import friday_on_cmd
from fridaybot.Configs import Config
issudousing = Config.SUDO_USERS
islogokay = Config.PRIVATE_GROUP_ID
isdbfine = Config.DB_URI
isherokuokay = Config.HEROKU_APP_NAME
gdriveisshit = Config.AUTH_TOKEN_DATA
wttrapi = Config.OPEN_WEATHER_MAP_APPID
rmbg = Config.REM_BG_API_KEY
hmmok = Config.LYDIA_API
currentversion = "6.5"
amiusingsudo = "Active ✅" if issudousing else "Inactive ❌"
logchat = "Connected ✅" if islogokay else "Dis-Connected ❌"
riplife = "Connected ✅" if isherokuokay else "Not Connected ❌"
wearenoob = "Active ✅" if gdriveisshit else "Inactive ❌"
gendu = "Added ✅" if rmbg else "Not Added ❌"
starknoobs = "Added ✅" if wttrapi else "Not Added ❌"
meiko = "Added ✅" if hmmok else "Not Added ❌"
dbstats = "Fine ✅" if isdbfine else "Not Fine ❌"
inlinestats = (
    f"✘ SHOWING FRIDAY STATS ✘\n"
    f"VERSION = {currentversion} \n"
    f"DATABASE = {dbstats} \n"
    f"SUDO = {amiusingsudo} \n"
    f"LOG-CHAT = {logchat} \n"
    f"HEROKU = {riplife} \n"
    f"G-DRIVE = {wearenoob}"
)
