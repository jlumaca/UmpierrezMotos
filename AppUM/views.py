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
# Create your views here.

##VISTA DEL LOGIN AL ENTRAR AL SITIO##

def vista_login(req):
    return render(req,"login/login.html",{})

##VALIDACION DE USUARIO Y CONTRASEÑA##
def validacion_login(req):
    try:
        usuario = req.GET['usuario_login']
        passw = req.GET['pass_login']

        usuario_consulta = Personal.objects.filter(usuario=usuario,contrasena=passw).first()
    

        if usuario_consulta:
            mecanico = Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id).first()
            if mecanico:
                if mecanico.activo == 1:
                    existe_mecanico = 1
                    if mecanico.jefe == 1:
                        mecanico_jefe = 1
                    else:
                        mecanico_jefe = 0
                else:
                    existe_mecanico = 0
            else:
                mecanico_jefe = 0
                existe_mecanico = 0
                
            administrativo = Administrativo.objects.filter(personal_ptr_id=usuario_consulta.id).first()
            if administrativo:
                if administrativo.activo == 1:
                    existe_administrativo = 1
                else:
                    existe_administrativo = 0
            else:
                existe_administrativo = 0
        
            if existe_mecanico == 1 and mecanico_jefe == 1 and existe_administrativo == 1:
                renderizar_en = "login/login.html"
                contexto = "Administrativo y Mecanico Jefe"
            elif existe_mecanico == 1 and mecanico_jefe == 0 and existe_administrativo == 1:
                renderizar_en = "login/login.html"
                contexto = "Administrativo y Mecanico Empleado"
            elif existe_administrativo == 1 and existe_mecanico == 0:
                renderizar_en = "perfil_administrativo/padre_perfil_administrativo.html"
                contexto = {"existe_mecanico":0,"mecanico_jefe":0,"existe_administrativo":1}
            elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 1:
                renderizar_en = "login/login.html"
                contexto = "Solo Mecanico Jefe"
            elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 0:
                renderizar_en = "login/login.html"
                contexto = "Solo Mecanico Empleado" 
            else:
                renderizar_en = "login/login.html"
                contexto = "Este usuario fue dado de baja, contactese con el administrador del sistema."
           
        else:
            renderizar_en = "login/login.html"
            contexto = {"resultado":"Error de usuario y/o contraseña"}

    except:
        renderizar_en = "login/login.html"
        contexto = "Algo salió mal"
    #print(existe_mecanico)
    return render(req,renderizar_en,contexto)


def vista_inventario_motos(req):
    motos = Moto.objects.filter(pertenece_tienda=1).order_by('-fecha_ingreso')

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(motos, 5)  # 5 motos por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None})


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

def datos_moto(num_motor, num_chasis):
    existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
    existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first() 
    existen_ambos = Moto.objects.filter(num_motor = num_motor, num_chasis = num_chasis).first() 

    if existe_num_motor:
        if existe_num_motor.pertenece_tienda == 1:
            return "existe_num_motor"
    
    if existe_num_chasis:
        if existe_num_chasis.pertenece_tienda == 1:
            return "existe_num_chasis"
    
    if existe_num_motor and existe_num_chasis:
        if existe_num_motor.id != existe_num_chasis.id: #PENSADO EN CASO DE QUE SI UNA MOTO VUELVE A LA TIENDA COINCIDAN EL NUM DE CHASIS Y NUM DE MOTOR
            return "num_motor_chasis_error"             #EVITAR QUE SE INGRESE NUM DE CHASIS DE MOTO X CON NUM DE MOTOR DE MOTO Y
    
    if existen_ambos:
        if existen_ambos.pertenece_tienda == 0:
            return "update_pert_tienda_a_1"
        
def datos_moto_pert_tienda(num_motor, num_chasis):
    existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
    existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first() 
    #existen_ambos = Moto.objects.filter(num_motor = num_motor, num_chasis = num_chasis).first() 

    if existe_num_motor and existe_num_chasis:
        
        if existe_num_motor.pertenece_tienda == 0 and existe_num_chasis.pertenece_tienda == 0: #LA MOTO INGRESA NUEVAMENTE A LA TIENDA TIEMPO DESPUES DE SER VENDIDA
            return "update_pert_tienda"
    else:
        return None
    
    # if existe_num_chasis:
    #     if existe_num_chasis.pertenece_tienda == 0:
    #         return "update_pert_tienda"

