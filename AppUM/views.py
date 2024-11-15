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
                contexto = {"resultado":"Administrativo y Mecanico Jefe"}
            elif existe_mecanico == 1 and mecanico_jefe == 0 and existe_administrativo == 1:
                renderizar_en = "login/login.html"
                contexto = {"resultado":"Administrativo y Mecanico Empleado"}
            elif existe_administrativo == 1 and existe_mecanico == 0:
                renderizar_en = "perfil_administrativo/padre_perfil_administrativo.html"
                contexto = {"existe_mecanico":0,"mecanico_jefe":0,"existe_administrativo":1}
            elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 1:
                renderizar_en = "login/login.html"
                contexto ={"resultado":"Solo Mecanico Jefe"}
            elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 0:
                renderizar_en = "login/login.html"
                contexto = {"resultado":"Solo Mecanico Empleado" }
            else:
                renderizar_en = "login/login.html"
                contexto = {"resultado":"Este usuario fue dado de baja, contactese con el administrador del sistema."}
           
        else:
            renderizar_en = "login/login.html"
            contexto = {"resultado":"Error de usuario y/o contraseña"}

    except:
        renderizar_en = "login/login.html"
        contexto = {"resultado":"Algo salió mal"}
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

def num_padron(num_padron):
    existe_num_padron = ComprasVentas.objects.filter(padron = num_padron).first()

    if existe_num_padron:
        return existe_num_padron.id
    else:
        return "insert_num_padron"

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
                        messages.success(req, "Moto ingresada con éxito.")
                        return redirect('Motos')
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
                    valid_compra_venta = num_padron(req.POST['num_padron'])
                    
                    if cliente:
                        valid_pert_tienda = datos_moto_pert_tienda(num_motor, num_chasis)
                        if valid_pert_tienda == "update_pert_tienda": #SI LA MOTO FUE VENDIDA ANTERIORMENTE DE LA TIENDA Y VUELVE A LA MISMA, SE ACTUALIZA PERT_TIENDA = 1
                            # print("ENTRA IF")
                           
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

                            libreta_propiedad = req.FILES.get('libreta_propiedad_moto')
                            if valid_compra_venta == "insert_num_padron":
                                cliente_moto = ComprasVentas(
                                    fecha_compra = datetime.now(),
                                    padron = req.POST['num_padron'],
                                    tipo = "CV",
                                    fotocopia_libreta = libreta_propiedad,
                                    cliente_id = cliente.id,
                                    moto_id = regresa_moto.id,
                                    cantidad_cuotas = 0,
                                    cuotas_pagas = 0
                                )

                                cliente_moto.save()
                            else:
                                upd_compra_venta = ComprasVentas.objects.get(padron=req.POST['num_padron'])
                                upd_compra_venta.tipo = "CV"
                                upd_compra_venta.save()

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
                            
                            checkbox = 'crear_pdf' in req.POST
                            if checkbox:
                                logo_um = Logos.objects.get(id=1)
                                logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
                                ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                                
                                datos_a_pdf = contexto_para_pdf_moto(regresa_moto,logo_um_url)
                                renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                                nombre_archivo = f"identificacion_{regresa_moto.id}.pdf"
                                mensaje = f"Los datos ingresados corresponden a la moto {regresa_moto.marca} {regresa_moto.modelo}, que anteriormente fue vendida."
                                pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,regresa_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
                                return pdf_ret
                            else:
                                # contexto = {
                                # "messages":"Moto ingresada con éxito.",
                                # }
                                # return render(req,"perfil_administrativo/motos/motos.html",contexto)
                            
                                messages.success(req, "Moto ingresada con éxito.")
                                return redirect('Motos')
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
                            libreta_propiedad = req.FILES.get('libreta_propiedad_moto')
                            cliente_moto = ComprasVentas(
                                fecha_compra = datetime.now(),
                                padron = req.POST['num_padron'],
                                tipo = "CV",
                                fotocopia_libreta = libreta_propiedad,
                                cliente_id = cliente.id,
                                moto_id = nueva_moto.id,
                                cantidad_cuotas = 0,
                                cuotas_pagas = 0
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
                                ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
                                datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
                                renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
                                nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
                                mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
                                pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
                                return pdf_ret
                            else:
                                messages.success(req, "Moto ingresada con éxito.")
                                return redirect('Motos')
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
        contexto = {'page_obj': page_obj,"motos":moto}
    else:
        contexto = {'page_obj': None,"motos":None}

    return render(req,"perfil_administrativo/motos/motos.html",contexto)


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
                    "pdf":pdf,
                    "cliente":cliente,
                    "libreta":libreta,
                    "telefono_principal":telefono_principal,
                    "correo":correo
                    }
    else:
        contexto = {"moto":moto,"descripcion":descripcion,"pdf":pdf,"cliente":cliente,"libreta":libreta,"telefono_principal":telefono_principal,"correo":correo}
      
    print(pdf)
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
            'cantidad_cuotas', 
            'cuotas_pagas', 
            'moto__precio', 
            'fotocopia_libreta', 
            'compra_venta', 
            'certificado_venta',
            'valor_cuota'
        )
    )
    res_documentacion = []
    for resultado in resultados_motos:
            cv = ComprasVentas.objects.get(id=resultado['id'])
            res_documentacion.append({
            'moto': resultado,
            'libreta': cv.fotocopia_libreta.url if cv.fotocopia_libreta else None,
            'compra_venta': cv.compra_venta.url if cv.compra_venta else None,
            'certificado_venta': cv.certificado_venta.url if cv.certificado_venta else None,
        })


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
                                                                             "page_obj_accesorio":page_obj_accesorio
                                                                             })



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
                return "update_activo"
        else:
            return "ingresar_en_administrativo" #SI LA PERSONA EXISTE PERO NUNCA FUE ADMINISTRATIVA, SE INGRESA COMO NUEVA ADMINISTRATIVA (EJ. MECANICO QUE EMPEZARA CON TAREAS DE ADMINISTRATIVO)
    
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
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"Existe administrativo"})
            elif valid_personal == "existe_telefono":
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"El teléfono ingresado ya existe en el sistema, el mismo no debe estar repetido"})
            elif valid_personal == "existe_correo":
                return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"El correo ingresado ya existe en el sistema, el mismo no debe estar repetido"})
            else:
                # if valid_personal == "update_activo":
                #     return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"Modificar activo = 1"})
                # elif valid_personal == "ingresar_en_administrativo":
                #     # return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":"Ingresar nuevo administrativo"})
                #     personal = Personal.objects.filter(documento=documento).first()
                #     solo_administrativo = Administrativo(
                #         personal_ptr_id = personal.id,
                #         activo = 1
                #     )
                #     solo_administrativo.id
                # else:
                                    
                f_nac_str = req.POST.get('f_nac')  # Cambiado a paréntesis
                f_nac = datetime.strptime(f_nac_str, '%Y-%m-%d').date() if f_nac_str else None
                usuario = nombre_usuario(req.POST['nombre'],req.POST['apellido'])
                
                administrativo = Administrativo.objects.create(
                        documento=documento,
                        nombre=req.POST['nombre'].capitalize(),
                        apellido=req.POST['apellido'].capitalize(),
                        fecha_nacimiento=f_nac,
                        usuario=usuario,
                        contrasena="Inicio1234",
                        correo=correo,
                        telefono=telefono,
                        activo=True
                     )

                messages.success(req, "Personal ingresado con éxito")
                return redirect('Personal')
                
        else:
            return render(req,"perfil_administrativo/personal/alta_personal.html",{})
    except Exception as e:
        return render(req,"perfil_administrativo/personal/alta_personal.html",{"error_message":e})

def detalles_personal(req,id_personal):
    # try:
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
    # except Exception as e:
    #     pass

def prueba_compra_venta(req):
    logo_um = Logos.objects.get(id=1)
    logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
    ruta_pdf = "perfil_administrativo/motos/compra_venta.html"

    regresa_moto = Moto.objects.get(id=1)
    
    datos_a_pdf = contexto_para_pdf_moto(regresa_moto,logo_um_url)
    renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
    nombre_archivo = "compra_venta_prueba.pdf"
    mensaje = "PRUEBA DE MOTO MENSAJE"
    pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,regresa_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
    return pdf_ret


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
                return render(req,"perfil_administrativo/motos/venta_moto.html",{"datos_moto":True,
                                                                                "cliente":cliente,
                                                                                "moto":moto,
                                                                                "tel1":tel_1,
                                                                                "tel2":tel_2,
                                                                                "correo1":c_1,
                                                                                "correo2":c_2,})
            else:
                return render(req,"perfil_administrativo/motos/venta_moto.html",{"datos_moto":False,"error_message_cliente":"El cliente no se encuentra registrado en el sistema, para ingresarlo haga clic "})
        else:
            return render(req,"perfil_administrativo/motos/venta_moto.html",{})
    except Exception as e:
        pass