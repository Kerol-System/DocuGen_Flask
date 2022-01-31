import os  # For File Manipulations like get paths, rename
from flask import Flask, flash, request, redirect, render_template, url_for, send_file, make_response, Response
from werkzeug.utils import secure_filename
import tarfile
from docx import Document
from docx.shared import Inches
from docxtpl import DocxTemplate
# from google.cloud import storage

import shutil
import re
import mammoth
import datetime
import logging
import logging.config
import os
import glob
import time
import ssl
from pathlib import Path

import urllib3
from helpers import PanHelpers
from paloalto import PaloFirewall, PaloPanorama
from swift_doc import SwiftDoc
from tsf_handler import PanTSFHandler
from firewall import Firewall
from panorama import Panorama

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.config.fileConfig(
    "logging.conf",
    defaults={"logfilename": "SwiftDoc.log"},
    disable_existing_loggers=False,
)
logger = logging.getLogger("__name__")
# context = ssl.SSLContext()
# context.load_cert_chain('laragon.crt', 'laragon.key')
app = Flask(__name__)

app.config.from_pyfile('debug_environment.cfg')

# Get current path
path = os.path.dirname(os.path.abspath(__file__))
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
INPUT_FOLDER = os.path.join(path, 'static/template_file/')
OUTPUT_FOLDER = os.path.join(path, 'output')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= os.path.join(path, 'flask-swiftdoc-e3de075bfc2f.json')
# app.config['GOOGLE_APPLICATION_CREDENTIALS'] = "flask-swiftdoc-e3de075bfc2f.json"
app.config['INPUT_FOLDER'] = INPUT_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2147483648 # 2GB limit

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['tgz'])
IMAGES_EXTENSIONS = set(['png', 'jpg'])


# customer_name=""
# imagename=""


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in IMAGES_EXTENSIONS


@app.route('/tsf_info')
def upload_form():
    return render_template('upload_tsf_file.html')


@app.route('/cust_info')
def cust_info_form():
    return render_template('customer_info.html')


@app.route('/login')
def login_info_form():
    return render_template('login.html')


@app.route('/report')
def report_form():
    return render_template('generate_report.html')


@app.route('/login', methods=['POST'])
def login_info():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "admin" and password == 'password':
            return redirect(url_for('template'))
        else:
            error = "Incorrect username and password"
            return render_template('login.html', error=error)


