#!/bin/bash
rm destinyGrimoire.json
curl -s -H "X-API-Key: $1" https://www.bungie.net/Platform/Destiny/Vanguard/Grimoire/Definition/ | jq '.Response as $response | { themes: [ ($response.themeCollection[] as $theme | { themeName: $theme.themeName, pages: [ ($theme.pageCollection[] as $page | { pageName: $page.pageName, cards: [ ($page.cardCollection[] as $card | { cardName: $card.cardName, cardIntro: $card.cardIntro, cardDescription: $card.cardDescription, image: { sourceImage: ("http://www.bungie.net" + $card.normalResolution.image.sheetPath), regionXStart: $card.normalResolution.image.rect.x, regionYStart: $card.normalResolution.image.rect.y, regionWidth: $card.normalResolution.image.rect.width, regionHeight: $card.normalResolution.image.rect.height }}) ]}) ] }) ]}' > destinyGrimoire.json
rm -rf images
mkdir images
for f in $(jq -r .themes[].pages[].cards[].image.sourceImage destinyGrimoire.json | sort | uniq); do curl -s "$f" > images/$(basename $f) ; done
python generateEbook.py
