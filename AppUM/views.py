from django.shortcuts import render
from .models import *
from .utils import crear_pdf
from django.http import HttpResponse
from django.core.files.base import ContentFile
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.hashers import check_password
# Create your views here.
from django.contrib.auth.hashers import make_password
from decimal import Decimal
from num2words import num2words
from datetime import date
from django.urls import reverse
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import admin_required, mecanico_jefe_required, mecanico_empleado_required
from django.core.mail import send_mail

# for usuario in Personal.objects.all():
#     usuario.contrasena = make_password(usuario.contrasena)
#     usuario.save()

##VISTA DEL LOGIN AL ENTRAR AL SITIO##

def vista_login(req):
    return render(req,"login/login.html",{})

def acceso_login(req):
    try:
        if req.method == "POST":
            usuario = req.POST.get('usuario_login')
            passw = req.POST.get('pass_login')

            exito = authenticate(username=usuario,password=passw)
            if exito:
                login(req,exito)
                usuario_consulta = Personal.objects.filter(usuario=usuario).first()
                

                if usuario_consulta:
                    obtener_administrativo = Administrativo.objects.filter(personal_ptr_id=usuario_consulta.id).first()
                    obtener_mecanico = Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id).first()

                    administrativo = obtener_administrativo.activo
                    mecanico_jefe = obtener_mecanico.activo and obtener_mecanico.jefe
                    mecanico_empleado = obtener_mecanico.activo and not obtener_mecanico.jefe

                    if usuario_consulta.primera_sesion:
                        return render(req,"login/cambio_pass.html",{"usuario":usuario})
                    else:
                    
                        if administrativo and mecanico_jefe:
                            renderizar_en = "login/rol_usuario.html"
                            roles = ['Administrativo','Mecanico jefe']
                            contexto = {"roles":roles}
                        elif administrativo and mecanico_empleado:
                            renderizar_en = "login/rol_usuario.html"
                            roles = ['Administrativo','Mecanico empleado']
                            contexto = {"roles":roles}
                        elif administrativo:
                            renderizar_en = "perfil_administrativo/padre_perfil_administrativo.html"
                            contexto = {}
                        elif mecanico_jefe:
                            renderizar_en = "login/login.html"
                            contexto = {"resultado":"MEC JEFE"}
                        elif mecanico_empleado:
                            renderizar_en = "login/rol_usuario.html"
                            roles = ['Mecanico empleado']
                            contexto = {"roles":roles}
                        else:
                            renderizar_en = "login/login.html"
                            contexto = {"resultado":"USUARIO DADO DE BAJA"}
                else:
                    #ACCEDER CON SUPER USUARIO
                    renderizar_en = "login/rol_usuario.html"
                    roles = ['Administrativo','Mecanico jefe','Mecanico empleado']
                    contexto = {"roles":roles}

                return render(req,renderizar_en,contexto)
            else:
                return render(req,"login/login.html",{"resultado":"Error usuario y/o pass"})
        else:
            return render(req,"login/login.html",{})
    except Exception as e:
        return render(req,"login/login.html",{"resultado":e})

@login_required()
def cerrar_sesion(req):
    try:
        logout(req)
        messages.success(req, "Has cerrado sesión correctamente.")  # Agrega el mensaje
        return redirect('Login')
    except:
        pass

@login_required()
def cambio_pass(req):
    try:
        pass1 = req.POST.get('nueva_contrasena')
        pass2 = req.POST.get('nueva_contrasena_2')
       
        if (len(pass1) < 8):
            return render(req,"login/cambio_pass.html",{"resultado":"La contraseña debe tener un mínimo de 8 caracteres"})
        elif pass1 != pass2:
            return render(req,"login/cambio_pass.html",{"resultado":"Las contraseñas deben coincidir"})
        else:
            #usuario.contrasena = make_password(usuario.contrasena)
            usuario = req.user
            personal = Personal.objects.filter(usuario=usuario.username).first()
            personal.primera_sesion = 0
            personal.contrasena = make_password(pass1)
            personal.save()

            usuario.password = make_password(pass1)
            usuario.save()
            messages.success(req, "Contraseña cambiada correctamente.")  # Agrega el mensaje
            return redirect('Login')
            
    except Exception as e:
        pass

@login_required()
def seleccion_rol(req):
    try:
        rol = req.POST['rol_usuario']
        if rol == "Administrativo":
            renderizar_en = "perfil_administrativo/padre_perfil_administrativo.html"
            contexto={}
        elif rol == "Mecanico jefe":
            renderizar_en = ""
            contexto={}
        else:
            renderizar_en = ""
            contexto={}

        return render(req,renderizar_en,contexto)
    except Exception as e:
        return render(req,"login/login.html",{"resultado":e})

def departamento_matricula(matricula):
    primer_letra = matricula[0:1:1]
    if primer_letra == "A":
        departamento = "Canelones"
    elif primer_letra == "B":
        departamento = "Maldonado"
    elif primer_letra == "C":
        departamento = "Rocha"
    elif primer_letra == "D":
        departamento = "Treina y Tres"
    elif primer_letra == "E":
        departamento = "Cerro Largo"
    elif primer_letra == "F":
        departamento = "Rivera"
    elif primer_letra == "G":
        departamento = "Artigas"
    elif primer_letra == "H":
        departamento = "Salto"
    elif primer_letra == "I":
        departamento = "Paysandú"
    elif primer_letra == "J":
        departamento = "Río Negro"
    elif primer_letra == "K":
        departamento = "Soriano"
    elif primer_letra == "L":
        departamento = "Colonia"
    elif primer_letra == "M":
        departamento = "San José"
    elif primer_letra == "N":
        departamento = "Flores"
    elif primer_letra == "O":
        departamento = "Florida"
    elif primer_letra == "P":
        departamento = "Lavalleja"
    elif primer_letra == "Q":
        departamento = "Durazno"
    elif primer_letra == "R":
        departamento = "Tacuarembó"
    elif primer_letra == "S":
        departamento = "Montevideo"
    return departamento

##VALIDACION DE USUARIO Y CONTRASEÑA##
# def validacion_login(req):
#     if req.method == "POST":
#         usuario = req.POST.get('usuario_login')
#         passw = req.POST.get('pass_login')

#         try:
#             # Buscar usuario
#             usuario_consulta = Personal.objects.filter(usuario=usuario).first()

#             if usuario_consulta and check_password(passw, usuario_consulta.contrasena):
#                 # Concatenar nombre completo
#                 nombre_apellido = f"{usuario_consulta.nombre} {usuario_consulta.apellido}"
                
#                 # Verificar roles
#                 mecanico = Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id).first()
#                 administrativo = Administrativo.objects.filter(personal_ptr_id=usuario_consulta.id).first()

#                 existe_mecanico = mecanico and mecanico.activo
#                 mecanico_jefe = mecanico and mecanico.jefe
#                 existe_administrativo = administrativo and administrativo.activo

#                 # Decidir redirección y contexto
#                 if existe_administrativo and mecanico_jefe:
#                     contexto = {"resultado": "Administrativo y Mecánico Jefe"}
#                     renderizar_en = "login/login.html"
#                 elif existe_administrativo and existe_mecanico:
#                     contexto = {"resultado": "Administrativo y Mecánico Empleado"}
#                     renderizar_en = "login/login.html"
#                 elif existe_administrativo:
#                     contexto = {
#                         "usuario": nombre_apellido,
#                         "existe_mecanico": 0,
#                         "mecanico_jefe": 0,
#                         "existe_administrativo": 1
#                     }
#                     renderizar_en = "perfil_administrativo/padre_perfil_administrativo.html"
#                 elif mecanico_jefe:
#                     contexto = {"resultado": "Solo Mecánico Jefe"}
#                     renderizar_en = "login/login.html"
#                 elif existe_mecanico:
#                     contexto = {"resultado": "Solo Mecánico Empleado"}
#                     renderizar_en = "login/login.html"
#                 else:
#                     contexto = {"resultado": "Este usuario fue dado de baja, contacte al administrador del sistema."}
#                     renderizar_en = "login/login.html"
#             else:
#                 # Usuario o contraseña incorrectos
#                 contexto = {"resultado": "Error de usuario y/o contraseña"}
#                 renderizar_en = "login/login.html"

#         except Exception as e:
#             # Manejar errores específicos o generales
#             contexto = {"resultado": f"Algo salió mal: {str(e)}"}
#             renderizar_en = "login/login.html"

#     else:
#         # Redirigir si el método no es POST
#         contexto = {"resultado": "Método de solicitud no válido"}
#         renderizar_en = "login/login.html"

#     return render(req, renderizar_en, contexto)

@admin_required
def vista_inventario_motos(req):
    motos = Moto.objects.filter(pertenece_tienda=1).order_by('-fecha_ingreso')

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(motos, 5)  # 5 motos por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None,"active_page": 'Motos'})

@admin_required
def vista_inventario_accesorios(req):
    return render(req,"perfil_administrativo/accesorios/accesorios.html",{})

# def existe_matricula_moto_tienda(matr):
#     existe_moto = Moto.objects.filter(matricula = matr).first()

#     if existe_moto.pertenece_tienda == 0:
#         return "update"
#     else:
#         return "existe_matr"

# def existe_num_motor_moto_tienda(num_motor):
#     existe_moto = Moto.objects.filter(num_motor = num_motor).first()
    
#     if existe_moto.pertenece_tienda == 0:
#         return "update_pert_tienda"
#     else:
#         return "existe_num_motor"

# def existe_num_chasis_moto_tienda(num_motor):
#     existe_moto = Moto.objects.filter(num_motor = num_motor).first()
    
#     if existe_moto.pertenece_tienda == 0:
#         return "update_pert_tienda"
#     else:
#         return "existe_num_motor"

# def datos_moto(num_motor, num_chasis):
#     existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
#     existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first() 
#     existen_ambos = Moto.objects.filter(num_motor = num_motor, num_chasis = num_chasis).first() 

#     if existe_num_motor:
#         if existe_num_motor.pertenece_tienda == 1:
#             return "existe_num_motor"
    
#     if existe_num_chasis:
#         if existe_num_chasis.pertenece_tienda == 1:
#             return "existe_num_chasis"
    
#     if existe_num_motor and existe_num_chasis:
#         if existe_num_motor.id != existe_num_chasis.id: #PENSADO EN CASO DE QUE SI UNA MOTO VUELVE A LA TIENDA COINCIDAN EL NUM DE CHASIS Y NUM DE MOTOR
#             return "num_motor_chasis_error"             #EVITAR QUE SE INGRESE NUM DE CHASIS DE MOTO X CON NUM DE MOTOR DE MOTO Y
    
#     if existen_ambos:
#         if existen_ambos.pertenece_tienda == 0:
#             return "update_pert_tienda_a_1"
        
# def datos_moto_pert_tienda(num_motor, num_chasis):
#     existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
#     existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first() 
#     #existen_ambos = Moto.objects.filter(num_motor = num_motor, num_chasis = num_chasis).first() 

#     if existe_num_motor and existe_num_chasis:
        
#         if existe_num_motor.pertenece_tienda == 0 and existe_num_chasis.pertenece_tienda == 0: #LA MOTO INGRESA NUEVAMENTE A LA TIENDA TIEMPO DESPUES DE SER VENDIDA
#             return "update_pert_tienda"
#     else:
#         return None

def pdf_crear(req,ruta_pdf,renderizar_en,model_insert,datos_a_pdf,nombre_archivo,mensaje,negocio):
    if negocio == "UM":
        logo = Logos.objects.get(id=1)
        logo_um_url = req.build_absolute_uri(logo.logo_UM.url) if logo.logo_UM else None

        logo_contexto = logo.logo_UM.url if logo.logo_UM else None
    else:
        logo = Logos.objects.get(id=2)
        logo_dm_url = req.build_absolute_uri(logo.logo_DM.url) if logo.logo_DM else None
        logo_contexto = logo.logo_DM.url if logo.logo_DM else None
        
    pdf = crear_pdf(ruta_pdf, datos_a_pdf)             
    if pdf:
         pdf_file = ContentFile(pdf.content)
         file_name = nombre_archivo
 # Asignar el archivo al campo identificacion_pdf de la moto
         model_insert.identificacion_pdf.save(file_name, pdf_file)
         model_insert.save()

    contexto = {
                "messages":mensaje,
                'pdf_url': model_insert.identificacion_pdf.url,
                "logo_um": logo_contexto

                }
    return render(req,"perfil_administrativo/motos/contenido_pdf.html",contexto)

 #return render(req,"perfil_administrativo/motos/motos.html",{"motos":motos,"messages":"Moto ingresada con éxito"})

    
#     return render(req,renderizar_en,contexto_rend_pdf)

def contexto_para_pdf_moto(model_moto,logo):
        datos_a_pdf = {
                        "moto": {
                            "id":model_moto.id,
                            "marca": model_moto.marca,
                            "modelo": model_moto.modelo,
                            "motor": model_moto.motor,
                            "anio": model_moto.anio,
                            "kilometros": model_moto.kilometros,
                            "precio": model_moto.precio
                        },
                        "current_year": datetime.now().year,
                            "logo_um": logo  # Asegúrate de importar datetime
                        }
        
        return datos_a_pdf

