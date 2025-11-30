from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import CreateView
from .models import Client
from .forms import ClientForm
import csv, os 
from django.shortcuts import render
from django.contrib import messages
from .forms import CsvUploadForm
from .models import Client
from chardet.universaldetector import UniversalDetector
from .email import send_client_email, send_test_email
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone


# List View for Clients
class ClientListView(ListView):
    model = Client
    template_name = 'clientmanage/client_list.html'  # Template for listing clients
    context_object_name = 'clients'  # Name to use in the template for the clients list
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_number = self.request.GET.get('page', 1)
        context['current_page'] = page_number
        
        return context

# Update View for Clients
class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clientmanage/client_form.html'  # Template for editing a client
    context_object_name = 'client'
    success_url = reverse_lazy('clientmanage:client_list')  # Redirect to the client list after successful update

    def get_object(self):
        # Retrieve the Client object by its pk, passed in the URL
        return get_object_or_404(Client, pk=self.kwargs.get('pk'))
    
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clientmanage/client_form.html'  # Reuse the same template for creation
    success_url = reverse_lazy('clientmanage:client_list')  # Redirect to client list after creation

def confirm_email_send(request, pk):
    client = get_object_or_404(Client, id=pk)
    return render(request, 'clientmanage/confirm_send_email', client)

def email_send(request, pk, pg):
    client = get_object_or_404(Client, id=pk)

    if request.method == "POST" and request.POST.get("confirm") == "yes":

        if client.eng == True:
            email_send_e(request, pk)
            return redirect(f"/?page={pg}")

        cName = client.companyName
        sirName = client.sirName
        givenName = client.givenName
        email_to_send = [client.email]

        from email.utils import formataddr
        settings.DEFAULT_FROM_EMAIL = formataddr(('ソリトンキャピタル|紺野', 'web@soliton-cm.com'))

        html_content = render_to_string(
            'clientmanage/content2026.html',
            {'client':client, 'cName':cName, 'sirName':sirName, 'givenName':givenName}
        )
        # Send email notification
        subject = "新年のご挨拶|ソリトンキャピタル"
        image_path = os.path.join(settings.MEDIA_ROOT, '2026ny.jpg')
        # image_path = settings.MEDIA_URL + '2025_main.jpg'

        if request.GET.get("name") == "test":
            print("now passing test route //////////////////////////////////////////")
            send_test_email(
                    subject=subject, 
                    body='',
                    to=["konno.kenji@gmail.com"],
                    cc=["kkonno@soliton-cm.com"],
                    html_content=html_content,
                    # image_path=image_path,
                    )
        else:
            send_client_email(
                    subject=subject, 
                    body='', 
                    to=email_to_send,
                    cc=["kkonno@soliton-cm.com"],
                    html_content=html_content,
                    # image_path=image_path,
                    )
            print("now passing NORMAL route =======================")
            client.emailSend = True
            client.emailSendStamp = timezone.now()
            client.save()
        
        return redirect(f"/?page={pg}")
        # return redirect("clientmanage:client_list")
    
    return render(request, 'clientmanage/confirm_send_email.html', {'client': client, 'pg':pg})

def email_send_e(request, pk):
    client = get_object_or_404(Client, id=pk)

    cName = client.companyName
    sirName = client.sirName
    givenName = client.givenName
    email_to_send = [client.email]

    from email.utils import formataddr
    settings.DEFAULT_FROM_EMAIL = formataddr(('Kenji Konno|SCM', 'web@soliton-cm.com'))

    html_content = render_to_string(
        'clientmanage/content2026_eng.html',
        {'client':client, 'cName':cName, 'sirName':sirName, 'givenName':givenName}
    )
    # Send email notification
    subject = "Happy New Year from SOLITON Capital"
    image_path = os.path.join(settings.MEDIA_ROOT, '2026ny.jpg')
    # image_path = settings.MEDIA_URL + '2025_main.jpg'

    if request.GET.get("name") == "test":
        print("now passing ENG test route //////////////////////////////////////////")
        send_test_email(
                subject=subject, 
                body='',
                to=["konno.kenji@gmail.com"],
                cc=["kkonno@soliton-cm.com"],
                html_content=html_content,
                # image_path=image_path,
                )
    else:
        send_client_email(
                subject=subject, 
                body='', 
                to=email_to_send,
                cc=["kkonno@soliton-cm.com"],
                html_content=html_content,
                # image_path=image_path,
                )
        print("now passing ENG NORMAL route =======================")
        client.emailSend = True
        client.emailSendStamp = timezone.now()
        client.save()


    return redirect('clientmanage:client_list')

def detect_encoding(file):
    detector = UniversalDetector()
    for line in file:
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    file.seek(0)  # Reset file pointer
    return detector.result['encoding']


def handle_uploaded_file(f):
    # Assuming the file is encoded in UTF-8 (handle Japanese characters)
    encoding = detect_encoding(f)
    print(f"Detected file encoding: {encoding}")
    
    decoded_file = f.read().decode(encoding)
    csv_data = csv.reader(decoded_file.splitlines())

    # Skip header row if necessary
    # next(csv_data)  

    for row in csv_data:
        if len(row) > 1:  # Ensure there's data in the row
            Client.objects.create(
                companyName=row[0],
                divisionName=row[1],
                titleName=row[2],
                sirName=row[3],
                givenName=row[4],
                postCode=row[5],
                address1=row[6],
                address2=row[7],
                tel=row[8],
                cell=row[9],
                email=row[10],
                email2=row[11],
                note=row[12],
            )

def upload_csv(request):
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if a file has been uploaded
            if 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']
                
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'The file is not a CSV file.')
                else:
                    try:
                        handle_uploaded_file(csv_file)
                        messages.success(request, 'CSV file uploaded and data saved successfully.')
                    except Exception as e:
                        messages.error(request, f'Error uploading CSV file: {e}')
            else:
                messages.error(request, 'No CSV file uploaded.')
        else:
            messages.error(request, 'Form is not valid.')
        
        return render(request, 'clientmanage/upload.html', {'form': form})

    form = CsvUploadForm()
    return render(request, 'clientmanage/upload.html', {'form': form})


    # email_preview = f"<h3>Email Preview</h3><p><strong>Subject:</strong> {subject}</p>"
    # email_preview += f"<p><strong>HTML Content:</strong><br>{html_content}</p>"
    # email_preview += f"<p><strong>Image:</strong><br><img src='{image_path}' alt='Embedded Image' style='max-width: 300px;'></p>"
    # email_preview += f"<p><strong>Image Path:</strong> {image_path}</p>"