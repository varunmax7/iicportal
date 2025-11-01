from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iic-mgit-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db = SQLAlchemy(app)

# Ensure upload directories exist
os.makedirs('static/images/uploads', exist_ok=True)
os.makedirs('static/documents', exist_ok=True)

# Database Models
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20))
    branch = db.Column(db.String(50))
    year_sem = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))
    display_order = db.Column(db.Integer, default=999)  # For custom ordering

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50))
    venue = db.Column(db.String(100))
    overview = db.Column(db.Text)
    event_type = db.Column(db.String(20))  # 'upcoming' or 'past'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event = db.Column(db.String(200))
    testimonial = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class GalleryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_path = db.Column(db.String(300))
    category = db.Column(db.String(50))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

def init_sample_data():
    # Add sample members
    if Member.query.count() == 0:
        # Define priority roles for display order
        priority_roles = {
            "Head": 1,
            "Co-Head": 2,
            "Secretary": 3,
            "Developers Head": 4,
            "Social Media Head": 5
        }
        
        sample_members = [
            { "name": "T Achut Balaji", "roll_no": "23261A0250", "branch": "EEE", "year_sem": "3rd year", "phone": "9100658541", "email": "Tachutbalahi_eee230250@mgit.ac.in", "role": "Head" },
            { "name": "Nivas Salla", "roll_no": "24261A6754", "branch": "CSD-ET", "year_sem": "2nd", "phone": "6300632510", "email": "snivas_csd246754@mgit.ac.in", "role": "Co-Head" },
            { "name": "Markapuram Vishal Reddy", "roll_no": "23261A0233", "branch": "EEE", "year_sem": "3rd", "phone": "9441168182", "email": "mvishalreddy_eee230233@mgit.ac.in", "role": "Secretary" },
            { "name": "Ramavath Varun", "roll_no": "24261A1455", "branch": "MCT", "year_sem": "2nd", "phone": "7207157982", "email": "rvarun_mct241455@mgit.ac.in", "role": "Developers Head" },
            { "name": "Hasini Jella", "roll_no": "24261A0518", "branch": "CSE", "year_sem": "2nd year, 3rd sem", "phone": "9908419168", "email": "hjella_cse240518@mgit.ac.in", "role": "Social Media Head" },
            { "name": "Anvitha Bangalore", "roll_no": "24261A6702", "branch": "CSD", "year_sem": "2nd", "phone": "9030213008", "email": "abangalore_csd246702@mgit.ac.in", "role": "Outreach Manager" },
            { "name": "Namala Sreeshanth", "roll_no": "24261A6747", "branch": "CSD-ET", "year_sem": "2nd", "phone": "7416294256", "email": "nsreeshanth_csd246747@mgit.ac.in", "role": "Member" },
            { "name": "K Sai Karthik", "roll_no": "24261A0490", "branch": "ECE", "year_sem": "2nd Year (3rd SEM)", "phone": "6302577316", "email": "kkanuri14@gmail.com", "role": "Member" },
            { "name": "Akhilesh Kancharla", "roll_no": "24261A0502", "branch": "CSE", "year_sem": "2024", "phone": "88688812245", "email": "akhileshkancharla5@gmail.com", "role": "Documentation Head" },
            { "name": "Bojakar Akshaya Sree", "roll_no": "23261A6713", "branch": "CSD", "year_sem": "3rd", "phone": "6302214844", "email": "bakshayasree_csd236713@mgit.ac.in", "role": "DOP" },
            { "name": "Ashwini Tadkale", "roll_no": "23261A6708", "branch": "CSD", "year_sem": "3rd", "phone": "9989211003", "email": "atadkale_csd236708@mgit.ac.in", "role": "Content-Social Manager" },
            { "name": "Rahul Pusapati", "roll_no": "23261A0545", "branch": "CSE", "year_sem": "3rd", "phone": "7305480128", "email": "Prahul_cse230545@mgit.ac.in", "role": "PR Head" },
            { "name": "Y Sanjana Sheetal", "roll_no": "24261A6664", "branch": "CSM", "year_sem": "2nd", "phone": "7815935455", "email": "ysanjanasheetal_csm246664@mgit.ac.in", "role": "DOP" },
            { "name": "Angel Vyas", "roll_no": "23261A6706", "branch": "CSD", "year_sem": "3rd", "phone": "9441478732", "email": "avyas_csd236706@mgit.ac.in", "role": "Hospitality" },
            { "name": "Gade Srignesh", "roll_no": "24265A0204", "branch": "EEE", "year_sem": "III", "phone": "9392252615", "email": "gsrignesh_eee24265A0204@mgit.ac.in", "role": "Member" },
            { "name": "S. Shivram Reddy", "roll_no": "23261A1259", "branch": "IT", "year_sem": "III", "phone": "9346370934", "email": "sshivramreddy_it231259@mgit.ac.in", "role": "Member" },
            { "name": "Yasasvi Pisupati", "roll_no": "23261A0340", "branch": "Mechanical", "year_sem": "-", "phone": "8179407614", "email": "ypisupati_mec230340@mgit.ac.in", "role": "Member" },
            { "name": "Prashanth Kumar", "roll_no": "23261A6714", "branch": "CSD", "year_sem": "3rd", "phone": "9032652537", "email": "bprashanthkumar_csd236714@mgit.ac.in", "role": "Member" },
            { "name": "S. S. Sri Sowmya", "roll_no": "23261A04B2", "branch": "ECE", "year_sem": "3rd year", "phone": "9441458069", "email": "sowmyasamudrapu@gmail.com", "role": "Member" },
            { "name": "Ashish Gudla", "roll_no": "23261A0312", "branch": "Mechanical", "year_sem": "3rd", "phone": "7989765445", "email": "gashish_mec230312@mgit.ac.in", "role": "Member" },
            { "name": "Konka Mani Sai", "roll_no": "24261A1428", "branch": "Mechatronics", "year_sem": "2nd", "phone": "7013590782", "email": "kmanisai_mct241428@mgit.ac.in", "role": "Member" },
            { "name": "Abhinav B", "roll_no": "23261A0564", "branch": "CSE", "year_sem": "3rd", "phone": "9603729764", "email": "abalijepalli_cse230564@mgit.ac.in", "role": "Member" },
            { "name": "Ribhu S", "roll_no": "23261A6752", "branch": "CSD", "year_sem": "III", "phone": "9701389782", "email": "sribhu_csd236752@mgit.ac.in", "role": "Member" },
            { "name": "Prathyusha Lingampally", "roll_no": "23261A0493", "branch": "ECE", "year_sem": "3rd", "phone": "8919450193", "email": "lingampallyprathyusha1805@gmail.com", "role": "Member" },
            { "name": "Urvashi Sharma", "roll_no": "23261A0337", "branch": "Mechanical", "year_sem": "3rd", "phone": "9390695829", "email": "usharma_mec230337@mgit.ac.in", "role": "Member" },
            { "name": "M Sai Sri Bharani", "roll_no": "24261A1435", "branch": "Mechatronics", "year_sem": "2nd", "phone": "6281194936", "email": "msaisribharani_mct241435@mgit.ac.in", "role": "Member" },
            { "name": "P. Ramyaranjini", "roll_no": "22261A0229", "branch": "EEE", "year_sem": "4th", "phone": "7013205614", "email": "pramyaranjini_eee220229@mgit.ac.in", "role": "Served" },
            { "name": "Barathala Sai Chetan", "roll_no": "22261A0410", "branch": "ECE-1", "year_sem": "IV", "phone": "9392741859", "email": "bsaichetan_ece220410@mgit.ac.in", "role": "Previous Head - Served" },
            { "name": "Battu Vighnesh", "roll_no": "22261A0411", "branch": "ECE-1", "year_sem": "IV", "phone": "9398952819", "email": "bvighnesh_ece220411@mgit.ac.in", "role": "Served" }
        ]
        
        for member_data in sample_members:
            # Assign display order based on priority roles
            display_order = priority_roles.get(member_data["role"], 999)
            
            member = Member(
                name=member_data["name"],
                roll_no=member_data["roll_no"],
                branch=member_data["branch"],
                year_sem=member_data["year_sem"],
                phone=member_data["phone"],
                email=member_data["email"],
                role=member_data["role"],
                display_order=display_order
            )
            db.session.add(member)
    
    # Add sample activities
    if Activity.query.count() == 0:
        sample_activities = [
            # Past Events (2024)
            { "name": "Motivational Session By Successful Entrepreneur / Start-Up Founder", "date": "30 September 2024", "venue": "MGIT, Hyderabad", "overview": "09:30 AM to 1:00 PM; Speaker: K. Surya Prakash, CEO - Deeloop Technologies; Motivational talk on entrepreneurship and startup experiences.", "event_type": "past" },
            { "name": "Ideathon Hack4SDE", "date": "19 October 2024", "venue": "MGIT C Block Seminar Hall and E Block 301, Hyderabad", "overview": "Hackathon event focused on ideation and problem-solving for sustainable development; full-day event with participants pitching ideas.", "event_type": "past" },
            { "name": "Motivational Session by Successful Innovator", "date": "22 October 2024", "venue": "MGIT, Hyderabad", "overview": "09:30 AM to 12:30 PM; Speaker: Ms. Shantha Nerametla; Inspirational session sharing success stories in innovation.", "event_type": "past" },
            
            # Upcoming Events (2025)
            { "name": "Panel discussion with innovation and Start-up Ecosystem Enablers", "date": "21 November 2024", "venue": "MGIT Auditorium, Hyderabad", "overview": "Interactive panel with ecosystem enablers discussing opportunities, challenges, and support for startups at regional, state, and national levels.", "event_type": "upcoming" },
            { "name": "Lean Start-up & Minimum Viable Product/Business – Boot Camp", "date": "25 February 2025", "venue": "MGIT, Hyderabad", "overview": "09:15 AM to 04:15 PM; Speakers: Ayush Kulkarni (Founder, BrightPitch) and Nivas Salla (Founder, LearnApart); Hands-on boot camp and mentoring on lean startup principles and developing MVPs.", "event_type": "upcoming" },
            { "name": "Protecting Intellectual Property Rights (IPRs) and IP Management for Start-ups", "date": "24 April 2025", "venue": "MGIT, Hyderabad", "overview": "01:15 PM to 4:15 PM; Speaker: Dr. Umakanth Choudhury, Professor and Advisor at CBIT; Workshop on IPR protection strategies and IP management essentials for startups.", "event_type": "upcoming" },
            { "name": "Achieving Value Proposition Fit & Business Fit", "date": "30 July 2025", "venue": "MGIT Auditorium, Hyderabad", "overview": "Full session in Quarter IV; Speaker: Dr. K.C. Sabitha, Convener IIC MGIT; Focus on aligning value propositions with business models and market needs.", "event_type": "upcoming" },
            { "name": "Process of Establishing a Startup-NSIC(MSME)", "date": "31 July 2025", "venue": "MGIT, Hyderabad", "overview": "10:00 AM to 12:15 PM; Speaker: Mr. Abdul Khadar, Deputy Manager, NSIC(MSME); Guidance on the step-by-step process of registering and establishing startups under MSME schemes.", "event_type": "upcoming" },
            { "name": "Session on Business Model Canvas", "date": "4 August 2025", "venue": "MGIT, Hyderabad", "overview": "1:00 PM to 4:00 PM; Speaker: Sunil Reddy VemaReddy; Interactive session on using the Business Model Canvas tool for startup planning.", "event_type": "upcoming" },
            { "name": "Session on Achieving Problem-Solution Fit and Product-Market Fit", "date": "4 August 2025", "venue": "MGIT, Hyderabad", "overview": "10:00 AM to 12:30 PM; Speaker: Sunil Reddy VemaReddy; Strategies for validating problem-solution alignment and achieving product-market fit in early-stage ventures.", "event_type": "upcoming" },
            { "name": "Commercialization of Lab Technologies & Technology Transfer", "date": "26 August 2025", "venue": "MGIT, Hyderabad", "overview": "10:00 AM to 1:00 PM; Speaker: N. Venkata Reddy; Overview of innovation processes, technology readiness levels, and commercialization pathways for lab technologies.", "event_type": "upcoming" },
            { "name": "Problem Solving and Ideation Workshop", "date": "26 August 2025", "venue": "MGIT, Hyderabad", "overview": "1:15 PM to 4:15 PM; Speaker: N. Venkata Reddy; Practical workshop on ideation techniques and structured problem-solving for innovative solutions.", "event_type": "upcoming" },
            { "name": "Session on Angel Investment & Venture Capital Funding Opportunity", "date": "29 August 2025", "venue": "MGIT, Hyderabad", "overview": "10:00 AM to 12:30 PM; Speaker: Dr. Shiva Kumar M.P., Associate Professor at IIRM; Insights into funding opportunities via angel investors and VC for early-stage startups.", "event_type": "upcoming" },
            { "name": "B-Plan Pitch: Demo Day & Exhibition", "date": "30 August 2025", "venue": "MGIT, Hyderabad", "overview": "09:30 AM to 4:30 PM; Demo day event for pitching business plans, showcasing innovations, and networking with potential investors.", "event_type": "upcoming" }
        ]
        
        for activity_data in sample_activities:
            activity = Activity(
                name=activity_data["name"],
                date=activity_data["date"],
                venue=activity_data["venue"],
                overview=activity_data["overview"],
                event_type=activity_data["event_type"]
            )
            db.session.add(activity)
    
    # Add sample testimonials
    if Testimonial.query.count() == 0:
        sample_testimonials = [
            Testimonial(name="Shanmukh Satwik", event="B-Plan Pitch: Demo Day", 
                       testimonial="The Demo Day was an incredible platform to showcase our business plan. The feedback from judges and investors was invaluable!", approved=True),
            Testimonial(name="Hasini Jella", event="B-Plan Pitch: Demo Day", 
                       testimonial="Pitching on Demo Day felt like a real investor meeting. The exhibition allowed great networking!", approved=True),
        ]
        for testimonial in sample_testimonials:
            db.session.add(testimonial)
    
    # Add sample contacts
    if Contact.query.count() == 0:
        sample_contacts = [
            Contact(name="K.C. Sabitha", role="Convener", email="kcsabitha_mct@mgit.ac.in", phone="9959827778"),
            Contact(name="Dr. M. Sreevani", role="Vice President", email="msreevani_cse@mgit.ac.in", phone="8790018470"),
            Contact(name="K Bapayya", role="Innovation Activity", email="kbapayya_ece@mgit.ac.in", phone="9912565721"),
        ]
        for contact in sample_contacts:
            db.session.add(contact)
    
    db.session.commit()

