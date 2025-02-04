import streamlit as st
import requests

# Title of the application
st.title("Hotel Booking Cancellation Predictor")
st.markdown("""
This application predicts whether a hotel booking is likely to be **canceled** or **confirmed** based on various booking details.
Fill in the required details and click on **Predict Cancellation** to get the prediction result.
""")

# User Inputs with Descriptions
st.subheader("Booking Details")

hotel = st.selectbox("Hotel Type", ["City Hotel", "Resort Hotel"], help="Select the type of hotel for the booking.")
lead_time = st.number_input("Lead Time (days)", min_value=0, help="Number of days between the booking date and the arrival date.")
arrival_date_year = st.selectbox("Arrival Year", [2015, 2016, 2017], help="Year when the guest is expected to arrive.")
arrival_date_month = st.selectbox("Arrival Month", ["January", "February", "March", "April", "May"], help="Month of arrival.")
arrival_date_week_number = st.number_input("Week Number", min_value=1, max_value=53, help="Week number of the year when the guest is arriving.")
arrival_date_day_of_month = st.number_input("Day of Month", min_value=1, max_value=31, help="Exact day of the month when the guest will arrive.")

st.subheader("Stay Duration")
stays_in_weekend_nights = st.number_input("Weekend Nights", min_value=0, help="Number of weekend nights (Friday or Saturday) the guest will stay.")
stays_in_week_nights = st.number_input("Week Nights", min_value=0, help="Number of weekday nights (Sunday to Thursday) the guest will stay.")

st.subheader("Guest Information")
adults = st.number_input("Number of Adults", min_value=1, help="Number of adult guests.")
children = st.number_input("Number of Children", min_value=0, help="Number of children included in the booking.")
babies = st.number_input("Number of Babies", min_value=0, help="Number of babies included in the booking.")
meal = st.selectbox("Meal Type", ["BB", "FB", "HB", "SC", "Undefined"], help="Meal plan chosen by the guest.")

st.subheader("Booking Information")
market_segment = st.selectbox("Market Segment", ["Online TA", "Offline TA/TO", "Groups", "Direct", "Corporate", "Complementary"], help="How the booking was made.")
distribution_channel = st.selectbox("Distribution Channel", ["TA/TO", "Direct", "Corporate", "Undefined"], help="Distribution channel through which the booking was made.")
is_repeated_guest = st.radio("Repeated Guest?", [0, 1], help="Indicates if the guest has stayed at the hotel before.")
previous_cancellations = st.number_input("Previous Cancellations", min_value=0, help="Number of previous bookings canceled by the guest.")
previous_bookings_not_canceled = st.number_input("Previous Non-Canceled Bookings", min_value=0, help="Number of previous bookings not canceled by the guest.")
reserved_room_type = st.selectbox("Reserved Room Type", list("ABCDEFGHIJL"), help="Room type reserved by the guest.")
assigned_room_type = st.selectbox("Assigned Room Type", list("ABCDEFGHIJL"), help="Room type actually assigned to the guest.")
booking_changes = st.number_input("Booking Changes", min_value=0, help="Number of changes made to the booking.")
deposit_type = st.selectbox("Deposit Type", ["No Deposit", "Non Refund", "Refundable"], help="Type of deposit made at the time of booking.")

st.subheader("Agent & Company Details")
agent = st.number_input("Agent ID", min_value=0, help="ID of the travel agency that handled the booking (if applicable).")
company = st.number_input("Company ID", min_value=0, help="ID of the company that made the booking (if applicable).")
days_in_waiting_list = st.number_input("Days in Waiting List", min_value=0, help="Number of days the booking was on the waiting list before being confirmed.")
customer_type = st.selectbox("Customer Type", ["Transient", "Contract", "Transient-Party", "Group"], help="Category of the customer.")
adr = st.number_input("Average Daily Rate (ADR)", min_value=0.0, help="Revenue per occupied room per night.")
required_car_parking_spaces = st.number_input("Required Car Parking Spaces", min_value=0, help="Number of car parking spaces required by the guest.")
total_of_special_requests = st.number_input("Total Special Requests", min_value=0, help="Number of special requests made by the guest (e.g., extra pillows, room location, etc.).")
country = st.text_input("Country", "PRT", help="Country of the guest.")

# Create JSON payload
data = {
    "hotel": hotel,
    "lead_time": lead_time,
    "arrival_date_year": arrival_date_year,
    "arrival_date_month": arrival_date_month,
    "arrival_date_week_number": arrival_date_week_number,
    "arrival_date_day_of_month": arrival_date_day_of_month,
    "stays_in_weekend_nights": stays_in_weekend_nights,
    "stays_in_week_nights": stays_in_week_nights,
    "adults": adults,
    "children": children,
    "babies": babies,
    "meal": meal,
    "market_segment": market_segment,
    "distribution_channel": distribution_channel,
    "is_repeated_guest": is_repeated_guest,
    "previous_cancellations": previous_cancellations,
    "previous_bookings_not_canceled": previous_bookings_not_canceled,
    "reserved_room_type": reserved_room_type,
    "assigned_room_type": assigned_room_type,
    "booking_changes": booking_changes,
    "deposit_type": deposit_type,
    "agent": agent,
    "company": company,
    "days_in_waiting_list": days_in_waiting_list,
    "customer_type": customer_type,
    "adr": adr,
    "required_car_parking_spaces": required_car_parking_spaces,
    "total_of_special_requests": total_of_special_requests,
    "country": country
}

if st.button("Predict Cancellation"):
    response = requests.post("http://127.0.0.1:5000/predict", json=data)
    
    if response.status_code == 200:
        prediction = response.json().get("prediction", "Error: No prediction received")
        
        if prediction == 1:
            st.error("⚠️ Booking is likely to be CANCELED!")
        else:
            st.success("✅ Booking is likely to be CONFIRMED!")
    else:
        st.error(f"API Error: {response.text}")
