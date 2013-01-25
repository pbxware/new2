# coding=utf-8
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
import cStringIO as StringIO
from sx.pisa3 import pisaDocument
import cgi



def render_to_pdf(template_src, context_dict, filename='document'):
    '''
    Renderiza el template con el contexto.
    Envía al cliente la Respuesta HTTP del contenido PDF para
    el template renderizado.
    '''
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO.StringIO()

    pdf = pisaDocument(StringIO.StringIO(html.encode("utf-8")), result, path=settings.REPORT_STATIC, encoding='utf-8')
    if not pdf.err:
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % filename
        response.write(result.getvalue())
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % cgi.escape(html))
