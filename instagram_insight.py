from flask import Flask, redirect, url_for, request, render_template,send_from_directory
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from igramscraper.instagram import Instagram

app = Flask(__name__)
instagram = Instagram()
# instagram.with_credentials(<username>, <password>,"folderpath") #fill the details
instagram.login()

def generate_image(user_name,words=500,fontsize=45):
    '''
        This method saves the image as image.png
        PARAMETERS :
            user_name (str): instagram user name
            words(int): the maximum number of words in the image
            font size(int): the font size of the text
    '''
    #get all the media from that instagram user name
    medias = instagram.get_medias(user_name,2000)

    #get the all the text from the caption
    text = ""
    for media in medias:
        text += str(media.caption)

    if text == "":
        text = "None none"

    wordcloud = WordCloud(max_font_size=30, max_words=700).generate(text)

    # Display the generated image
    plt.figure(figsize=(20,10))
    plt.axis('off')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.savefig('image.png', dpi=700, bbox_inches='tight')


@app.route('/')
def hello():
    return render_template("index.html",text=" ")

@app.route('/api',methods=['post'])
def scraper():
    
    name = request.values.get("nm")

    try :
        medias = instagram.get_medias(name,2000)
    except Exception as err:
        return render_template("index.html",text=f"Enter a valid user name {err}")
    
    generate_image(name)

    return send_from_directory("./","image.png", as_attachment=True,attachment_filename=f"{name}.png")


if __name__ == '__main__':
    app.run(debug=True)
