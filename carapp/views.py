from datetime import datetime

import requests
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from django_daraja.mpesa.core import MpesaClient

import logging, json

from carapp.forms import NewsletterForm, DriverApplicationForm, CarPurchaseForm
from carapp.models import CarBooking, RideHailing
from dashboard.models import Car, Staff
from royal import settings

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    template_name = 'index.html'
    context = {}
    return render(request, template_name, context)

def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing to our newsletter!")
            return redirect('index')
    else:
        form = NewsletterForm()
    return render(request, 'index.html', {'form': form})

def about(request):
    template_name = 'aboutus.html'
    context = {}
    return render(request, template_name, context)


def apply_as_driver(request):
    if request.method == 'POST':
        form = DriverApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)  # Don't save to DB yet
            application.status = 'Pending'  # Set status programmatically
            application.save()  # Save with status set
            messages.success(request, "Your application has been submitted successfully!")
            return redirect('cardetails')  # Prevent form resubmission
        else:
            messages.error(request, "There was an error with your application. Please try again.")
    else:
        form = DriverApplicationForm()

    return render(request, 'driverapp.html', {'form': form})


# Helper function to get MPESA access token
def get_mpesa_token():
    """Get the MPESA access token using OAuth"""
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth = (settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        response_data = response.json()
        return response_data['access_token']
    else:
        logger.error(f"Failed to get MPESA token: {response.text}")
        return None


def mpesa_callback(request):
    if request.method == "POST":
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body.decode('utf-8'))

            # Log the incoming data for debugging
            logger.debug(f"Callback received: {data}")

            # Extract the necessary fields from the callback response
            stk_callback = data.get('Body', {}).get('stkCallback', {})
            transaction_id = stk_callback.get('CheckoutRequestID')
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')

            # Log the payment result details
            logger.debug(f"Transaction ID: {transaction_id}")
            logger.debug(f"Result Code: {result_code}")
            logger.debug(f"Result Description: {result_desc}")

            # Try to find the booking using transaction_id
            try:
                booking = CarBooking.objects.get(transaction_id=transaction_id)
            except CarBooking.DoesNotExist:
                return JsonResponse({"error": "Booking not found"}, status=404)

            # Handle success or failure
            if result_code == 0:  # Payment was successful
                booking.status = 'Success'
                booking.is_paid = True
                callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                amount = next((item.get('Value') for item in callback_metadata if item.get('Name') == 'Amount'), None)
                mpesa_receipt_number = next(
                    (item.get('Value') for item in callback_metadata if item.get('Name') == 'MpesaReceiptNumber'), None)
                phone_number = next(
                    (item.get('Value') for item in callback_metadata if item.get('Name') == 'PhoneNumber'), None)
                transaction_date_str = next(
                    (item.get('Value') for item in callback_metadata if item.get('Name') == 'TransactionDate'), None)

                if transaction_date_str:
                    transaction_date = timezone.datetime.strptime(transaction_date_str, "%Y%m%d%H%M%S")
                else:
                    transaction_date = None

                # Update booking with payment info
                booking.mpesa_receipt_number = mpesa_receipt_number
                booking.phone_number = phone_number
                booking.transaction_date = transaction_date
                booking.amount = amount
                booking.save()

                logger.debug(
                    f"Payment successful for booking {transaction_id}. Amount: {amount}, MpesaReceipt: {mpesa_receipt_number}, Phone: {phone_number}")

            elif result_code == 1032:  # User cancelled the transaction
                booking.status = 'Terminated'
                booking.description = "Transaction cancelled by user"
                booking.save()
                logger.debug(f"Transaction {transaction_id} terminated by user.")

            else:  # For other failures or unexpected results, initiate payment confirmation
                logger.debug(f"Transaction {transaction_id} failed, Result: {result_desc}. Reconfirming status...")

                # Reconfirm the payment status with the MPESA API if needed
                access_token = get_mpesa_token()
                if not access_token:
                    return JsonResponse({"error": "Failed to retrieve MPESA access token"}, status=500)

                headers = {'Authorization': f'Bearer {access_token}'}
                query_url = f"{MPESA_API_URL}?CheckoutRequestID={transaction_id}"
                mpesa_response = requests.get(query_url, headers=headers)

                if mpesa_response.status_code == 200:
                    mpesa_response_data = mpesa_response.json()

                    # Log the response from MPESA for debugging
                    logger.debug(f"MPESA payment confirmation response: {mpesa_response_data}")

                    # Confirm the payment status
                    if mpesa_response_data.get("Body", {}).get("stkCallback", {}).get("ResultCode") == 0:
                        booking.status = 'Success'
                        booking.is_paid = True
                        logger.debug(f"Payment confirmed for transaction {transaction_id} after recheck.")
                    else:
                        booking.status = 'Failed'
                        booking.description = "Payment failed after retry."
                        logger.debug(f"Payment failure confirmed for transaction {transaction_id}.")
                else:
                    booking.status = 'Failed'
                    booking.description = "Failed to confirm payment with MPESA."
                    logger.error(
                        f"Failed to confirm payment for {transaction_id}. MPESA response: {mpesa_response.text}")

                booking.save()

            return JsonResponse({"message": "Callback processed successfully"}, status=200)

        except Exception as e:
            logger.error(f"Error processing callback: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def book_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date()

        # Create and save the booking initially with a "Pending" status
        booking = CarBooking(
            car=car,
            name=name,
            phone_number=phone_number,
            start_date=start_date,
            end_date=end_date,
            status='Pending'  # Default status before payment
        )
        booking.save()

        # Initiate STK Push
        client = MpesaClient()
        amount = int(booking.deposit)  # Assuming deposit is defined in the model
        account_reference = f'CarBooking-{booking.id}'
        transaction_desc = f'Car booking deposit for {car.name}'
        callback_url = 'https://51e-41-90-176-35.ngrok-free.app/carapp/mpesa-callback/'

        response = client.stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=account_reference,
            transaction_desc=transaction_desc,
            callback_url=callback_url
        )

        # Handle response from Mpesa
        if response.response_description == 'Success' and response.redirect_url:
            # If STK push is successful, redirect the user to the payment page
            booking.status = 'Payment Initiated'
            booking.transaction_time = timezone.now()
            booking.save()
            return render(request, 'payment_prompt_sent.html', {
                'booking': booking,
                'phone_number': phone_number,
                'car': car,
                'redirect_url': response.redirect_url  # Include the redirect URL for M-Pesa
            })
        elif response.response_description == 'Terminated':
            # If the user terminated the payment initiation
            booking.status = 'Terminated'
            booking.transaction_time = timezone.now()
            booking.save()
            return render(request, 'payment_failed.html', {
                'message': 'Payment was terminated by the user.',
                'car': car
            })
        else:
            # If failed initiation
            booking.status = 'Failed'
            booking.transaction_time = timezone.now()
            booking.save()
            return render(request, 'payment_failed.html', {
                'message': response.error_message,
                'car': car
            })

    return render(request, 'bookcar.html', {'car': car})

