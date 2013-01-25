# coding=utf-8
from checkout.models import Order
from django.shortcuts import get_object_or_404
from checkout.reports import render_to_pdf

#from django.template import RequestContext, Template
#from django.http import HttpResponse




def invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render_to_pdf('reports/invoice.html', {
        'order': order,
        'contact': order.owner.contact,
        'pagesize': 'A4',
    }, 'invoice_%s' % order.id)

    #pdf = trml2pdf.parseString(templ.render(con).encode('utf-8'))
    #if os.path.exists(report_file):
    #    parseString(open(report_file).read(), fout='test.pdf')
    #response = HttpResponse(mimetype='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    #response.write(pdf)
    #return response
    #print order