@admin_required
def datos_cliente_venta(req):
    if req.method == 'POST':
        tipo_documento = req.POST['tipo_documento']
        documento_num = req.POST['documento']
        if tipo_documento == "cedula":
            documento = "CI" + str(documento_num)
        elif tipo_documento == "pasaporte":
            documento = "PAS" + str(documento_num)
        else:
            documento = "DNI" + str(documento_num)
        
        cliente = Cliente.objects.filter(documento=documento).first()

        if cliente:
            contexto = {
                "datos_cliente":cliente,
                "active_page": 'Motos'
            }
            return render(req,"perfil_administrativo/motos/alta_moto.html",contexto)
        else:
            contexto = {
                "error_message_cliente":"El cliente no existe, debe ingresar los datos del mismo haciendo clic ",
                "form_cliente":True,
                "active_page": 'Motos'
            }
            return render(req,"perfil_administrativo/motos/alta_moto.html",contexto)

@admin_required
def cliente_moto(req):
    try:
        num_motor = req.POST['num_motor_moto'].upper()
        documento = req.POST['tipo_documento'] + str(req.POST['documento'])

        moto = Moto.objects.filter(num_motor=num_motor).first()
        cliente = Cliente.objects.filter(documento=documento).first()

        if not cliente:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message_cliente":"El cliente no existe, para ingresarlo haga clic ",
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":False,
                                                                            "form_moto_ingresada":False})
        elif not moto:
            #SI LA MOTO NO EXISTE, SE INGRESA LA MOTO DESDE 0
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"La moto no se encuentra registrada en el sistema, debe ingresar la misma completando todos los datos requeridos"})
        else:
            #SI LA MOTO Y EL CLIENTE EXISTEN, ENTONCES SE MODIFICAN CAMPOS EN MOT (PERT_TIENDA = 1)
            if moto.pertenece_tienda:
                return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"La moto que usted desea ingresar ya existe en el inventario de la tienda",
                                                                                "active_page": 'Motos',
                                                                                "form_moto_usada":False,
                                                                                "form_moto_ingresada":False})
            else:
                existe_matricula = Matriculas.objects.filter(moto_id=moto.id).first()
                if existe_matricula:
                    matricula = existe_matricula.matricula
                else:
                    matricula = "Sin matrícula"
                return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                                "moto":moto,
                                                                                "matricula":matricula,
                                                                                "active_page": 'Motos',
                                                                                "form_moto_usada":False,
                                                                                "form_moto_ingresada":True,
                                                                                "consultar_moto_cliente":False})
    except Exception as e:
        return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":e})

@admin_required
def alta_moto_usada(req,id_cliente):
    try:
    #INSERT EN MOTO
        cliente = Cliente.objects.get(id=id_cliente)
        num_chasis = req.POST['num_chasis_moto'].upper()
        num_motor = req.POST['num_motor_moto'].upper()
        existe_num_motor = Moto.objects.filter(num_motor=num_motor).first()
        existe_num_chasis = Moto.objects.filter(num_chasis=num_chasis).first()
        matricula = req.POST['matricula_letras'].upper() + str(req.POST['matricula_numeros'].upper())
        padron = req.POST['num_padron']
        existe_matricula = Matriculas.objects.filter(matricula=matricula).first()
        existe_padron = Matriculas.objects.filter(padron=padron).first()
        if existe_num_motor:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"Ya existe el número de motor ingresado"})
        elif existe_num_chasis:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"Ya existe el número de chasis ingresado"})
        elif existe_matricula:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"Ya existe la matricula ingresada"})
        elif existe_padron:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"Ya existe el número de padrón ingresado"})
        else:
            marca = req.POST['marca_moto'].upper()
            modelo = req.POST['modelo_moto'].upper()
            color = req.POST['color_moto'].upper()

            foto = req.FILES.get('foto_moto')
            nueva_moto = Moto(marca = marca,
                    modelo = modelo,
                    anio = req.POST['anio_moto'],
                    estado = "Usada",
                    motor = req.POST['motor_moto'],
                    kilometros = req.POST['km_moto'],
                    moneda_precio = req.POST['moneda_precio'],
                    precio = req.POST['precio_moto'],
                    color = color,
                    num_motor = num_motor,
                    num_chasis = num_chasis,
                    num_cilindros = req.POST['num_cilindros'],
                    cantidad_pasajeros = req.POST['num_pasajeros'],
                    pertenece_tienda = 1,
                    pertenece_taller = 0,
                    fecha_ingreso = datetime.now(),
                    observaciones = req.POST['descripcion_moto'],
                    foto = foto
                    )
            nueva_moto.save()
            libreta_propiedad = req.FILES.get('libreta_propiedad_moto')
            cliente_moto = ComprasVentas(
                fecha_compra = datetime.now(),
                tipo = "CV",
                fotocopia_libreta = libreta_propiedad,
                cliente_id = id_cliente,
                moto_id = nueva_moto.id
            )
            cliente_moto.save()

            nueva_matricula = Matriculas(
                matricula = matricula,
                padron = padron,
                moto_id = nueva_moto.id
            )
            nueva_matricula.save()
            checkbox = 'crear_pdf' in req.POST
            if checkbox:
                ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                logo_um = Logos.objects.get(id=1)
                logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
                datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
                renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
                mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
                pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
                return pdf_ret
            else:
                messages.success(req, "Moto ingresada con éxito.")
                return redirect('Motos')

            
    except Exception as e:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"cliente":cliente,
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":e})

@admin_required
def reingresar_moto_usada(req,id_moto,id_cliente):
    try:
    #UPDATE MOTO PERT_TIENDA = 1
        moto = Moto.objects.get(id=id_moto)
        
        moto.kilometros = req.POST['km_moto']
        moto.moneda_precio = req.POST['moneda_precio']
        moto.precio = req.POST['precio_moto']
        moto.observaciones = req.POST['descripcion_moto']
        moto.foto = req.FILES.get('foto_moto')
        moto.pertenece_tienda = 1
        moto.fecha_ingreso = datetime.now()
        moto.save()

        # compra_venta = ComprasVentas.objects.filter(moto_id=id_moto,cliente_id=id_cliente).first()
        libreta_propiedad = req.FILES.get('libreta_propiedad_moto')
        # if compra_venta:
        #     compra_venta.tipo = "CV"
        #     compra_venta.save()
        # else:
        #     c_v = ComprasVentas(
        #         fecha_compra = datetime.now(),
        #         fotocopia_libreta = libreta_propiedad,
        #         tipo = "CV",
        #         cliente_id = id_cliente,
        #         moto_id = id_moto
        #     )
        #     c_v.save()
        c_v = ComprasVentas(
                fecha_compra = datetime.now(),
                fotocopia_libreta = libreta_propiedad,
                tipo = "CV",
                cliente_id = id_cliente,
                moto_id = id_moto
            )
        c_v.save()
        checkbox = 'crear_pdf' in req.POST
        if checkbox:
            ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
            logo_um = Logos.objects.get(id=1)
            logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
            datos_a_pdf = contexto_para_pdf_moto(moto,logo_um_url)
            renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
            nombre_archivo = f"identificacion_{moto.id}.pdf"
            mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
            pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
            return pdf_ret
        else:
            messages.success(req, "Moto ingresada con éxito.")
            return redirect('Motos')

    except Exception as e:
        return render(req,"perfil_administrativo/motos/alta_moto.html",{"active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":e})

@admin_required
def alta_moto_nueva(req):
    try:
    #INSERT EN MOTO
        num_chasis = req.POST['num_chasis_moto'].upper()
        num_motor = req.POST['num_motor_moto'].upper()
        existe_num_motor = Moto.objects.filter(num_motor=num_motor).first()
        existe_num_chasis = Moto.objects.filter(num_chasis=num_chasis).first()
        if existe_num_motor:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"Ya existe el número de motor ingresado"})
        elif existe_num_chasis:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{
                                                                            "active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":"Ya existe el número de chasis ingresado"})
        else:
            marca = req.POST['marca_moto'].upper()
            modelo = req.POST['modelo_moto'].upper()
            color = req.POST['color_moto'].upper()

            foto = req.FILES.get('foto_moto')
            nueva_moto = Moto(marca = marca,
                    modelo = modelo,
                    anio = req.POST['anio_moto'],
                    estado = "Nueva",
                    motor = req.POST['motor_moto'],
                    kilometros = 0,
                    moneda_precio = req.POST['moneda_precio'],
                    precio = req.POST['precio_moto'],
                    color = color,
                    num_motor = num_motor,
                    num_chasis = num_chasis,
                    num_cilindros = req.POST['num_cilindros'],
                    cantidad_pasajeros = req.POST['num_pasajeros'],
                    pertenece_tienda = 1,
                    pertenece_taller = 0,
                    fecha_ingreso = datetime.now(),
                    observaciones = req.POST['descripcion_moto'],
                    foto = foto
                    )
            nueva_moto.save()

            checkbox = 'crear_pdf' in req.POST
            if checkbox:
                ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                logo_um = Logos.objects.get(id=1)
                logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
                datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
                renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
                mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
                pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
                return pdf_ret
            else:
                messages.success(req, "Moto ingresada con éxito.")
                return redirect('Motos')

            
    except Exception as e:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{"active_page": 'Motos',
                                                                            "form_moto_usada":True,
                                                                            "form_moto_ingresada":False,
                                                                            "consultar_moto_cliente":False,
                                                                            "error_message":e})                                                                            