# Routes
@app.route('/')
def index():
    # Get all members ordered by display_order first, then by name
    members = Member.query.order_by(Member.display_order, Member.name).all()
    
    # First 5 members (priority roles)
    initial_members = members[:5]
    # Remaining members
    additional_members = members[5:]
    
    # Debug output
    print("=== INITIAL MEMBERS (First 5 - Priority Roles) ===")
    for member in initial_members:
        print(f"Name: {member.name}, Role: {member.role}, Order: {member.display_order}")
    
    print("\n=== ADDITIONAL MEMBERS ===")
    for member in additional_members:
        print(f"Name: {member.name}, Role: {member.role}, Order: {member.display_order}")
    
    print(f"\nTotal members: {len(members)}")
    print(f"Initial members: {len(initial_members)}")
    print(f"Additional members: {len(additional_members)}")
    
    upcoming_activities = Activity.query.filter_by(event_type='upcoming').all()
    past_activities = Activity.query.filter_by(event_type='past').all()
    testimonials = Testimonial.query.filter_by(approved=True).all()
    contacts = Contact.query.all()
    gallery_images = GalleryImage.query.all()
    
    return render_template('index.html', 
                         members=members,
                         initial_members=initial_members,
                         additional_members=additional_members,
                         upcoming_activities=upcoming_activities,
                         past_activities=past_activities,
                         testimonials=testimonials,
                         contacts=contacts,
                         gallery_images=gallery_images)

