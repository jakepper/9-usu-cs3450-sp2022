from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import JobPostForm
from .forms import ReviewPostForm

# Responsible for creating the view a user sees when navigating to their customer page.

def empty(request):
    return redirect('/yardsite/home')

@login_required(login_url='/accounts/login')
def home(request):
    filters = []
    checked = []
    qs = Job.objects.all().filter(available=True)
    for job_type,name in Job.JOB_TYPES:
        if request.GET.get(job_type) != 'on':
            filters.append(job_type)
        else:
            checked.append(job_type)
    if len(checked) > 0:
        for filter in filters:
            qs = qs.exclude(job_type=filter)

    if request.GET.get('zip') == 'on':
        qs = qs.filter(zip_code=request.user.zip_code)
        checked.append('zip')

    return render(request, 'yardSite/home.html', { 'queryset': qs, 'checked': checked })

@login_required(login_url='/accounts/login')
def CustomerDashboard(request):

    if request.method == 'POST':
        user = request.user
        if(request.POST.get("Add")):
            sumToAdd = int(request.POST.get("Add"))
            user.wallet += sumToAdd
        elif(request.POST.get("Withdraw")):
            sumToSub = int(request.POST.get("Withdraw"))
            if (user.wallet >= sumToSub):
                user.wallet -= sumToSub
        user.save()
        return redirect('/yardsite/customer')
    else:
        # Grab the customer that is tied to the logged in user
        currentUserCustomerProfile = request.user.customer
        review_list = Review.objects.filter(reviewee=request.user).exclude(isCustomer_bool = False)

        
        pending_jobs = Job.objects.filter(customer=currentUserCustomerProfile).filter(available=True).filter(completed=False)
        progressing_jobs = Job.objects.filter(customer=currentUserCustomerProfile).filter(available=False).filter(completed=False)
        completed_jobs = Job.objects.filter(customer=currentUserCustomerProfile).filter(completed=True)

        context = {
            'pending_jobs': pending_jobs,
            'progressing_jobs': progressing_jobs,
            'completed_jobs': completed_jobs,
            'customerReviews': review_list,
            'currentCustomer' : currentUserCustomerProfile,
        }
        return render(request, 'yardSite/customerDashboard.html', context)

@login_required(login_url='/accounts/login')
def WorkerDashboard(request):
    w_user = request.user
    w_name = w_user.get_full_name()
    worker = w_user.worker
    wallet = w_user.wallet

    if request.method == 'POST':
        user = request.user
        if(request.POST.get("Withdraw")):
            sumToSub = int(request.POST.get("Withdraw"))
            if (user.wallet >= sumToSub):
                user.wallet -= sumToSub
        user.save()
        return redirect('/yardsite/worker')

    # Gets available jobs that weren't posted by this user
    #available_jobs = Job.objects.filter(available=True).filter(completed=False).exclude(customer=w_user.customer)
    review_list = Review.objects.filter(reviewee=w_user).exclude(isCustomer_bool = True)
    
    job_list = Job.objects.filter(worker=worker).filter(completed=False)
    completed_job_list = Job.objects.filter(worker=worker).filter(completed=True)
    context = {
        'name': w_name,
        'assigned': job_list,
        #'available': available_jobs,
        'completed': completed_job_list,
        'workerReviews': review_list,
        'wallet' : wallet,
    }
    return render(request, 'yardSite/workerDashboard.html', context)

@login_required(login_url='/accounts/login')
def OwnedJobDetails(request, job_id):
    requested_job = Job.objects.filter(id=job_id)[0]
    currentUserCustomerProfile = request.user.customer

    can_assign_to_self = True
    can_edit = False
    if requested_job.customer == currentUserCustomerProfile:
        can_assign_to_self = False
        can_edit = True
    # can_assign_to_self should only be True if the user is accessing the job as a worker. can_edit same
    # except for as customer
    context = {
        'can_assign': can_assign_to_self,
        'can_edit': can_edit,
        'job': requested_job
    }

    return render(request, 'yardSite/ownedJobDetails.html', context)