@admin_required
def form_alta_moto(req):
    return render(req,"perfil_administrativo/motos/alta_moto.html",{"active_page": 'Motos',
                                                                            "consultar_moto_cliente":True})
    # try:
    #     if req.method == "POST":
    #         marca = req.POST['marca_moto'].upper()
    #         modelo = req.POST['modelo_moto'].upper()
    #         color = req.POST['color_moto'].upper()
    #         matricula_mayus = req.POST['matricula_letras'].upper()
    #         matricula = matricula_mayus + str(req.POST['matricula_numeros'])
    #         num_motor = req.POST['num_motor_moto'].upper()
    #         num_chasis = req.POST['num_chasis_moto'].upper()
            
    #         valid_matricula = matricula_valid(matricula,num_motor,num_chasis)
    #         valid_moto = datos_moto(num_motor,num_chasis)
    #         #valid_matricula = matricula(matricula_mayus)
    #         # print(req.POST['estado_moto'])
    #         estado_moto = req.POST['estado_moto']
            
    #         if valid_moto == "existe_num_motor":
    #             return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Ya existe una moto con ese numero de motor","active_page": 'Motos'})
    #         elif valid_moto == "existe_num_chasis":
    #             return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Ya existe una moto con ese numero de chasis","active_page": 'Motos'})
    #         elif valid_moto == "num_motor_chasis_error":
    #             return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"El número de chasis y/o motor pertenecen a otra moto ingresada en el sistema","active_page": 'Motos'})
    #         elif valid_matricula == "matricula_existe":
    #             return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Ya existe la matricula","active_page": 'Motos'})
    #         else:
    #             if estado_moto == "nueva":
    #                 foto = req.FILES.get('foto_moto')
    #                 nueva_moto = Moto(marca = marca,
    #                         modelo = modelo,
    #                         anio = req.POST['anio_moto'],
    #                         estado = "Nueva",
    #                         motor = req.POST['motor_moto'],
	# 		                kilometros = 0,
    #                         precio = req.POST['precio_moto'],
    #                         color = color,
    #                         num_motor = num_motor,
    #                         num_chasis = num_chasis,
    #                         num_cilindros = req.POST['num_cilindros'],
    #                         cantidad_pasajeros = req.POST['num_pasajeros'],
    #                         pertenece_tienda = 1,
    #                         pertenece_taller = 0,
    #                         fecha_ingreso = datetime.now(),
    #                         observaciones = req.POST['descripcion_moto'],
    #                         foto = foto
    #                         )
    #                 nueva_moto.save()

                    
    #                 checkbox = 'crear_pdf' in req.POST
    #                 if checkbox:
    #                     ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
    #                     logo_um = Logos.objects.get(id=1)
    #                     logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
    #                     datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
    #                     renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
    #                     nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
    #                     mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
    #                     pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
    #                     return pdf_ret
    #                 else:
    #                     messages.success(req, "Moto ingresada con éxito.")
    #                     return redirect('Motos')
    #                 #return HttpResponse(pdf, content_type='application/pdf')
    #             else:
    #                 #INGRESAR MOTOS USADAS
    #                 tipo_documento = req.POST['tipo_documento']
    #                 documento_num = req.POST['documento']
    #                 if tipo_documento == "cedula":
    #                     documento = "CI" + str(documento_num)
    #                 elif tipo_documento == "pasaporte":
    #                     documento = "PAS" + str(documento_num)
    #                 else:
    #                     documento = "DNI" + str(documento_num)
                    
    #                 cliente = Cliente.objects.filter(documento=documento).first()
    #                 valid_compra_venta = num_padron(req.POST['num_padron'])
                    
    #                 if cliente:
    #                     valid_pert_tienda = datos_moto_pert_tienda(num_motor, num_chasis)
    #                     if valid_pert_tienda == "update_pert_tienda": #SI LA MOTO FUE VENDIDA ANTERIORMENTE DE LA TIENDA Y VUELVE A LA MISMA, SE ACTUALIZA PERT_TIENDA = 1
    #                         # print("ENTRA IF")
                           
    #                         foto = req.FILES.get('foto_moto')
    #                         regresa_moto = Moto.objects.get(num_chasis=num_chasis,num_motor=num_motor)
    #                         regresa_moto.pertenece_tienda = 1
    #                         regresa_moto.fecha_ingreso = datetime.now()
    #                         regresa_moto.kilometros = req.POST['km_moto']
    #                         regresa_moto.precio = req.POST['precio_moto']
    #                         regresa_moto.estado = "Usada"
    #                         regresa_moto.num_cilindros = req.POST['num_cilindros']
    #                         regresa_moto.cantidad_pasajeros = req.POST['num_pasajeros']
    #                         regresa_moto.observaciones = req.POST['descripcion_moto']
    #                         regresa_moto.foto = foto
    #                         regresa_moto.save()

    #                         libreta_propiedad = req.FILES.get('libreta_propiedad_moto')
    #                         if valid_compra_venta == "insert_num_padron":
    #                             cliente_moto = ComprasVentas(
    #                                 fecha_compra = datetime.now(),
    #                                 padron = req.POST['num_padron'],
    #                                 tipo = "CV",
    #                                 fotocopia_libreta = libreta_propiedad,
    #                                 cliente_id = cliente.id,
    #                                 moto_id = regresa_moto.id,
    #                                 cantidad_cuotas = 0,
    #                                 cuotas_pagas = 0
    #                             )

    #                             cliente_moto.save()
    #                         else:
    #                             upd_compra_venta = ComprasVentas.objects.get(padron=req.POST['num_padron'])
    #                             upd_compra_venta.tipo = "CV"
    #                             upd_compra_venta.save()

    #                         if req.POST['matricula_letras'] and req.POST['matricula_numeros']: #SI LOS CAMPOS DE TEXTO DE LA MATRICULA NO ESTAN VACIOS
    #                             nueva_matricula = matricula_valid(matricula,num_motor,num_chasis)
    #                             ultima_matricula = Matriculas.objects.filter(activo=1,moto_id=regresa_moto.id)

    #                             if ultima_matricula.exists(): #SI EXISTIERA UNA MATRICULA ASIGNADA A ESA MOTO Y ESTA ACTIVA, ENTONCES ACCEDE
    #                                 ult_matricula = Matriculas.objects.filter(activo=1,moto_id=regresa_moto.id).first()
    #                                 if ult_matricula.matricula != matricula: #LA MATRICULA A INGRESAR ES DIFERENTE A LA ANTERIOR, SE PROCEDE A INGRESAR UNA NUEVA

    #                                     update_activo_0 = Matriculas.objects.get(id=ult_matricula.id)
    #                                     update_activo_0.activo = 0
    #                                     update_activo_0.save()

    #                                     if nueva_matricula == "ingresar_matr": #SI LA MATRICULA EXISTIERA Y ES DE LA MISMA MOTO NO HACE NADA PUESTO QUE NO SE ESTARIA CAMBIANDO
    #                                         new_matricula = Matriculas(
    #                                                 matricula = matricula,
    #                                                 activo = 1,
    #                                                 moto_id = regresa_moto.id
    #                                             )
    #                                         new_matricula.save()
    #                             else: #CASO CONTRARIO INGRESA UNA NUEVA
    #                                     if nueva_matricula == "ingresar_matr": #SI LA MATRICULA EXISTIERA Y ES DE LA MISMA MOTO NO HACE NADA PUESTO QUE NO SE ESTARIA CAMBIANDO
    #                                         new_matricula = Matriculas(
    #                                                 matricula = matricula,
    #                                                 activo = 1,
    #                                                 moto_id = regresa_moto.id
    #                                             )
    #                                         new_matricula.save()
                            
    #                         checkbox = 'crear_pdf' in req.POST
    #                         if checkbox:
    #                             logo_um = Logos.objects.get(id=1)
    #                             logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
    #                             ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                                
    #                             datos_a_pdf = contexto_para_pdf_moto(regresa_moto,logo_um_url)
    #                             renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
    #                             nombre_archivo = f"identificacion_{regresa_moto.id}.pdf"
    #                             mensaje = f"Los datos ingresados corresponden a la moto {regresa_moto.marca} {regresa_moto.modelo}, que anteriormente fue vendida."
    #                             pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,regresa_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
    #                             return pdf_ret
    #                         else:
    #                             # contexto = {
    #                             # "messages":"Moto ingresada con éxito.",
    #                             # }
    #                             # return render(req,"perfil_administrativo/motos/motos.html",contexto)
                            
    #                             messages.success(req, "Moto ingresada con éxito.")
    #                             return redirect('Motos')
    #                     else: #SI LA MOTO NUNCA ESTUVO EN LA TIENDA, SE INGRESA DE 0
    #                         moto_taller = Moto.objects.filter(num_chasis=num_chasis,num_motor=num_motor).first()
    #                         if moto_taller: #LA MOTO PUEDE QUE EXISTA EN EL TALLER
    #                             pert_taller = moto_taller.pertenece_taller
    #                         else:
    #                             pert_taller = 0
    #                         foto = req.FILES.get('foto_moto')
    #                         nueva_moto = Moto(marca = marca,
    #                             modelo = modelo,
    #                             anio = req.POST['anio_moto'],
    #                             estado = "Usada",
    #                             motor = req.POST['motor_moto'],
    #                             kilometros = req.POST['km_moto'],
    #                             precio = req.POST['precio_moto'],
    #                             color = color,
    #                             num_motor = num_motor,
    #                             num_chasis = num_chasis,
    #                             num_cilindros = req.POST['num_cilindros'],
    #                             cantidad_pasajeros = req.POST['num_pasajeros'],
    #                             pertenece_tienda = 1,
    #                             pertenece_taller = pert_taller,
    #                             fecha_ingreso = datetime.now(),
    #                             observaciones = req.POST['descripcion_moto'],
    #                             foto = foto
    #                             )
    #                         nueva_moto.save()
    #                         libreta_propiedad = req.FILES.get('libreta_propiedad_moto')
    #                         cliente_moto = ComprasVentas(
    #                             fecha_compra = datetime.now(),
    #                             padron = req.POST['num_padron'],
    #                             tipo = "CV",
    #                             fotocopia_libreta = libreta_propiedad,
    #                             cliente_id = cliente.id,
    #                             moto_id = nueva_moto.id,
    #                             cantidad_cuotas = 0,
    #                             cuotas_pagas = 0
    #                         )

    #                         cliente_moto.save()
                            
    #                         nueva_matricula = matricula_valid(matricula,nueva_moto.num_motor,nueva_moto.num_chasis)

    #                         if nueva_matricula == "ingresar_matr":
    #                             new_matricula = Matriculas(
    #                                 matricula = matricula,
    #                                 activo = 1,
    #                                 moto_id = nueva_moto.id
    #                             )
    #                             new_matricula.save()
                            
    #                         checkbox = 'crear_pdf' in req.POST
    #                         if checkbox:

    #                             logo_um = Logos.objects.get(id=1)
    #                             logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
    #                             ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
    #                             datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
    #                             renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
    #                             nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
    #                             mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
    #                             pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
    #                             return pdf_ret
    #                         else:
    #                             messages.success(req, "Moto ingresada con éxito.")
    #                             return redirect('Motos')
    #                 else:
    #                     contexto = {
    #                         "error_message_cliente":"El cliente no existe, debe ingresar los datos del mismo haciendo clic ",
    #                         "active_page": 'Motos'
    #                     }
    #                     return render(req,"perfil_administrativo/motos/alta_moto.html",contexto)

    #         # return render(req,"perfil_administrativo/motos/alta_moto.html",{})
    #     else:
    #         return render(req,"perfil_administrativo/motos/alta_moto.html",{"active_page": 'Motos',
    #                                                                         "consultar_moto_cliente":True})
    
    # except Exception as e:
    #     return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Algo salió mal"+ type(e).__name__,"active_page": 'Motos'})


@admin_required
def baja_moto(req,id_moto):
    if req.method == 'POST':

      motoDel = Moto.objects.get(id=id_moto)
      motoDel.pertenece_tienda = 0
      motoDel.save()
      return render(req, "perfil_administrativo/motos/baja_moto.html", {"message":"Moto borrada con éxito","id_moto":0,"active_page": 'Motos'})
      #return HttpResponse(f"<p>{id_auto}</p>")
    else:
       #print(f"Id auto es: {id_auto}")
       return render(req, "perfil_administrativo/motos/baja_moto.html", {"id_moto":id_moto,"active_page": 'Motos'})
       #return HttpResponse(f"<p>{id_auto}</p>")

@admin_required
def busqueda_codigo(req):
    codigo = req.GET.get('codigo')
    #if req.method == 'get':
    motos = Moto.objects.filter(id=codigo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_marca(req):
    marca = req.GET.get('marca')
    #if req.method == 'get':
    motos = Moto.objects.filter(marca__icontains=marca,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_modelo(req):
    modelo = req.GET.get('modelo')
    #if req.method == 'get':
    motos = Moto.objects.filter(modelo__icontains=modelo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_marca_modelo(req):
    marca = req.GET.get('marca_modelo')
    modelo = req.GET.get('modelo_marca')
    #if req.method == 'get':
    motos = Moto.objects.filter(marca__icontains=marca,modelo__icontains=modelo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_anio(req):
    anio = req.GET.get('anio')
    
    #if req.method == 'get':
    motos = Moto.objects.filter(anio=anio,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_kms(req):
    km_minimo = req.GET.get('km_minimo')
    km_maximo = req.GET.get('km_maximo')
    #if req.method == 'get':
    motos = Moto.objects.filter(kilometros__range=(km_minimo, km_maximo),pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_precio(req):
    precio_minimo = req.GET.get('precio_minimo')
    precio_maximo = req.GET.get('precio_maximo')
    #if req.method == 'get':
    motos = Moto.objects.filter(precio__range=(precio_minimo, precio_maximo),pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"active_page": 'Motos'})

@admin_required
def busqueda_matricula(req):
    matricula_letras = req.GET.get('letras_matricula').upper()
    matricula_numeros = str(req.GET.get('numeros_matricula'))
    matricula = matricula_letras + matricula_numeros

    busq_matricula = Matriculas.objects.filter(matricula = matricula).first()
    if busq_matricula:
        moto = Moto.objects.filter(id=busq_matricula.moto_id,pertenece_tienda=1)
        paginator = Paginator(moto, 5)  # 10 motos por página
        page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada
        contexto = {'page_obj': page_obj,"motos":moto,"active_page": 'Motos'}
    else:
        contexto = {'page_obj': None,"motos":None,"active_page": 'Motos'}

    return render(req,"perfil_administrativo/motos/motos.html",contexto)


def validacion_moto(id_moto,num_motor,num_chasis):
    moto_actual = Moto.objects.filter(id = id_moto).first()
    existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
    existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first()
    
    if existe_num_motor:
        if existe_num_motor.num_motor != moto_actual.num_motor:
            return "existe_num_motor"
    
    if existe_num_chasis:
        if existe_num_chasis.num_chasis != moto_actual.num_chasis:
            return "existe_num_chasis"
        
def matricula_valid(matricula,padron,id_moto):
    existe_matricula = Matriculas.objects.filter(matricula = matricula).first()
    # moto = Moto.objects.filter(num_motor = num_motor,num_chasis = num_chasis).first()
    if existe_matricula:
        if existe_matricula.moto_id != id_moto:
            return "matricula_existe"
    
    existe_padron = Matriculas.objects.filter(padron=padron).first()
    if existe_padron:
        if existe_padron.moto_id != id_moto:
            return "padron_existe"
    
@admin_required
def modificacion_moto(req,id_moto):
    try:
        if req.method == "POST":
                
                moto_upd = Moto.objects.get(id=id_moto)
                num_motor = req.POST['num_motor_moto'].upper()
                num_chasis = req.POST['num_chasis_moto'].upper()

                # matricula_actual = Matriculas.objects.filter(moto_id=id_moto).first()

                if req.POST['matricula_letras'] and req.POST['matricula_numeros']:
                    letras_matricula = req.POST['matricula_letras']
                    num_matricula = req.POST['matricula_numeros']
                else:
                    letras_matricula = None
                    num_matricula = None
                matricula = req.POST['matricula_letras'].upper() + str(req.POST['matricula_numeros'])
                padron = req.POST['num_padron']
                if not padron:
                    padron = None
                validar_matricula = matricula_valid(matricula,padron,id_moto)
                validacion_datos_moto = validacion_moto(id_moto,num_motor,num_chasis)

                if validacion_datos_moto == "existe_num_motor":
                    return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"El número de motor ya se encuentra asignado a otra moto",
                                                                                            'datos_moto': moto_upd,
                                                                                            "letras_matricula":letras_matricula,
                                                                                            "num_matricula":num_matricula,
                                                                                            "active_page": 'Motos'}) 
                elif validacion_datos_moto == "existe_num_chasis":
                    return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"El número de chasis ya se encuentra asignado a otra moto",
                                                                                            'datos_moto': moto_upd,
                                                                                            "letras_matricula":letras_matricula,
                                                                                            "num_matricula":num_matricula,
                                                                                            "active_page": 'Motos'}) 
                elif (req.POST['matricula_letras'] and req.POST['matricula_numeros']) and (validar_matricula == "matricula_existe"): #EXISTE UNA MATRICULA REGISTRADA Y ADEMAS ES DIFERENTE
                    return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"La matricula ingresada ya existe",
                                                                                            'datos_moto': moto_upd,
                                                                                            "letras_matricula":letras_matricula,
                                                                                            "num_matricula":num_matricula,
                                                                                            "active_page": 'Motos'}) 
                elif (req.POST['num_padron']) and (validar_matricula == "padron_existe"):
                    return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"El número de padrón ya existe",
                                                                                            'datos_moto': moto_upd,
                                                                                            "letras_matricula":letras_matricula,
                                                                                            "num_matricula":num_matricula,
                                                                                            "active_page": 'Motos'})
                else:
                            
                    marca = req.POST['marca_moto'].upper()
                    modelo = req.POST['modelo_moto'].upper()
                    color = req.POST['color_moto'].upper()

                    foto = req.FILES.get('foto_moto')
                    
                    moto_upd = Moto.objects.get(id=id_moto)
                    moto_upd.marca = marca
                    moto_upd.modelo = modelo
                    moto_upd.motor = req.POST['motor_moto']
                    moto_upd.anio = req.POST['anio_moto']

                    if req.POST['estado_moto'] == "nueva":
                        estado = "Nueva"
                    else:
                        estado = "Usada"
                        
                    moto_upd.estado = estado
                    moto_upd.kilometros = req.POST['km_moto']
                    moto_upd.num_motor = num_motor
                    moto_upd.num_chasis = num_chasis
                    moto_upd.num_cilindros = req.POST['num_cilindros']
                    moto_upd.cantidad_pasajeros = req.POST['num_pasajeros']
                    moto_upd.color = color
                    moto_upd.moneda_precio = req.POST['moneda_precio']
                    moto_upd.precio = req.POST['precio_moto']
                    moto_upd.observaciones = req.POST['descripcion_moto']
                    moto_upd.foto = foto
                    moto_upd.save()

                    matricula_actual = Matriculas.objects.filter(moto_id=id_moto).first()
                    if req.POST['matricula_letras'] and req.POST['matricula_numeros'] and req.POST['num_padron']:
                        if matricula_actual:
                            if matricula_actual.matricula != matricula: #EN CASO DE QUE LA MATRICULA INGRESADA EN EL TEMPLATE SEA DIFERENTE A LA EXISTENTE EN LA BASE DE DATOS, ENTONCES ACCEDE
                                
                                matricula_actual.delete()
                                nueva_matricula = Matriculas(
                                    matricula = matricula,
                                    padron = req.POST['num_padron'],
                                    moto_id = moto_upd.id
                                )
                                nueva_matricula.save()

                        else:
                                nueva_matricula = Matriculas(
                                    matricula = matricula,
                                    padron = req.POST['num_padron'],
                                    moto_id = moto_upd.id
                                )
                                nueva_matricula.save()


                    checkbox = 'crear_pdf' in req.POST
                    if checkbox:
                            ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                            logo_um = Logos.objects.get(id=1)
                            logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None

                            datos_a_pdf = contexto_para_pdf_moto(moto_upd,logo_um_url)
                            renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                            nombre_archivo = f"identificacion_{moto_upd.id}.pdf"
                            mensaje = "Moto modificada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
                            pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,moto_upd,datos_a_pdf,nombre_archivo,mensaje,"UM")
                            return pdf_ret
                    else:
                        messages.success(req, "La moto ha sido modificada con éxito.")
                        return redirect('Motos')
        else:
            moto_upd = Moto.objects.get(id=id_moto)
            matricula_upd = Matriculas.objects.filter(moto_id=moto_upd.id).first()

            if matricula_upd:
                letras_matricula = matricula_upd.matricula[0:3:1]
                num_matricula = matricula_upd.matricula[3:7:1]
                padron = matricula_upd.padron
            else:
                letras_matricula = None
                num_matricula = None
                padron = None

            if moto_upd.observaciones == None:
                moto_upd.observaciones = "Sin descripción"
            precio = int(moto_upd.precio) if moto_upd.precio else 0
            return render(req,"perfil_administrativo/motos/modificacion_moto.html",{'datos_moto': moto_upd,
            "letras_matricula":letras_matricula,
            "num_matricula":num_matricula,
            "padron":padron,
            "precio":precio,
            "active_page": 'Motos'}) 
    except Exception as e:
        return render(req,"perfil_administrativo/motos/modificacion_moto.html",{'datos_moto': moto_upd,
            "letras_matricula":letras_matricula,
            "num_matricula":num_matricula,"active_page": 'Motos',"error_message":str(e)}) 
    