@app.route('/gallery')
def gallery():
    """Full gallery page showing all images"""
    gallery_images = GalleryImage.query.all()
    return render_template('gallery.html', gallery_images=gallery_images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{filename}"
            
            # Save to appropriate directory based on file type
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                file_path = os.path.join('static/images/uploads', filename)
                file.save(file_path)
                
                # Create gallery entry
                gallery_image = GalleryImage(
                    title=request.form.get('title', 'Untitled'),
                    description=request.form.get('description', ''),
                    image_path=f"images/uploads/{filename}",
                    category=request.form.get('category', 'general')
                )
                db.session.add(gallery_image)
                db.session.commit()
                flash('Image uploaded and added to gallery successfully!', 'success')
            else:
                file_path = os.path.join('static/documents', filename)
                file.save(file_path)
                flash('File uploaded successfully!', 'success')
                
            return redirect(url_for('upload'))
        else:
            flash('Invalid file type. Allowed: images (png, jpg, jpeg, gif) and documents (pdf, doc, docx)', 'error')
    
    uploads = []
    if os.path.exists('static/images/uploads'):
        uploads = os.listdir('static/images/uploads')
    
    return render_template('upload.html', uploads=uploads)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/images/uploads', filename)

@app.route('/documents/<filename>')
def document_file(filename):
    return send_from_directory('static/documents', filename)

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_member', methods=['POST'])
def add_member():
    if request.method == 'POST':
        member = Member(
            name=request.form['name'],
            roll_no=request.form['roll_no'],
            branch=request.form['branch'],
            year_sem=request.form['year_sem'],
            phone=request.form['phone'],
            email=request.form['email'],
            role=request.form['role']
        )
        db.session.add(member)
        db.session.commit()
        flash('Member added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/add_activity', methods=['POST'])
def add_activity():
    if request.method == 'POST':
        activity = Activity(
            name=request.form['name'],
            date=request.form['date'],
            venue=request.form['venue'],
            overview=request.form['overview'],
            event_type=request.form['event_type']
        )
        db.session.add(activity)
        db.session.commit()
        flash('Activity added successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/add_testimonial', methods=['POST'])
def add_testimonial():
    if request.method == 'POST':
        testimonial = Testimonial(
            name=request.form['name'],
            event=request.form['event'],
            testimonial=request.form['testimonial']
        )
        db.session.add(testimonial)
        db.session.commit()
        flash('Testimonial submitted for approval!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_sample_data()
    app.run(debug=True)