def matricula_valid(matricula,num_motor,num_chasis):
    existe_matricula = Matriculas.objects.filter(matricula = matricula).first()
    moto = Moto.objects.filter(num_motor = num_motor,num_chasis = num_chasis).first()
    if existe_matricula:
        if moto:
            if existe_matricula.moto_id != moto.id: #SI LA MOTO EXISTE Y LA MATRICULA PERTENECE A OTRA MOTO DA ERROR
                return "matricula_existe"
        elif not moto: #LA MOTO NO EXISTE, POR LO TANTO LA MATRICULA INGRESADA PERTENECE A OTRA MOTO DEL SISTEMA
            return "matricula_existe"
        # elif existe_matricula.activo == 1: #SI LA MATRICULA EXISTE, ESTA ACTIVA Y PERTENECE A LA MISMA MOTO, NO SE MODIFICA NINGUN DATO
            # return "no_hacer_nada"
        # else:
        #     return "update_activo"

    else: #AL NO EXISTIR LA MATRICULA SE INGRESA DE 0
        return "ingresar_matr"

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
                "datos_cliente":cliente
            }
            return render(req,"perfil_administrativo/motos/alta_moto.html",contexto)
        else:
            contexto = {
                "error_message_cliente":"El cliente no existe, debe ingresar los datos del mismo haciendo clic ",
                "form_cliente":True
            }
            return render(req,"perfil_administrativo/motos/alta_moto.html",contexto)