@admin_required
def detalles_moto(req,id_moto):
    moto = Moto.objects.get(id=id_moto)
    
    matriculas_moto = Matriculas.objects.filter(moto_id=id_moto).first()

    if not moto.observaciones:
        descripcion = "Sin descripción"
    else:
        descripcion = moto.observaciones
    
    if moto.identificacion_pdf:
        pdf = moto.identificacion_pdf.url
    else:
        pdf = None
    
    compra_venta = ComprasVentas.objects.filter(moto_id=id_moto,tipo="CV").first()

    if compra_venta:
        cliente_id = compra_venta.cliente_id
        telefono_principal_cliente = ClienteTelefono.objects.filter(cliente_id=cliente_id,principal=1).first()
        correo_cliente = ClienteCorreo.objects.filter(cliente_id=cliente_id,principal=1).first()

        if correo_cliente:
            correo = correo_cliente.correo
        else:
            correo = None

        telefono_principal = telefono_principal_cliente.telefono
        libreta = req.build_absolute_uri(compra_venta.fotocopia_libreta.url) if compra_venta.fotocopia_libreta else None
        # print("ID CLIENTE --->>>" + str(cliente_id))
        cliente = Cliente.objects.get(id=cliente_id)
    else:
        cliente = None
        libreta = None
        telefono_principal = None
        correo = None

    # print("Matr actual: "+str(matricula_actual.matricula))
    # print("Matr anterior: "+str(matricula_anterior.matricula))

    if matriculas_moto:
    # Obtiene la matrícula actual, o None si no existe
        matricula = Matriculas.objects.filter(moto_id=id_moto).first()
    
        if not matricula: 
            matr_act = None
        else:
            matr_act = matricula.matricula
        
        contexto = {"moto":moto,
                    "descripcion":descripcion,
                    "matr_actual":matr_act,
                    "foto_moto":moto.foto.url if moto.foto else None,
                    "pdf":pdf,
                    "cliente":cliente,
                    "libreta":libreta,
                    "telefono_principal":telefono_principal,
                    "correo":correo,
                    "active_page": 'Motos'
                    }
    else:
        contexto = {"moto":moto,"descripcion":descripcion,"pdf":pdf,"cliente":cliente,"libreta":libreta,"telefono_principal":telefono_principal,"correo":correo,"active_page": 'Motos'}
      
    print(pdf)
    # if not matricula_anterior:
    #     matricula_anterior.matricula = None

    return render(req,"perfil_administrativo/motos/detalles_moto.html",contexto)

@admin_required
def vista_inventario_accesorios(req):
    accesorios = Accesorio.objects.filter(activo=1).order_by('-fecha_ingreso')

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(accesorios, 5)  # 5 accesorios por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/accesorios/accesorios.html",{'page_obj': page_obj,"accesorios":accesorios,"logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None})

@admin_required
def alta_accesorio(req):
    try:
        if req.method == "POST":
            tipo = req.POST['tipo_accesorio'].upper()     
            marca = req.POST['marca_accesorio'].upper()
            modelo = req.POST['modelo_accesorio'].upper()
            precio = req.POST['precio_accesorio']

            foto = req.FILES.get('foto_accesorio')

            nuevo_accesorio = Accesorio(
                tipo = tipo,
                marca = marca,
                modelo = modelo,
                activo = 1,
                foto = foto,
                precio = precio,
                fecha_ingreso = datetime.now()
            )

            nuevo_accesorio.save()

            if req.POST['tipo_accesorio'] == "Otro":
                tipo = "Accesorio"
            else:
                tipo = req.POST['tipo_accesorio']
            # return render(req,"perfil_administrativo/accesorios/accesorios.html",{"message":"Accesorio ingresado con éxito"})
            messages.success(req, f"{tipo} ingresado con éxito.")
            return redirect('Accesorios')
        else:
            return render(req,"perfil_administrativo/accesorios/alta_accesorio.html",{})
    except Exception as e:
        pass

# def datos_a_modificacion_accesorio(req,id_accesorio):
#     try:
        
#     except Exception as e:
#         pass

@admin_required
def modificacion_accesorio(req,id_accesorio):
    try:
        
        if req.method == "POST": 
            accesorio_upd = Accesorio.objects.get(id=id_accesorio)
            accesorio_upd.tipo = req.POST['tipo_accesorio']
            accesorio_upd.marca = req.POST['marca_accesorio']
            accesorio_upd.modelo = req.POST['modelo_accesorio']
            accesorio_upd.precio = req.POST['precio_accesorio']
            accesorio_upd.foto = req.FILES.get('foto_accesorio')
            accesorio_upd.save()
            messages.success(req, "El accesorio ha sido modificado con éxito.")
            return redirect('Accesorios')
        else:
            accesorio = Accesorio.objects.get(id=id_accesorio)
            return render(req,"perfil_administrativo/accesorios/modificacion_accesorio.html",{"datos_accesorio":accesorio})
    except Exception as e:
        pass

@admin_required
def baja_accesorio(req,id_accesorio):
    try:
        
        if req.method == 'POST':
            accesorio_baja = Accesorio.objects.get(id=id_accesorio)
            accesorio_baja.activo = 0
            accesorio_baja.save()
            return render(req, "perfil_administrativo/accesorios/baja_accesorio.html", {"message":"Accesorio borrado con éxito","id_accesorio":0})
      #return HttpResponse(f"<p>{id_auto}</p>")
        else:
       #print(f"Id auto es: {id_auto}")
            return render(req, "perfil_administrativo/accesorios/baja_accesorio.html", {"id_accesorio":id_accesorio})
       #return HttpResponse(f"<p>{id_auto}</p>")
    except Exception as e:
        pass

@admin_required
def detalles_accesorio(req,id_accesorio):
    try:
        accesorio_detalle = Accesorio.objects.get(id=id_accesorio)
        return render(req, "perfil_administrativo/accesorios/detalles_accesorio.html", {"accesorio":accesorio_detalle})
    except Exception as e:
        pass


@admin_required
def venta_accesorio(req,id_accesorio):
    try:
        pass
    except Exception as e:
        pass


@admin_required
def busqueda_tipo_accesorio(req):
    try:
        tipo = req.GET.get('tipo_accesorio')
        accesorio = Accesorio.objects.filter(tipo__icontains=tipo,activo=1)
        paginator = Paginator(accesorio, 5)  # 10 accesorios por página
        page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

        return render(req,"perfil_administrativo/accesorios/accesorios.html",{'page_obj': page_obj,"accesorios":accesorio})
    except Exception as e:
        pass


@admin_required
def busqueda_codigo_accesorio(req):
    try:
        codigo = req.GET.get('codigo')
        accesorio = Accesorio.objects.filter(id=codigo)
        paginator = Paginator(accesorio, 5)  # 10 accesorios por página
        page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

        return render(req,"perfil_administrativo/accesorios/accesorios.html",{'page_obj': page_obj,"accesorios":accesorio})
    except Exception as e:
        return render(req,"perfil_administrativo/accesorios/accesorios.html",{'message': e})


@admin_required
def busqueda_marca_modelo_accesorio(req):
    try:
        marca = req.GET.get('marca_modelo')
        modelo = req.GET.get('modelo_marca')
        #if req.method == 'get':
        accesorio = Accesorio.objects.filter(marca__icontains=marca,modelo__icontains=modelo,activo=1)
        paginator = Paginator(accesorio, 5)  # 10 accesorios por página
        page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
        page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

        return render(req,"perfil_administrativo/accesorios/accesorios.html",{'page_obj': page_obj,"accesorios":accesorio})
    except Exception as e:
        pass

@admin_required
def vista_clientes(req):
    clientes = Cliente.objects.filter(
        cliente_telefono__principal=True
    ).values('id','nombre', 'apellido', 'cliente_telefono__telefono').order_by('nombre')

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(clientes, 5)  # 5 clientes por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/cliente/clientes.html",{'page_obj': page_obj,"clientes":clientes})

def valid_cliente(documento,tel1,tel2,correo1,correo2):
    existe_cliente = Cliente.objects.filter(documento=documento).first()
    if existe_cliente:
        return "existe_cliente"
    
    existe_tel_1 = ClienteTelefono.objects.filter(telefono=tel1).first()

    if existe_tel_1:
        return "existe_telefono_1"
    
    if tel2:
        existe_tel_2 = ClienteTelefono.objects.filter(telefono=tel2).first()
        if existe_tel_2:
            return "existe_telefono_2"
    

    if correo1:
        existe_correo_1 = ClienteCorreo.objects.filter(correo=correo1).first()
        if existe_correo_1:
            return "existe_correo_1"
        
    if correo2:
        existe_correo_2 = ClienteCorreo.objects.filter(correo=correo2).first()
        if existe_correo_2:
            return "existe_correo_2"

