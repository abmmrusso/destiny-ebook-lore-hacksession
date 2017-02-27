#!/usr/bin/python
from ebooklib import epub
from PIL import Image
import json
import re
import lxml.html
import os

def chapterId( cardName ):
	return re.sub(r"[^\d\w]","_", cardName)

def chapterBaseFileName( cardName, counter ):
	return "%03d-%s" % (counter,chapterId( cardName ))

def chapterPageFile( cardName, counter ):
	return chapterBaseFileName( cardName, counter ) + ".xhtml"

def chapterTitle( cardName ):
	return lxml.html.fromstring(cardName).text

def safeValue( value ):
	if value is None:
		return ""
	return value

def createCardImage( fileBaseName, sourceImagePath, cropXStart, cropYStart, cropWidth, cropHeight):
	imagePath = os.path.join('images/%s.%s' % (fileBaseName, os.path.splitext(sourceImagePath)[1]))
	if not os.path.isfile(imagePath):
		sourceImage = Image.open(sourceImagePath)
		cardImage = Image.new(sourceImage.mode, (cropHeight, cropWidth), sourceImage.palette)
		cardImage = sourceImage.crop((cropXStart, cropYStart, cropXStart+cropWidth, cropYStart+cropHeight))
		cardImage.thumbnail(([0.7 * x for x in cardImage.size]))
		cardImage.save(imagePath, optimize=True)
	return imagePath

def createEbook( grimoireData ):
	book = epub.EpubBook()

	book.set_identifier('destinyGrimoire')
	book.set_title('Destiny Grimoire')
	book.set_language('en')
	book.add_author('Bungie')
	book.set_cover("cover.jpg", open('cover.jpg', 'rb').read())

	style = '''    
	cardname {
		display: block;
    	text-align: center;
    	font-size:150%;
    }
  	cardimage {
  		float: left;
  		margin-right: 5%;
  		width: 40%;
  		height: 40%;
  	}
  	cardintro {
  		display: block;
  		padding: 5%;
  	}
  	carddescription {}
  	container {
  		width: 100%;
  		clear: both;
  	}
  	'''

	default_css = epub.EpubItem(uid="style_default", file_name="style/default.css", media_type="text/css", content=style)
	book.add_item(default_css)

	book.spine = ['nav']

	counter = 1
	tocSections=()
	for theme in grimoireData["themes"]:
		themePages = ()
		for page in theme["pages"]:
			pageCards = ()
			for card in page["cards"]:
				if counter > 0:
					bookPage = epub.EpubHtml(title=chapterTitle(card["cardName"]), file_name=chapterPageFile(card["cardName"], counter), lang='en', content="")
					bookPage.add_item(default_css)
					imageBaseFileName = '%s_img' % (chapterBaseFileName(card["cardName"], counter))
					imagePath = createCardImage(imageBaseFileName, os.path.join('images/%s' % (os.path.basename(card["image"]["sourceImage"]))), card["image"]["regionXStart"], card["image"]["regionYStart"], card["image"]["regionWidth"], card["image"]["regionHeight"])
					book.add_item(epub.EpubItem(uid=imageBaseFileName, file_name=imagePath, content=open(imagePath, 'rb').read()))
					bookPage.content = u'''	<cardname">%s</cardname>
											<cardintro>%s</cardintro>
											<container>
												<cardimage><img src="%s"/></cardimage>
												<carddescription">%s</carddescription>
											</container>''' % ( card["cardName"], safeValue(card["cardIntro"]), imagePath, safeValue(card["cardDescription"]))
					book.add_item(bookPage)
					pageCards = pageCards + (bookPage,)
					book.spine.append(bookPage)
				counter += 1

			themePages = themePages + ((epub.Section(page["pageName"]), pageCards),)

		tocSections = tocSections + ((epub.Section(theme["themeName"]), themePages),)

	book.toc=tocSections

	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())

	epub.write_epub('destinyGrimoire.epub', book)

if __name__ == "__main__":
	with open('destinyGrimoire.json') as grimoireJSON:
		grimoireData = json.load(grimoireJSON)
		createEbook(grimoireData)
	