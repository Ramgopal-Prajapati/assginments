from django.core.management.base import BaseCommand
from django.utils import timezone
from assignments.models import CustomUser, Assignment, Notification


class Command(BaseCommand):
    help = 'Create demo users and sample assignments for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🎓 Samyak Computer Classes — Demo Setup\n'))

        # ── Admin ──────────────────────────────────────────────────────────
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@samyak.com',
                password='admin@123',
                first_name='Admin',
                last_name='Samyak',
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Superuser   → admin / admin@123'))
        else:
            self.stdout.write('  ⚠️  admin already exists, skipping.')

        # ── Faculty (Tech) ─────────────────────────────────────────────────
        ram, created = CustomUser.objects.get_or_create(username='ramsir')
        if created:
            ram.set_password('ram@123')
            ram.first_name = 'Ram'
            ram.last_name = 'Sir'
            ram.email = 'ram@samyak.com'
            ram.role = 'faculty'
            ram.category = 'tech'
            ram.student_id = 'FAC-001'
            ram.phone_number = '9988776655'
            ram.address = 'Samyak Computer Classes, Indore'
            ram.is_staff = True
            ram.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Faculty(Tech) → ramsir / ram@123'))
        else:
            self.stdout.write('  ⚠️  ramsir already exists, skipping.')

        # ── Faculty (Non-Tech) ─────────────────────────────────────────────
        priya, created = CustomUser.objects.get_or_create(username='priyamam')
        if created:
            priya.set_password('priya@123')
            priya.first_name = 'Priya'
            priya.last_name = 'Mam'
            priya.email = 'priya@samyak.com'
            priya.role = 'faculty'
            priya.category = 'non_tech'
            priya.student_id = 'FAC-002'
            priya.phone_number = '9911223344'
            priya.is_staff = True
            priya.save()
            self.stdout.write(self.style.SUCCESS('  ✅ Faculty(Non-Tech) → priyamam / priya@123'))

        # ── Students (Tech) ────────────────────────────────────────────────
        students_tech = [
            ('rahul001', 'Rahul',   'Sharma',  'STU-001', 'Python + Django',     '9876543210'),
            ('anita002', 'Anita',   'Verma',   'STU-002', 'Full Stack Web Dev',  '9812345678'),
            ('mohit003', 'Mohit',   'Gupta',   'STU-003', 'React + Node.js',     '9823456789'),
        ]
        for uname, fname, lname, sid, course, phone in students_tech:
            s, created = CustomUser.objects.get_or_create(username=uname)
            if created:
                s.set_password('student@123')
                s.first_name = fname
                s.last_name = lname
                s.email = f'{uname}@student.samyak.com'
                s.role = 'student'
                s.category = 'tech'
                s.student_id = sid
                s.course_name = course
                s.phone_number = phone
                s.save()
                self.stdout.write(self.style.SUCCESS(f'  ✅ Student(Tech)  → {uname} / student@123'))

        # ── Students (Non-Tech) ────────────────────────────────────────────
        students_nontech = [
            ('pooja004', 'Pooja',  'Patel',   'STU-004', 'Tally + Accounting',  '9834567890'),
            ('suresh005','Suresh', 'Yadav',   'STU-005', 'MS Office + DTP',     '9845678901'),
        ]
        for uname, fname, lname, sid, course, phone in students_nontech:
            s, created = CustomUser.objects.get_or_create(username=uname)
            if created:
                s.set_password('student@123')
                s.first_name = fname
                s.last_name = lname
                s.email = f'{uname}@student.samyak.com'
                s.role = 'student'
                s.category = 'non_tech'
                s.student_id = sid
                s.course_name = course
                s.phone_number = phone
                s.save()
                self.stdout.write(self.style.SUCCESS(f'  ✅ Student(Non-Tech) → {uname} / student@123'))

        # ── Sample Assignments ─────────────────────────────────────────────
        rahul = CustomUser.objects.filter(username='rahul001').first()
        anita = CustomUser.objects.filter(username='anita002').first()

        if rahul and ram and not Assignment.objects.filter(assignment_number='ASS-001').exists():
            a1 = Assignment.objects.create(
                assignment_number='ASS-001',
                title='Build a Django REST API',
                details=(
                    'Create a simple REST API using Django REST Framework.\n\n'
                    'Requirements:\n'
                    '1. Set up a Django project with DRF installed.\n'
                    '2. Create a model called "Product" with fields: name, price, description.\n'
                    '3. Build CRUD endpoints for the Product model.\n'
                    '4. Test all endpoints using Postman or curl.\n'
                    '5. Push the code to GitHub.'
                ),
                assigned_by=ram,
                assigned_to=rahul,
                status='pending',
            )
            Notification.objects.create(
                user=rahul,
                message=f"New assignment: '{a1.title}' (#{a1.assignment_number})",
                notification_type='info'
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Sample assignment ASS-001 created'))

        if anita and ram and not Assignment.objects.filter(assignment_number='ASS-002').exists():
            Assignment.objects.create(
                assignment_number='ASS-002',
                title='React Todo Application',
                details=(
                    'Build a fully functional Todo App using React.\n\n'
                    'Requirements:\n'
                    '1. Use functional components with hooks (useState, useEffect).\n'
                    '2. Add, edit, delete, and mark todos as complete.\n'
                    '3. Persist data using localStorage.\n'
                    '4. Style it with CSS Modules or Tailwind CSS.\n'
                    '5. Deploy on Vercel or Netlify and share the link.'
                ),
                assigned_by=ram,
                assigned_to=anita,
                status='pending',
            )
            self.stdout.write(self.style.SUCCESS('  ✅ Sample assignment ASS-002 created'))

        self.stdout.write(self.style.MIGRATE_HEADING('\n── Login Credentials ──────────────────────'))
        self.stdout.write('  Admin      → admin        / admin@123')
        self.stdout.write('  Faculty    → ramsir       / ram@123')
        self.stdout.write('  Faculty    → priyamam     / priya@123')
        self.stdout.write('  Students   → rahul001     / student@123')
        self.stdout.write('             → anita002     / student@123')
        self.stdout.write('             → mohit003     / student@123')
        self.stdout.write('             → pooja004     / student@123')
        self.stdout.write('             → suresh005    / student@123')
        self.stdout.write(self.style.SUCCESS('\n✅ Setup complete! Run: python manage.py runserver\n'))