def payment_prompted(request):
    return render(request, "payment_prompt_sent.html")
def payment_terminated(request):
    return render(request, "payment_terminated.html")
def payment_success(request):
    return render(request, "payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")


def book_road_test(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        form = CarPurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.car = car
            purchase.save()
            messages.success(request, 'Road test booked successfully!')
            return redirect('cardetails') # Redirect to a car detail page
    else:
        form = CarPurchaseForm()

    return render(request, 'book_road_test.html', {'form': form, 'car': car})

def services(request):
    template_name = 'services.html'
    context = {}
    return render(request, template_name, context)

def cardetails(request):
    cars = Car.objects.all()
    template_name = 'cars.html'
    context = {'cars': cars}
    return render(request, template_name, context)


def ridehail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        pickup_location = request.POST['pickup_location']
        pickup_latitude = request.POST['pickup_latitude']
        pickup_longitude = request.POST['pickup_longitude']
        dropoff_location = request.POST['dropoff_location']
        dropoff_latitude = request.POST['dropoff_latitude']
        dropoff_longitude = request.POST['dropoff_longitude']
        pickup_date = request.POST['pickup_date']
        pickup_time = request.POST['pickup_time']

        RideHailing.objects.create(
            car=car,
            pickup_location=pickup_location,
            pickup_latitude=pickup_latitude,
            pickup_longitude=pickup_longitude,
            dropoff_location=dropoff_location,
            dropoff_latitude=dropoff_latitude,
            dropoff_longitude=dropoff_longitude,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
        )

        return redirect('cardetails')  # Define this URL for a success message

    return render(request, 'ridehailing.html', {'car': car})

def team_view(request):
    staff_members = Staff.objects.all()  # Fetch all staff members
    context= {'staff_members': staff_members}
    template_name = 'team.html'
    return render(request, template_name, context)