def form_alta_moto(req):
    try:
        if req.method == "POST":
            marca = req.POST['marca_moto'].upper()
            modelo = req.POST['modelo_moto'].upper()
            color = req.POST['color_moto'].upper()
            matricula_mayus = req.POST['matricula_letras'].upper()
            matricula = matricula_mayus + str(req.POST['matricula_numeros'])
            num_motor = req.POST['num_motor_moto'].upper()
            num_chasis = req.POST['num_chasis_moto'].upper()
            
            valid_matricula = matricula_valid(matricula,num_motor,num_chasis)
            valid_moto = datos_moto(num_motor,num_chasis)
            #valid_matricula = matricula(matricula_mayus)
            # print(req.POST['estado_moto'])
            estado_moto = req.POST['estado_moto']
            
            if valid_moto == "existe_num_motor":
                return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Ya existe una moto con ese numero de motor"})
            elif valid_moto == "existe_num_chasis":
                return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Ya existe una moto con ese numero de chasis"})
            elif valid_moto == "num_motor_chasis_error":
                return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"El número de chasis y/o motor pertenecen a otra moto ingresada en el sistema"})
            elif valid_matricula == "matricula_existe":
                return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Ya existe la matricula"})
            else:
                if estado_moto == "nueva":
                    foto = req.FILES.get('foto_moto')
                    nueva_moto = Moto(marca = marca,
                            modelo = modelo,
                            anio = req.POST['anio_moto'],
                            estado = "Nueva",
                            motor = req.POST['motor_moto'],
			                kilometros = 0,
                            precio = req.POST['precio_moto'],
                            color = color,
                            num_motor = num_motor,
                            num_chasis = num_chasis,
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
                        contexto = {
                            "messages":"Moto ingresada con éxito.",
                        }
                        return render(req,"perfil_administrativo/motos/motos.html",contexto)
                    #return HttpResponse(pdf, content_type='application/pdf')
                else:
                    #INGRESAR MOTOS USADAS
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
                        valid_pert_tienda = datos_moto_pert_tienda(num_motor, num_chasis)
                        if valid_pert_tienda == "update_pert_tienda": #SI LA MOTO FUE VENDIDA ANTERIORMENTE DE LA TIENDA Y VUELVE A LA MISMA, SE ACTUALIZA PERT_TIENDA = 1
                            # print("ENTRA IF")
                            print("ID DEL CLIENTE --->>> " + str(req.POST['cliente_id']))
                            foto = req.FILES.get('foto_moto')
                            regresa_moto = Moto.objects.get(num_chasis=num_chasis,num_motor=num_motor)
                            regresa_moto.pertenece_tienda = 1
                            regresa_moto.fecha_ingreso = datetime.now()
                            regresa_moto.kilometros = req.POST['km_moto']
                            regresa_moto.precio = req.POST['precio_moto']
                            regresa_moto.estado = "Usada"
                            regresa_moto.observaciones = req.POST['descripcion_moto']
                            regresa_moto.foto = foto
                            regresa_moto.save()

                            if req.POST['matricula_letras'] and req.POST['matricula_numeros']: #SI LOS CAMPOS DE TEXTO DE LA MATRICULA NO ESTAN VACIOS
                                nueva_matricula = matricula_valid(matricula,num_motor,num_chasis)
                                ultima_matricula = Matriculas.objects.filter(activo=1,moto_id=regresa_moto.id)

                                if ultima_matricula.exists(): #SI EXISTIERA UNA MATRICULA ASIGNADA A ESA MOTO Y ESTA ACTIVA, ENTONCES ACCEDE
                                    ult_matricula = Matriculas.objects.filter(activo=1,moto_id=regresa_moto.id).first()
                                    if ult_matricula.matricula != matricula: #LA MATRICULA A INGRESAR ES DIFERENTE A LA ANTERIOR, SE PROCEDE A INGRESAR UNA NUEVA

                                        update_activo_0 = Matriculas.objects.get(id=ult_matricula.id)
                                        update_activo_0.activo = 0
                                        update_activo_0.save()

                                        if nueva_matricula == "ingresar_matr": #SI LA MATRICULA EXISTIERA Y ES DE LA MISMA MOTO NO HACE NADA PUESTO QUE NO SE ESTARIA CAMBIANDO
                                            new_matricula = Matriculas(
                                                    matricula = matricula,
                                                    activo = 1,
                                                    moto_id = regresa_moto.id
                                                )
                                            new_matricula.save()
                                else: #CASO CONTRARIO INGRESA UNA NUEVA
                                        if nueva_matricula == "ingresar_matr": #SI LA MATRICULA EXISTIERA Y ES DE LA MISMA MOTO NO HACE NADA PUESTO QUE NO SE ESTARIA CAMBIANDO
                                            new_matricula = Matriculas(
                                                    matricula = matricula,
                                                    activo = 1,
                                                    moto_id = regresa_moto.id
                                                )
                                            new_matricula.save()
                            

                            logo_um = Logos.objects.get(id=1)
                            logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
                            ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                            
                            datos_a_pdf = contexto_para_pdf_moto(regresa_moto,logo_um_url)
                            renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                            nombre_archivo = f"identificacion_{regresa_moto.id}.pdf"
                            mensaje = f"Los datos ingresados corresponden a la moto {regresa_moto.marca} {regresa_moto.modelo}, que anteriormente fue vendida."
                            pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,regresa_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
                            return pdf_ret
                        else: #SI LA MOTO NUNCA ESTUVO EN LA TIENDA, SE INGRESA DE 0
                            moto_taller = Moto.objects.filter(num_chasis=num_chasis,num_motor=num_motor).first()
                            if moto_taller: #LA MOTO PUEDE QUE EXISTA EN EL TALLER
                                pert_taller = moto_taller.pertenece_taller
                            else:
                                pert_taller = 0
                            foto = req.FILES.get('foto_moto')
                            nueva_moto = Moto(marca = marca,
                                modelo = modelo,
                                anio = req.POST['anio_moto'],
                                estado = "Usada",
                                motor = req.POST['motor_moto'],
                                kilometros = req.POST['km_moto'],
                                precio = req.POST['precio_moto'],
                                color = color,
                                num_motor = num_motor,
                                num_chasis = num_chasis,
                                pertenece_tienda = 1,
                                pertenece_taller = pert_taller,
                                fecha_ingreso = datetime.now(),
                                observaciones = req.POST['descripcion_moto'],
                                foto = foto
                                )
                            nueva_moto.save()

                            cliente_moto = ComprasVentas(
                                fecha_compra = datetime.now(),
                                padron = req.POST['num_padron'],
                                tipo = "CV",
                                cliente_id = cliente.id,
                                moto_id = nueva_moto.id
                            )

                            cliente_moto.save()
                            
                            nueva_matricula = matricula_valid(matricula,nueva_moto.num_motor,nueva_moto.num_chasis)

                            if nueva_matricula == "ingresar_matr":
                                new_matricula = Matriculas(
                                    matricula = matricula,
                                    activo = 1,
                                    moto_id = nueva_moto.id
                                )
                                new_matricula.save()
                            
                            checkbox = 'crear_pdf' in req.POST
                            if checkbox:

                                logo_um = Logos.objects.get(id=1)
                                logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
                                datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
                                renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                                nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
                                mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
                                pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
                                return pdf_ret
                            else:
                                contexto = {
                            "messages":"Moto ingresada con éxito.",
                                }
                                return render(req,"perfil_administrativo/motos/motos.html",contexto)
                    else:
                        contexto = {
                            "error_message_cliente":"El cliente no existe, debe ingresar los datos del mismo haciendo clic "
                        }
                        return render(req,"perfil_administrativo/motos/alta_moto.html",contexto)

            # return render(req,"perfil_administrativo/motos/alta_moto.html",{})
        else:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{})
    
    except Exception as e:
        return render(req,"perfil_administrativo/motos/alta_moto.html",{"error_message":"Algo salió mal"+ type(e).__name__})


