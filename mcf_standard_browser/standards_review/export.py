import time
from django.http import FileResponse, HttpResponse
from collections import defaultdict
from django.conf import settings
import zipfile
from django.template import loader
from tempfile import TemporaryFile
from django.core.urlresolvers import reverse
import os
import logging
import datetime

def write_massbank(fn, spec_pairs):
    logging.debug("writing massbank file %s", fn)
    fn_counter = defaultdict(int)  # counts filename occurence for disambiguation
    zf_n = open(fn, 'wb')
    with zipfile.ZipFile(zf_n, mode="w") as zf:
        for spectrum, peak_list in spec_pairs:
            if spectrum.standard:
                ambiguous_fn = "Inventory_ID{}".format(spectrum.standard.inventory_id)
            else:
                ambiguous_fn = 'unknown_standard'
            export_filename = "{}_{}.txt".format(ambiguous_fn, fn_counter[ambiguous_fn])
            fn_counter[ambiguous_fn] += 1
            t = loader.get_template('mcf_standards_browse/export_template_massbank.txt')
            timestamp = time.localtime(time.time())
            full_url = settings.SITE_URL + reverse('fragmentSpectrum-detail', args=(spectrum.pk,))
            r = t.render({'spectrum': spectrum, 'peak_list': peak_list, 'num_peak': len(peak_list),
                          'settings': settings,
                          'info': {
                              'url': full_url,
                              'ion_mode': 'POSITIVE' if spectrum.adduct.charge > 0 else 'NEGATIVE'}
                          })

            info = zipfile.ZipInfo(export_filename, date_time=timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.comment = 'generated by curatr'
            info.create_system = 0
            zf.writestr(info, r.encode('utf-8'))
    return True

def get_massbank(request, spec_pairs):
    polarity = request.GET.get('polarity', None)
    d = datetime.datetime.now()
    fn = os.path.join(settings.MEDIA_ROOT, d.strftime("%y%d%m_massbank.zip"))
    if polarity:
        fn = fn.replace("_massbank", "_massbank_"+polarity)
    logging.debug(('get massbank', fn, polarity))
    if not os.path.exists(fn):
        write_massbank(fn, spec_pairs)
    response = FileResponse(open(fn, 'rb'), content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="spectra.zip"'
    return response


def get_mgf(request, spec_pairs):
    c = {'spec_data': spec_pairs}
    content_type = "text/txt"
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=spectra.mgf'
    t = loader.get_template('mcf_standards_browse/mgf_template.mgf')
    response.write(t.render(c))
    return response


def get_tsv(request, spec_pairs):
    c = {'spec_data': spec_pairs}
    content_type = "text/tsv"
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=spectra.tsv'
    t = loader.get_template('mcf_standards_browse/spectra_export_template.csv')
    response.write(t.render(c))
    return response



def get_metabolights(request, spec_pairs):
    # if you wanted to do this in memory
    # in_memory = StringIO()
    # zip = ZipFile(in_memory, "w")
    zf_n = os.path.join(settings.MEDIA_ROOT, 'tmp_ebi_export.zip')
    zf = zipfile.ZipFile(zf_n, mode="w")
    filename_list = []
    for cc in spec_pairs:
        if cc[0].standard:
            export_filename = "InventoryID{}".format(cc[0].standard.inventory_id)
        else:
            export_filename = 'unknown_standard'
        ii = 0
        _export_filename = export_filename
        while _export_filename in filename_list:
            _export_filename = "{}_{}".format(export_filename, ii)
            ii += 1
        export_filename = _export_filename
        filename_list.append(export_filename)
        logging.debug(export_filename)
        t = loader.get_template('mcf_standards_browse/export_template_ebi.json')
        r = t.render({'spec_data': [cc, ]})
        info = zipfile.ZipInfo(export_filename.format(ii),
                               date_time=time.localtime(time.time()),
                               )
        info.compress_type = zipfile.ZIP_DEFLATED
        info.comment = b'Remarks go here'
        info.create_system = 0
        zf.writestr(info, r)
    zf.close()
    logging.debug('open file: ')
    zfr = zipfile.ZipFile(zf_n, 'r')
    if spec_pairs:
        logging.debug(zfr.read(export_filename))
    response = HttpResponse(content_type="application/zip")
    response['Content-Disposition'] = 'attachment; filename="spectra.zip"'
    response.write(open(zf_n, 'r').read())
    return response


def get_msp(request, spec_pairs):
    content_type = "text/txt"
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=spectra.msp'
    t = loader.get_template('mcf_standards_browse/mgf_template.msp')
    response.write(t.render({'spec_data': spec_pairs}))
    return response