@admin_required
def alta_cliente(req):
    try:
        if req.method == "POST":
            tipo_doc = req.POST['tipo_doc']
            doc = req.POST['doc']
            nombre = req.POST['nombre']
            apellido = req.POST['apellido']
            f_nac_str = req.POST.get('f_nac')  # Cambiado a paréntesis
            f_nac = datetime.strptime(f_nac_str, '%Y-%m-%d').date() if f_nac_str else None
            telefono_principal = req.POST['telefono_principal']
            telefono_secundario = req.POST['telefono_secundario']
            correo = req.POST['correo_1']
            dominio_correo = req.POST['dominio_correo']
            otro_correo = req.POST['otro_correo']
            correo_2 = req.POST['correo_2']
            dominio_correo_2 = req.POST['dominio_correo_2']
            otro_correo_2 = req.POST['otro_correo_2']
            localidad = req.POST['localidad']
            localidad_otro = req.POST['localidad_otro']
            calle = req.POST['calle']
            numero = req.POST['numero']
            num_apto = req.POST['num_apto']
            
            if correo:
                correo_principal = correo + dominio_correo
            else:
                correo_principal = None
            
            if correo_2:
                correo_secundario = correo_2 + dominio_correo_2
            else:
                correo_secundario = None
            
            doc_compuesto = tipo_doc + str(doc)
            existe_cliente = valid_cliente(doc_compuesto,telefono_principal,telefono_secundario,correo_principal,correo_secundario)
            if existe_cliente == "existe_cliente":
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"El cliente ya existe"})
            elif existe_cliente == "existe_telefono_1":
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"El telefono 1 ya existe"})
            elif existe_cliente == "existe_telefono_2":
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"El telefono 2 ya existe"})
            elif existe_cliente == "existe_correo_1":
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"El correo 1 ya existe"})
            elif existe_cliente == "existe_correo_2":
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"El correo 2 ya existe"})
            elif telefono_principal == telefono_secundario:
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"Los numeros de teléfono no pueden ser iguales"})
            elif (correo_principal and correo_secundario) and (correo_principal == correo_secundario):
                return render(req,"perfil_administrativo/cliente/alta_cliente.html",{"error_message":"Los correos no pueden ser iguales"})
            else:
                if localidad == "Otro":
                    ciudad = localidad_otro
                else:
                    ciudad = localidad

                if num_apto:
                    n_a = num_apto
                else:
                    n_a = 0

                nuevo_cliente = Cliente(
                    documento = doc_compuesto,
                    nombre = nombre,
                    apellido = apellido,
                    fecha_nacimiento = f_nac,
                    ciudad = ciudad,
                    calle = calle,
                    numero = numero,
                    num_apartamento = n_a
                )

                nuevo_cliente.save()
                
                telefono_cliente = ClienteTelefono(
                    telefono = telefono_principal,
                    principal = 1,
                    
                    cliente_id = nuevo_cliente.id
                )
                telefono_cliente.save()

                if telefono_secundario:
                    telefono_sec_cliente = ClienteTelefono(
                    telefono = telefono_secundario,
                    principal = 0,
                   
                    cliente_id = nuevo_cliente.id
                )
                    telefono_sec_cliente.save()

                if correo_principal:
                    correo_cliente = ClienteCorreo(
                        correo = correo_principal,
                        principal = 1,
                        
                        cliente_id = nuevo_cliente.id
                    )
                    correo_cliente.save()
                
                if correo_secundario:
                    correo_sec_cliente = ClienteCorreo(
                        correo = correo_secundario,
                        principal = 0,
                        
                        cliente_id = nuevo_cliente.id
                    )
                    correo_sec_cliente.save()



                messages.success(req, "El cliente fue ingresado con éxito.")
                return redirect('Clientes')
        else:
            return render(req,"perfil_administrativo/cliente/alta_cliente.html",{})
    except Exception as e:
        pass




