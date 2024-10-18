from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def index(request):
    if request.method == 'POST':
        # Retrieve the uploaded file from the request
        uploaded_file = request.FILES['document']
        
        # Read the file using Pandas
        df = pd.read_excel(uploaded_file)
        
        # Summary Report: Group by 'Cust State'
        summary = df.groupby('Cust State').agg(
            total_customers=('Cust Pin', 'count'),  # Total number of customers per state
            total_dpd=('DPD', 'sum'),               # Total DPD per state
            avg_dpd=('DPD', 'mean')                 # Average DPD per state
        ).reset_index()
        
        # Convert summary to plain text for email
        summary_str = summary.to_string(index=False)

        # Rename 'Cust State' to 'Cust_State' to avoid issues in the template
        summary = summary.rename(columns={'Cust State': 'Cust_State'})

        # Send the summary via email
        send_mail(
            subject='Python Assignment - Vasu Gadde',  # Replace with your name
            message=f"Summary Report:\n\n{summary_str}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['vasugadde1234@gmail.com'],
        )
        
        # Convert summary data into a list of dictionaries to pass to the template
        summary_data = summary.to_dict(orient='records')

        # Pass the summary data to the 'summary.html' template for display
        return render(request, 'upload/summary.html', {'summary': summary_data})

    # If no POST request, render the form
    return render(request, 'upload/index.html')
