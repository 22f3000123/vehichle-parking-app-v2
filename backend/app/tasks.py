from flask import render_template
from celery import shared_task
from flask_mailman import EmailMessage
from .models import User, Reservation, ParkingLot
from datetime import datetime, timedelta
import csv
import io


@shared_task
def send_daily_reminders():
    yesterday = datetime.now() - timedelta(days=1)
    users_to_remind = User.query.filter(
        ~User.reservations.any(Reservation.parking_timestamp > yesterday)
    ).all()
    print(users_to_remind)

    for user in users_to_remind:
        msg = EmailMessage(
            "We miss you!",
            "You haven't booked a parking spot in the last 24 hours. Book now!",
            to=[user.email],
        )
        msg.send()


@shared_task
def generate_monthly_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return

    today = datetime.now()
    last_month = today - timedelta(days=30)

    reservations = Reservation.query.filter(
        Reservation.user_id == user_id, Reservation.parking_timestamp >= last_month
    ).all()

    total_bookings = len(reservations)
    total_amount_spent = sum(r.parking_cost or 0 for r in reservations)

    lot_usage = {}
    for res in reservations:
        spot = ParkingLot.query.get(res.spot_id)
        if spot:
            lot_id = spot.lot_id
            lot_usage[lot_id] = lot_usage.get(lot_id, 0) + 1

    most_used_lot = None
    if lot_usage:
        most_used_lot_id = max(lot_usage, key=lot_usage.get)
        most_used_lot = ParkingLot.query.get(most_used_lot_id).name

    html_content = render_template(
        "monthly_report.html",
        user=user,
        total_bookings=total_bookings,
        total_amount_spent=total_amount_spent,
        most_used_lot=most_used_lot,
    )

    msg = EmailMessage("Your Monthly Parking Report", html_content, to=[user.email])
    msg.content_subtype = "html"
    msg.send()


@shared_task
def export_reservations_as_csv(user_id):
    user = User.query.get(user_id)
    if not user:
        return

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "Reservation ID",
            "Spot ID",
            "Parking Lot",
            "Parking Timestamp",
            "Leaving Timestamp",
            "Cost",
        ]
    )

    for res in reservations:
        parking_lot_name = ""
        if res.spot:
            parking_lot_name = res.spot.parking_lot.name
        writer.writerow(
            [
                res.id,
                res.spot_id,
                parking_lot_name,
                res.parking_timestamp,
                res.leaving_timestamp,
                res.parking_cost,
            ]
        )

    csv_data = output.getvalue()

    msg = EmailMessage(
        "Your Reservation Data",
        "Here is your reservation data as a CSV file.",
        to=[user.email],
    )
    msg.attach("reservations.csv", csv_data, "text/csv")
    msg.send()
