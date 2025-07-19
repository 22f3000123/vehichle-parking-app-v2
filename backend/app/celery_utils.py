from .celery_instance import celery
from .models import User, ParkingLot, Reservation, db, ParkingSpot
from datetime import datetime, timedelta
import csv
import os
from flask import current_app
from sqlalchemy import func
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from weasyprint import HTML

@celery.task
def send_daily_reminders():
    print("Sending daily reminders...")
    with current_app.app_context():
        users = User.query.all()
        for user in users:
            # Check if user has not booked a spot in the last 7 days
            seven_days_ago = datetime.now() - timedelta(days=7)
            last_reservation = Reservation.query.filter_by(user_id=user.id).filter(Reservation.parking_timestamp >= seven_days_ago).first()

            if not last_reservation:
                print(f"Sending reminder to {user.email}: Don't forget to book your parking spot!")
                try:
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = "Daily Parking Reminder"
                    msg['From'] = current_app.config['MAIL_USERNAME']
                    msg['To'] = user.email

                    text_content = f"Hi {user.first_name},\n\nDon't forget to book your parking spot if you need one today!\n\nBest regards,\nYour Parking App Team"
                    html_content = f"""
                    <html>
                    <head></head>
                    <body>
                        <p>Hi {user.first_name},</p>
                        <p>Don't forget to book your parking spot if you need one today!</p>
                        <p>Best regards,<br>Your Parking App Team</p>
                    </body>
                    </html>
                    """

                    part1 = MIMEText(text_content, 'plain')
                    part2 = MIMEText(html_content, 'html')

                    msg.attach(part1)
                    msg.attach(part2)

                    with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                        server.sendmail(current_app.config['MAIL_USERNAME'], user.email, msg.as_string())
                    print(f"Daily reminder email sent to {user.email}")
                except Exception as e:
                    print(f"Error sending daily reminder email to {user.email}: {e}")
            else:
                print(f"No reminder for {user.email}: Booked recently.")

@celery.task
def generate_monthly_report(user_id):
    print(f"Generating monthly report for user ID: {user_id}")
    with current_app.app_context():
        user = User.query.get(user_id)
        if not user:
            print(f"User with ID {user_id} not found.")
            return "User not found"

        today = datetime.now()
        first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        # Calculate last day of the current month correctly
        if today.month == 12:
            last_day_of_month = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            last_day_of_month = today.replace(month=today.month + 1, day=1) - timedelta(days=1)

        monthly_reservations = Reservation.query.filter_by(user_id=user.id).filter(
            Reservation.parking_timestamp >= first_day_of_month,
            Reservation.parking_timestamp <= last_day_of_month
        ).all()

        total_bookings_month = len(monthly_reservations)
        total_amount_spent_month = sum(res.parking_cost for res in monthly_reservations if res.parking_cost is not None)

        most_used_lot_name = "N/A"
        if monthly_reservations:
            lot_counts = db.session.query(ParkingSpot.lot_id, func.count(ParkingSpot.lot_id)).\
                join(Reservation, Reservation.spot_id == ParkingSpot.id).\
                filter(Reservation.user_id == user.id).\
                filter(Reservation.parking_timestamp >= first_day_of_month).\
                filter(Reservation.parking_timestamp <= last_day_of_month).\
                group_by(ParkingSpot.lot_id).\
                order_by(func.count(ParkingSpot.lot_id).desc()).first()

            if lot_counts:
                most_used_lot_id = lot_counts[0]
                most_used_lot = ParkingLot.query.get(most_used_lot_id)
                if most_used_lot:
                    most_used_lot_name = most_used_lot.name

        report_data = {
            "user_email": user.email,
            "month": today.strftime('%B %Y'),
            "total_bookings_this_month": total_bookings_month,
            "total_amount_spent_this_month": round(total_amount_spent_month, 2),
            "most_used_parking_lot_this_month": most_used_lot_name
        }
        print(f"Generated monthly report for {user.email}: {report_data}")

        # Generate HTML report
        html_content = f"""
        <html>
        <head></head>
        <body>
            <h1>Monthly Parking Activity Report for {user.email}</h1>
            <p>Month: {report_data['month']}</p>
            <p>Total Bookings: {report_data['total_bookings_this_month']}</p>
            <p>Total Amount Spent: ${report_data['total_amount_spent_this_month']:.2f}</p>
            <p>Most Used Parking Lot: {report_data['most_used_parking_lot_this_month']}</p>
            <h2>Your Reservations:</h2>
            <table border="1" style="width:100%; border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>Spot ID</th>
                        <th>Parking Lot</th>
                        <th>Parking Time</th>
                        <th>Leaving Time</th>
                        <th>Cost</th>
                    </tr>
                </thead>
                <tbody>
        """
        for res in monthly_reservations:
            parking_spot = ParkingSpot.query.get(res.spot_id)
            parking_lot_name = ParkingLot.query.get(parking_spot.lot_id).name if parking_spot else "N/A"
            html_content += f"""
                    <tr>
                        <td>{res.spot_id}</td>
                        <td>{parking_lot_name}</td>
                        <td>{res.parking_timestamp.strftime('%Y-%m-%d %H:%M:%S')}</td>
                        <td>{res.leaving_timestamp.strftime('%Y-%m-%d %H:%M:%S') if res.leaving_timestamp else 'N/A'}</td>
                        <td>${res.parking_cost:.2f}</td>
                    </tr>
            """
        html_content += f"""
                </tbody>
            </table>
        </body>
        </html>
        """

        # Generate PDF
        pdf_file = HTML(string=html_content).write_pdf()

        # Send email
        try:
            msg = MIMEMultipart('mixed') # Changed to mixed to allow attachments
            msg['Subject'] = f"Monthly Parking Report - {report_data['month']}"
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = user.email

            # Attach HTML part
            msg.attach(MIMEText(html_content, 'html'))

            # Attach PDF part
            part = MIMEApplication(pdf_file, _subtype="pdf")
            part.add_header('Content-Disposition', 'attachment', filename=f"monthly_report_{report_data['month']}.pdf")
            msg.attach(part)

            with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.sendmail(current_app.config['MAIL_USERNAME'], user.email, msg.as_string())
            print(f"Monthly report email with PDF sent to {user.email}")
        except Exception as e:
            print(f"Error sending monthly report email to {user.email}: {e}")