def contexto_para_cliente(id_cliente,mensaje_error):
            cliente = Cliente.objects.get(id=id_cliente)
            tel_princ = ClienteTelefono.objects.get(principal=1,cliente_id=id_cliente)
            tel_sec = ClienteTelefono.objects.filter(principal=0,cliente_id=id_cliente).first()

            tipo_documento_ci = cliente.documento[0:2:1]
            tipo_documento_pas_dni = cliente.documento[0:3:1]

            longitud_doc = len(cliente.documento)
            doc_num = ""
            
            if tipo_documento_ci == "CI":
                tipo_doc = "CI"
                for i in range(2,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
            elif tipo_documento_pas_dni == "DNI":
                tipo_doc = "DNI"
                for i in range(3,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
            else:
                tipo_doc = "PAS"
                for i in range(3,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
            
            correo_princ = ClienteCorreo.objects.filter(principal=1,cliente_id=id_cliente).first()
            correo_sec = ClienteCorreo.objects.filter(principal=0,cliente_id=id_cliente).first()

            if tel_sec:
                t_s = tel_sec.telefono
            else:
                t_s = None

            if correo_princ:
                longitud_correo_princ = len(correo_princ.correo)
                c_p = "" 
                lon = 0
                for i in range(0,longitud_correo_princ):
                    if correo_princ.correo[i] == "@":
                        j = i
                        break
                    else:
                        lon += 1
                        c_p = c_p + correo_princ.correo[i]
                
                longitud_dominio = longitud_correo_princ - lon
                dom_princ = ""
                pos = j
                for j in range(pos,longitud_correo_princ):
                    dom_princ = dom_princ + correo_princ.correo[j]
            else:
                c_p = ""
                dom_princ = None
            
            if correo_sec:
                
                longitud_correo_sec = len(correo_sec.correo)
                c_s = "" 
                lon = 0
                for i in range(0,longitud_correo_sec):
                    if correo_sec.correo[i] == "@":
                        j = i
                        break
                    else:
                        lon += 1
                        c_s = c_s + correo_sec.correo[i]
                
            
                dom_sec = ""
                pos = j
                for j in range(pos,longitud_correo_sec):
                    dom_sec = dom_sec + correo_sec.correo[j]
            else:
                c_s = ""
                dom_sec = None
            f_nac_formateada = cliente.fecha_nacimiento.strftime('%Y-%m-%d')
            contexto = {"datos_cliente":cliente,
                        "tipo_doc":tipo_doc,
                        "doc_num":doc_num,
                        "tel_princ":tel_princ,
                        "fecha_nac":f_nac_formateada,
                        "tel_sec":t_s,
                        "correo_princ":c_p,
                        "dom_princ":dom_princ,
                        "dom_sec":dom_sec,
                        "correo_sec":c_s,
                        "error_message":mensaje_error}
            return contexto

def valid_cliente_mod(id_cliente,documento,tel1,tel2,correo1,correo2):
    cliente_id = Cliente.objects.get(id=id_cliente)
    cliente_doc = Cliente.objects.filter(documento=documento).first()

    if cliente_doc:
        if id_cliente != cliente_doc.id:
            return "existe_cliente"
    
    tel_principal = ClienteTelefono.objects.filter(telefono=tel1).first()
    if tel_principal:
        if tel_principal.cliente_id != id_cliente:
            return "existe_tel_principal"
    
    tel_secundario = ClienteTelefono.objects.filter(telefono=tel2).first()
    if tel_secundario:
        if tel_secundario.cliente_id != id_cliente:
            return "existe_tel_secundario"
        
    correo_princ = ClienteCorreo.objects.filter(correo=correo1).first()
    if correo_princ:
        if correo_princ.cliente_id != id_cliente:
            return "existe_correo_principal"

    correo_sec = ClienteCorreo.objects.filter(correo=correo2).first()
    if correo_sec:
        if correo_sec.cliente_id != id_cliente:
            return "existe_correo_secundario"
        

@admin_required
def modificacion_cliente(req,id_cliente):
    try:
        if req.method == "POST":
            tipo_doc = req.POST['tipo_doc']
            doc = req.POST['doc']
            documento = tipo_doc + str(doc)
            tel1 = req.POST['telefono_principal']
            tel2 = req.POST['telefono_secundario']
            correo1 = req.POST['correo_1'] + req.POST['dominio_correo']
            correo2 = req.POST['correo_2'] + req.POST['dominio_correo_2']
    
            valid_cliente = valid_cliente_mod(id_cliente,documento,tel1,tel2,correo1,correo2)
            if valid_cliente == "existe_cliente":
                contexto = contexto_para_cliente(id_cliente,"El documento ingresado ya existe")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            
            elif valid_cliente == "existe_tel_principal":
                contexto = contexto_para_cliente(id_cliente,"El telefono 1 ingresado ya existe")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            elif valid_cliente == "existe_tel_secundario":
                contexto = contexto_para_cliente(id_cliente,"El telefono 2 ingresado ya existe")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            elif valid_cliente == "existe_correo_principal":
                contexto = contexto_para_cliente(id_cliente,"El correo 1 ingresado ya existe")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            elif valid_cliente == "existe_correo_secundario":
                contexto = contexto_para_cliente(id_cliente,"El correo 2 ingresado ya existe")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            elif tel1 == tel2:
                contexto = contexto_para_cliente(id_cliente,"Los telefonos no pueden ser iguales")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            elif correo1 == correo2:
                contexto = contexto_para_cliente(id_cliente,"Los correos no pueden ser iguales")
                return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
            else:
            
                tel1_actual = ClienteTelefono.objects.filter(cliente_id=id_cliente,principal=1).first()
                if tel1_actual.telefono != tel1:
                    #SI EL TEL1 INGRESADO ES DISTINTO DEL ACTUAL --->>> BORRAR ACTUAL E INGRESAR NUEVO TEL1
                    tel1_actual.delete()
                    nuevo_tel1 = ClienteTelefono(
                        telefono = tel1,
                        principal = 1,
                        cliente_id = id_cliente
                    )
                    nuevo_tel1.save()

                if tel2:
                    tel2_actual = ClienteTelefono.objects.filter(cliente_id=id_cliente,principal=0).first()
                    checkbox = 'convert_to_tel1' in req.POST    
                    if tel2_actual.telefono != tel2:
                        #SI EL TEL2 INGRESADO ES DISTINTO DEL ACTUAL --->>> BORRAR ACTUAL E INGRESAR NUEVO TEL2
                        tel2_actual.delete()
                        nuevo_tel2 = ClienteTelefono(
                            telefono = tel2,
                            principal = 0,
                            cliente_id = id_cliente
                        )
                        nuevo_tel2.save()
                    if checkbox:
                        tel2_actual = ClienteTelefono.objects.filter(cliente_id=id_cliente,principal=0).first()
                        tel2_actual.principal = 1
                        tel1_actual.principal = 0
                        tel2_actual.save()
                        tel1_actual.save()

                if req.POST['correo_1']:
                    correo1_actual = ClienteCorreo.objects.filter(cliente_id=id_cliente,principal=1).first()
                    if correo1_actual.correo != correo1:
                        #SI EL CORREO1 INGRESADO ES DISTINTO DEL ACTUAL --->>> BORRAR ACTUAL E INGRESAR NUEVO CORREO1
                        correo1_actual.delete()
                        nuevo_correo1 = ClienteCorreo(
                            correo = correo1,
                            principal = 1,
                            cliente_id = id_cliente
                        )
                        nuevo_correo1.save()
                
                if req.POST['correo_2']:
                    correo2_actual = ClienteCorreo.objects.filter(cliente_id=id_cliente,principal=0).first()
                    checkbox_correo = 'convert_to_correo1' in req.POST
                    if correo2_actual.correo != correo2:
                        #SI EL CORREO2 INGRESADO ES DISTINTO DEL ACTUAL --->>> BORRAR ACTUAL E INGRESAR NUEVO CORREO2
                        correo2_actual.delete()
                        nuevo_correo2 = ClienteCorreo(
                            correo = correo2,
                            principal = 0,
                            cliente_id = id_cliente
                        )
                        nuevo_correo2.save()
                    
                    if checkbox_correo:
                        correo2_actual = ClienteCorreo.objects.filter(cliente_id=id_cliente,principal=0).first()
                        correo2_actual.principal = 1
                        correo1_actual.principal = 0 
                        correo1_actual.save()
                        correo2_actual.save()
                
                f_nac_str = req.POST.get('f_nac')  # Cambiado a paréntesis
                f_nac = datetime.strptime(f_nac_str, '%Y-%m-%d').date() if f_nac_str else None

                mod_cliente = Cliente.objects.get(id=id_cliente)
                mod_cliente.documento = documento
                mod_cliente.nombre = req.POST['nombre'].capitalize()
                mod_cliente.apellido = req.POST['apellido'].capitalize()
                mod_cliente.fecha_nacimiento = f_nac
                mod_cliente.ciudad = req.POST['localidad'].capitalize()
                mod_cliente.calle = req.POST['calle'].capitalize()
                mod_cliente.numero = req.POST['numero']
                mod_cliente.num_apartamento = req.POST['num_apto']
                
                mod_cliente.save()
                messages.success(req, "Cliente modificado con éxito")
                return redirect('Clientes')
        else:
            contexto = contexto_para_cliente(id_cliente,None)
            return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",contexto)
    except Exception as e:
        return render(req,"perfil_administrativo/cliente/modificacion_cliente.html",{"error_message":e})

@admin_required
def buscar_por_doc(req):
    tipo_doc = req.GET.get('tipo_doc_busq')
    doc_num = req.GET.get('documento')
    documento = tipo_doc + str(doc_num)

    cliente = Cliente.objects.filter(
         documento = documento,
         cliente_telefono__principal=True
     ).values('id','nombre', 'apellido', 'cliente_telefono__telefono')

    paginator = Paginator(cliente, 5)  # 5 clientes por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/cliente/clientes.html",{'page_obj': page_obj,"clientes":cliente})

@admin_required
def buscar_nom_ape(req):
    nombre = req.GET.get('nombre').capitalize()
    apellido = req.GET.get('apellido').capitalize()
    cliente = Cliente.objects.filter(
         nombre = nombre,
         apellido = apellido,
         cliente_telefono__principal=True
     ).values('id','nombre', 'apellido', 'cliente_telefono__telefono')

    paginator = Paginator(cliente, 5)  # 5 clientes por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/cliente/clientes.html",{'page_obj': page_obj,"clientes":cliente})

@admin_required
def ficha_cliente(req,id_cliente):
    cliente = Cliente.objects.get(id=id_cliente)
    tel1 = ClienteTelefono.objects.filter(principal=1,cliente_id=cliente.id).first()
    tel_1 = tel1.telefono
    tel2 = ClienteTelefono.objects.filter(principal=0,cliente_id=cliente.id).first()

    correo1 = ClienteCorreo.objects.filter(principal=1,cliente_id=cliente.id).first()
    correo2 = ClienteCorreo.objects.filter(principal=0,cliente_id=cliente.id).first()
    if tel2:
        tel_2 = tel2.telefono
    else:
        tel_2 = None

    if correo1:
        c_1 = correo1.correo
    else:
        c_1 = None
    
    if correo2:
        c_2 = correo1.correo
    else:
        c_2 = None
    
    resultados_motos = (
        ComprasVentas.objects
        .filter(cliente__id=id_cliente, tipo='V')
        .select_related('moto', 'cliente')
        .values(
            'id',
            'moto__marca', 
            'moto__modelo', 
            'fecha_compra', 
            # 'cantidad_cuotas', 
            # 'cuotas_pagas', 
            'moto__precio', 
            'fotocopia_libreta', 
            'compra_venta', 
            'certificado_venta',
            # 'valor_cuota'
        ).order_by('-fecha_compra')
    )
    #cantidad_cuotas = CuotasMoto.cantidad_cuotas
    #valor_cuota = cuotasmoto.valor_cuota
    #cuotas_pagas = obtener el valor de la columna cuotas_pagas del ultimo registro ingresado en model CuotasMoto
    res_documentacion = []
    for resultado in resultados_motos:
            cv = ComprasVentas.objects.get(id=resultado['id'])
            res_documentacion.append({
            'moto': resultado,
            'libreta': cv.fotocopia_libreta.url if cv.fotocopia_libreta else None,
            'compra_venta': cv.compra_venta.url if cv.compra_venta else None,
            'certificado_venta': cv.certificado_venta.url if cv.certificado_venta else None,
            # 'cantidad_cuotas':cv.cantidad_cuotas
        })
    # show_acciones = any(item['moto']['cantidad_cuotas'] > 1 for item in res_documentacion)

    paginator = Paginator(res_documentacion, 5)  # 5 clientes por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)

    resultados_accesorios = (
        ClienteAccesorio.objects
        .filter(cliente__id=id_cliente)
        .select_related('accesorio', 'cliente')
        .values(
            'id',
            'accesorio__tipo',
            'accesorio__marca',
            'accesorio__modelo',
            'fecha_compra',
            'factura_documento'
        )
    )
    res_facturas = []
    for resultado_accesorio in resultados_accesorios:
            ca = ClienteAccesorio.objects.get(id=resultado_accesorio['id'])
            res_facturas.append({
            'accesorio': resultado_accesorio,
            'factura_documento': ca.factura_documento.url if ca.factura_documento else None
        })
    paginator_accesorio = Paginator(res_facturas, 5)  # 5 clientes por página
    page_number_accesorio = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj_accesorio = paginator_accesorio.get_page(page_number_accesorio)
    return render(req,"perfil_administrativo/cliente/detalles_cliente.html",{"cliente":cliente,
                                                                             "tel1":tel_1,
                                                                             "tel2":tel_2,
                                                                             "correo1":c_1,
                                                                             "correo2":c_2,
                                                                             "page_obj":page_obj,
                                                                             "page_obj_accesorio":page_obj_accesorio,
                                                                            #  "show_acciones": show_acciones
                                                                             })

@admin_required
def cargar_certificado(req,id_cv):
    try:
         certificado = req.FILES.get('certificado_venta')
         venta = ComprasVentas.objects.get(id=id_cv)
         venta.certificado_venta = certificado
         venta.save()
         messages.success(req, "Certificado ingresado con éxito")
         return redirect(f"{reverse('ClienteFicha',kwargs={'id_cliente':venta.cliente_id})}")
    except Exception as e:
        pass

@admin_required
def cargar_libreta(req,id_cv):
    try:
         libreta = req.FILES.get('libreta_venta')
         venta = ComprasVentas.objects.get(id=id_cv)
         venta.fotocopia_libreta = libreta
         venta.save()
         messages.success(req, "Libreta ingresada con éxito")
         return redirect(f"{reverse('ClienteFicha',kwargs={'id_cliente':venta.cliente_id})}")
    except Exception as e:
        pass

@admin_required
def alta_cuota(req,id_cv):
    try:
        if req.method == "POST":
            compra_venta = ComprasVentas.objects.get(id=id_cv)
            compra_venta.cuotas_pagas = compra_venta.cuotas_pagas + 1
            id_cliente = compra_venta.cliente_id
            compra_venta.save()

            return render(req,"perfil_administrativo/ventas/alta_cuota.html",{"message":"Cuota dada de alta con éxito","id_cliente":id_cliente})
        else:
            id_c = ComprasVentas.objects.get(id=id_cv)
            id_cliente = id_c.cliente_id
            return render(req,"perfil_administrativo/ventas/alta_cuota.html",{"id_cliente":id_cliente})

    except Exception as e:
        pass



@admin_required
def vista_personal(req):
    administrativos = (Administrativo.objects
                       .filter(activo=True)
                       .values('id', 'nombre', 'apellido', 'telefono', 'correo', 'activo')
                       .order_by('nombre'))
    paginator = Paginator(administrativos, 5)  # 5 clientes por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)

    mecanicos = (Mecanico.objects
                       .filter(activo=True)
                       .values('id', 'nombre', 'apellido', 'telefono', 'correo', 'activo')
                       .order_by('nombre'))
    paginatorMec = Paginator(mecanicos, 5)  # 5 clientes por página
    page_numberMec = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_objMec = paginatorMec.get_page(page_numberMec)

    return render(req,"perfil_administrativo/personal/personal.html",{"page_obj":page_obj,"page_objMec":page_objMec})

def validar_personal(documento,telefono,correo):
    personal = Personal.objects.filter(documento=documento).first()
    if personal:
        #VERIFICAR SI EXISTE EN ADMINISTRATIVO
        administrativo = Administrativo.objects.filter(personal_ptr_id = personal.id).first()
        if administrativo:
            if administrativo.activo == 1: #SI EXISTIERA DEVUELVE ERROR 
                return "existe_admin"
            else: #SI EXISTIERA Y FUE DADO DE BAJA COMO ADMINISTRATIVO (EJ. FUE ADMIN, PASO A SER MECANICO Y VUELVE A SER ADMIN), SIMPLEMENTE SE MODIFICA EL CAMPO ACTIVO = 1
                return "admin_desactivado"
    
    telefono_pers = Personal.objects.filter(telefono = telefono).first()

    if telefono_pers: #SI EL TELEFONO DEL PERSONAL A INGRESAR EXISTIERA (PUEDE QUE SEA UN MECANICO QUE SE LE ASIGNARA TAREAS DE ADMINISTRATIVO), EL ADMINISTRATIVO LOGEADO EN EL SISTEMA DEBERA OTORGARLE PERMISOS DE ADMINISTRATIVO
        # tel_admin = Administrativo.objects.filter(ptr_personal_id = telefono_pers.id).first()
        # if tel_admin:
        #     if tel_admin.activo == 1: 
                return "existe_telefono" 
    
    correo_pers = Personal.objects.filter(correo = correo).first()
    if correo_pers: #SI EL CORREO DEL PERSONAL A INGRESAR EXISTIERA (PUEDE QUE SEA UN MECANICO QUE SE LE ASIGNARA TAREAS DE ADMINISTRATIVO), EL ADMINISTRATIVO LOGEADO EN EL SISTEMA DEBERA OTORGARLE PERMISOS DE ADMINISTRATIVO
        # correo_admin = Administrativo.objects.filter(ptr_personal_id = correo_pers.id).first()
        # if correo_admin:
        #     if correo_admin.activo == 1:
                return "existe_correo"

def nombre_usuario(nombre,apellido):
    #SI EXISTE EL USUARIO, AGREGAR NUMERO AL FINAL (EJ. jperez, jperez1, jperez2)
    apellido_unido = apellido.replace(' ','')
    usuario = nombre[0:1:1] + apellido_unido
    cant_usuario = Personal.objects.filter(usuario__contains=usuario).count()
    if cant_usuario > 0: #EXISTE MAS DE UN jperez
        usuario = nombre[0:1:1] + apellido + str(cant_usuario)
    return usuario

@admin_required
def alta_personal(req):
    try:
        if req.method == "POST":
            documento = req.POST['tipo_doc'] + str(req.POST['doc'])
            telefono = req.POST['telefono'] 
            correo_nombre = req.POST['correo'] 
            correo_dominio = req.POST['dominio_correo'] 
            correo = correo_nombre + correo_dominio
            # print(documento)
             
            valid_personal = validar_personal(documento,telefono,correo)
            # print(valid_personal)
            if valid_personal == "existe_admin":
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"La persona que desea ingresar ya existe en el sistema"})
            elif valid_personal == "existe_telefono":
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"El teléfono ingresado ya existe en el sistema, el mismo no debe estar repetido"})
            elif valid_personal == "existe_correo":
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"El correo ingresado ya existe en el sistema, el mismo no debe estar repetido"})
            elif valid_personal == "admin_desactivado":    
                persona = Personal.objects.filter(documento=documento).first()
                id = persona.id
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"reingresar":True,"id_personal":id})
            else:
                    f_nac_str = req.POST.get('f_nac')  # Cambiado a paréntesis
                    f_nac = datetime.strptime(f_nac_str, '%Y-%m-%d').date() if f_nac_str else None
                    usuario = nombre_usuario(req.POST['nombre'],req.POST['apellido'])
                    
                    personal = Personal.objects.create(
                        documento=documento,
                        nombre=req.POST['nombre'].capitalize(),
                        apellido=req.POST['apellido'].capitalize(),
                        fecha_nacimiento=f_nac,
                        usuario=usuario,
                        contrasena="Inicio1234",
                        correo=correo,
                        telefono=telefono,
                        primera_sesion = True
                    )
                    personal.save()
                    # Crear registro en Administrativo asociado al Personal
                    administrativo = Administrativo.objects.create(
                        personal_ptr=personal,  # Asociar al registro de Personal
                        activo=True,
                        documento=documento,
                        nombre=req.POST['nombre'].capitalize(),
                        apellido=req.POST['apellido'].capitalize(),
                        fecha_nacimiento=f_nac,
                        usuario=usuario,
                        contrasena="Inicio1234",
                        correo=correo,
                        telefono=telefono,
                        primera_sesion = True
                    )
                    administrativo.save()

                    # Crear registro en Mecanico asociado al Personal
                    mecanico = Mecanico.objects.create(
                        personal_ptr=personal,  # Asociar al registro de Personal
                        activo=False,
                        jefe=False,
                        documento=documento,
                        nombre=req.POST['nombre'].capitalize(),
                        apellido=req.POST['apellido'].capitalize(),
                        fecha_nacimiento=f_nac,
                        usuario=usuario,
                        contrasena="Inicio1234",
                        correo=correo,
                        telefono=telefono,
                        primera_sesion = True
                    )
                    mecanico.save()

                    user = User.objects.create_user(
                        username=usuario,
                        password="Inicio1234",  # La contraseña predeterminada
                        email=correo,
                        first_name=req.POST['nombre'].capitalize(),
                        last_name=req.POST['apellido'].capitalize()
                    )
                    
                    # Asignar permisos o grupos si es necesario
                    user.is_staff = False  # Si deseas que tenga acceso al admin de Django
                    user.save()

                    messages.success(req, "Personal ingresado con éxito")
                    return redirect('Personal')
                
        else:
            return render(req,"perfil_administrativo/personal/alta_personal.html",{})
    except Exception as e:
        return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":e})


@admin_required
def ingresar_tienda(req,id_personal):
    try:
        administrativo = Administrativo.objects.get(personal_ptr_id=id_personal)
        administrativo.activo = 1
        administrativo.save()
        messages.success(req, "Personal reingresado con éxito")
        return redirect('Personal')
    except Exception as e:
        return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":e})

@admin_required
def detalles_personal(req,id_personal):
    try:
        personal = Personal.objects.get(id=id_personal)
        administrativo = Administrativo.objects.filter(personal_ptr_id = id_personal,activo = 1).first()
        if administrativo:
            admin = True
        else:
            admin = False
        
        mecanico = Mecanico.objects.filter(personal_ptr_id = id_personal,activo = 1).first()
        if mecanico:
            mec = True
            if mecanico.jefe == 1:
                jefe = True
            else:
                jefe = False
        else:
            mec = False
            jefe = False
        contexto = {
            "personal":personal,
            "admin":admin,
            "mec":mec,
            "jefe":jefe
        }
        return render(req,"perfil_administrativo/personal/detalles_personal.html",contexto)
    except Exception as e:
         pass

# def prueba_compra_venta(req):
#     logo_um = Logos.objects.get(id=1)
#     logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
#     ruta_pdf = "perfil_administrativo/motos/compra_venta.html"

