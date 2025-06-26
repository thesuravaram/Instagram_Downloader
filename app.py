from flask import Flask, request, jsonify, render_template
import instaloader

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    if not url or 'instagram.com' not in url:
        return jsonify({'success': False, 'error': 'Invalid Instagram URL'})

    try:
        loader = instaloader.Instaloader()
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(loader.context, shortcode)
        media = []

        if post.typename == 'GraphImage':
            media.append({'url': post.url, 'type': 'image'})
        elif post.typename == 'GraphVideo':
            media.append({'url': post.video_url, 'type': 'video'})
        elif post.typename == 'GraphSidecar':
            for node in post.get_sidecar_nodes():
                media.append({'url': node.video_url if node.is_video else node.display_url, 'type': 'video' if node.is_video else 'image'})

        return jsonify({'success': True, 'media': media})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)