@celery.task
def export_user_parking_details_csv(user_id):
    print(f"[Celery Task] Starting CSV export for user ID: {user_id}")
    user = User.query.get(user_id)
    if not user:
        print(f"[Celery Task] User with ID {user_id} not found.")
        return "User not found"

    reservations = Reservation.query.filter_by(user_id=user.id).all()
    
    # Construct absolute path
    instance_path = os.path.join(current_app.root_path, 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    file_path = os.path.join(instance_path, f'parking_details_{user.id}.csv')

    print(f"[Celery Task] Attempting to write CSV to: {file_path}")
    try:
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['reservation_id', 'spot_id', 'parking_timestamp', 'leaving_timestamp', 'parking_cost']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for res in reservations:
                writer.writerow({
                    'reservation_id': res.id,
                    'spot_id': res.spot_id,
                    'parking_timestamp': res.parking_timestamp,
                    'leaving_timestamp': res.leaving_timestamp,
                    'parking_cost': res.parking_cost
                })
        print(f"[Celery Task] CSV exported successfully to {file_path}")
        
        # Send email notification to user
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Your Parking Details CSV Export is Ready!"
            msg['From'] = current_app.config['MAIL_USERNAME']
            msg['To'] = user.email

            text_content = f"Hi {user.first_name},\n\nYour parking details CSV export is ready and saved to: {file_path}\n\nBest regards,\nYour Parking App Team"
            html_content = f"""
            <html>
            <head></head>
            <body>
                <p>Hi {user.first_name},</p>
                <p>Your parking details CSV export is ready and saved to: <code>{file_path}</code></p>
                <p>Best regards,<br>Your Parking App Team</p>
            </body>
            </html>
            """

            part1 = MIMEText(text_content, 'plain')
            part2 = MIMEText(html_content, 'html')

            msg.attach(part1)
            msg.attach(part2)

            with smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                server.sendmail(current_app.config['MAIL_USERNAME'], user.email, msg.as_string())
            print(f"CSV export notification email sent to {user.email}")
        except Exception as e:
            print(f"Error sending CSV export notification email to {user.email}: {e}")

    except Exception as e:
        print(f"[Celery Task] Error writing CSV file: {e}")
