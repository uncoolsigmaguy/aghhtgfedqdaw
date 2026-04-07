from flask import Flask, jsonify
import requests
import certifi

app = Flask(__name__)

# ================= global repos =================

GLOBAL_REPOS = [
    { "url": "https://fastsign.dev/repo.json", "useProxy": true, "category": "tweaked" },
    { "url": "https://driftywinds.github.io/AltStore/apps.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/titouan336/Spotify-AltStoreRepo-mirror/refs/heads/main/source.json", "category": "community" },
    { "url": "https://gablilli.github.io/somereposblocked/cypwn.json", "category": "tweaked" },
    { "url": "https://qnblackcat.github.io/AltStore/apps.json", "category": "community" },
    { "url": "https://wuxu1.github.io/wuxu-complete-plus.json", "category": "tweaked" },
    { "url": "https://community-apps.sidestore.io/sidecommunity.json", "category": "community" },
    { "url": "https://stikdebug.xyz/index.json", "useProxy": true, "category": "developer" },
    { "url": "https://raw.githubusercontent.com/lo-cafe/winston-altstore/main/apps.json", "category": "community" },
    { "url": "https://raw.githubusercontent.com/yodaluca23/SpotC-AltStore-Repo/main/AltStore%20Repo.json", "category": "community" },
    { "url": "https://theodyssey.dev/altstore/odysseysource.json", "category": "developer" },
    { "url": "https://provenance-emu.com/apps.json", "category": "developer" },
    { "url": "https://ish.app/altstore.json", "useProxy": true, "category": "developer" },
    { "url": "https://raw.githubusercontent.com/arichornlover/arichornlover.github.io/refs/heads/main/apps2.json", "category": "developer" },
    { "url": "https://raw.githubusercontent.com/tapframe/NuvioStreaming/main/nuvio-source.json", "category": "developer" },
    { "url": "https://raw.githubusercontent.com/LiveContainer/LiveContainer/refs/heads/main/.github/apps.json", "category": "developer" },
    { "url": "https://balackburn.github.io/Apollo/apps.json", "category": "developer" },
    { "url": "https://repo.owo.network/", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/AntonP29/AntonP29-Repo/refs/heads/main/repo.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/Balackburn/YTLitePlusAltstore/main/apps.json", "category": "developer" },
    { "url": "https://altstore.oatmealdome.me/", "useProxy": true, "category": "developer" },
    { "url": "https://alts.lao.sb/", "category": "community" },
    { "url": "https://quarksources.github.io/dist/quantumsource%2B%2B.min.json", "category": "tweaked" },
    { "url": "https://xitrix.github.io/iTorrent/AltStore.json", "category": "developer" },
    { "url": "https://driftywinds.github.io/repos/esign.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/WhySooooFurious/Ultimate-Sideloading-Guide/refs/heads/main/raw-files/app-repo.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/khcrysalis/Feather/main/app-repo.json", "category": "developer" },
    { "url": "https://gablilli.github.io/somereposblocked/nabzclan.json", "category": "tweaked" },
    { "url": "https://gablilli.github.io/stremiorepo/index.json", "category": "community" },
    { "url": "https://flyinghead.github.io/flycast-builds/altstore.json", "category": "developer" },
    { "url": "https://alt.thatstel.la/", "useProxy": true, "category": "developer" },
    { "url": "https://gablilli.github.io/somereposblocked/app.json", "category": "tweaked" },
    { "url": "https://alt.crystall1ne.dev/", "useProxy": true, "category": "developer" },
    { "url": "https://apps.sidestore.io/", "category": "developer" },
    { "url": "https://raw.githubusercontent.com/Neoncat-OG/TrollStore-IPAs/main/apps_esign.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/vizunchik/AltStoreRus/master/apps.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/swaggyP36000/TrollStore-IPAs/main/apps_esign.json", "category": "tweaked" },
    { "url": "https://raw.githubusercontent.com/Gliddd4/gliddd4-repo/refs/heads/main/app.json", "category": "tweaked" },
    { "url": "https://therealfoxster.github.io/altsource/apps.json", "category": "tweaked" }
]

# ================= fetch repo =================

def fetch_repo(repo):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(
            repo["url"],
            headers=headers,
            timeout=10,
            verify=certifi.where()
        )

        data = r.json()

        return {
            "meta": repo,
            "data": data
        }

    except Exception as e:
        return {
            "meta": repo,
            "error": str(e)
        }

# ================= index apps =================

def index_apps(repos_data):
    all_apps = []
    keys = set()

    for repo in repos_data:
        if "data" not in repo:
            continue

        data = repo["data"]
        repo_name = data.get("name", repo["meta"]["name"])

        for app in data.get("apps", []):
            key = f"{app.get('name')}|{repo_name}"

            if key in keys:
                continue

            app["__repoName"] = repo_name
            all_apps.append(app)
            keys.add(key)

    return all_apps

# ================= routes =================

@app.route("/")
def home():
    return "Global Repo API Running"

@app.route("/repos")
def repos():
    return jsonify(GLOBAL_REPOS)

@app.route("/apps")
def apps():
    repos_data = []

    for repo in GLOBAL_REPOS:
        repos_data.append(fetch_repo(repo))

    apps = index_apps(repos_data)

    return jsonify({
        "repo_count": len(repos_data),
        "app_count": len(apps),
        "apps": apps
    })

# ================= run =================

if __name__ == "__main__":
    app.run()