#     regresa_moto = Moto.objects.get(id=1)
    
#     datos_a_pdf = contexto_para_pdf_moto(regresa_moto,logo_um_url)
#     renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
#     nombre_archivo = "compra_venta_prueba.pdf"
#     mensaje = "PRUEBA DE MOTO MENSAJE"
#     pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,regresa_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
#     return pdf_ret


@admin_required
def form_venta_moto(req,id_moto):
    try:
        if req.method == "POST":
            tipo_doc = req.POST['tipo_documento']
            doc = req.POST['documento']
            documento = tipo_doc + str(doc)
            cliente = Cliente.objects.filter(documento=documento).first()
            if cliente:
                tel1 = ClienteTelefono.objects.filter(principal=1,cliente_id=cliente.id).first()
                tel_1 = tel1.telefono
                tel2 = ClienteTelefono.objects.filter(principal=0,cliente_id=cliente.id).first()

                correo1 = ClienteCorreo.objects.filter(principal=1,cliente_id=cliente.id).first()
                correo2 = ClienteCorreo.objects.filter(principal=0,cliente_id=cliente.id).first()
                if tel2:
                    tel_2 = tel2.telefono
                else:
                    tel_2 = None

                if correo1:
                    c_1 = correo1.correo
                else:
                    c_1 = None
                
                if correo2:
                    c_2 = correo1.correo
                else:
                    c_2 = None
                moto = Moto.objects.get(id=id_moto)
                existe_matricula = Matriculas.objects.filter(moto_id=id_moto).first()
                if existe_matricula:
                    matricula = existe_matricula.matricula 
                    padron = existe_matricula.padron
                    departamento = departamento_matricula(matricula)
                else:
                    matricula = None
                    departamento = None
                    padron = None
                # existe_padron = ComprasVentas.objects.filter(moto_id=moto.id).first()
                # if existe_padron:
                #     padron = existe_padron.padron
                # else:
                #     padron = None
                #RENDERIZAR PAPEL COMPRA-VENTA
                numero_letra = num2words(moto.precio, lang='es').upper()
                fecha = date.today()
                logo_cv = Logos.objects.get(id=2)
                logo_cv_url = req.build_absolute_uri(logo_cv.logo_UM.url) if logo_cv.logo_UM else None
                # print(numero_letra)
                return render(req,"perfil_administrativo/motos/venta_moto.html",{"datos_moto":True,
                                                                                "cliente":cliente,
                                                                                "moto":moto,
                                                                                "tel1":tel_1,
                                                                                "tel2":tel_2,
                                                                                "correo1":c_1,
                                                                                "correo2":c_2,
                                                                                "num_letra":numero_letra,
                                                                                "matricula":matricula,
                                                                                "padron":padron,
                                                                                "departamento":departamento,
                                                                                "fecha":fecha,
                                                                                "logo_cv":logo_cv_url})
            else:
                return render(req,"perfil_administrativo/motos/venta_moto.html",{"datos_moto":False,"error_message_cliente":"El cliente no se encuentra registrado en el sistema, para ingresarlo haga clic "})
        else:
            return render(req,"perfil_administrativo/motos/venta_moto.html",{})
    except Exception as e:
        return render(req,"perfil_administrativo/motos/venta_moto.html",{"error_message":e})


@admin_required
def venta_moto(req,id_moto,id_cliente):
    try:

        # compra_venta = ComprasVentas.objects.filter(moto_id=id_moto,cliente_id=id_cliente,tipo="R").first()
        # if compra_venta:
        #     #ACA MODIFICAMOS CAMPO tipo = "V"
        #     # return render(req,"perfil_administrativo/motos/venta_moto.html",{"error_message":f"ID Moto es {id_moto}, ID Cliente es {id_cliente}"})
        #     compra_venta_archivo = req.FILES.get('compra_venta_moto')
        #     # compra_venta = ComprasVentas.objects.filter(moto_id=id_moto,cliente_id=id_cliente).first()
        #     compra_venta.tipo = "V"
        #     compra_venta.compra_venta = compra_venta_archivo
        #     compra_venta.fecha_compra = datetime.now()
        #     compra_venta.forma_de_pago = req.POST['forma_pago']
        #     compra_venta.save()
        #     retornar_cliente = ficha_cliente(req,id_cliente)
        #     return retornar_cliente
        # else:
            #INGRESAMOS EN COMPRAVENTA CON VALORES: fecha_compra = datetime.now(),padron = Null, compra_venta = ,certificado_venta = , tipo = 'V',cliente_id = id_cliente, moto_id = id_moto, forma_de_pago = 
            #CONSULTAMOS LA MOTO Y MODIFICAMOS EL CAMPO pertenece_tienda = 0
        moto = Moto.objects.get(id=id_moto)
        moto.pertenece_tienda = 0
        moto.save()
        compra_venta = req.FILES.get('compra_venta_moto')
        
        existe_reserva = ComprasVentas.objects.filter(moto_id=id_moto,cliente_id=id_cliente,tipo="R").first()
        if existe_reserva:
            # existe_reserva.delete() NO BORRAR YA QUE EN CASO DE HABER UN PAGO EN CUOTASMOTOS (SEÑA) SE BORRARIA TAMBIEN
            # ADEMAS LA RESERVA NO ES UN DATO QUE SE NECESITE CONSERVAR UNA VEZ VENDIDA LA MOTO
            existe_reserva.tipo = "V"
            existe_reserva.fecha_compra = datetime.now()
            #existe_reserva.certificado_venta = ,
            existe_reserva.compra_venta = compra_venta
            existe_reserva.forma_de_pago = req.POST['forma_pago']
            existe_reserva.save()
        else:
            nueva_venta = ComprasVentas(
                fecha_compra = datetime.now(),
                compra_venta = compra_venta,
                # certificado_venta = ,
                tipo = "V",
                forma_de_pago = req.POST['forma_pago'],
                cliente_id = id_cliente,
                moto_id = id_moto
            )
            nueva_venta.save()
        #REDIRIGIR A LA FICHA DEL CLIENTE
        # return render(req,"perfil_administrativo/motos/venta_moto.html",{"error_message":"VENTA EJECUTADA"})
        messages.success(req, "Venta generada con éxito")
        return redirect(f"{reverse('ClienteFicha',kwargs={'id_cliente':id_cliente})}")
    except Exception as e:
        return render(req,"perfil_administrativo/motos/venta_moto.html",{"error_message":e})

@admin_required
def vista_ventas(req):
    try:
            resultados_motos = (
                ComprasVentas.objects
                .filter(tipo='V')
                .select_related('moto','cliente')
                .values(
                    'id',
                    'moto__marca', 
                    'moto__modelo', 
                    'fecha_compra', 
                    'cliente__nombre',
                    'cliente__apellido'
                ).order_by('-fecha_compra')
            )

            res_documentacion = []
            for resultado in resultados_motos:
                cv = ComprasVentas.objects.get(id=resultado['id'])
                res_documentacion.append({
                'moto': resultado
            })


            paginator = Paginator(res_documentacion, 5)  # 5 clientes por página
            page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
            page_obj = paginator.get_page(page_number)
            
            resultados_accesorios = (
                ClienteAccesorio.objects
                # .filter(cliente__id=1)
                .select_related('accesorio', 'cliente')
                .values(
                    'id',
                    'accesorio__tipo',
                    'accesorio__marca',
                    'accesorio__modelo',
                    'fecha_compra',
                    'cliente__nombre',
                    'cliente__apellido'
                
                ).order_by('-fecha_compra')
            )
            res_facturas = []
            for resultado_accesorio in resultados_accesorios:
                    ca = ClienteAccesorio.objects.get(id=resultado_accesorio['id'])
                    res_facturas.append({
                    'accesorio': resultado_accesorio,
                    'factura_documento': ca.factura_documento.url if ca.factura_documento else None
                })
            paginator_accesorio = Paginator(res_facturas, 5)  # 5 clientes por página
            page_number_accesorio = req.GET.get('page')  # Obtiene el número de página desde la URL
            page_obj_accesorio = paginator_accesorio.get_page(page_number_accesorio)

            # prueba = num2words(42)
            
            return render(req,"perfil_administrativo/ventas/ventas.html",{"page_obj":page_obj,"page_objAccs":page_obj_accesorio})
    except Exception as e:
        pass

@admin_required
def detalles_cuotas(req,id_cv):
    try: 
        resultados_cuotas = (
                CuotasMoto.objects
                .filter(venta_id=id_cv)
                .values(
                    'id',
                    'fecha_pago', 
                    'fecha_prox_pago',  
                    'cant_restante_dolares', 
                    'cant_restante_pesos', 
                    'moneda', 
                    'observaciones',
                    'valor_pago_dolares',
                    'valor_pago_pesos',
                    'comprobante_pago'
                )
            )
            
        res_documentacion = []
        i = 1
        for resultado in resultados_cuotas:
                    cm = CuotasMoto.objects.get(id=resultado['id'])
                    res_documentacion.append({
                    'cuota': resultado,
                    'comprobante_pago': cm.comprobante_pago.url if cm.comprobante_pago else None,
                    'mostrar_boton': i == len(resultados_cuotas)           
                    })
                    i = i + 1
        
        c_v = ComprasVentas.objects.get(id=id_cv)
        
        paginator = Paginator(res_documentacion, 30)  
        page_number = req.GET.get('page') 
        page_obj = paginator.get_page(page_number)
        
        return render(req,"perfil_administrativo/ventas/detalles_cuotas.html",{"page_obj":page_obj,"id_cv":id_cv,"pago_acordado":c_v.forma_de_pago,"id_cliente":c_v.cliente_id})
    except Exception as e:
        return render(req,"perfil_administrativo/ventas/detalles_cuotas.html",{"error_message":e})

@admin_required
def alta_pago(req,id_cv):
    try:
        existe_cuota = CuotasMoto.objects.filter(venta_id=id_cv).first()
        comprobante = req.FILES.get('comprobante_pago')
        moneda = req.POST['moneda_entrega']
        if not existe_cuota:
            cv = ComprasVentas.objects.get(id=id_cv)
            moto = Moto.objects.get(id=cv.moto_id)

            dolar = PrecioDolar.objects.get(id=1)
            precio_dolar = dolar.precio_dolar_tienda
            if moneda == "Pesos":
                entrega_pesos = req.POST['valor_a_pagar']
                entrega_dolares = 0
                if moto.moneda_precio == "Pesos":
                    resto_pesos = int(moto.precio) - int(entrega_pesos)
                    resto_dolares = resto_pesos / precio_dolar
                else:
                    resto_pesos = int((moto.precio * precio_dolar)) - int(entrega_pesos)
                    resto_dolares = resto_pesos / precio_dolar
            else:
                entrega_pesos = 0
                entrega_dolares = req.POST['valor_a_pagar']
                if moto.moneda_precio == "Pesos":
                    resto_dolares = int((moto.precio / precio_dolar)) - int(entrega_dolares)
                    resto_pesos = resto_dolares * precio_dolar
                else:
                    resto_dolares = int(moto.precio) - int(entrega_dolares)
                    resto_pesos = resto_dolares * precio_dolar 

            nueva_cuota = CuotasMoto(
                fecha_pago = datetime.now(),
                fecha_prox_pago = req.POST['f_prox_pago'],
                venta_id = id_cv,
                cant_restante_dolares = resto_dolares, 
                cant_restante_pesos = resto_pesos, 
                moneda = moneda,
                observaciones = req.POST['observaciones_pago'],
                precio_dolar = precio_dolar,
                valor_pago_dolares = entrega_dolares, 
                valor_pago_pesos = entrega_pesos, 
                comprobante_pago = comprobante 
            )
            nueva_cuota.save()
    
        else:
            cuota = CuotasMoto.objects.filter(venta_id=id_cv).latest('id')
            
            precio_dolar = cuota.precio_dolar
            if moneda == "Pesos":
                entrega_pesos = req.POST['valor_a_pagar']
                entrega_dolares = 0
                resto_pesos = int(cuota.cant_restante_pesos) - int(entrega_pesos)
                resto_dolares = resto_pesos / precio_dolar
            else:
                entrega_pesos = 0
                entrega_dolares = req.POST['valor_a_pagar']
                resto_dolares = int(cuota.cant_restante_dolares) - int(entrega_dolares)
                resto_pesos = resto_dolares * precio_dolar

            nueva_cuota = CuotasMoto(
                fecha_pago = datetime.now(),
                fecha_prox_pago = req.POST['f_prox_pago'],
                venta_id = id_cv,
                cant_restante_dolares = resto_dolares,
                cant_restante_pesos = resto_pesos,
                moneda = moneda,
                observaciones = req.POST['observaciones_pago'],
                precio_dolar = precio_dolar,
                valor_pago_dolares = entrega_dolares,
                valor_pago_pesos = entrega_pesos,
                comprobante_pago = comprobante
            )
            nueva_cuota.save()

        if nueva_cuota.comprobante_pago:
            comprobante_url = nueva_cuota.comprobante_pago.url
        else:
            comprobante_url = None
            
        messages.success(req, "Pago ingresado con éxito")
        return redirect(f"{reverse('DetallesCuotas',kwargs={'id_cv':id_cv})}?comprobante_url={comprobante_url}")
    except Exception as e:
        return render(req,"perfil_administrativo/ventas/detalles_cuotas.html",{"error_message":e})

