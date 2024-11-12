from django.shortcuts import render,redirect
from .models import Medicine,Customer,Prescription,Sales
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum,Count
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .forms import PrescriptionForm
from django.utils import timezone
from .forms import CustomerForm
 


def home1(request):
    return render(request,'home.html',{'msg':"welcome  to DIGIPHARMA"})
def userpage(request):
    return render(request,'login.html')
def welcome(request):
    return render(request,'welcome.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Both username and password are required.")
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request,'welcome.html')  # Replace 'home' with your homepage or dashboard URL
            else:
                messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')

    return render(request, 'register.html')

def medicine_list(request):
    # Retrieve all medicines that are available (e.g., stock > 0)
    medicines = Medicine.objects.filter(stock__gt=0)
    return render(request, 'medicine_list.html', {'medicines': medicines})

def medicine_detail(request, medicine_id):
    # Retrieve the specific medicine based on its ID
    medicine = get_object_or_404(Medicine, id=medicine_id)
    return render(request, 'medicine_detail.html', {'medicine': medicine})

def buy_medicine(request):
    medicines = Medicine.objects.all()
    if request.method == "POST":
        selected_medicine_ids = request.POST.getlist('medicine_ids')
        payment_method = request.POST.get('payment_method')
        total_amount = Decimal(0)
        purchased_medicines = []

        for med_id in selected_medicine_ids:
            medicine = Medicine.objects.get(id=med_id)
            total_amount += medicine.price
            purchased_medicines.append(medicine)
            Sales.objects.create(
                customer=request.user.customer,
                medicine=medicine,
                total_amount=medicine.price,
                 sale_date=timezone.now(),
                payment_method=payment_method  # Set default payment or allow user to choose
            )

        request.session['total_amount'] = str(total_amount)
        request.session['payment_method'] = payment_method
        return redirect('view_invoice')

    return render(request, 'buy_medicine.html', {'medicines': medicines})


def view_invoice(request):
    total_amount = request.session.get('total_amount')
    payment_method = request.session.get('payment_method')
    return render(request, 'view_invoice.html',
    {
        'total_amount': total_amount,
        'payment_method': payment_method
    })


def manage_prescriptions(request):
    # Get the prescriptions for the logged-in customer
    prescriptions = Prescription.objects.filter(customer__user=request.user)
    return render(request, 'manage_prescriptions.html', {'prescriptions': prescriptions})

def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)  # Create an instance but don't save to the database yet
            prescription.customer = request.user.customer  # Assign the logged-in customer
            prescription.save()  # Save the prescription instance
            form.save_m2m()  # Save the many-to-many relationship for medicines
            return redirect('manage_prescriptions')  # Redirect to the prescription management page
    else:
        form = PrescriptionForm()  # Instantiate the form for GET request

    return render(request, 'create_prescription.html', {'form': form})


def prescription_success(request, prescription_id):
    prescription = Prescription.objects.get(id=prescription_id)
    return render(request, 'prescription_success.html', {'prescription': prescription})

def sales_details(request):
    sales = Sales.objects.all()
    total_sales_amount = sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    # Calculate most salable medicine
    most_salable_medicine = (
        Sales.objects.values('medicine')
        .annotate(total_quantity=Count('id'), total_profit=Sum('total_amount'))
        .order_by('-total_profit')
        .first()
    )

    # Retrieve medicine instance for the most salable medicine
    most_profitable_medicine = None
    most_profitable_medicine_profit = 0
    if most_salable_medicine:
        medicine_id = most_salable_medicine['medicine']
        most_profitable_medicine = Medicine.objects.get(id=medicine_id)
        most_profitable_medicine_profit = most_salable_medicine['total_profit'] 
    return render(request, 'sales_details.html', {
        'sales': sales,
        'total_sales_amount': total_sales_amount,
        'most_profitable_medicine': most_profitable_medicine,
        'most_profitable_medicine_profit': most_profitable_medicine_profit,  
    })
def medicine_stock_availability(request):
    medicines = Medicine.objects.all()  # Fetch all medicines
    return render(request, 'medicine_stock.html', {'medicines': medicines})

def search_medicines(request):
    query = request.GET.get('q', '')  # Get the search query from the URL
    if query:
        # Filter medicines based on the search query
        medicines = Medicine.objects.filter(name__icontains=query)
    else:
        # If there's no query, return all medicines
        medicines = Medicine.objects.all()
    
    return render(request, 'search_medicines.html', {'medicines': medicines, 'query': query})


def recent_purchases(request):
    if request.user.is_authenticated:
        # Get the sales for the logged-in customer, ordered by sale date
        recent_sales = Sales.objects.filter(customer=request.user.customer).order_by('-sale_date')[:5]  # Adjust the number as needed
    else:
        recent_sales = []

    return render(request, 'recent_purchases.html', {'recent_sales': recent_sales})
def profile_management(request):
    customer = request.user.customer  # Get the customer's profile
    
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer_instance = form.save(commit=False)  # Get the updated customer instance
            
            # Update the username if necessary
            if request.user.username != customer_instance.name:  # Assuming you want the name as the username
                request.user.username = customer_instance.name
                request.user.save()  # Save the user instance to update the username
            
            customer_instance.save()  # Save the updated customer profile
            
            messages.success(request, "Your profile has been updated successfully!")  # Success message
            return redirect('profile_management')  # Redirect to the same page after saving
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'profile_management.html', {'form': form})

def happy_customers(request):
    customers = Customer.objects.all()  # Get all customers who have used the application
    return render(request, 'happy_customers.html', {'customers': customers})
from django.shortcuts import render

def feedback_view(request):
    if request.method == "POST":
        feedback_text = request.POST.get('feedback_text')
        # You can process feedback_text as needed, but it won't be saved in a model
        return render(request, 'thank_you.html')  # Show thank you message
    
    return render(request, 'feedback.html')  # Show the feedback form
def about_page(request):
    return render(request, 'about.html')