@app.route('/tsf_info', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        current_chunk = int(request.form['dzchunkindex'])
        if os.path.exists(save_path) and current_chunk == 0:
            # 400 and 500s will tell dropzone that an error occurred and show an error
            return make_response(('File already exists', 400))
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        try:
            with open(save_path, 'ab') as f:
                f.seek(int(request.form['dzchunkbyteoffset']))
                f.write(file.stream.read())
                # storage_client = storage.Client()
                # # buckets = storage_client.list_buckets()
                #
                # # for bucket in buckets:
                # # print(buckets)
                # bucket = storage_client.get_bucket('tsf_file')
                # blob = bucket.blob(filename)
                # blob.upload_from_file(file)
        except OSError:
            # log.exception will include the traceback so we can see what's wrong
            logger.info('Could not write to file')
            return make_response(("Not sure why,"
                                  " but we couldn't write the file to disk", 500))
        total_chunks = int(request.form['dztotalchunkcount'])
        if current_chunk + 1 == total_chunks:
            # This was the last chunk, the file should be complete and the size we expect
            if os.path.getsize(save_path) != int(request.form['dztotalfilesize']):
                logger.info(f"File {filename} was completed, "
                          f"but has a size mismatch."
                          f"Was {os.path.getsize(save_path)} but we"
                          f" expected {request.form['dztotalfilesize']} ")
                return make_response(('Size mismatch', 500))
            else:
                logger.info(f'File {filename} has been uploaded successfully')
        else:
            logger.info(f'Chunk {current_chunk + 1} of {total_chunks} '
                      f'for file {file.filename} complete')

        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_without_ext = os.path.splitext(filename)[0]
        path1 = os.path.join(UPLOAD_FOLDER, file_without_ext)
        if not os.path.isdir(path1):
            os.mkdir(path1)
        os.chdir(rf'{UPLOAD_FOLDER}')
        # flash('File(s) successfully uploaded')
        message1 = f"{file.filename} is successfully uploaded"
        # return make_response(("Chunk upload successful", 200))
        return render_template('upload_tsf_file.html', message1=message1)


@app.route('/streaming')
def streaming():
    os.chdir(INPUT_FOLDER)
    files = glob.glob("*.docx")
    return render_template('troubleshooting.html', files=files)


@app.route('/streaming', methods=['POST'])
def stream_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        docxfile = secure_filename(file.filename)
        if not os.path.isdir(INPUT_FOLDER):
            os.mkdir(INPUT_FOLDER)
        docxfile_ext = os.path.splitext(docxfile)
        file.save(os.path.join(app.config['INPUT_FOLDER'], docxfile))
        flash('File(s) successfully uploaded')
        return redirect(url_for('streaming'))


@app.route('/static/template_file/<filename>/delete')
def delete_file(filename):
    file_path = os.path.join(INPUT_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash("File is successfully deleted")
        return redirect(url_for('streaming'))
    else:
        flash("File is not successfully deleted because it is not present or it is deleted")
        return redirect(url_for('streaming'))


@app.route('/stream')
def stream():
    filepath = os.path.join(path, 'SwiftDoc.log')
    with open(filepath, "r") as f:
        content = f.read()
    return app.response_class(content, mimetype='text/plain')


@app.route('/')
def template():
    try:
        if os.path.isdir(OUTPUT_FOLDER):
            shutil.rmtree(OUTPUT_FOLDER)
        if os.path.isdir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    os.chdir(INPUT_FOLDER)
    # for file in glob.glob("*.docx"):
    files = glob.glob("*.docx")
    myvariable = request.form.get("template_select")
    logger.info(str(myvariable))
    return render_template('select_template.html', files=files)


@app.route('/', methods=['POST'])
def template1():
    global template1, product_type
    template1 = request.form.get("template_select")
    product_type = request.form.get("product_select")
    logger.info(str(template1))
    return redirect(url_for('upload_form'))


@app.route('/logs')
def logs():
    filepath = os.path.join(path, 'SwiftDoc.log')
    return send_file(filepath, as_attachment=True)


@app.route('/cust_info', methods=['POST'])
def cust_info():
    if request.method == 'POST':
        global customer_name
        customer_name = request.form['customername']
        if customer_name == "":
            flash("Please enter customer name")
            return redirect(url_for('cust_info_form'))
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        global imagename
        imagename = secure_filename(file.filename)
        imagename_ext = os.path.splitext(imagename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
        message1 = f"Your customer logo({file.filename}) is successfully uploaded"
        message2 = f"Your customer name is: {customer_name}"
        return render_template('customer_info.html', message1=message1, message2=message2)


@app.route('/report', methods=['POST'])
def report():
    if request.method == 'POST':
        global report_name
        report_name = request.form['reportname']
        if report_name == "":
            flash("Please enter report name")
            return redirect(request.url)
        elif len(report_name) > 35:
            flash("The length of report name should not be greater than 35 characters.")
            return redirect(request.url)
        elif report_name != "" and len(report_name) <= 35:
            if customer_name == "":
                flash("Please enter customer name")
                return redirect(url_for('cust_info_form'))
            elif len(customer_name) > 35:
                flash("The length of customer name should not be greater than 35 characters.")
                return redirect(url_for('cust_info_form'))
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if customer_name != "" and bool(re.match('^[a-zA-Z0-9 ]*$', customer_name)) == True and len(
                    customer_name) <= 50:
                psmain()  # Starting the Report Generator in the Backend
                docx_file = report_name + ".docx"
                doc = Document(os.path.join(app.config['OUTPUT_FOLDER'], docx_file))
                header = doc.sections[0].first_page_header
                image2 = os.path.join(app.config['UPLOAD_FOLDER'], imagename)
                image1 = os.path.join(app.config['INPUT_FOLDER'], 'Picture1.png')
                header_tp = header.add_paragraph()
                header_run = header_tp.add_run()
                header_run.add_picture(image2, width=Inches(2.051181), height=Inches(1.283465))
                header_run.add_text('\t\t\t\t')
                header_run.add_picture(image1, width=Inches(2.051181), height=Inches(0.3740157))
                reportfile = os.path.join(app.config['OUTPUT_FOLDER'], report_name) + '.docx'
                doc.save(reportfile)
            report_status = True
            try:
                if report_status and os.path.isdir(UPLOAD_FOLDER):
                    shutil.rmtree(UPLOAD_FOLDER)
                    print("Successfully removed all files")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
            return redirect(url_for('upload_form'))
        else:
            flash("Please enter valid report name")
            return redirect(request.url)
    return redirect(url_for('upload_form'))


@app.route('/download')
def download():
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], report_name) + '.docx'
    return send_file(filepath, as_attachment=True)



@app.route('/preview')
def preview():
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], report_name) + '.docx'
    with open(os.path.join(app.config['OUTPUT_FOLDER'], report_name) + '.docx', "rb") as file:
        result = mammoth.convert_to_html(file)
    with open(os.path.join(app.config['OUTPUT_FOLDER'], report_name) + '.docx',
              "w") as html_file:
        html_file.write(result.value)
    response = Response(open(filepath, "rb"), mimetype="text/html")
    # response["Content-Disposition"] = "inline;filename=%s" % name
    return response