def baja_moto(req,id_moto):
    if req.method == 'POST':

      motoDel = Moto.objects.get(id=id_moto)
      motoDel.pertenece_tienda = 0
      motoDel.save()
      return render(req, "perfil_administrativo/motos/baja_moto.html", {"message":"Moto borrada con éxito","id_moto":0})
      #return HttpResponse(f"<p>{id_auto}</p>")
    else:
       #print(f"Id auto es: {id_auto}")
       return render(req, "perfil_administrativo/motos/baja_moto.html", {"id_moto":id_moto})
       #return HttpResponse(f"<p>{id_auto}</p>")

def busqueda_codigo(req):
    codigo = req.GET.get('codigo')
    #if req.method == 'get':
    motos = Moto.objects.filter(id=codigo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_marca(req):
    marca = req.GET.get('marca')
    #if req.method == 'get':
    motos = Moto.objects.filter(marca__icontains=marca,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_modelo(req):
    modelo = req.GET.get('modelo')
    #if req.method == 'get':
    motos = Moto.objects.filter(modelo__icontains=modelo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_marca_modelo(req):
    marca = req.GET.get('marca_modelo')
    modelo = req.GET.get('modelo_marca')
    #if req.method == 'get':
    motos = Moto.objects.filter(marca__icontains=marca,modelo__icontains=modelo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_anio(req):
    anio = req.GET.get('anio')
    
    #if req.method == 'get':
    motos = Moto.objects.filter(anio=anio,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_kms(req):
    km_minimo = req.GET.get('km_minimo')
    km_maximo = req.GET.get('km_maximo')
    #if req.method == 'get':
    motos = Moto.objects.filter(kilometros__range=(km_minimo, km_maximo),pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_precio(req):
    precio_minimo = req.GET.get('precio_minimo')
    precio_maximo = req.GET.get('precio_maximo')
    #if req.method == 'get':
    motos = Moto.objects.filter(precio__range=(precio_minimo, precio_maximo),pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def datos_a_modificacion_moto(req,id_moto):
    try:
        moto_upd = Moto.objects.get(id=id_moto)
        matricula_upd = Matriculas.objects.filter(moto_id=moto_upd.id,activo=1).first()

        if matricula_upd:
            letras_matricula = matricula_upd.matricula[0:3:1]
            num_matricula = matricula_upd.matricula[3:7:1]
        else:
            letras_matricula = None
            num_matricula = None

        if moto_upd.observaciones == None:
            moto_upd.observaciones = "Sin descripción"
        return render(req,"perfil_administrativo/motos/modificacion_moto.html",{'datos_moto': moto_upd,
        "letras_matricula":letras_matricula,
        "num_matricula":num_matricula})   
    except:
        pass

def datos_moto_modificacion(id_moto,num_motor,num_chasis):
    moto_actual = Moto.objects.filter(id = id_moto).first()
    existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
    existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first()
    
    if existe_num_motor:
        if existe_num_motor.num_motor != moto_actual.num_motor:
            return "existe_num_motor"
    
    if existe_num_chasis:
        if existe_num_chasis.num_chasis != moto_actual.num_chasis:
            return "existe_num_chasis"

def modificacion_moto(req,id_moto):
    try:
                if req.method == "POST":
                        print("ACCEDE POST")
                        moto_upd = Moto.objects.get(id=id_moto)
                        num_motor = req.POST['num_motor_moto'].upper()
                        num_chasis = req.POST['num_chasis_moto'].upper()

                        if req.POST['matricula_letras'] and req.POST['matricula_numeros']:
                            letras_matricula = req.POST['matricula_letras']
                            num_matricula = req.POST['matricula_numeros']
                        else:
                            letras_matricula = None
                            num_matricula = None
                        
                        validacion_datos_moto = datos_moto_modificacion(id_moto,num_motor,num_chasis)

                        if validacion_datos_moto == "existe_num_motor":
                            return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"Ya existe el numero de motor",
                                                                                                    'datos_moto': moto_upd,
                                                                                                    "letras_matricula":letras_matricula,
                                                                                                    "num_matricula":num_matricula}) 
                        elif validacion_datos_moto == "existe_num_chasis":
                            return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"Ya existe el numero de chasis",
                                                                                                    'datos_moto': moto_upd,
                                                                                                    "letras_matricula":letras_matricula,
                                                                                                    "num_matricula":num_matricula}) 
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
                            moto_upd.color = color
                            moto_upd.precio = req.POST['precio_moto']
                            moto_upd.observaciones = req.POST['descripcion_moto']
                            moto_upd.foto = foto
                            moto_upd.save()


                            if req.POST['matricula_letras'] and req.POST['matricula_numeros']: #SI UNO O LOS DOS CAMPOS ESTAN VACIOS NO ACCEDE PUES LA MATRICULA ES INVALIDA
                                matr_letras = req.POST['matricula_letras'].upper()
                                matr_num = req.POST['matricula_numeros']
                                matricula = matr_letras + str(matr_num)
                                valid_matr = matricula_valid(matricula,num_motor,num_chasis)

                                matr_upd = Matriculas.objects.filter(activo=1,moto_id=moto_upd.id).first() #SE OBTIENE MATRICULA ACTUAL DE LA MOTO

                                if valid_matr == "matricula_existe":
                                    return render(req,"perfil_administrativo/motos/modificacion_moto.html",{"error_message":"Ya existe la matricula",
                                                                                                            'datos_moto': moto_upd,
                                                                                                            "letras_matricula":matr_letras,
                                                                                                            "num_matricula":matr_num})
                                else:
                                    if matr_upd: #SI EXISTIERA UNA MATRICULA ASIGNADA A LA MOTO INGRESA, LA MISMA SERA BORRADA DESPUES
                                        
                                        if matr_upd.matricula != matricula: #ACCEDE SI Y SOLO SI LA MATRICULA FUE MODIFICADA EN LOS CAMPOS DE TEXTO, ES DECIR, SE CAMBIA LA MATRICULA, SINO NO HACE NADA
                                            matr_delete = Matriculas.objects.get(matricula=matr_upd.matricula) #SE BORRA PUESTO QUE SE ENTIENDE QUE LA MATRICULA A MODIFICAR FUE ASIGNADA POR ERROR
                                            if matr_delete:
                                                matr_delete.delete()                                               #EL SISTEMA PERMITE ASIGNAR NUEVA MATRICULA (SIN BORRAR LA ANTERIOR) EN CASO DE QUE UNA MOTO REGRESE A LA TIENDA
                                            
                                            update_matricula = Matriculas(
                                                matricula = matricula,
                                                activo = 1,
                                                moto_id = moto_upd.id
                                            )
                                            update_matricula.save()
                                    else: #PENSADO ESPECIFICAMENTE CUANDO LA MOTO NO TIENE NI HA TENIDO UNA MATRICULA ASIGNADA Y SE LE DESEA ASIGNAR UNA
                                            update_matricula = Matriculas(
                                                matricula = matricula,
                                                activo = 1,
                                                moto_id = moto_upd.id
                                            )
                                            update_matricula.save()
                            
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
                                # motos = Moto.objects.filter(pertenece_tienda=1).order_by('-fecha_ingreso')
                                # logo_um = Logos.objects.get(id=1)
                                # paginator = Paginator(motos, 5)  # 10 motos por página
                                # page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
                                # page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

                                # return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None})
                                messages.success(req, "La moto ha sido modificada con éxito.")
                                return redirect('Motos')
                else:
                    moto_upd = Moto.objects.get(id=id_moto)
                    matricula_upd = Matriculas.objects.filter(moto_id=moto_upd.id,activo=1).first()

                    if matricula_upd:
                        letras_matricula = matricula_upd.matricula[0:3:1]
                        num_matricula = matricula_upd.matricula[3:7:1]
                    else:
                        letras_matricula = None
                        num_matricula = None

                    if moto_upd.observaciones == None:
                        moto_upd.observaciones = "Sin descripción"
                    return render(req,"perfil_administrativo/motos/modificacion_moto.html",{'datos_moto': moto_upd,
                    "letras_matricula":letras_matricula,
                    "num_matricula":num_matricula}) 
    except:
        pass
    

def detalles_moto(req,id_moto):
    moto = Moto.objects.get(id=id_moto)
    
    matriculas_moto = Matriculas.objects.filter(moto_id=id_moto)

    if not moto.observaciones:
        descripcion = "Sin descripción"
    else:
        descripcion = moto.observaciones
    
    if moto.identificacion_pdf:
        pdf = moto.identificacion_pdf.url
    else:
        pdf = None

    # print("Matr actual: "+str(matricula_actual.matricula))
    # print("Matr anterior: "+str(matricula_anterior.matricula))

    if matriculas_moto.exists():
    # Obtiene la matrícula actual, o None si no existe
        matricula_actual = Matriculas.objects.filter(moto_id=moto.id, activo=1).first()
    # Obtiene las matrículas anteriores, o un queryset vacío si no existen
        matricula_anterior = Matriculas.objects.filter(moto_id=moto.id, activo=0).first()
        if not matricula_anterior:
            matr_ant = None
        else:
            matr_ant = matricula_anterior.matricula
        
        if not matricula_actual: 
            matr_act = None
        else:
            matr_act = matricula_actual.matricula
        
        contexto = {"moto":moto,
                    "descripcion":descripcion,
                    "matr_anterior": matr_ant,
                    "matr_actual":matr_act,
                    "foto_moto":moto.foto.url if moto.foto else None,
                    "pdf":pdf}
    else:
        contexto = {"moto":moto,"descripcion":descripcion,"pdf":pdf}
      
    
    # if not matricula_anterior:
    #     matricula_anterior.matricula = None

    return render(req,"perfil_administrativo/motos/detalles_moto.html",contexto)


def vista_inventario_accesorios(req):
    accesorios = Accesorio.objects.filter(activo=1).order_by('-fecha_ingreso')

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(accesorios, 5)  # 5 accesorios por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/accesorios/accesorios.html",{'page_obj': page_obj,"accesorios":accesorios,"logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None})

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

def detalles_accesorio(req,id_accesorio):
    try:
        accesorio_detalle = Accesorio.objects.get(id=id_accesorio)
        return render(req, "perfil_administrativo/accesorios/detalles_accesorio.html", {"accesorio":accesorio_detalle})
    except Exception as e:
        pass

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

def vista_clientes(req):
    clientes = Cliente.objects.filter(
        cliente_correo__activo=True,
        cliente_correo__principal=True,
        cliente_telefono__activo=True,
        cliente_telefono__principal=True
    ).values('nombre', 'apellido', 'cliente_telefono__telefono', 'cliente_correo__correo').order_by('nombre')

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(clientes, 5)  # 5 clientes por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/cliente/clientes.html",{'page_obj': page_obj,"clientes":clientes})