@login_required(login_url='/accounts/login')
def accepted_job(request, job_id):
    accepted_job = Job.objects.filter(id=job_id)[0]
    currentUserWorkerProfile = request.user.worker

    accepted_job.available = False
    accepted_job.worker = currentUserWorkerProfile
    accepted_job.save()

    context = {
        'job': accepted_job
    }

    return render(request, 'yardSite/acceptedJob.html', context)

@login_required(login_url='/accounts/login')
def finish_job(request, job_id):
    completed_job = Job.objects.filter(id=job_id)[0]

    completed_job.completed = True

    workerUser = CustomUser.objects.get(id=completed_job.worker.user.id)
    customerUser = CustomUser.objects.get(id=completed_job.customer.user.id)

    # Calculate the different cuts
    totalReward = int(completed_job.cash_reward)
    ownerCut = totalReward * 0.1
    workerCut = totalReward - ownerCut

    # Add or subtract cuts from the appropriate users
    workerUser.wallet += workerCut
    customerUser.user.wallet -= totalReward

    # Save changes
    workerUser.save()
    customerUser.save()
    completed_job.save()

    context = {
        'job': completed_job
    }

    return render(request, 'yardSite/finishJob.html', context)

@login_required(login_url='/accounts/login')
def create_job_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = request.user.get_full_name()
            instance.zip_code = request.user.zip_code
            instance.customer = request.user.customer
            instance.save()
            return redirect('/yardsite/customer')
        else: 
            print(form.errors)
    else:
        form = JobPostForm()
    return render(request, 'yardSite/create-job-post.html', { 'form': form })

@login_required(login_url='/accounts/login')
def editJob(request, job_id):
    requested_job = Job.objects.filter(id=job_id)[0]

    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=requested_job)
        if form.is_valid():
            form.save()
            return redirect('/yardsite/customer')
        else: 
            print(form.errors)
    else:
        form = JobPostForm(instance=requested_job)

    context = {
        'job': requested_job,
        'form': form
    }

    return render(request, 'yardSite/editJob.html', context)

@login_required(login_url='/accounts/login')
def customer_create_review_post(request, job_id):
    requested_job = Job.objects.filter(id=job_id)[0]

    if request.method == 'POST':
        form = ReviewPostForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.reviewerName_text = request.user.get_full_name()
            instance.job = requested_job
            instance.published_date = datetime.datetime.now()
            instance.reviewee = requested_job.worker.user
            instance.isCustomer_bool = False
            instance.save()
            return redirect('/yardsite/home')
        else:
            print(form.errors)
    else: 
        form = ReviewPostForm(instance=requested_job)
    return render(request, 'yardsite/create-review-post.html', { 'form': form })

@login_required(login_url='/accounts/login')
def create_review_post(request, job_id):
    requested_job = Job.objects.filter(id=job_id)[0]

    if request.method == 'POST':
        form = ReviewPostForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.reviewerName_text = request.user.get_full_name()
            instance.job = requested_job
            instance.published_date = datetime.datetime.now()
            instance.reviewee = requested_job.customer.user
            instance.isCustomer_bool = True
            instance.save()
            return redirect('/yardsite/home')
        else:
            print(form.errors)
    else: 
        form = ReviewPostForm(instance=requested_job)
    return render(request, 'yardsite/create-review-post.html', { 'form': form })

@login_required(login_url='/accounts/login')
def editReview(request, review_id):
    requested_review = Job.objects.filter(id=job_id)[0]

    if request.method == 'POST':
        form = ReviewPostForm(request.POST, instance=requested_job)
        if form.is_valid():
            form.save()
            return redirect('/customer')
        else:
            print(form.errors)
    else:
        form = ReviewPostForm(instance=requested_review)

    context = {
        'review': requested_job,
        'form': form
    }

    return render(request, 'yardSite/editReview.html', context)

@login_required(login_url='/accounts/login')
def OwnedReviewDetails(request, review_id):
    requested_review = Review.objects.filter(id=review_id)[0]

    can_assign_to_self = True
    context = {
        'review': requested_review
    }

    return render(request, 'yardSite/ownedReviewDetails.html', context)

@login_required(login_url='/accounts/login')
def SentReviewDetails(request, review_id):
    requested_review = Review.objects.filter(id=review_id)[0]

    context = {
        'review': requested_review
    }

    return render(request, 'yardSite/sentReviewDetails.html', context)