def psmain():


    my_helper = PanHelpers()
    logger.info('Starting "SwiftDoc" As Built Generator')
    my_helper.print_output('Starting "SwiftDoc" As Built Generator')
    my_helper.debug_info()
    my_helper.print_output("Setting paths")
    my_helper.date_string = datetime.datetime.now().strftime(
        "%y%m%d-%H%M%S"
    )  # used for naming the temp directory
    my_helper.set_separator()  # slash or backslash? This is your legacy Bill Gates, hope you're happy.
    my_helper.set_path()
    context = {'Customer': customer_name, 'Month': datetime.datetime.now().strftime('%B'),
               'Year': datetime.datetime.now().strftime('%Y')}
    pan_hosts = []
    # Declare an empty list to hold the devices we find TSF and XML creds for.
    """Process the provided TSF files."""
    my_helper.print_output("Processing your TSF files, just a moment please...")
    my_tsf_handler = PanTSFHandler(
        my_helper.input_path, my_helper.tmp_path, my_helper.my_separator
    )  # Create a TSF handler object
    customer_files = my_tsf_handler.load_tsf_archive()

    if customer_files is not None:  # see if there are ay tgz files in inputs/ directory
        logger.debug("Set process_tsf to True.")
        process_tsf = True
    else:
        logger.info("No TSF files found in inputs directory.")

    if process_tsf:
        for my_file in customer_files:
            my_helper.set_path()  # make sure the temp path exists
            logger.info("Processing file: %s", my_file)
            tsf_info = my_tsf_handler.extract_info_from_tsf(my_file)
            my_helper.remove_tmp_dir()  # blow away the temp files for this device

            hostname = tsf_info["hostname"]
            serial = tsf_info["serial"]

            if tsf_info["model"] in ["Panorama", "M-100", "M-500", "M-200", "M-600"]:
                my_panorama = PaloPanorama(hostname, serial)
                pan_hosts.append(my_panorama)

                my_panorama.opmode = tsf_info["opmode"]
                my_panorama.admins = tsf_info["admins"]
                my_panorama.templates = tsf_info["templates"]
                my_panorama.devicegroups = tsf_info["devicegroups"]
                my_panorama.snmpv2_system = tsf_info["snmpv2s"]
                my_panorama.snmpv2_manager = tsf_info["snmpv2m"]
                my_panorama.snmpv3 = tsf_info["snmpv3"]
                my_panorama.hapriority = tsf_info["hapriority"]
                my_panorama.model = tsf_info["model"]
                my_panorama.panos = tsf_info["panos"]
                my_panorama.licenses = tsf_info["licenses"]
                my_panorama.mgmtinfo = tsf_info["mgmtinfo"]
            else:
                my_fw = PaloFirewall(hostname, serial)
                pan_hosts.append(my_fw)

                if "hainfo" in tsf_info:
                    logger.debug("Processing HA info.")
                    my_fw.hainfo = tsf_info["hainfo"]
                    my_fw.haotherinfo = tsf_info["haotherinfo"]
                    my_fw.hapeername = tsf_info["hapeername"]

                my_fw.multivsys = tsf_info["multivsys"]
                my_fw.model = tsf_info["model"]
                my_fw.panos = tsf_info["panos"]
                my_fw.licenses = tsf_info["licenses"]
                my_fw.mgmtinfo = tsf_info["mgmtinfo"]
                my_fw.admins = tsf_info["admins"]
                my_fw.vsys = tsf_info["vsys"]
                my_fw.interfaces = tsf_info["interfaces"]
                my_fw.logintsettings = tsf_info["logintsettings"]
                my_fw.antivirus = tsf_info["antivirus"]
                my_fw.antispy = tsf_info["antispy"]
                my_fw.vulnerability = tsf_info["vulnerability"]
                my_fw.url = tsf_info["url"]
                my_fw.wildfire = tsf_info["wildfire"]
                my_fw.fileblocking = tsf_info["fileblocking"]
                my_fw.update_sched = tsf_info["update_sched"]
                my_fw.data_filtering = tsf_info["data_filtering"]
                my_fw.data_objects = tsf_info["data_objects"]
                my_fw.secprof = tsf_info["secprof"]
                my_fw.dos = tsf_info["dos"]
                my_fw.ike_crypto = tsf_info["ike_crypto"]
                my_fw.ipsec_crypto = tsf_info["ipsec_crypto"]
                my_fw.ike_gw = tsf_info["ike_gw"]
                my_fw.ipsec_vpn = tsf_info["ipsec_vpn"]
                my_fw.zones = tsf_info["zones"]
                my_fw.logforwarding = tsf_info["logforwarding"]
                my_fw.snmpv2_system = tsf_info["snmpv2s"]
                my_fw.snmpv2_manager = tsf_info["snmpv2m"]
                my_fw.snmpv3 = tsf_info["snmpv3"]
                my_fw.gp_portals = tsf_info["gp_portals"]
                my_fw.gp_gateways = tsf_info["gp_gateways"]
                my_fw.hip = tsf_info["hip"]
                my_fw.groups = tsf_info["groups"]
                my_fw.userid = tsf_info["userid"]

                hapeername = my_fw.hapeername
                if hapeername:
                    peerhainfo = {}
                    pan_hosts[hapeername] = PaloFirewall(
                        hapeername, my_fw.hainfo["peerserial"]
                    )
                    pan_hosts[hapeername].model = tsf_info["model"]
                    pan_hosts[hapeername].panos = tsf_info["panos"]
                    pan_hosts[hapeername].licenses = my_fw.licenses
                    peerhainfo["ha1a"] = pan_hosts[-2].hainfo["peerha1a"]
                    peerhainfo["ha1b"] = pan_hosts[-2].hainfo["peerha1b"]
                    peerhainfo["ha2a"] = pan_hosts[-2].hainfo["peerha2a"]
                    peerhainfo["ha2b"] = pan_hosts[-2].hainfo["peerha2b"]
                    peerhainfo["hamode"] = pan_hosts[-2].hainfo["hamode"]

                    peermgmtinfo = {
                        "ip": pan_hosts[-2].hainfo["peermgmtip"],
                        "ipv6": pan_hosts[-2].hainfo["peermgmtipv6"],
                        "mask": pan_hosts[-2].mgmtinfo["mask"],
                        "gw": pan_hosts[-2].mgmtinfo["gw"],
                        "speed": pan_hosts[-2].mgmtinfo["speed"],
                        "mtu": pan_hosts[-2].mgmtinfo["mtu"],
                        "services": pan_hosts[-2].mgmtinfo["services"],
                        "permitted_ips": pan_hosts[-2].mgmtinfo["permitted_ips"],
                    }
                    my_fw.hainfo["heartbeat"] = tsf_info["hainfo"]["heartbeat"]
                    my_fw.mgmtinfo = peermgmtinfo
            logger.info("Finished Processing TS file: %s", my_file)
    else:
        logger.info("No valid TSF files found.")

    if not process_tsf and not process_api:
        logger.info("Nothing to do!")
        my_helper.print_output("Nothing to do!")
    else:
        logger.info("Generating SwiftDoc.")
        my_helper.print_output("Generating as-built.")


        if product_type == "Firewall":
            my_firewall_report = Firewall(
                my_helper.date_string,
                my_helper.input_path,
                my_helper.output_path,
                report_name,
                template1,
                context
            )
            my_firewall_report.pan_hosts = pan_hosts
            my_firewall_report.populate_lists()
            my_firewall_report.gen_doc()

        elif product_type == "Panorama":
            my_panorama_report = Panorama(
                my_helper.date_string,
                my_helper.input_path,
                my_helper.output_path,
                report_name,
                template1,
                context
            )
            my_panorama_report.pan_hosts = pan_hosts
            my_panorama_report.populate_lists()
            my_panorama_report.gen_doc()

        elif product_type == "All":
            my_swift_doc = SwiftDoc(
                my_helper.date_string,
                my_helper.input_path,
                my_helper.output_path,
                report_name,
                template1,
                context
            )
            my_swift_doc.pan_hosts = pan_hosts
            my_swift_doc.populate_lists()
            my_swift_doc.gen_doc()


if __name__ == "__main__":  # on running python app.py
    # port = int(os.environ.get('PORT', 8080))
    # context = ('laragon.crt', 'laragon.key')#certificate and key files
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))  # run the flask app
    # ssl_context = 'adhoc'
