from flask import Flask, render_template, request, jsonify, send_from_directory
import datetime
import json
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'mp3', 'mp4', 'mov', 'avi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_checkins():
    """Load previous check-ins from file"""
    if os.path.exists("checkins.json"):
        try:
            with open("checkins.json", "r") as f:
                return [json.loads(line) for line in f]
        except Exception:
            return []
    return []

def save_checkin(checkin_data):
    """Save check-in data to file"""
    try:
        with open("checkins.json", "a") as f:
            f.write(json.dumps(checkin_data) + "\n")
        return True
    except Exception as e:
        print(f"Error saving check-in: {e}")
        return False

def update_checkin(date, updated_data):
    """Update an existing check-in for a specific date"""
    try:
        checkins = load_checkins()
        updated = False

        for i, checkin in enumerate(checkins):
            if checkin.get('date') == date:
                checkins[i].update(updated_data)
                checkins[i]['timestamp'] = datetime.datetime.now().isoformat()
                updated = True
                break

        if updated:
            with open("checkins.json", "w") as f:
                for checkin in checkins:
                    f.write(json.dumps(checkin) + "\n")
            return True
        return False
    except Exception as e:
        print(f"Error updating check-in: {e}")
        return False

@app.route('/')
def index():
    """Main page showing the check-in form and recent check-ins"""
    recent_checkins = load_checkins()[-5:]  # Last 5 check-ins
    recent_checkins.reverse()  # Show newest first

    # Check if user already checked in today and get today's checkin
    today = datetime.date.today().isoformat()
    todays_checkin = None
    for checkin in recent_checkins:
        if checkin.get('date') == today:
            todays_checkin = checkin
            break

    already_checked_in = todays_checkin is not None

    return render_template('index.html',
                         recent_checkins=recent_checkins,
                         already_checked_in=already_checked_in,
                         todays_checkin=todays_checkin,
                         today=datetime.date.today().strftime('%B %d, %Y'))

@app.route('/checkin', methods=['POST'])
def submit_checkin():
    """Handle check-in form submission"""
    # Handle form data (including files)
    mood = request.form.get('mood')
    plans_json = request.form.get('plans')
    thoughts = request.form.get('thoughts', '').strip()
    links_json = request.form.get('links')
    is_edit = request.form.get('is_edit') == 'true'

    try:
        plans = json.loads(plans_json) if plans_json else []
        links = json.loads(links_json) if links_json else []
    except json.JSONDecodeError:
        return jsonify({'success': False, 'error': 'Invalid data format'})

    if not mood or not plans:
        return jsonify({'success': False, 'error': 'Please select a mood and enter at least one plan'})

    # Handle file uploads
    uploaded_files = []
    if 'files' in request.files:
        files = request.files.getlist('files')
        for file in files:
            if file and file.filename != '' and allowed_file(file.filename):
                # Generate unique filename
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                unique_filename = f"{uuid.uuid4()}.{file_extension}"

                # Save file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)

                uploaded_files.append({
                    'filename': unique_filename,
                    'original_name': secure_filename(file.filename),
                    'type': file.content_type or 'application/octet-stream',
                    'size': os.path.getsize(file_path)
                })

    today = datetime.date.today().isoformat()

    if is_edit:
        # Update existing check-in
        updated_data = {
            "mood": mood,
            "plans": plans,
            "thoughts": thoughts,
            "links": links,
            "files": uploaded_files
        }
        if update_checkin(today, updated_data):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to update check-in'})
    else:
        # Create new check-in
        checkin_data = {
            "date": today,
            "timestamp": datetime.datetime.now().isoformat(),
            "mood": mood,
            "plans": plans,
            "thoughts": thoughts,
            "links": links,
            "files": uploaded_files
        }

        if save_checkin(checkin_data):
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Failed to save check-in'})

@app.route('/api/checkins')
def get_checkins():
    """API endpoint to get recent check-ins"""
    checkins = load_checkins()[-10:]  # Last 10 check-ins
    checkins.reverse()
    return jsonify(checkins)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)