@admin_required
def baja_pago(req,id_cm):
    try:
        cuota = CuotasMoto.objects.get(id=id_cm)
        id_cv = cuota.venta_id
        if req.method == "POST":
            cuota.delete()    
            return render(req, "perfil_administrativo/ventas/baja_pago.html", {"message":"Pago borrado con éxito","id_cv":id_cv})
        else:
            return render(req,"perfil_administrativo/ventas/baja_pago.html",{"id_cv":id_cv})
    except Exception as e:
        return render(req,"perfil_administrativo/ventas/baja_pago.html",{"error_message":e})

@admin_required
def reservas(req):
    try:
        resultados_motos = (
                ComprasVentas.objects
                .filter(tipo='R')
                .select_related('moto','cliente')
                .values(
                    'id',
                    'moto__id',
                    'moto__marca', 
                    'moto__modelo', 
                    'fecha_compra', 
                    'cliente__nombre',
                    'cliente__apellido'
                ).order_by('-fecha_compra')
            )

        res_documentacion = []
        for resultado in resultados_motos:
                cv = ComprasVentas.objects.get(id=resultado['id'])
                res_documentacion.append({
                'moto': resultado
            })


        paginator = Paginator(res_documentacion, 5)  # 5 clientes por página
        page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
        page_obj = paginator.get_page(page_number)
        return render(req,"perfil_administrativo/motos/reservas.html",{"page_obj":page_obj})
    except Exception as e:
        pass

@admin_required
def form_reservar_moto(req,id_moto):
    try:
        if req.method == "POST":
            tipo_doc = req.POST['tipo_documento']
            doc = req.POST['documento']
            documento = tipo_doc + str(doc)
            cliente = Cliente.objects.filter(documento=documento).first()
            if cliente:
                tel1 = ClienteTelefono.objects.filter(principal=1,cliente_id=cliente.id).first()
                tel_1 = tel1.telefono
                tel2 = ClienteTelefono.objects.filter(principal=0,cliente_id=cliente.id).first()

                correo1 = ClienteCorreo.objects.filter(principal=1,cliente_id=cliente.id).first()
                correo2 = ClienteCorreo.objects.filter(principal=0,cliente_id=cliente.id).first()
                if tel2:
                    tel_2 = tel2.telefono
                else:
                    tel_2 = None

                if correo1:
                    c_1 = correo1.correo
                else:
                    c_1 = None
                
                if correo2:
                    c_2 = correo1.correo
                else:
                    c_2 = None
                moto = Moto.objects.get(id=id_moto)
                
                #RENDERIZAR PAPEL COMPRA-VENTA

                # print(numero_letra)
                return render(req,"perfil_administrativo/motos/reservar_moto.html",{"datos_moto":True,
                                                                                "cliente":cliente,
                                                                                "moto":moto,
                                                                                "tel1":tel_1,
                                                                                "tel2":tel_2,
                                                                                "correo1":c_1,
                                                                                "correo2":c_2
                                                                                })
            else:
                return render(req,"perfil_administrativo/motos/reservar_moto.html",{"datos_moto":False,"error_message_cliente":"El cliente no se encuentra registrado en el sistema, para ingresarlo haga clic "})
        else:
            return render(req,"perfil_administrativo/motos/reservar_moto.html",{})
    except Exception as e:
        return render(req,"perfil_administrativo/motos/reservar_moto.html",{"error_message":e})

@admin_required
def reservar_moto(req,id_moto,id_cliente):
    try:
        # compras_ventas = ComprasVentas.objects.filter(moto_id=id_moto,cliente_id=id_cliente).first()
        # if compras_ventas:
        #     compras_ventas.tipo = "R"
        #     compras_ventas.save()
        # else:
        compras_ventas = ComprasVentas(
            fecha_compra = datetime.now(),
            tipo = "R",
            cliente_id = id_cliente,
            moto_id = id_moto
        )
        compras_ventas.save()
        moneda = req.POST['moneda_senia']
        dolar = PrecioDolar.objects.get(id=1)
        precio_dolar = dolar.precio_dolar_tienda
        id_cv = compras_ventas.id

        moto = Moto.objects.get(id=id_moto)

        if moneda == "Pesos":
                entrega_pesos = req.POST['senia']
                entrega_dolares = 0
                if moto.moneda_precio == "Pesos":
                    resto_pesos = int(moto.precio) - int(entrega_pesos)
                    resto_dolares = resto_pesos / precio_dolar
                else:
                    resto_pesos = int((moto.precio * precio_dolar)) - int(entrega_pesos)
                    resto_dolares = resto_pesos / precio_dolar
        else:
                entrega_pesos = 0
                entrega_dolares = req.POST['senia']
                if moto.moneda_precio == "Pesos":
                    resto_dolares = int((moto.precio / precio_dolar)) - int(entrega_dolares)
                    resto_pesos = resto_dolares * precio_dolar
                else:
                    resto_dolares = int(moto.precio) - int(entrega_dolares)
                    resto_pesos = resto_dolares * precio_dolar

        nueva_cuota = CuotasMoto(
                fecha_pago = datetime.now(),
                fecha_prox_pago = datetime.now() + relativedelta(months=1),
                venta_id = id_cv,
                cant_restante_dolares = resto_dolares,
                cant_restante_pesos = resto_pesos,
                moneda = moneda,
                precio_dolar = precio_dolar,
                valor_pago_dolares = entrega_dolares,
                valor_pago_pesos = entrega_pesos,
                observaciones = "Seña"
            )
        nueva_cuota.save()
        moto.pertenece_tienda = 0
        moto.save()
        messages.success(req, "Moto reservada con éxito.")
        return redirect('Motos')
        
    except Exception as e:
        return render(req,"perfil_administrativo/motos/reservar_moto.html",{"error_message":e,"active_page":"Motos"})

@admin_required
def estadisticas(req):
    try:
        #VENTAS X MES
        anio = datetime.now().year
        mes_actual = datetime.now().month
        datos_ventas = []
        for n in range(1,mes_actual + 1):
            cant_ventas = ComprasVentas.objects.filter(fecha_compra__year=anio,fecha_compra__month=n,tipo="V").count()
            datos_ventas.append(int(cant_ventas))

        #5 MARCAS MAS VENDIDAS
        marcas_mas_vendidas = (
            ComprasVentas.objects
            .filter(tipo='V')  # Filtra solo las ventas
            .values('moto__marca')  # Agrupa por marca de moto
            .annotate(total_vendidas=Count('id'))  # Cuenta las ventas por marca
            .order_by('-total_vendidas')[:5]  # Ordena de mayor a menor y toma las primeras 5
        )
        
        datos_marcas = [
        {'marca': resultado['moto__marca'], 'total_vendidas': resultado['total_vendidas']}
        for resultado in marcas_mas_vendidas
        ]

        #5 MOTOS MAS VENDIDAS

        motos_mas_vendidas = (
            ComprasVentas.objects
            .filter(tipo='V')  # Filtra solo las ventas
            .values('moto__marca','moto__modelo')  # Agrupa por marca de moto
            .annotate(total_motos_vendidas=Count('id'))  # Cuenta las ventas por marca
            .order_by('-total_motos_vendidas')[:5]  # Ordena de mayor a menor y toma las primeras 5
        )
        
        datos_motos = [
        {'marca': resultado_moto['moto__marca'],'modelo':resultado_moto['moto__modelo'], 'total_motos_vendidas': resultado_moto['total_motos_vendidas']}
        for resultado_moto in motos_mas_vendidas
        ]
        
        datos_accesorios_ventas = []
        for n in range(1,mes_actual + 1):
            cant_accesorios = ClienteAccesorio.objects.filter(fecha_compra__year=anio,fecha_compra__month=n).count()
            datos_accesorios_ventas.append(int(cant_accesorios))
                      
        return render(req,"perfil_administrativo/estadisticas/estadisticas.html",{"datos":datos_ventas,
                                                                                  "marcas":datos_marcas,
                                                                                  "motos":datos_motos,
                                                                                  "active_page":"Estadisticas",
                                                                                  "prueba":datos_marcas,
                                                                                  "accesorios":datos_accesorios_ventas})
    except Exception as e:
        return render(req,"perfil_administrativo/estadisticas/estadisticas.html",{"error_message":e,"active_page":"Estadisticas"})

@admin_required
def datos_tienda(req):
    try:
        dolar = PrecioDolar.objects.get(id=1)
        logo_tienda = Logos.objects.get(id=1)
        logo_cv = Logos.objects.get(id=2)
        #"foto_moto":moto.foto.url if moto.foto else None
        imagen_logo_tienda = logo_tienda.logo_UM.url if logo_tienda.logo_UM else None
        imagen_logo_cv = logo_cv.logo_UM.url if logo_cv.logo_UM else None
        return render(req,"perfil_administrativo/tienda.html",{"dolar_precio":dolar.precio_dolar_tienda,
                                                               "imagen_logo_tienda":imagen_logo_tienda,
                                                               "imagen_logo_cv":imagen_logo_cv})
    except Exception as e:
        return render(req,"perfil_administrativo/tienda.html",{"error_message":e})

@admin_required
def modificar_precio_dolar(req):
    try:
        precio = req.POST['precio_dolar']
        dolar = PrecioDolar.objects.get(id=1)
        dolar.precio_dolar_tienda = precio
        dolar.save()
        messages.success(req, "Precio del dólar modificado con éxito.")
        return redirect('Tienda')

    except Exception as e:
        return render(req,"perfil_administrativo/tienda.html",{"error_message":e})

@admin_required
def modificar_logo_tienda(req):
    try:
        logo_tienda = Logos.objects.get(id=1)
        nuevo_logo = req.FILES.get('nuevo_logo')
        logo_tienda.logo_UM = nuevo_logo
        logo_tienda.save()
        messages.success(req, "Logo modificado modificado con éxito.")
        return redirect('Tienda')
    except Exception as e:
        return render(req,"perfil_administrativo/tienda.html",{"error_message":e})

@admin_required
def modificar_logo_cv(req):
    try:
        logo_cv = Logos.objects.get(id=2)
        nuevo_logo = req.FILES.get('nuevo_logo_cv')
        logo_cv.logo_UM = nuevo_logo
        logo_cv.save()
        messages.success(req, "Logo del papel compraventa modificado modificado con éxito.")
        return redirect('Tienda')
    except Exception as e:
        return render(req,"perfil_administrativo/tienda.html",{"error_message":e})

def notificaciones_cumples():

    #EJECUTAR ESTA FUNCION TODOS LOS DIAS A LAS 6AM
    today = datetime.now()
    cumples_cliente = Cliente.objects.filter(fecha_nacimiento__month=today.month,fecha_nacimiento__day=today.day)
    for cliente in cumples_cliente:
        tiene_correo = ClienteCorreo.objects.filter(cliente_id=cliente.id,principal=1).first()
        if tiene_correo:
            correo_enviado = True
            send_mail(
            subject='¡Feliz cumpleaños!',
            message=f'Hola {cliente.nombre}, ¡de parte de Umpierrez Motos y Motos Daniel te deseamos un feliz cumpleaños!',
            #CAMBIAR POR CORREO DE UMPIERREZ MOTOS
            from_email='lumacajuanmanuel@gmail.com',
            #CAMBIAR POR CORREO DE CLIENTE (tiene_correo.correo)
            recipient_list=[tiene_correo.correo],
        )
        else:
            correo_enviado = False
            
        if correo_enviado:
            mensaje = "Se le ha enviado un correo de saludos."
        else:
            mensaje = ""
        nueva_notificacion = Notificaciones(
            descripcion = f"¡Hoy es el cumpleaños de {cliente.nombre} {cliente.apellido}! {mensaje}",
            fecha = datetime.now(),
            tipo = "Cumpleaños"
        )
        #nueva_notificacion.save()

def notificaciones_pagos_atrasados():
    #EJECUTAR ESTA FUNCION TODOS LOS DIAS A LAS 6AM
    pass

def notificaciones_administrativo(req):
    try:
        #notificaciones_cumples()
        # notificaciones = [
        # {
        # "titulo": "Pago pendiente",
        # "fecha": "2024-11-28",
        # "descripcion": "El cliente Juan Pérez tiene un pago atrasado desde hace 7 días.",
        # "acciones": [
        #     {"nombre": "Ver detalle", "url": "/detalle_pago/123/"},
        #     {"nombre": "Contactar cliente", "url": "/contacto_cliente/123/"}
        # ]
        # },
        # {
        # "titulo": "Cumpleaños del cliente",
        # "fecha": "2024-11-29",
        # "descripcion": "Hoy es el cumpleaños de María López. Envíale un saludo especial.",
        # "acciones": [{"nombre": "Enviar saludo", "url": "/enviar_saludo/456/"}]
        #     }
        #     ]
        notificaciones = Notificaciones.objects.all()
        data = []
        for notificacion in notificaciones:
            if notificacion.tipo == "Atraso en pago":
                acciones = {"nombre": "Enviar correo", "url": ""}
            elif notificacion.tipo == "Cumpleaños":
                acciones = [{"nombre": "Ver detalle", "url": ""},]
            data.append({
                "notificacion":notificacion,
                "acciones":acciones
            })
        
        return render(req,"perfil_administrativo/notificaciones/notificaciones.html",{"notificaciones":data}) 
    except Exception as e:
        return render(req,"perfil_administrativo/notificaciones/notificaciones.html",{"error_message":e})