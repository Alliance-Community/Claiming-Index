# About
This generates 3 different maps:
- Icon -> Asset List
- Asset -> Icon
- Faction + Asset -> Icon

And outputs them in html. Its all very crude and primitive python.

To run, pass the path to your `pr_repo` folder. Eg. `python3 gen_index.py "path-to-pr-repo"`.

# Icon Lister
The icon lister goes through the assets and checks if the icons are correct. It verifies:
- All `mini_` (= minimap) and `menuIcon_` (= squad menu) icons are the same of a single asset
- Vehicle `X` uses the same icon as `X_bf2`, `X_sp`, and `X_prsp`
- The icons used exist

To run it, supply `pr_repo` as well. Eg. `python3 icon_lister.py "path-to-pr-repo"`.
